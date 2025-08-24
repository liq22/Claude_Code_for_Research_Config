#!/usr/bin/env python3
"""
Goal Manager for Claude Code Agent System

This module manages core goals, success criteria, and performance tracking
for all 18 agents in the research configuration system.
"""

import json
import yaml
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union
from pathlib import Path
import logging
from dataclasses import dataclass, asdict

@dataclass
class AgentGoal:
    """Represents a single agent's goal structure"""
    mission: str
    success_criteria: List[str]
    key_metrics: List[str]
    target_scores: Dict[str, float]
    description: str = ""
    
class GoalManager:
    """Manages agent goals, tracking, and performance metrics"""
    
    def __init__(self, config_path: str = ".claude/goals"):
        self.config_path = Path(config_path)
        self.config_path.mkdir(parents=True, exist_ok=True)
        
        self.goals_file = self.config_path / "agent_goals.yaml"
        self.tracking_file = self.config_path / "goal_tracking.json"
        self.metrics_file = self.config_path / "performance_metrics.json"
        
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        self._load_goals()
        self._load_tracking_data()
        
    def _setup_logging(self):
        """Setup logging for goal manager"""
        log_file = self.config_path / "goal_manager.log"
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
    def _load_goals(self):
        """Load agent goals from YAML configuration"""
        if not self.goals_file.exists():
            self._create_default_goals()
        
        with open(self.goals_file, 'r', encoding='utf-8') as f:
            self.goals_config = yaml.safe_load(f)
            
    def _create_default_goals(self):
        """Create default goals configuration for all 18 agents"""
        default_goals = {
            'metadata': {
                'version': '1.0',
                'created': datetime.now().isoformat(),
                'description': 'Goal definitions for 18-agent research system'
            },
            'agents': {
                # Research Agents (7)
                'research-literature': {
                    'mission': 'Enable comprehensive, accurate, and efficient literature discovery and synthesis',
                    'success_criteria': [
                        'Find 90%+ relevant papers for any research query',
                        'Complete systematic reviews 75% faster than manual methods',
                        'Maintain 95%+ accuracy in data extraction',
                        'Provide comprehensive coverage of research domains'
                    ],
                    'key_metrics': [
                        'relevance_score',
                        'coverage_completeness', 
                        'time_efficiency',
                        'user_satisfaction',
                        'citation_accuracy'
                    ],
                    'target_scores': {
                        'relevance_score': 0.90,
                        'coverage_completeness': 0.85,
                        'time_efficiency': 0.75,
                        'user_satisfaction': 0.90,
                        'citation_accuracy': 0.95
                    }
                },
                'research-knowledge-graph': {
                    'mission': 'Construct comprehensive knowledge networks and identify research connections',
                    'success_criteria': [
                        'Map 95%+ of citation relationships in target domains',
                        'Identify novel cross-domain connections',
                        'Generate actionable insights from network analysis',
                        'Support research strategy planning'
                    ],
                    'key_metrics': [
                        'network_completeness',
                        'connection_accuracy',
                        'insight_quality',
                        'strategy_support'
                    ],
                    'target_scores': {
                        'network_completeness': 0.95,
                        'connection_accuracy': 0.90,
                        'insight_quality': 0.85,
                        'strategy_support': 0.80
                    }
                },
                'research-hypothesis': {
                    'mission': 'Generate novel, testable hypotheses based on evidence analysis',
                    'success_criteria': [
                        'Produce creative yet grounded research hypotheses',
                        'Ensure 80%+ hypothesis testability',
                        'Align hypotheses with research gaps',
                        'Support breakthrough research directions'
                    ],
                    'key_metrics': [
                        'novelty_score',
                        'testability_rate',
                        'evidence_grounding',
                        'breakthrough_potential'
                    ],
                    'target_scores': {
                        'novelty_score': 0.85,
                        'testability_rate': 0.80,
                        'evidence_grounding': 0.90,
                        'breakthrough_potential': 0.75
                    }
                },
                'research-gap-identifier': {
                    'mission': 'Systematically identify research gaps and unexplored opportunities',
                    'success_criteria': [
                        'Find 95%+ of significant research gaps',
                        'Prioritize gaps by research impact potential',
                        'Suggest actionable research directions',
                        'Support funding proposal development'
                    ],
                    'key_metrics': [
                        'gap_coverage',
                        'impact_assessment',
                        'actionability',
                        'proposal_support'
                    ],
                    'target_scores': {
                        'gap_coverage': 0.95,
                        'impact_assessment': 0.85,
                        'actionability': 0.80,
                        'proposal_support': 0.85
                    }
                },
                'research-trends': {
                    'mission': 'Analyze research trends and predict future directions accurately',
                    'success_criteria': [
                        'Identify emerging trends 6+ months early',
                        'Achieve 80%+ prediction accuracy',
                        'Support strategic research planning',
                        'Guide resource allocation decisions'
                    ],
                    'key_metrics': [
                        'trend_detection_speed',
                        'prediction_accuracy',
                        'strategic_support',
                        'resource_guidance'
                    ],
                    'target_scores': {
                        'trend_detection_speed': 0.85,
                        'prediction_accuracy': 0.80,
                        'strategic_support': 0.85,
                        'resource_guidance': 0.75
                    }
                },
                'research-academic': {
                    'mission': 'Provide comprehensive academic literature search and analysis',
                    'success_criteria': [
                        'Access 90%+ of relevant academic sources',
                        'Deliver high-quality bibliographic analysis',
                        'Support rigorous research methodology',
                        'Enable evidence-based decision making'
                    ],
                    'key_metrics': [
                        'source_coverage',
                        'analysis_quality',
                        'methodology_support',
                        'evidence_quality'
                    ],
                    'target_scores': {
                        'source_coverage': 0.90,
                        'analysis_quality': 0.85,
                        'methodology_support': 0.90,
                        'evidence_quality': 0.95
                    }
                },
                'research-semantic-scholar': {
                    'mission': 'Optimize Semantic Scholar API integration for maximum research value',
                    'success_criteria': [
                        'Maximize API efficiency and cost-effectiveness',
                        'Deliver comprehensive paper metadata',
                        'Support advanced search capabilities',
                        'Enable large-scale literature analysis'
                    ],
                    'key_metrics': [
                        'api_efficiency',
                        'metadata_completeness',
                        'search_capability',
                        'scale_support'
                    ],
                    'target_scores': {
                        'api_efficiency': 0.90,
                        'metadata_completeness': 0.95,
                        'search_capability': 0.85,
                        'scale_support': 0.80
                    }
                },
                
                # Writer Agents (8)
                'writer-intro-cluster': {
                    'mission': 'Create compelling, well-structured introductions that engage and inform',
                    'success_criteria': [
                        'Generate Nature-quality introductions',
                        'Achieve perfect logical flow and narrative coherence',
                        'Integrate background, literature, and contributions seamlessly',
                        'Meet journal-specific requirements consistently'
                    ],
                    'key_metrics': [
                        'narrative_quality',
                        'logical_coherence',
                        'integration_quality',
                        'journal_compliance'
                    ],
                    'target_scores': {
                        'narrative_quality': 0.95,
                        'logical_coherence': 0.90,
                        'integration_quality': 0.85,
                        'journal_compliance': 0.95
                    }
                },
                'writer-method-cluster': {
                    'mission': 'Document methodologies with technical precision and clarity',
                    'success_criteria': [
                        'Ensure complete reproducibility of methods',
                        'Maintain mathematical rigor and accuracy',
                        'Provide clear implementation guidelines',
                        'Support peer review requirements'
                    ],
                    'key_metrics': [
                        'reproducibility_score',
                        'mathematical_accuracy',
                        'implementation_clarity',
                        'review_readiness'
                    ],
                    'target_scores': {
                        'reproducibility_score': 0.95,
                        'mathematical_accuracy': 0.98,
                        'implementation_clarity': 0.90,
                        'review_readiness': 0.85
                    }
                },
                'writer-results-cluster': {
                    'mission': 'Present experimental results with clarity and statistical rigor',
                    'success_criteria': [
                        'Ensure statistical significance and validity',
                        'Create compelling data visualizations',
                        'Provide comprehensive performance analysis',
                        'Support scientific conclusions with evidence'
                    ],
                    'key_metrics': [
                        'statistical_rigor',
                        'visualization_quality',
                        'analysis_completeness',
                        'evidence_support'
                    ],
                    'target_scores': {
                        'statistical_rigor': 0.95,
                        'visualization_quality': 0.90,
                        'analysis_completeness': 0.85,
                        'evidence_support': 0.90
                    }
                },
                'writer-discussion-cluster': {
                    'mission': 'Provide insightful analysis and interpretation of research findings',
                    'success_criteria': [
                        'Deliver deep, thoughtful interpretation of results',
                        'Connect findings to broader research context',
                        'Address limitations honestly and constructively',
                        'Suggest meaningful future research directions'
                    ],
                    'key_metrics': [
                        'interpretation_depth',
                        'contextual_connection',
                        'limitation_analysis',
                        'future_direction_quality'
                    ],
                    'target_scores': {
                        'interpretation_depth': 0.90,
                        'contextual_connection': 0.85,
                        'limitation_analysis': 0.85,
                        'future_direction_quality': 0.80
                    }
                },
                'writer-format-cluster': {
                    'mission': 'Ensure perfect formatting and presentation for target journals',
                    'success_criteria': [
                        'Achieve 100% compliance with journal guidelines',
                        'Optimize readability and visual appeal',
                        'Ensure consistent style throughout',
                        'Support multiple journal format requirements'
                    ],
                    'key_metrics': [
                        'format_compliance',
                        'readability_score',
                        'style_consistency',
                        'multi_journal_support'
                    ],
                    'target_scores': {
                        'format_compliance': 1.0,
                        'readability_score': 0.90,
                        'style_consistency': 0.95,
                        'multi_journal_support': 0.85
                    }
                },
                'writer-quality-controller': {
                    'mission': 'Ensure Nature-level quality through 4-gate validation',
                    'success_criteria': [
                        'Detect and prevent all quality issues',
                        'Implement comprehensive validation protocols',
                        'Maintain publication-ready standards',
                        'Support continuous quality improvement'
                    ],
                    'key_metrics': [
                        'issue_detection_rate',
                        'validation_completeness',
                        'publication_readiness',
                        'improvement_tracking'
                    ],
                    'target_scores': {
                        'issue_detection_rate': 0.98,
                        'validation_completeness': 0.95,
                        'publication_readiness': 0.95,
                        'improvement_tracking': 0.90
                    }
                },
                'writer-style-formatter': {
                    'mission': 'Apply journal-specific formatting with perfect accuracy',
                    'success_criteria': [
                        'Master all major journal formatting requirements',
                        'Achieve zero formatting errors',
                        'Support rapid format conversion',
                        'Enable multi-journal submission workflows'
                    ],
                    'key_metrics': [
                        'format_mastery',
                        'error_rate',
                        'conversion_speed',
                        'workflow_support'
                    ],
                    'target_scores': {
                        'format_mastery': 0.95,
                        'error_rate': 0.0,
                        'conversion_speed': 0.90,
                        'workflow_support': 0.85
                    }
                },
                'writer-cache-manager': {
                    'mission': 'Optimize performance through intelligent caching and learning',
                    'success_criteria': [
                        'Achieve 75% improvement in task efficiency',
                        'Maintain high cache hit rates',
                        'Enable pattern-based optimization',
                        'Support continuous learning and improvement'
                    ],
                    'key_metrics': [
                        'efficiency_improvement',
                        'cache_hit_rate',
                        'pattern_recognition',
                        'learning_effectiveness'
                    ],
                    'target_scores': {
                        'efficiency_improvement': 0.75,
                        'cache_hit_rate': 0.80,
                        'pattern_recognition': 0.85,
                        'learning_effectiveness': 0.80
                    }
                },
                
                # Coder Agents (3)
                'coder-reviewer': {
                    'mission': 'Ensure code quality, security, and maintainability excellence',
                    'success_criteria': [
                        'Detect 100% of security vulnerabilities',
                        'Maintain zero critical quality issues',
                        'Ensure production-ready code standards',
                        'Support continuous integration workflows'
                    ],
                    'key_metrics': [
                        'vulnerability_detection',
                        'quality_score',
                        'production_readiness',
                        'ci_integration'
                    ],
                    'target_scores': {
                        'vulnerability_detection': 1.0,
                        'quality_score': 0.95,
                        'production_readiness': 0.90,
                        'ci_integration': 0.85
                    }
                },
                'coder-debugger': {
                    'mission': 'Achieve rapid and accurate debugging with root cause analysis',
                    'success_criteria': [
                        'Resolve 95%+ of reported issues successfully',
                        'Provide accurate root cause analysis',
                        'Minimize debugging time and effort',
                        'Support preventive debugging practices'
                    ],
                    'key_metrics': [
                        'resolution_rate',
                        'analysis_accuracy',
                        'time_efficiency',
                        'prevention_support'
                    ],
                    'target_scores': {
                        'resolution_rate': 0.95,
                        'analysis_accuracy': 0.90,
                        'time_efficiency': 0.85,
                        'prevention_support': 0.80
                    }
                },
                'coder-industrial-ai': {
                    'mission': 'Deploy production-ready AI systems optimized for real-world use',
                    'success_criteria': [
                        'Achieve production-grade performance and reliability',
                        'Optimize for edge and cloud deployment',
                        'Ensure scalability and maintainability',
                        'Support industrial AI best practices'
                    ],
                    'key_metrics': [
                        'performance_optimization',
                        'deployment_success',
                        'scalability_score',
                        'best_practices_compliance'
                    ],
                    'target_scores': {
                        'performance_optimization': 0.90,
                        'deployment_success': 0.95,
                        'scalability_score': 0.85,
                        'best_practices_compliance': 0.90
                    }
                }
            }
        }
        
        with open(self.goals_file, 'w', encoding='utf-8') as f:
            yaml.dump(default_goals, f, default_flow_style=False, sort_keys=False, indent=2)
        
        self.logger.info(f"Created default goals configuration at {self.goals_file}")
        
    def _load_tracking_data(self):
        """Load performance tracking data"""
        if not self.tracking_file.exists():
            self.tracking_data = {'agents': {}}
        else:
            with open(self.tracking_file, 'r', encoding='utf-8') as f:
                self.tracking_data = json.load(f)
                
    def get_agent_goal(self, agent_name: str) -> Optional[Dict[str, Any]]:
        """Get goal configuration for specific agent"""
        return self.goals_config.get('agents', {}).get(agent_name)
        
    def get_all_agents(self) -> List[str]:
        """Get list of all agent names"""
        return list(self.goals_config.get('agents', {}).keys())
        
    def update_agent_performance(self, agent_name: str, metrics: Dict[str, float], 
                                task_description: str = "", execution_time: float = 0):
        """Update performance metrics for an agent"""
        if agent_name not in self.tracking_data['agents']:
            self.tracking_data['agents'][agent_name] = {
                'history': [],
                'current_metrics': {},
                'trend_data': {}
            }
        
        # Add new performance record
        record = {
            'timestamp': datetime.now().isoformat(),
            'metrics': metrics,
            'task_description': task_description,
            'execution_time': execution_time
        }
        
        self.tracking_data['agents'][agent_name]['history'].append(record)
        self.tracking_data['agents'][agent_name]['current_metrics'] = metrics
        
        # Update trend data
        self._update_trends(agent_name, metrics)
        
        # Save tracking data
        self._save_tracking_data()
        
        self.logger.info(f"Updated performance metrics for {agent_name}")
        
    def _update_trends(self, agent_name: str, metrics: Dict[str, float]):
        """Update trend analysis for agent performance"""
        agent_data = self.tracking_data['agents'][agent_name]
        
        if 'trend_data' not in agent_data:
            agent_data['trend_data'] = {}
            
        for metric, value in metrics.items():
            if metric not in agent_data['trend_data']:
                agent_data['trend_data'][metric] = []
                
            agent_data['trend_data'][metric].append({
                'timestamp': datetime.now().isoformat(),
                'value': value
            })
            
            # Keep only last 100 records for trend analysis
            if len(agent_data['trend_data'][metric]) > 100:
                agent_data['trend_data'][metric] = agent_data['trend_data'][metric][-100:]
                
    def get_agent_performance(self, agent_name: str, days: int = 30) -> Dict[str, Any]:
        """Get performance data for agent within specified time period"""
        if agent_name not in self.tracking_data['agents']:
            return {}
            
        agent_data = self.tracking_data['agents'][agent_name]
        cutoff_date = datetime.now() - timedelta(days=days)
        
        # Filter history by date
        recent_history = [
            record for record in agent_data['history']
            if datetime.fromisoformat(record['timestamp']) > cutoff_date
        ]
        
        return {
            'recent_history': recent_history,
            'current_metrics': agent_data.get('current_metrics', {}),
            'goal_achievement': self._calculate_goal_achievement(agent_name),
            'trend_analysis': self._analyze_trends(agent_name, days)
        }
        
    def _calculate_goal_achievement(self, agent_name: str) -> Dict[str, float]:
        """Calculate how well agent is meeting its goals"""
        agent_goal = self.get_agent_goal(agent_name)
        if not agent_goal:
            return {}
            
        agent_data = self.tracking_data['agents'].get(agent_name, {})
        current_metrics = agent_data.get('current_metrics', {})
        target_scores = agent_goal.get('target_scores', {})
        
        achievement = {}
        for metric, target in target_scores.items():
            if metric in current_metrics:
                achievement[metric] = min(current_metrics[metric] / target, 1.0)
            else:
                achievement[metric] = 0.0
                
        return achievement
        
    def _analyze_trends(self, agent_name: str, days: int) -> Dict[str, str]:
        """Analyze performance trends for agent"""
        agent_data = self.tracking_data['agents'].get(agent_name, {})
        trend_data = agent_data.get('trend_data', {})
        
        cutoff_date = datetime.now() - timedelta(days=days)
        trends = {}
        
        for metric, values in trend_data.items():
            recent_values = [
                v for v in values
                if datetime.fromisoformat(v['timestamp']) > cutoff_date
            ]
            
            if len(recent_values) < 2:
                trends[metric] = "insufficient_data"
                continue
                
            # Simple trend analysis
            first_half = recent_values[:len(recent_values)//2]
            second_half = recent_values[len(recent_values)//2:]
            
            avg_first = sum(v['value'] for v in first_half) / len(first_half)
            avg_second = sum(v['value'] for v in second_half) / len(second_half)
            
            if avg_second > avg_first * 1.05:
                trends[metric] = "improving"
            elif avg_second < avg_first * 0.95:
                trends[metric] = "declining"
            else:
                trends[metric] = "stable"
                
        return trends
        
    def generate_goal_report(self, agent_name: str = None) -> Dict[str, Any]:
        """Generate comprehensive goal achievement report"""
        if agent_name:
            agents = [agent_name]
        else:
            agents = self.get_all_agents()
            
        report = {
            'generated_at': datetime.now().isoformat(),
            'agents': {}
        }
        
        for agent in agents:
            agent_performance = self.get_agent_performance(agent)
            agent_goal = self.get_agent_goal(agent)
            
            report['agents'][agent] = {
                'goal': agent_goal,
                'performance': agent_performance,
                'recommendations': self._generate_recommendations(agent)
            }
            
        return report
        
    def _generate_recommendations(self, agent_name: str) -> List[str]:
        """Generate improvement recommendations for agent"""
        achievement = self._calculate_goal_achievement(agent_name)
        recommendations = []
        
        for metric, score in achievement.items():
            if score < 0.8:
                recommendations.append(f"Focus on improving {metric} (current: {score:.2%})")
            elif score >= 0.95:
                recommendations.append(f"Excellent performance in {metric} - maintain standards")
                
        if not recommendations:
            recommendations.append("All metrics meeting targets - continue current approach")
            
        return recommendations
        
    def _save_tracking_data(self):
        """Save tracking data to file"""
        with open(self.tracking_file, 'w', encoding='utf-8') as f:
            json.dump(self.tracking_data, f, indent=2, ensure_ascii=False)
            
    def export_goals(self, format_type: str = 'yaml') -> str:
        """Export goals configuration in specified format"""
        if format_type.lower() == 'json':
            return json.dumps(self.goals_config, indent=2, ensure_ascii=False)
        elif format_type.lower() == 'yaml':
            return yaml.dump(self.goals_config, default_flow_style=False, sort_keys=False)
        else:
            raise ValueError(f"Unsupported format: {format_type}")
            
    def get_system_overview(self) -> Dict[str, Any]:
        """Get system-wide goal and performance overview"""
        total_agents = len(self.get_all_agents())
        active_agents = len([a for a in self.get_all_agents() 
                           if a in self.tracking_data['agents']])
        
        # Calculate average achievement across all agents
        all_achievements = []
        for agent in self.get_all_agents():
            achievement = self._calculate_goal_achievement(agent)
            if achievement:
                all_achievements.extend(achievement.values())
                
        avg_achievement = sum(all_achievements) / len(all_achievements) if all_achievements else 0
        
        return {
            'total_agents': total_agents,
            'active_agents': active_agents,
            'average_goal_achievement': avg_achievement,
            'system_health': 'excellent' if avg_achievement > 0.9 else 
                           'good' if avg_achievement > 0.8 else
                           'needs_attention',
            'last_updated': datetime.now().isoformat()
        }

# CLI Interface
def main():
    """Command-line interface for goal management"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Claude Agent Goal Manager')
    parser.add_argument('command', choices=['init', 'status', 'report', 'update'], 
                       help='Command to execute')
    parser.add_argument('--agent', help='Specific agent name')
    parser.add_argument('--days', type=int, default=30, help='Days for analysis')
    parser.add_argument('--format', choices=['yaml', 'json'], default='yaml', 
                       help='Output format')
    
    args = parser.parse_args()
    
    manager = GoalManager()
    
    if args.command == 'init':
        print("Goal manager initialized successfully!")
        print(f"Configuration saved to: {manager.goals_file}")
        
    elif args.command == 'status':
        overview = manager.get_system_overview()
        print("\n🎯 Agent Goal System Overview")
        print("=" * 40)
        print(f"Total Agents: {overview['total_agents']}")
        print(f"Active Agents: {overview['active_agents']}")
        print(f"Average Achievement: {overview['average_goal_achievement']:.1%}")
        print(f"System Health: {overview['system_health']}")
        
    elif args.command == 'report':
        report = manager.generate_goal_report(args.agent)
        if args.format == 'json':
            print(json.dumps(report, indent=2, ensure_ascii=False))
        else:
            print(yaml.dump(report, default_flow_style=False))
            
    elif args.command == 'update':
        if args.agent:
            # Example metrics update
            manager.update_agent_performance(args.agent, {
                'test_metric': 0.85,
                'performance_score': 0.90
            }, "Test performance update")
            print(f"Updated performance metrics for {args.agent}")
        else:
            print("Please specify --agent for update command")

if __name__ == '__main__':
    main()