#!/usr/bin/env python3
"""
Agent Enhancement Script for Claude Code Agent System

This script batch updates all 18 agent files with goal-oriented architecture,
integrating goal sections, task tracking, and summary generation capabilities.
"""

import os
import sys
import yaml
import json
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import re
import shutil

class AgentEnhancer:
    """Enhances agent files with goal-oriented architecture"""
    
    def __init__(self, agents_path: str = ".claude/agents", goals_path: str = ".claude/goals"):
        self.agents_path = Path(agents_path)
        self.goals_path = Path(goals_path)
        
        # Ensure paths exist
        self.agents_path.mkdir(parents=True, exist_ok=True)
        self.goals_path.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        
        # Load goal definitions
        self.goal_manager = None
        self._load_goal_manager()
        
    def _setup_logging(self):
        """Setup logging for agent enhancer"""
        log_file = self.goals_path / "agent_enhancer.log"
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
    def _load_goal_manager(self):
        """Load goal manager for goal definitions"""
        try:
            sys.path.append(str(Path(__file__).parent))
            from goal_manager import GoalManager
            self.goal_manager = GoalManager()
        except ImportError as e:
            self.logger.error(f"Failed to load goal manager: {e}")
            
    def enhance_all_agents(self, backup: bool = True) -> Dict[str, Any]:
        """Enhance all agent files with goal-oriented architecture"""
        results = {
            'enhanced_agents': [],
            'skipped_agents': [],
            'errors': [],
            'backup_location': None,
            'timestamp': datetime.now().isoformat()
        }
        
        # Create backup if requested
        if backup:
            backup_path = self._create_backup()
            results['backup_location'] = str(backup_path)
            
        # Get all agent files
        agent_files = self._find_agent_files()
        
        for agent_file in agent_files:
            try:
                agent_name = self._extract_agent_name(agent_file)
                if self._enhance_agent_file(agent_file, agent_name):
                    results['enhanced_agents'].append(agent_name)
                    self.logger.info(f"Successfully enhanced {agent_name}")
                else:
                    results['skipped_agents'].append(agent_name)
                    self.logger.info(f"Skipped {agent_name} (already enhanced or no changes needed)")
            except Exception as e:
                error_msg = f"Failed to enhance {agent_file}: {str(e)}"
                results['errors'].append(error_msg)
                self.logger.error(error_msg)
                
        return results
        
    def _create_backup(self) -> Path:
        """Create backup of existing agent files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = self.agents_path.parent / "backups" / f"agents_backup_{timestamp}"
        backup_path.mkdir(parents=True, exist_ok=True)
        
        # Copy all agent files
        for agent_file in self.agents_path.glob("*.md"):
            shutil.copy2(agent_file, backup_path)
            
        self.logger.info(f"Created backup at {backup_path}")
        return backup_path
        
    def _find_agent_files(self) -> List[Path]:
        """Find all agent markdown files"""
        agent_files = list(self.agents_path.glob("*.md"))
        
        # Filter for actual agent files (exclude documentation)
        actual_agents = []
        for file in agent_files:
            if not file.name.lower().startswith(('readme', 'index', 'doc')):
                actual_agents.append(file)
                
        return actual_agents
        
    def _extract_agent_name(self, agent_file: Path) -> str:
        """Extract agent name from file path or content"""
        # First try to extract from filename
        filename = agent_file.stem
        if filename.startswith(('writer-', 'research-', 'coder-')):
            return filename
            
        # Try to extract from file content
        try:
            with open(agent_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for name in YAML frontmatter
            yaml_match = re.search(r'^---\s*\nname:\s*(.+?)\n', content, re.MULTILINE)
            if yaml_match:
                return yaml_match.group(1).strip()
                
            # Look for name in description
            desc_match = re.search(r'name:\s*(\S+)', content)
            if desc_match:
                return desc_match.group(1)
                
        except Exception as e:
            self.logger.warning(f"Could not extract name from {agent_file}: {e}")
            
        # Fallback to filename
        return filename
        
    def _enhance_agent_file(self, agent_file: Path, agent_name: str) -> bool:
        """Enhance a single agent file with goal-oriented architecture"""
        # Read existing content
        with open(agent_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Check if already enhanced
        if 'goal:' in content and '## Goal-Oriented Execution' in content:
            return False  # Already enhanced
            
        # Get goal definition for this agent
        goal_config = None
        if self.goal_manager:
            goal_config = self.goal_manager.get_agent_goal(agent_name)
            
        if not goal_config:
            self.logger.warning(f"No goal configuration found for {agent_name}")
            return False
            
        # Parse existing YAML frontmatter
        yaml_section, remaining_content = self._parse_yaml_frontmatter(content)
        
        # Add goal section to YAML
        enhanced_yaml = self._add_goal_to_yaml(yaml_section, goal_config)
        
        # Enhance the main content
        enhanced_content = self._enhance_agent_content(remaining_content, agent_name, goal_config)
        
        # Reconstruct the file
        new_content = self._reconstruct_agent_file(enhanced_yaml, enhanced_content)
        
        # Write enhanced content
        with open(agent_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        return True
        
    def _parse_yaml_frontmatter(self, content: str) -> tuple:
        """Parse YAML frontmatter from agent file"""
        if content.startswith('---'):
            # Find end of YAML
            yaml_end = content.find('---', 3)
            if yaml_end != -1:
                yaml_content = content[3:yaml_end].strip()
                remaining_content = content[yaml_end + 3:].strip()
                
                try:
                    yaml_data = yaml.safe_load(yaml_content)
                    return yaml_data or {}, remaining_content
                except yaml.YAMLError as e:
                    self.logger.warning(f"Failed to parse YAML: {e}")
                    
        # No valid YAML frontmatter found
        return {}, content
        
    def _add_goal_to_yaml(self, yaml_data: Dict[str, Any], goal_config: Dict[str, Any]) -> Dict[str, Any]:
        """Add goal configuration to YAML frontmatter"""
        # Create enhanced YAML with goal section
        enhanced_yaml = yaml_data.copy()
        
        # Add goal section
        enhanced_yaml['goal'] = {
            'mission': goal_config['mission'],
            'success_criteria': goal_config['success_criteria'],
            'key_metrics': goal_config['key_metrics'],
            'target_scores': goal_config['target_scores']
        }
        
        return enhanced_yaml
        
    def _enhance_agent_content(self, content: str, agent_name: str, goal_config: Dict[str, Any]) -> str:
        """Enhance the main content of the agent file"""
        lines = content.split('\n')
        enhanced_lines = []
        
        # Find insertion point for goal-oriented execution section
        insertion_point = len(lines)  # Default to end if not found
        
        for i, line in enumerate(lines):
            # Look for good insertion points
            if line.startswith('## ') and any(keyword in line.lower() 
                for keyword in ['execution', 'protocol', 'workflow', 'process']):
                insertion_point = i
                break
            elif line.startswith('You are') or line.startswith('You are the'):
                # Insert after the initial introduction
                insertion_point = min(i + 1, len(lines))
                break
                
        # Insert goal-oriented execution section
        goal_section = self._generate_goal_section(agent_name, goal_config)
        
        # Reconstruct content with goal section
        enhanced_lines = lines[:insertion_point] + goal_section + lines[insertion_point:]
        
        return '\n'.join(enhanced_lines)
        
    def _generate_goal_section(self, agent_name: str, goal_config: Dict[str, Any]) -> List[str]:
        """Generate the goal-oriented execution section"""
        lines = [
            "",
            "## Goal-Oriented Execution",
            "",
            f"**Core Mission**: {goal_config['mission']}",
            "",
            "### Success Criteria",
            ""
        ]
        
        # Add success criteria
        for criteria in goal_config['success_criteria']:
            lines.append(f"- {criteria}")
        lines.append("")
        
        # Add key metrics
        lines.extend([
            "### Key Metrics",
            ""
        ])
        
        for metric in goal_config['key_metrics']:
            target_score = goal_config['target_scores'].get(metric, 'N/A')
            if isinstance(target_score, (int, float)):
                lines.append(f"- **{metric}**: Target {target_score:.1%}")
            else:
                lines.append(f"- **{metric}**: {target_score}")
        lines.append("")
        
        # Add execution guidelines
        lines.extend([
            "### Execution Guidelines",
            "",
            "- Always align actions with core mission",
            "- Track progress toward success criteria",
            "- Document learnings for continuous improvement",
            "- Measure and report key metrics",
            "- Integrate with goal management system",
            ""
        ])
        
        # Add agent-specific guidelines
        if agent_name.startswith('research-'):
            lines.extend([
                "### Research-Specific Guidelines",
                "",
                "- Prioritize accuracy and comprehensiveness",
                "- Maintain scientific rigor in all analyses",
                "- Document sources and methodology",
                "- Enable reproducible research processes",
                ""
            ])
        elif agent_name.startswith('writer-'):
            lines.extend([
                "### Writing-Specific Guidelines",
                "",
                "- Maintain consistent voice and style",
                "- Ensure logical flow and coherence",
                "- Meet journal-specific requirements",
                "- Optimize for reader engagement",
                ""
            ])
        elif agent_name.startswith('coder-'):
            lines.extend([
                "### Coding-Specific Guidelines",
                "",
                "- Follow security best practices",
                "- Write maintainable, readable code",
                "- Implement comprehensive testing",
                "- Document code and processes thoroughly",
                ""
            ])
            
        return lines
        
    def _reconstruct_agent_file(self, yaml_data: Dict[str, Any], content: str) -> str:
        """Reconstruct the agent file with enhanced YAML and content"""
        # Convert YAML back to string
        yaml_str = yaml.dump(yaml_data, default_flow_style=False, sort_keys=False, 
                            allow_unicode=True, indent=2)
        
        # Reconstruct file
        return f"---\n{yaml_str}---\n\n{content}"
        
    def validate_enhancements(self) -> Dict[str, Any]:
        """Validate that all enhancements were applied correctly"""
        validation_results = {
            'validated_agents': [],
            'validation_errors': [],
            'missing_goals': [],
            'invalid_yaml': []
        }
        
        agent_files = self._find_agent_files()
        
        for agent_file in agent_files:
            agent_name = self._extract_agent_name(agent_file)
            
            try:
                with open(agent_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Check for goal section in YAML
                yaml_section, _ = self._parse_yaml_frontmatter(content)
                
                if 'goal' not in yaml_section:
                    validation_results['missing_goals'].append(agent_name)
                    continue
                    
                # Check for goal-oriented execution section
                if '## Goal-Oriented Execution' not in content:
                    validation_results['validation_errors'].append(
                        f"{agent_name}: Missing goal-oriented execution section"
                    )
                    continue
                    
                # Validate YAML structure
                goal_section = yaml_section.get('goal', {})
                required_keys = ['mission', 'success_criteria', 'key_metrics', 'target_scores']
                
                for key in required_keys:
                    if key not in goal_section:
                        validation_results['validation_errors'].append(
                            f"{agent_name}: Missing required goal key: {key}"
                        )
                        
                if not validation_results['validation_errors'] or agent_name not in [
                    e.split(':')[0] for e in validation_results['validation_errors']
                ]:
                    validation_results['validated_agents'].append(agent_name)
                    
            except Exception as e:
                validation_results['invalid_yaml'].append(f"{agent_name}: {str(e)}")
                
        return validation_results
        
    def generate_enhancement_report(self, results: Dict[str, Any]) -> str:
        """Generate a comprehensive enhancement report"""
        report_lines = [
            "# Agent Enhancement Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            f"- Enhanced Agents: {len(results['enhanced_agents'])}",
            f"- Skipped Agents: {len(results['skipped_agents'])}",
            f"- Errors: {len(results['errors'])}",
            ""
        ]
        
        if results.get('backup_location'):
            report_lines.extend([
                f"- Backup Location: {results['backup_location']}",
                ""
            ])
            
        # Enhanced agents
        if results['enhanced_agents']:
            report_lines.extend([
                "## Enhanced Agents",
                ""
            ])
            for agent in results['enhanced_agents']:
                report_lines.append(f"✅ {agent}")
            report_lines.append("")
            
        # Skipped agents
        if results['skipped_agents']:
            report_lines.extend([
                "## Skipped Agents",
                ""
            ])
            for agent in results['skipped_agents']:
                report_lines.append(f"⏭️ {agent}")
            report_lines.append("")
            
        # Errors
        if results['errors']:
            report_lines.extend([
                "## Errors",
                ""
            ])
            for error in results['errors']:
                report_lines.append(f"❌ {error}")
            report_lines.append("")
            
        # Add validation results if available
        validation = self.validate_enhancements()
        report_lines.extend([
            "## Validation Results",
            f"- Successfully Validated: {len(validation['validated_agents'])}",
            f"- Validation Errors: {len(validation['validation_errors'])}",
            f"- Missing Goals: {len(validation['missing_goals'])}",
            f"- Invalid YAML: {len(validation['invalid_yaml'])}",
            ""
        ])
        
        if validation['validation_errors']:
            report_lines.extend([
                "### Validation Errors",
                ""
            ])
            for error in validation['validation_errors']:
                report_lines.append(f"⚠️ {error}")
            report_lines.append("")
            
        return '\n'.join(report_lines)
        
    def rollback_enhancements(self, backup_path: str) -> bool:
        """Rollback enhancements from backup"""
        try:
            backup_dir = Path(backup_path)
            if not backup_dir.exists():
                self.logger.error(f"Backup directory not found: {backup_path}")
                return False
                
            # Copy backup files back
            for backup_file in backup_dir.glob("*.md"):
                target_file = self.agents_path / backup_file.name
                shutil.copy2(backup_file, target_file)
                
            self.logger.info(f"Successfully rolled back from backup: {backup_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to rollback: {e}")
            return False

# CLI Interface
def main():
    """Command-line interface for agent enhancement"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Claude Agent Enhancement Tool')
    parser.add_argument('command', choices=['enhance', 'validate', 'rollback'],
                       help='Command to execute')
    parser.add_argument('--no-backup', action='store_true', 
                       help='Skip creating backup before enhancement')
    parser.add_argument('--backup-path', help='Backup path for rollback')
    parser.add_argument('--report-file', help='Save enhancement report to file')
    
    args = parser.parse_args()
    
    enhancer = AgentEnhancer()
    
    if args.command == 'enhance':
        print("🚀 Starting agent enhancement process...")
        results = enhancer.enhance_all_agents(backup=not args.no_backup)
        
        # Generate and display report
        report = enhancer.generate_enhancement_report(results)
        print(report)
        
        # Save report if requested
        if args.report_file:
            with open(args.report_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"Report saved to: {args.report_file}")
            
    elif args.command == 'validate':
        print("🔍 Validating agent enhancements...")
        validation = enhancer.validate_enhancements()
        
        print(f"\nValidation Results:")
        print(f"✅ Validated: {len(validation['validated_agents'])}")
        print(f"❌ Errors: {len(validation['validation_errors'])}")
        print(f"⚠️ Missing Goals: {len(validation['missing_goals'])}")
        print(f"🔥 Invalid YAML: {len(validation['invalid_yaml'])}")
        
        if validation['validation_errors']:
            print("\nValidation Errors:")
            for error in validation['validation_errors']:
                print(f"  - {error}")
                
    elif args.command == 'rollback':
        if not args.backup_path:
            print("❌ Please specify --backup-path for rollback")
            return
            
        print(f"🔄 Rolling back from backup: {args.backup_path}")
        success = enhancer.rollback_enhancements(args.backup_path)
        
        if success:
            print("✅ Rollback completed successfully")
        else:
            print("❌ Rollback failed")

if __name__ == '__main__':
    main()