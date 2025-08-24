#!/usr/bin/env python3
"""
Task Tracker for Claude Code Agent System

This module automatically captures user tasks, extracts requirements,
analyzes patterns, and stores task data for all agents in the system.
"""

import json
import re
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Union, Tuple
from pathlib import Path
import logging
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter

@dataclass
class Task:
    """Represents a single task given to an agent"""
    task_id: str
    agent_name: str
    timestamp: str
    user_query: str
    extracted_requirements: List[str]
    task_type: str
    priority: str
    estimated_complexity: float
    keywords: List[str]
    completion_status: str = "pending"
    execution_time: Optional[float] = None
    success_metrics: Dict[str, float] = None
    completion_summary: str = ""
    
    def __post_init__(self):
        if self.success_metrics is None:
            self.success_metrics = {}

class TaskTracker:
    """Tracks and analyzes user tasks for all agents"""
    
    def __init__(self, task_base_path: str = ".claude/Task"):
        self.task_base_path = Path(task_base_path)
        self.task_base_path.mkdir(parents=True, exist_ok=True)
        
        self.logger = logging.getLogger(__name__)
        self._setup_logging()
        
        # Load existing patterns and history
        self._load_patterns()
        self._initialize_agent_directories()
        
    def _setup_logging(self):
        """Setup logging for task tracker"""
        log_file = self.task_base_path.parent / "goals" / "task_tracker.log"
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
        """Initialize task directories for all agents"""
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
            agent_dir = self.task_base_path / agent_name
            agent_dir.mkdir(parents=True, exist_ok=True)
            
            # Initialize default files if they don't exist
            task_history_file = agent_dir / "task_history.json"
            if not task_history_file.exists():
                with open(task_history_file, 'w', encoding='utf-8') as f:
                    json.dump({"tasks": [], "metadata": {"created": datetime.now().isoformat()}}, f, indent=2)
                    
            patterns_file = agent_dir / "task_patterns.json"
            if not patterns_file.exists():
                with open(patterns_file, 'w', encoding='utf-8') as f:
                    json.dump({"patterns": {}, "metadata": {"created": datetime.now().isoformat()}}, f, indent=2)
                    
    def _load_patterns(self):
        """Load existing task patterns for analysis"""
        self.global_patterns = defaultdict(int)
        self.agent_patterns = defaultdict(lambda: defaultdict(int))
        
    def capture_task(self, agent_name: str, user_query: str, session_context: Dict[str, Any] = None) -> str:
        """Capture a new task for an agent"""
        task_id = self._generate_task_id(agent_name)
        timestamp = datetime.now().isoformat()
        
        # Extract task information
        requirements = self._extract_requirements(user_query)
        task_type = self._classify_task_type(user_query, agent_name)
        priority = self._assess_priority(user_query, requirements)
        complexity = self._estimate_complexity(user_query, requirements)
        keywords = self._extract_task_keywords(user_query)
        
        # Create task object
        task = Task(
            task_id=task_id,
            agent_name=agent_name,
            timestamp=timestamp,
            user_query=user_query,
            extracted_requirements=requirements,
            task_type=task_type,
            priority=priority,
            estimated_complexity=complexity,
            keywords=keywords
        )
        
        # Save task
        self._save_task(task)
        
        # Update patterns
        self._update_patterns(task)
        
        self.logger.info(f"Captured task {task_id} for agent {agent_name}")
        return task_id
        
    def _generate_task_id(self, agent_name: str) -> str:
        """Generate unique task ID"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return f"{agent_name}_{timestamp}_{hash(str(datetime.now())) % 10000:04d}"
        
    def _extract_requirements(self, user_query: str) -> List[str]:
        """Extract specific requirements from user query"""
        requirements = []
        
        # Pattern-based requirement extraction
        requirement_patterns = [
            r"需要|需求|要求|必须|应该|希望|期望",  # Chinese requirement indicators
            r"need|require|must|should|want|expect|desire",  # English requirement indicators
            r"请|让|帮助|协助",  # Request indicators
            r"搜索|分析|生成|创建|实现|优化|修复",  # Action verbs
            r"search|analyze|generate|create|implement|optimize|fix"
        ]
        
        # Extract explicit requirements
        for pattern in requirement_patterns:
            matches = re.findall(rf'{pattern}[^。！？]*[。！？]?', user_query, re.IGNORECASE)
            requirements.extend([match.strip() for match in matches])
            
        # Extract numbered or bulleted requirements
        numbered_reqs = re.findall(r'[1-9]\.\s*(.+?)(?=\n|$)', user_query)
        bulleted_reqs = re.findall(r'[•·-]\s*(.+?)(?=\n|$)', user_query)
        requirements.extend(numbered_reqs + bulleted_reqs)
        
        # Remove duplicates and empty items
        requirements = list(set([req.strip() for req in requirements if req.strip()]))
        
        # If no explicit requirements found, use the whole query as requirement
        if not requirements:
            requirements = [user_query.strip()]
            
        return requirements[:10]  # Limit to top 10 requirements
        
    def _classify_task_type(self, user_query: str, agent_name: str) -> str:
        """Classify the type of task based on query and agent"""
        query_lower = user_query.lower()
        
        # Agent-specific task types
        if agent_name.startswith('research-'):
            if any(word in query_lower for word in ['search', 'find', 'literature', '搜索', '查找']):
                return 'literature_search'
            elif any(word in query_lower for word in ['graph', 'network', 'citation', '图谱', '网络']):
                return 'knowledge_mapping'
            elif any(word in query_lower for word in ['hypothesis', 'theory', '假设', '理论']):
                return 'hypothesis_generation'
            elif any(word in query_lower for word in ['gap', 'opportunity', '空白', '机会']):
                return 'gap_analysis'
            elif any(word in query_lower for word in ['trend', 'future', '趋势', '未来']):
                return 'trend_analysis'
            else:
                return 'research_general'
                
        elif agent_name.startswith('writer-'):
            if any(word in query_lower for word in ['introduction', 'intro', '引言', '介绍']):
                return 'introduction_writing'
            elif any(word in query_lower for word in ['method', 'methodology', '方法']):
                return 'methodology_writing'
            elif any(word in query_lower for word in ['result', 'experiment', '结果', '实验']):
                return 'results_writing'
            elif any(word in query_lower for word in ['discussion', 'conclusion', '讨论', '结论']):
                return 'discussion_writing'
            elif any(word in query_lower for word in ['format', 'style', '格式', '样式']):
                return 'formatting'
            elif any(word in query_lower for word in ['quality', 'review', '质量', '审查']):
                return 'quality_control'
            else:
                return 'writing_general'
                
        elif agent_name.startswith('coder-'):
            if any(word in query_lower for word in ['review', 'audit', '审查', '检查']):
                return 'code_review'
            elif any(word in query_lower for word in ['debug', 'fix', 'error', '调试', '修复', '错误']):
                return 'debugging'
            elif any(word in query_lower for word in ['deploy', 'production', 'industrial', '部署', '生产']):
                return 'deployment'
            else:
                return 'coding_general'
                
        return 'general'
        
    def _assess_priority(self, user_query: str, requirements: List[str]) -> str:
        """Assess task priority based on query content and requirements"""
        query_lower = user_query.lower()
        
        # High priority indicators
        high_priority_words = [
            'urgent', 'asap', 'immediately', 'critical', 'important', 'deadline',
            '紧急', '立即', '马上', '重要', '关键', '截止'
        ]
        
        # Low priority indicators
        low_priority_words = [
            'when convenient', 'no rush', 'sometime', 'eventually', 'later',
            '方便时', '不急', '有空时', '后续', '以后'
        ]
        
        if any(word in query_lower for word in high_priority_words):
            return 'high'
        elif any(word in query_lower for word in low_priority_words):
            return 'low'
        elif len(requirements) > 5:  # Complex tasks get medium priority
            return 'medium'
        else:
            return 'medium'
            
    def _estimate_complexity(self, user_query: str, requirements: List[str]) -> float:
        """Estimate task complexity on scale of 0-1"""
        complexity_score = 0.3  # Base complexity
        
        # Add complexity based on number of requirements
        complexity_score += min(len(requirements) * 0.1, 0.4)
        
        # Add complexity based on query length
        complexity_score += min(len(user_query) / 1000, 0.2)
        
        # Add complexity for technical terms
        technical_terms = [
            'algorithm', 'optimization', 'neural', 'machine learning', 'deep learning',
            'statistical', 'mathematical', 'computational', 'analysis',
            '算法', '优化', '神经', '机器学习', '深度学习', '统计', '数学', '计算', '分析'
        ]
        
        tech_term_count = sum(1 for term in technical_terms if term in user_query.lower())
        complexity_score += min(tech_term_count * 0.05, 0.1)
        
        return min(complexity_score, 1.0)
        
    def _extract_task_keywords(self, user_query: str) -> List[str]:
        """Extract keywords from user query for indexing"""
        # Import keywords extractor from existing logging system
        try:
            from scripts.logging.keywords_extractor import KeywordsExtractor
            extractor = KeywordsExtractor()
            return extractor.extract_keywords(user_query, max_keywords=8)
        except ImportError:
            # Fallback keyword extraction
            return self._simple_keyword_extraction(user_query)
            
    def _simple_keyword_extraction(self, text: str) -> List[str]:
        """Simple keyword extraction as fallback"""
        # Remove common words
        stop_words = {
            'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with',
            'to', 'for', 'of', 'as', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            '的', '是', '在', '有', '和', '或', '但是', '与', '为了', '关于', '通过', '期间'
        }
        
        # Extract words (3+ characters, not stop words)
        words = re.findall(r'\b\w{3,}\b', text.lower())
        keywords = [word for word in words if word not in stop_words]
        
        # Return most frequent words
        word_counts = Counter(keywords)
        return [word for word, count in word_counts.most_common(8)]
        
    def _save_task(self, task: Task):
        """Save task to agent's task history"""
        agent_dir = self.task_base_path / task.agent_name
        task_history_file = agent_dir / "task_history.json"
        individual_task_file = agent_dir / f"task_{task.task_id}.json"
        
        # Load existing history
        with open(task_history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
            
        # Add new task
        history['tasks'].append(asdict(task))
        history['metadata']['last_updated'] = datetime.now().isoformat()
        history['metadata']['total_tasks'] = len(history['tasks'])
        
        # Save updated history
        with open(task_history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
            
        # Save individual task file
        with open(individual_task_file, 'w', encoding='utf-8') as f:
            json.dump(asdict(task), f, indent=2, ensure_ascii=False)
            
    def _update_patterns(self, task: Task):
        """Update task patterns for analysis"""
        agent_dir = self.task_base_path / task.agent_name
        patterns_file = agent_dir / "task_patterns.json"
        
        # Load existing patterns
        with open(patterns_file, 'r', encoding='utf-8') as f:
            patterns = json.load(f)
            
        # Update patterns
        if 'task_types' not in patterns['patterns']:
            patterns['patterns']['task_types'] = {}
        if 'keywords' not in patterns['patterns']:
            patterns['patterns']['keywords'] = {}
        if 'complexity_distribution' not in patterns['patterns']:
            patterns['patterns']['complexity_distribution'] = {}
        if 'priority_distribution' not in patterns['patterns']:
            patterns['patterns']['priority_distribution'] = {}
            
        # Update task type frequency
        task_type = task.task_type
        patterns['patterns']['task_types'][task_type] = patterns['patterns']['task_types'].get(task_type, 0) + 1
        
        # Update keyword frequency
        for keyword in task.keywords:
            patterns['patterns']['keywords'][keyword] = patterns['patterns']['keywords'].get(keyword, 0) + 1
            
        # Update complexity distribution
        complexity_range = f"{int(task.estimated_complexity * 10) / 10:.1f}"
        patterns['patterns']['complexity_distribution'][complexity_range] = \
            patterns['patterns']['complexity_distribution'].get(complexity_range, 0) + 1
            
        # Update priority distribution
        patterns['patterns']['priority_distribution'][task.priority] = \
            patterns['patterns']['priority_distribution'].get(task.priority, 0) + 1
            
        patterns['metadata']['last_updated'] = datetime.now().isoformat()
        
        # Save updated patterns
        with open(patterns_file, 'w', encoding='utf-8') as f:
            json.dump(patterns, f, indent=2, ensure_ascii=False)
            
    def update_task_completion(self, task_id: str, success_metrics: Dict[str, float], 
                             execution_time: float, summary: str):
        """Update task with completion information"""
        # Find task file
        for agent_dir in self.task_base_path.iterdir():
            if agent_dir.is_dir():
                task_file = agent_dir / f"task_{task_id}.json"
                if task_file.exists():
                    # Load and update task
                    with open(task_file, 'r', encoding='utf-8') as f:
                        task_data = json.load(f)
                        
                    task_data['completion_status'] = 'completed'
                    task_data['execution_time'] = execution_time
                    task_data['success_metrics'] = success_metrics
                    task_data['completion_summary'] = summary
                    
                    # Save updated task
                    with open(task_file, 'w', encoding='utf-8') as f:
                        json.dump(task_data, f, indent=2, ensure_ascii=False)
                        
                    # Update history file
                    history_file = agent_dir / "task_history.json"
                    with open(history_file, 'r', encoding='utf-8') as f:
                        history = json.load(f)
                        
                    # Find and update task in history
                    for i, task in enumerate(history['tasks']):
                        if task['task_id'] == task_id:
                            history['tasks'][i] = task_data
                            break
                            
                    with open(history_file, 'w', encoding='utf-8') as f:
                        json.dump(history, f, indent=2, ensure_ascii=False)
                        
                    self.logger.info(f"Updated task completion for {task_id}")
                    return
                    
        self.logger.warning(f"Task {task_id} not found for completion update")
        
    def get_agent_tasks(self, agent_name: str, days: int = 30, status: str = None) -> List[Dict[str, Any]]:
        """Get tasks for specific agent within time period"""
        agent_dir = self.task_base_path / agent_name
        if not agent_dir.exists():
            return []
            
        history_file = agent_dir / "task_history.json"
        if not history_file.exists():
            return []
            
        with open(history_file, 'r', encoding='utf-8') as f:
            history = json.load(f)
            
        # Filter by time and status
        cutoff_date = datetime.now() - timedelta(days=days)
        filtered_tasks = []
        
        for task in history['tasks']:
            task_date = datetime.fromisoformat(task['timestamp'])
            if task_date > cutoff_date:
                if status is None or task['completion_status'] == status:
                    filtered_tasks.append(task)
                    
        return filtered_tasks
        
    def get_task_analytics(self, agent_name: str = None, days: int = 30) -> Dict[str, Any]:
        """Get comprehensive task analytics"""
        if agent_name:
            agents = [agent_name]
        else:
            agents = [d.name for d in self.task_base_path.iterdir() if d.is_dir()]
            
        analytics = {
            'generated_at': datetime.now().isoformat(),
            'time_period_days': days,
            'agents': {}
        }
        
        for agent in agents:
            tasks = self.get_agent_tasks(agent, days)
            if not tasks:
                continue
                
            # Calculate analytics
            total_tasks = len(tasks)
            completed_tasks = len([t for t in tasks if t['completion_status'] == 'completed'])
            avg_complexity = sum(t['estimated_complexity'] for t in tasks) / total_tasks
            
            # Task type distribution
            task_types = Counter(t['task_type'] for t in tasks)
            
            # Priority distribution
            priorities = Counter(t['priority'] for t in tasks)
            
            # Completion rate by complexity
            completion_by_complexity = {}
            for task in tasks:
                complexity_range = f"{int(task['estimated_complexity'] * 10) / 10:.1f}"
                if complexity_range not in completion_by_complexity:
                    completion_by_complexity[complexity_range] = {'total': 0, 'completed': 0}
                completion_by_complexity[complexity_range]['total'] += 1
                if task['completion_status'] == 'completed':
                    completion_by_complexity[complexity_range]['completed'] += 1
                    
            analytics['agents'][agent] = {
                'total_tasks': total_tasks,
                'completed_tasks': completed_tasks,
                'completion_rate': completed_tasks / total_tasks if total_tasks > 0 else 0,
                'average_complexity': avg_complexity,
                'task_type_distribution': dict(task_types),
                'priority_distribution': dict(priorities),
                'completion_by_complexity': completion_by_complexity
            }
            
        return analytics
        
    def recommend_tasks(self, agent_name: str, context: str = "") -> List[Dict[str, Any]]:
        """Recommend tasks based on historical patterns"""
        # Load patterns for agent
        agent_dir = self.task_base_path / agent_name
        patterns_file = agent_dir / "task_patterns.json"
        
        if not patterns_file.exists():
            return []
            
        with open(patterns_file, 'r', encoding='utf-8') as f:
            patterns = json.load(f)
            
        recommendations = []
        
        # Most common task types
        task_types = patterns['patterns'].get('task_types', {})
        most_common_types = sorted(task_types.items(), key=lambda x: x[1], reverse=True)[:3]
        
        for task_type, frequency in most_common_types:
            recommendations.append({
                'type': 'frequent_task_type',
                'suggestion': f"Consider {task_type} tasks (completed {frequency} times)",
                'confidence': min(frequency / 10, 1.0)
            })
            
        # High-success complexity ranges
        recent_tasks = self.get_agent_tasks(agent_name, days=60)
        successful_tasks = [t for t in recent_tasks if t['completion_status'] == 'completed' 
                          and t.get('success_metrics', {}).get('performance_score', 0) > 0.8]
        
        if successful_tasks:
            avg_successful_complexity = sum(t['estimated_complexity'] for t in successful_tasks) / len(successful_tasks)
            recommendations.append({
                'type': 'optimal_complexity',
                'suggestion': f"Optimal task complexity range: {avg_successful_complexity:.2f}",
                'confidence': 0.8
            })
            
        return recommendations
        
    def export_task_data(self, agent_name: str = None, format_type: str = 'json') -> Union[str, Dict]:
        """Export task data in specified format"""
        analytics = self.get_task_analytics(agent_name, days=365)  # Full year
        
        if format_type.lower() == 'json':
            return json.dumps(analytics, indent=2, ensure_ascii=False)
        elif format_type.lower() == 'csv':
            # Convert to CSV format (simplified)
            import csv
            import io
            
            output = io.StringIO()
            writer = csv.writer(output)
            writer.writerow(['Agent', 'Total Tasks', 'Completed Tasks', 'Completion Rate', 'Avg Complexity'])
            
            for agent, data in analytics['agents'].items():
                writer.writerow([
                    agent, 
                    data['total_tasks'],
                    data['completed_tasks'], 
                    f"{data['completion_rate']:.2%}",
                    f"{data['average_complexity']:.3f}"
                ])
                
            return output.getvalue()
        else:
            return analytics

# CLI Interface
def main():
    """Command-line interface for task tracking"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Claude Agent Task Tracker')
    parser.add_argument('command', choices=['capture', 'status', 'analytics', 'recommend', 'export'],
                       help='Command to execute')
    parser.add_argument('--agent', help='Specific agent name')
    parser.add_argument('--query', help='User query for task capture')
    parser.add_argument('--days', type=int, default=30, help='Days for analysis')
    parser.add_argument('--format', choices=['json', 'csv'], default='json', help='Export format')
    
    args = parser.parse_args()
    
    tracker = TaskTracker()
    
    if args.command == 'capture':
        if args.agent and args.query:
            task_id = tracker.capture_task(args.agent, args.query)
            print(f"Task captured with ID: {task_id}")
        else:
            print("Please provide --agent and --query for capture command")
            
    elif args.command == 'status':
        if args.agent:
            tasks = tracker.get_agent_tasks(args.agent, args.days)
            print(f"\n📋 Tasks for {args.agent} (last {args.days} days)")
            print(f"Total tasks: {len(tasks)}")
            completed = len([t for t in tasks if t['completion_status'] == 'completed'])
            print(f"Completed: {completed}")
            print(f"Completion rate: {completed/len(tasks):.1%}" if tasks else "No tasks")
        else:
            print("Please specify --agent for status command")
            
    elif args.command == 'analytics':
        analytics = tracker.get_task_analytics(args.agent, args.days)
        print(json.dumps(analytics, indent=2, ensure_ascii=False))
        
    elif args.command == 'recommend':
        if args.agent:
            recommendations = tracker.recommend_tasks(args.agent)
            print(f"\n💡 Recommendations for {args.agent}")
            for rec in recommendations:
                print(f"- {rec['suggestion']} (confidence: {rec['confidence']:.1%})")
        else:
            print("Please specify --agent for recommend command")
            
    elif args.command == 'export':
        data = tracker.export_task_data(args.agent, args.format)
        print(data)

if __name__ == '__main__':
    main()