#!/usr/bin/env python3
"""
Summary Generator for Claude Code Agent System

This module generates execution summaries after task completion,
extracts insights and learnings, and maintains searchable documentation
for all agent activities.
"""

import json
import re
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
import hashlib

@dataclass
class ExecutionSummary:
    """Represents an execution summary for an agent"""
    summary_id: str
    agent_name: str
    task_id: str
    timestamp: str
    task_description: str
    actions_taken: List[str]
    results_achieved: List[str]
    challenges_encountered: List[str]
    learnings_captured: List[str]
    performance_metrics: Dict[str, float]
    execution_time: float
    success_indicators: Dict[str, Any]
    improvement_suggestions: List[str]
    knowledge_gained: str
    reusable_patterns: List[str]
    
class SummaryGenerator:
    """Generates and manages execution summaries for all agents"""
    
    def __init__(self, doc_base_path: str = ".claude/doc"):
        self.doc_base_path = Path(doc_base_path)
        self.doc_base_path.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        self._initialize_agent_directories()
        
    def _setup_logging(self):
        """Setup logging for summary generator"""
        log_file = self.doc_base_path.parent / "goals" / "summary_generator.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
    def _initialize_agent_directories(self):
        """Initialize documentation directories for all agents"""
        agent_names = [
            # Research Agents
            "research-literature", "research-knowledge-graph", "research-hypothesis",
            "research-gap-identifier", "research-trends", "research-academic", 
            "research-semantic-scholar",
            # Writer Agents
            "writer-intro-cluster", "writer-method-cluster", "writer-results-cluster",
            "writer-discussion-cluster", "writer-format-cluster", "writer-quality-controller",
            "writer-style-formatter", "writer-cache-manager",
            # Coder Agents
            "coder-reviewer", "coder-debugger", "coder-industrial-ai"
        ]
        
        for agent_name in agent_names:
            agent_dir = self.doc_base_path / agent_name
            agent_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize default files
            summary_index_file = agent_dir / "summary_index.json"
            if not summary_index_file.exists():
                with open(summary_index_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "summaries": [],
                        "metadata": {
                            "created": datetime.now().isoformat(),
                            "total_summaries": 0,
                            "agent_name": agent_name
                        }
                    }, f, indent=2)
                    
            performance_metrics_file = agent_dir / "performance_metrics.json"
            if not performance_metrics_file.exists():
                with open(performance_metrics_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        "metrics_history": [],
                        "current_metrics": {},
                        "trends": {},
                        "metadata": {
                            "created": datetime.now().isoformat(),
                            "agent_name": agent_name
                        }
                    }, f, indent=2)
                    
            # Create knowledge base file
            knowledge_base_file = agent_dir / "knowledge_base.md"
            if not knowledge_base_file.exists():
                with open(knowledge_base_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {agent_name.replace('-', ' ').title()} Knowledge Base\n\n")
                    f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                    f.write("## Key Learnings\n\n")
                    f.write("## Successful Patterns\n\n")
                    f.write("## Common Challenges\n\n")
                    f.write("## Best Practices\n\n")
                    
    def generate_summary(self, agent_name: str, task_id: str, execution_data: Dict[str, Any],
                        log_content: str = "", user_query: str = "") -> str:
        """Generate comprehensive execution summary"""
        summary_id = self._generate_summary_id(agent_name, task_id)
        timestamp = datetime.now().isoformat()
        
        # Extract information from execution data and logs
        actions_taken = self._extract_actions(execution_data, log_content)
        results_achieved = self._extract_results(execution_data, log_content)
        challenges = self._identify_challenges(execution_data, log_content)
        learnings = self._extract_learnings(execution_data, log_content, actions_taken, results_achieved)
        performance_metrics = execution_data.get('performance_metrics', {})
        execution_time = execution_data.get('execution_time', 0.0)
        
        # Analyze success indicators
        success_indicators = self._analyze_success(execution_data, results_achieved)
        
        # Generate improvement suggestions
        improvements = self._generate_improvements(challenges, performance_metrics, agent_name)
        
        # Extract knowledge and patterns
        knowledge_gained = self._extract_knowledge(actions_taken, results_achieved, learnings)
        reusable_patterns = self._identify_patterns(actions_taken, results_achieved, user_query)
        
        # Create summary object
        summary = ExecutionSummary(
            summary_id=summary_id,
            agent_name=agent_name,
            task_id=task_id,
            timestamp=timestamp,
            task_description=user_query or "Task execution",
            actions_taken=actions_taken,
            results_achieved=results_achieved,
            challenges_encountered=challenges,
            learnings_captured=learnings,
            performance_metrics=performance_metrics,
            execution_time=execution_time,
            success_indicators=success_indicators,
            improvement_suggestions=improvements,
            knowledge_gained=knowledge_gained,
            reusable_patterns=reusable_patterns
        )
        
        # Save summary
        self._save_summary(summary)
        
        # Update performance metrics
        self._update_performance_metrics(agent_name, performance_metrics, execution_time)
        
        # Update knowledge base
        self._update_knowledge_base(summary)
        
        self.logger.info(f"Generated summary {summary_id} for agent {agent_name}")
        return summary_id
        
    def _generate_summary_id(self, agent_name: str, task_id: str) -> str:
        """Generate unique summary ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        hash_input = f"{agent_name}_{task_id}_{timestamp}"
        hash_suffix = hashlib.md5(hash_input.encode()).hexdigest()[:8]
        return f"summary_{agent_name}_{timestamp}_{hash_suffix}"
        
    def _extract_actions(self, execution_data: Dict[str, Any], log_content: str) -> List[str]:
        """Extract actions taken during execution"""
        actions = []
        
        # Extract from execution data
        if 'actions' in execution_data:
            actions.extend(execution_data['actions'])
            
        # Extract from log content using patterns
        action_patterns = [
            r'(Creating|Created|Implementing|Implemented|Analyzing|Analyzed|Processing|Processed|Generating|Generated)\s+([^.\n]+)',
            r'(Searching|Found|Loading|Loaded|Saving|Saved|Updating|Updated)\s+([^.\n]+)',
            r'(Reading|Writing|Editing|Calling|Executing)\s+([^.\n]+)',
            r'Tool\s+(\w+):\s*([^.\n]+)',
            r'Action:\s*([^.\n]+)'
        ]
        
        for pattern in action_patterns:
            matches = re.findall(pattern, log_content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    action = ' '.join(match).strip()
                else:
                    action = match.strip()
                if action and len(action) > 10:  # Filter out very short matches
                    actions.append(action)
                    
        # Remove duplicates while preserving order
        seen = set()
        unique_actions = []
        for action in actions:
            if action.lower() not in seen:
                seen.add(action.lower())
                unique_actions.append(action)
                
        return unique_actions[:15]  # Limit to top 15 actions
        
    def _extract_results(self, execution_data: Dict[str, Any], log_content: str) -> List[str]:
        """Extract results achieved during execution"""
        results = []
        
        # Extract from execution data
        if 'results' in execution_data:
            results.extend(execution_data['results'])
            
        # Extract from log content
        result_patterns = [
            r'(Successfully|Completed|Finished|Generated|Created)\s+([^.\n]+)',
            r'Result:\s*([^.\n]+)',
            r'Output:\s*([^.\n]+)',
            r'Achievement:\s*([^.\n]+)',
            r'(Found|Identified|Discovered)\s+(\d+)\s+([^.\n]+)',
            r'Performance:\s*([^.\n]+)',
            r'Quality\s+score:\s*([^.\n]+)'
        ]
        
        for pattern in result_patterns:
            matches = re.findall(pattern, log_content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    result = ' '.join(match).strip()
                else:
                    result = match.strip()
                if result and len(result) > 5:
                    results.append(result)
                    
        # Remove duplicates
        seen = set()
        unique_results = []
        for result in results:
            if result.lower() not in seen:
                seen.add(result.lower())
                unique_results.append(result)
                
        return unique_results[:12]  # Limit to top 12 results
        
    def _identify_challenges(self, execution_data: Dict[str, Any], log_content: str) -> List[str]:
        """Identify challenges encountered during execution"""
        challenges = []
        
        # Extract from execution data
        if 'challenges' in execution_data:
            challenges.extend(execution_data['challenges'])
        if 'errors' in execution_data:
            challenges.extend([f"Error: {err}" for err in execution_data['errors']])
            
        # Extract from log content
        challenge_patterns = [
            r'(Error|Exception|Failed|Failure)\s*:?\s*([^.\n]+)',
            r'(Warning|Issue|Problem|Difficulty|Challenge)\s*:?\s*([^.\n]+)',
            r'(Could not|Unable to|Cannot|Failed to)\s+([^.\n]+)',
            r'(Timeout|Retry|Retrying)\s*:?\s*([^.\n]+)',
            r'(Unexpected|Unknown)\s+([^.\n]+)'
        ]
        
        for pattern in challenge_patterns:
            matches = re.findall(pattern, log_content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    challenge = ' '.join(match).strip()
                else:
                    challenge = match.strip()
                if challenge and len(challenge) > 10:
                    challenges.append(challenge)
                    
        return challenges[:10]  # Limit to top 10 challenges
        
    def _extract_learnings(self, execution_data: Dict[str, Any], log_content: str,
                          actions: List[str], results: List[str]) -> List[str]:
        """Extract key learnings from the execution"""
        learnings = []
        
        # Extract explicit learnings from execution data
        if 'learnings' in execution_data:
            learnings.extend(execution_data['learnings'])
            
        # Generate learnings from actions and results
        if actions and results:
            # Correlate successful actions with good results
            for action in actions[:5]:  # Top 5 actions
                for result in results[:3]:  # Top 3 results
                    if any(word in action.lower() for word in ['successfully', 'completed', 'generated']):
                        learnings.append(f"Action '{action}' led to result '{result}'")
                        
        # Extract patterns from log content
        learning_patterns = [
            r'(Learned|Discovered|Realized|Found that)\s+([^.\n]+)',
            r'(Key insight|Important)\s*:?\s*([^.\n]+)',
            r'(Pattern|Trend)\s*:?\s*([^.\n]+)',
            r'(Best practice|Recommendation)\s*:?\s*([^.\n]+)'
        ]
        
        for pattern in learning_patterns:
            matches = re.findall(pattern, log_content, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                if isinstance(match, tuple):
                    learning = ' '.join(match).strip()
                else:
                    learning = match.strip()
                if learning and len(learning) > 15:
                    learnings.append(learning)
                    
        # Generate synthetic learnings based on performance
        performance_metrics = execution_data.get('performance_metrics', {})
        if performance_metrics:
            high_performing = [k for k, v in performance_metrics.items() if v > 0.8]
            if high_performing:
                learnings.append(f"High performance achieved in: {', '.join(high_performing)}")
                
            low_performing = [k for k, v in performance_metrics.items() if v < 0.6]
            if low_performing:
                learnings.append(f"Areas needing improvement: {', '.join(low_performing)}")
                
        return learnings[:8]  # Limit to top 8 learnings
        
    def _analyze_success(self, execution_data: Dict[str, Any], results: List[str]) -> Dict[str, Any]:
        """Analyze success indicators"""
        success_indicators = {
            'overall_success': False,
            'success_score': 0.0,
            'key_achievements': [],
            'success_factors': []
        }
        
        # Check execution data for success indicators
        if 'success' in execution_data:
            success_indicators['overall_success'] = execution_data['success']
            
        # Calculate success score from performance metrics
        performance_metrics = execution_data.get('performance_metrics', {})
        if performance_metrics:
            avg_performance = sum(performance_metrics.values()) / len(performance_metrics)
            success_indicators['success_score'] = avg_performance
            success_indicators['overall_success'] = avg_performance > 0.7
            
        # Identify key achievements from results
        achievement_keywords = ['successfully', 'completed', 'achieved', 'generated', 'created', 'optimized']
        for result in results:
            if any(keyword in result.lower() for keyword in achievement_keywords):
                success_indicators['key_achievements'].append(result)
                
        # Identify success factors
        if success_indicators['success_score'] > 0.8:
            success_indicators['success_factors'] = [
                'High performance metrics achieved',
                'Multiple objectives completed',
                'Quality standards met'
            ]
        elif success_indicators['success_score'] > 0.6:
            success_indicators['success_factors'] = [
                'Acceptable performance levels',
                'Core objectives completed'
            ]
            
        return success_indicators
        
    def _generate_improvements(self, challenges: List[str], performance_metrics: Dict[str, float],
                             agent_name: str) -> List[str]:
        """Generate improvement suggestions"""
        improvements = []
        
        # Address specific challenges
        for challenge in challenges[:5]:  # Top 5 challenges
            if 'error' in challenge.lower():
                improvements.append(f"Implement error handling for: {challenge}")
            elif 'timeout' in challenge.lower():
                improvements.append(f"Optimize performance to avoid: {challenge}")
            elif 'unable to' in challenge.lower():
                improvements.append(f"Enhance capabilities to handle: {challenge}")
                
        # Address performance metrics
        low_metrics = [k for k, v in performance_metrics.items() if v < 0.7]
        for metric in low_metrics:
            improvements.append(f"Focus on improving {metric} (current: {performance_metrics[metric]:.2%})")
            
        # Agent-specific improvements
        if agent_name.startswith('research-'):
            improvements.append("Consider expanding search strategies for better coverage")
            improvements.append("Implement quality filters to improve relevance")
        elif agent_name.startswith('writer-'):
            improvements.append("Enhance writing quality through iterative refinement")
            improvements.append("Improve integration between different writing components")
        elif agent_name.startswith('coder-'):
            improvements.append("Strengthen code review processes")
            improvements.append("Implement more comprehensive testing strategies")
            
        # General improvements
        if not improvements:
            improvements.append("Continue current successful approaches")
            improvements.append("Monitor performance trends for optimization opportunities")
            
        return improvements[:6]  # Limit to top 6 improvements
        
    def _extract_knowledge(self, actions: List[str], results: List[str], learnings: List[str]) -> str:
        """Extract structured knowledge from execution"""
        knowledge_sections = []
        
        # Process understanding
        if actions:
            knowledge_sections.append(f"**Process Understanding**: Successfully executed {len(actions)} key actions including {', '.join(actions[:3])}")
            
        # Outcome knowledge
        if results:
            knowledge_sections.append(f"**Outcome Knowledge**: Achieved {len(results)} significant results, notably {', '.join(results[:2])}")
            
        # Learning insights
        if learnings:
            knowledge_sections.append(f"**Key Insights**: {'; '.join(learnings[:3])}")
            
        return '\n\n'.join(knowledge_sections)
        
    def _identify_patterns(self, actions: List[str], results: List[str], user_query: str) -> List[str]:
        """Identify reusable patterns"""
        patterns = []
        
        # Action patterns
        action_types = {}
        for action in actions:
            # Extract action type (first word)
            action_type = action.split()[0].lower() if action.split() else 'unknown'
            action_types[action_type] = action_types.get(action_type, 0) + 1
            
        # Most common action patterns
        for action_type, count in sorted(action_types.items(), key=lambda x: x[1], reverse=True)[:3]:
            patterns.append(f"Effective {action_type} pattern used {count} times")
            
        # Query-result patterns
        if user_query and results:
            query_keywords = user_query.lower().split()[:5]  # First 5 words
            if any(keyword in str(results).lower() for keyword in query_keywords):
                patterns.append("Query-result alignment pattern successful")
                
        # Success patterns
        success_keywords = ['successfully', 'completed', 'achieved', 'generated']
        success_count = sum(1 for result in results 
                          if any(keyword in result.lower() for keyword in success_keywords))
        if success_count > len(results) * 0.7:  # 70% success rate
            patterns.append("High success rate pattern identified")
            
        return patterns[:5]  # Limit to top 5 patterns
        
    def _save_summary(self, summary: ExecutionSummary):
        """Save execution summary to files"""
        agent_dir = self.doc_base_path / summary.agent_name
        
        # Save individual summary file (markdown format)
        timestamp_str = datetime.fromisoformat(summary.timestamp).strftime("%Y-%m-%d_%H-%M-%S")
        summary_file = agent_dir / f"{timestamp_str}_{summary.task_id[:8]}_summary.md"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(f"# Execution Summary: {summary.agent_name}\n\n")
            f.write(f"**Summary ID**: {summary.summary_id}\n")
            f.write(f"**Task ID**: {summary.task_id}\n")
            f.write(f"**Timestamp**: {summary.timestamp}\n")
            f.write(f"**Execution Time**: {summary.execution_time:.2f}s\n\n")
            
            f.write(f"## Task Description\n\n{summary.task_description}\n\n")
            
            f.write("## Actions Taken\n\n")
            for i, action in enumerate(summary.actions_taken, 1):
                f.write(f"{i}. {action}\n")
            f.write("\n")
            
            f.write("## Results Achieved\n\n")
            for i, result in enumerate(summary.results_achieved, 1):
                f.write(f"{i}. {result}\n")
            f.write("\n")
            
            if summary.challenges_encountered:
                f.write("## Challenges Encountered\n\n")
                for i, challenge in enumerate(summary.challenges_encountered, 1):
                    f.write(f"{i}. {challenge}\n")
                f.write("\n")
                
            f.write("## Key Learnings\n\n")
            for i, learning in enumerate(summary.learnings_captured, 1):
                f.write(f"{i}. {learning}\n")
            f.write("\n")
            
            if summary.performance_metrics:
                f.write("## Performance Metrics\n\n")
                for metric, value in summary.performance_metrics.items():
                    f.write(f"- **{metric}**: {value:.3f}\n")
                f.write("\n")
                
            f.write("## Success Analysis\n\n")
            si = summary.success_indicators
            f.write(f"- **Overall Success**: {si['overall_success']}\n")
            f.write(f"- **Success Score**: {si['success_score']:.2%}\n")
            if si['key_achievements']:
                f.write("- **Key Achievements**:\n")
                for achievement in si['key_achievements']:
                    f.write(f"  - {achievement}\n")
            f.write("\n")
            
            f.write("## Improvement Suggestions\n\n")
            for i, suggestion in enumerate(summary.improvement_suggestions, 1):
                f.write(f"{i}. {suggestion}\n")
            f.write("\n")
            
            if summary.reusable_patterns:
                f.write("## Reusable Patterns\n\n")
                for i, pattern in enumerate(summary.reusable_patterns, 1):
                    f.write(f"{i}. {pattern}\n")
                f.write("\n")
                
            f.write("## Knowledge Gained\n\n")
            f.write(summary.knowledge_gained)
            
        # Save JSON version for programmatic access
        json_file = agent_dir / f"{timestamp_str}_{summary.task_id[:8]}_summary.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(summary), f, indent=2, ensure_ascii=False)
            
        # Update summary index
        self._update_summary_index(summary)
        
    def _update_summary_index(self, summary: ExecutionSummary):
        """Update the summary index for the agent"""
        agent_dir = self.doc_base_path / summary.agent_name
        index_file = agent_dir / "summary_index.json"
        
        # Load existing index
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
            
        # Add new summary entry
        index_entry = {
            'summary_id': summary.summary_id,
            'task_id': summary.task_id,
            'timestamp': summary.timestamp,
            'task_description': summary.task_description[:100],  # Truncated
            'success_score': summary.success_indicators['success_score'],
            'execution_time': summary.execution_time,
            'keywords': summary.task_description.split()[:5]  # First 5 words as keywords
        }
        
        index['summaries'].append(index_entry)
        index['metadata']['total_summaries'] = len(index['summaries'])
        index['metadata']['last_updated'] = datetime.now().isoformat()
        
        # Sort by timestamp (most recent first)
        index['summaries'].sort(key=lambda x: x['timestamp'], reverse=True)
        
        # Save updated index
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index, f, indent=2, ensure_ascii=False)
            
    def _update_performance_metrics(self, agent_name: str, performance_metrics: Dict[str, float], 
                                  execution_time: float):
        """Update performance metrics file"""
        agent_dir = self.doc_base_path / agent_name
        metrics_file = agent_dir / "performance_metrics.json"
        
        # Load existing metrics
        with open(metrics_file, 'r', encoding='utf-8') as f:
            metrics_data = json.load(f)
            
        # Add new metrics entry
        metrics_entry = {
            'timestamp': datetime.now().isoformat(),
            'metrics': performance_metrics,
            'execution_time': execution_time
        }
        
        metrics_data['metrics_history'].append(metrics_entry)
        metrics_data['current_metrics'] = performance_metrics
        
        # Update trends (simple moving average over last 10 entries)
        recent_entries = metrics_data['metrics_history'][-10:]
        trends = {}
        
        for metric in performance_metrics.keys():
            values = [entry['metrics'].get(metric, 0) for entry in recent_entries if metric in entry['metrics']]
            if len(values) >= 2:
                recent_avg = sum(values[-5:]) / min(5, len(values))
                older_avg = sum(values[:-5]) / max(1, len(values) - 5) if len(values) > 5 else values[0]
                
                if recent_avg > older_avg * 1.05:
                    trends[metric] = 'improving'
                elif recent_avg < older_avg * 0.95:
                    trends[metric] = 'declining'
                else:
                    trends[metric] = 'stable'
                    
        metrics_data['trends'] = trends
        metrics_data['metadata']['last_updated'] = datetime.now().isoformat()
        
        # Save updated metrics
        with open(metrics_file, 'w', encoding='utf-8') as f:
            json.dump(metrics_data, f, indent=2, ensure_ascii=False)
            
    def _update_knowledge_base(self, summary: ExecutionSummary):
        """Update agent's knowledge base with new learnings"""
        agent_dir = self.doc_base_path / summary.agent_name
        kb_file = agent_dir / "knowledge_base.md"
        
        # Read existing knowledge base
        with open(kb_file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Extract new content to add
        new_learnings = summary.learnings_captured
        new_patterns = summary.reusable_patterns
        new_challenges = summary.challenges_encountered
        new_practices = summary.improvement_suggestions
        
        # Find sections and add content
        sections_to_update = {
            "## Key Learnings": new_learnings,
            "## Successful Patterns": new_patterns,
            "## Common Challenges": new_challenges,
            "## Best Practices": new_practices
        }
        
        for section_header, items in sections_to_update.items():
            if section_header in content and items:
                # Find the section
                section_start = content.find(section_header)
                if section_start != -1:
                    # Find next section or end of file
                    next_section = content.find("\n## ", section_start + len(section_header))
                    if next_section == -1:
                        next_section = len(content)
                        
                    # Insert new items
                    insertion_point = section_start + len(section_header) + 2  # After header and newlines
                    timestamp_str = datetime.now().strftime("%Y-%m-%d")
                    
                    new_content_lines = [f"\n### {timestamp_str} Update"]
                    for item in items[:3]:  # Limit to 3 items per update
                        new_content_lines.append(f"- {item}")
                    new_content_lines.append("")
                    
                    new_content = '\n'.join(new_content_lines)
                    content = content[:insertion_point] + new_content + content[insertion_point:]
                    
        # Write updated knowledge base
        with open(kb_file, 'w', encoding='utf-8') as f:
            f.write(content)
            
    def get_agent_summaries(self, agent_name: str, days: int = 30, limit: int = None) -> List[Dict[str, Any]]:
        """Get summaries for specific agent within time period"""
        agent_dir = self.doc_base_path / agent_name
        index_file = agent_dir / "summary_index.json"
        
        if not index_file.exists():
            return []
            
        with open(index_file, 'r', encoding='utf-8') as f:
            index = json.load(f)
            
        # Filter by time
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered_summaries = []
        
        for summary in index['summaries']:
            summary_date = datetime.fromisoformat(summary['timestamp'])
            if summary_date > cutoff_date:
                filtered_summaries.append(summary)
                
        # Apply limit
        if limit:
            filtered_summaries = filtered_summaries[:limit]
            
        return filtered_summaries
        
    def search_summaries(self, query: str, agent_name: str = None) -> List[Dict[str, Any]]:
        """Search summaries by content"""
        results = []
        
        if agent_name:
            agents = [agent_name]
        else:
            agents = [d.name for d in self.doc_base_path.iterdir() if d.is_dir()]
            
        query_lower = query.lower()
        
        for agent in agents:
            summaries = self.get_agent_summaries(agent, days=365)  # Search all summaries
            for summary in summaries:
                if query_lower in summary['task_description'].lower():
                    results.append({
                        'agent_name': agent,
                        'relevance_score': 1.0,  # Could implement more sophisticated scoring
                        **summary
                    })
                    
        # Sort by timestamp (most recent first)
        results.sort(key=lambda x: x['timestamp'], reverse=True)
        return results
        
    def generate_agent_report(self, agent_name: str, days: int = 30) -> Dict[str, Any]:
        """Generate comprehensive report for an agent"""
        summaries = self.get_agent_summaries(agent_name, days)
        
        if not summaries:
            return {'agent_name': agent_name, 'message': 'No summaries found'}
            
        # Load performance metrics
        agent_dir = self.doc_base_path / agent_name
        metrics_file = agent_dir / "performance_metrics.json"
        
        performance_data = {}
        if metrics_file.exists():
            with open(metrics_file, 'r', encoding='utf-8') as f:
                performance_data = json.load(f)
                
        # Calculate statistics
        total_summaries = len(summaries)
        avg_success_score = sum(s['success_score'] for s in summaries) / total_summaries
        avg_execution_time = sum(s['execution_time'] for s in summaries) / total_summaries
        
        # Recent trends
        trends = performance_data.get('trends', {})
        
        return {
            'agent_name': agent_name,
            'reporting_period_days': days,
            'total_summaries': total_summaries,
            'average_success_score': avg_success_score,
            'average_execution_time': avg_execution_time,
            'performance_trends': trends,
            'recent_summaries': summaries[:5],  # Most recent 5
            'current_metrics': performance_data.get('current_metrics', {}),
            'generated_at': datetime.now().isoformat()
        }

# CLI Interface
def main():
    """Command-line interface for summary generation"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Claude Agent Summary Generator')
    parser.add_argument('command', choices=['generate', 'list', 'search', 'report'],
                       help='Command to execute')
    parser.add_argument('--agent', help='Specific agent name')
    parser.add_argument('--task-id', help='Task ID for summary generation')
    parser.add_argument('--query', help='Search query')
    parser.add_argument('--days', type=int, default=30, help='Days for analysis')
    parser.add_argument('--limit', type=int, help='Limit number of results')
    
    args = parser.parse_args()
    
    generator = SummaryGenerator()
    
    if args.command == 'generate':
        if args.agent and args.task_id:
            # Mock execution data for testing
            execution_data = {
                'performance_metrics': {'accuracy': 0.85, 'efficiency': 0.78},
                'execution_time': 45.5,
                'success': True,
                'actions': ['Analyzed query', 'Searched database', 'Processed results'],
                'results': ['Found 10 relevant papers', 'Generated comprehensive summary']
            }
            summary_id = generator.generate_summary(args.agent, args.task_id, execution_data, 
                                                  user_query="Test task for summary generation")
            print(f"Generated summary with ID: {summary_id}")
        else:
            print("Please provide --agent and --task-id for generate command")
            
    elif args.command == 'list':
        if args.agent:
            summaries = generator.get_agent_summaries(args.agent, args.days, args.limit)
            print(f"\n📋 Summaries for {args.agent} (last {args.days} days)")
            for summary in summaries:
                print(f"- {summary['summary_id']}: {summary['task_description'][:50]}... "
                      f"(Score: {summary['success_score']:.2%})")
        else:
            print("Please specify --agent for list command")
            
    elif args.command == 'search':
        if args.query:
            results = generator.search_summaries(args.query, args.agent)
            print(f"\n🔍 Search results for '{args.query}'")
            for result in results[:10]:  # Top 10 results
                print(f"- [{result['agent_name']}] {result['task_description'][:50]}...")
        else:
            print("Please provide --query for search command")
            
    elif args.command == 'report':
        if args.agent:
            report = generator.generate_agent_report(args.agent, args.days)
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print("Please specify --agent for report command")

if __name__ == '__main__':
    main()