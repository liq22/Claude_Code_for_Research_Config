#!/usr/bin/env python3
"""
Claude Code Log Analyzer

Advanced analysis and search capabilities for Claude Code execution logs.
Provides comprehensive analytics, pattern detection, and insights.

Features:
- Full-text search across all logs
- Performance analytics and trends
- Usage pattern detection
- Tool and agent usage analysis
- Success/failure pattern analysis
- Export capabilities

Author: Claude Code Research System
Version: 1.0.0
"""

import json
import gzip
import re
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union, Tuple
from collections import defaultdict, Counter
from dataclasses import dataclass, asdict
import statistics
import argparse

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent))
from keywords_extractor import KeywordsExtractor

@dataclass
class SearchResult:
    """Search result with metadata"""
    session_id: str
    timestamp: str
    user_query: str
    keywords: List[str]
    log_filename: str
    relevance_score: float
    matched_terms: List[str]
    log_path: str

@dataclass
class AnalyticsReport:
    """Comprehensive analytics report"""
    time_period: str
    total_executions: int
    success_rate: float
    average_duration: float
    most_active_days: List[Tuple[str, int]]
    popular_keywords: List[Tuple[str, int]]
    most_used_tools: List[Tuple[str, int]]
    most_used_agents: List[Tuple[str, int]]
    performance_trends: Dict[str, Any]
    usage_patterns: Dict[str, Any]
    recommendations: List[str]

class LogAnalyzer:
    """Advanced log analysis system"""
    
    def __init__(self, logs_base_path: str = "logs"):
        self.logs_base_path = Path(logs_base_path)
        self.keywords_extractor = KeywordsExtractor()
        
        # Ensure logs directory exists
        if not self.logs_base_path.exists():
            raise FileNotFoundError(f"Logs directory not found: {self.logs_base_path}")
    
    def search(self, 
               query: str, 
               days: int = 30,
               limit: int = 50,
               include_content: bool = False) -> List[SearchResult]:
        """
        Search logs with advanced query capabilities
        
        Args:
            query: Search query (supports keywords, phrases, regex)
            days: Number of days to search back
            limit: Maximum number of results
            include_content: Whether to search in full log content
            
        Returns:
            List of SearchResult objects sorted by relevance
        """
        results = []
        query_terms = self._parse_query(query)
        
        # Search date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Search each day's logs
        current_date = start_date
        while current_date <= end_date:
            daily_results = self._search_daily_logs(
                current_date, query_terms, include_content
            )
            results.extend(daily_results)
            current_date += timedelta(days=1)
        
        # Sort by relevance score (descending)
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return results[:limit]
    
    def get_analytics(self, days: int = 30) -> AnalyticsReport:
        """Generate comprehensive analytics report"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        # Collect data across date range
        analytics_data = self._collect_analytics_data(start_date, end_date)
        
        # Calculate metrics
        total_executions = len(analytics_data['executions'])
        success_rate = self._calculate_success_rate(analytics_data['executions'])
        average_duration = self._calculate_average_duration(analytics_data['executions'])
        
        # Analyze patterns
        most_active_days = self._analyze_activity_patterns(analytics_data['daily_counts'])
        popular_keywords = self._analyze_keyword_trends(analytics_data['keywords'])
        most_used_tools = self._analyze_tool_usage(analytics_data['tools'])
        most_used_agents = self._analyze_agent_usage(analytics_data['agents'])
        
        # Performance trends
        performance_trends = self._analyze_performance_trends(analytics_data['executions'])
        
        # Usage patterns
        usage_patterns = self._analyze_usage_patterns(analytics_data)
        
        # Generate recommendations
        recommendations = self._generate_recommendations(analytics_data)
        
        return AnalyticsReport(
            time_period=f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
            total_executions=total_executions,
            success_rate=success_rate,
            average_duration=average_duration,
            most_active_days=most_active_days,
            popular_keywords=popular_keywords,
            most_used_tools=most_used_tools,
            most_used_agents=most_used_agents,
            performance_trends=performance_trends,
            usage_patterns=usage_patterns,
            recommendations=recommendations
        )
    
    def get_execution_details(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get full execution details for a session"""
        # Search across all daily logs for the session
        for daily_dir in self.logs_base_path.glob("executions/*/"):
            index_path = daily_dir / "index.json"
            
            if not index_path.exists():
                continue
                
            try:
                with open(index_path, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)
                
                for entry in index_data:
                    if entry.get('session_id') == session_id:
                        # Load full log content
                        log_path = daily_dir / entry['log_filename']
                        content = self._load_log_content(log_path)
                        
                        return {
                            'index_entry': entry,
                            'full_content': content,
                            'log_path': str(log_path)
                        }
                        
            except Exception as e:
                print(f"Error reading {index_path}: {e}")
                continue
        
        return None
    
    def export_analytics(self, 
                        output_path: str,
                        format: str = 'json',
                        days: int = 30) -> bool:
        """Export analytics to file"""
        try:
            analytics = self.get_analytics(days)
            output_path = Path(output_path)
            
            if format.lower() == 'json':
                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(asdict(analytics), f, indent=2, ensure_ascii=False)
                    
            elif format.lower() == 'markdown':
                markdown_content = self._generate_markdown_report(analytics)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_content)
                    
            elif format.lower() == 'csv':
                csv_content = self._generate_csv_report(analytics)
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(csv_content)
            else:
                raise ValueError(f"Unsupported format: {format}")
                
            return True
            
        except Exception as e:
            print(f"Export failed: {e}")
            return False
    
    def find_similar_sessions(self, session_id: str, limit: int = 10) -> List[SearchResult]:
        """Find sessions similar to given session"""
        # Get base session details
        base_session = self.get_execution_details(session_id)
        if not base_session:
            return []
        
        base_keywords = base_session['index_entry'].get('keywords', [])
        base_query = base_session['index_entry'].get('user_query', '')
        
        # Search for similar sessions using keywords
        similar_results = []
        
        # Use keywords as search terms
        for keyword in base_keywords:
            results = self.search(keyword, days=90, limit=50)
            for result in results:
                if result.session_id != session_id:
                    # Calculate similarity score
                    similarity = self._calculate_similarity(
                        base_keywords, base_query,
                        result.keywords, result.user_query
                    )
                    result.relevance_score = similarity
                    similar_results.append(result)
        
        # Remove duplicates and sort by similarity
        unique_results = {r.session_id: r for r in similar_results}
        sorted_results = sorted(unique_results.values(), 
                              key=lambda x: x.relevance_score, 
                              reverse=True)
        
        return sorted_results[:limit]
    
    def get_performance_insights(self, days: int = 30) -> Dict[str, Any]:
        """Get detailed performance insights"""
        analytics_data = self._collect_analytics_data(
            datetime.now() - timedelta(days=days),
            datetime.now()
        )
        
        insights = {
            'efficiency_metrics': self._analyze_efficiency(analytics_data['executions']),
            'bottlenecks': self._identify_bottlenecks(analytics_data['executions']),
            'success_patterns': self._analyze_success_patterns(analytics_data['executions']),
            'time_patterns': self._analyze_time_patterns(analytics_data['executions']),
            'tool_effectiveness': self._analyze_tool_effectiveness(analytics_data)
        }
        
        return insights
    
    # Private methods
    
    def _parse_query(self, query: str) -> List[str]:
        """Parse search query into terms"""
        # Support quoted phrases
        phrases = re.findall(r'"([^"]*)"', query)
        remaining = re.sub(r'"[^"]*"', '', query)
        
        # Extract individual terms
        terms = re.findall(r'\b\w+\b', remaining.lower())
        
        # Combine phrases and terms
        return phrases + terms
    
    def _search_daily_logs(self, 
                          date: datetime, 
                          query_terms: List[str],
                          include_content: bool) -> List[SearchResult]:
        """Search logs for a specific day"""
        results = []
        daily_path = self.logs_base_path / "executions" / date.strftime("%Y-%m-%d")
        
        if not daily_path.exists():
            return results
        
        index_path = daily_path / "index.json"
        
        if not index_path.exists():
            return results
        
        try:
            with open(index_path, 'r', encoding='utf-8') as f:
                index_data = json.load(f)
            
            for entry in index_data:
                relevance_score, matched_terms = self._calculate_relevance(
                    entry, query_terms, daily_path if include_content else None
                )
                
                if relevance_score > 0:
                    result = SearchResult(
                        session_id=entry.get('session_id', ''),
                        timestamp=entry.get('timestamp', ''),
                        user_query=entry.get('user_query', ''),
                        keywords=entry.get('keywords', []),
                        log_filename=entry.get('log_filename', ''),
                        relevance_score=relevance_score,
                        matched_terms=matched_terms,
                        log_path=str(daily_path / entry.get('log_filename', ''))
                    )
                    results.append(result)
                    
        except Exception as e:
            print(f"Error searching daily logs for {date}: {e}")
        
        return results
    
    def _calculate_relevance(self, 
                           entry: Dict[str, Any], 
                           query_terms: List[str],
                           log_dir: Optional[Path]) -> Tuple[float, List[str]]:
        """Calculate relevance score for log entry"""
        score = 0.0
        matched_terms = []
        
        # Search in user query
        user_query = entry.get('user_query', '').lower()
        for term in query_terms:
            if term.lower() in user_query:
                score += 1.0
                matched_terms.append(term)
        
        # Search in keywords
        keywords = [kw.lower() for kw in entry.get('keywords', [])]
        for term in query_terms:
            if term.lower() in keywords:
                score += 0.8
                if term not in matched_terms:
                    matched_terms.append(term)
        
        # Search in full content if requested
        if log_dir and entry.get('log_filename'):
            log_path = log_dir / entry['log_filename']
            if log_path.exists():
                content = self._load_log_content(log_path)
                if content:
                    content_lower = content.lower()
                    for term in query_terms:
                        if term.lower() in content_lower:
                            score += 0.5
                            if term not in matched_terms:
                                matched_terms.append(term)
        
        return score, matched_terms
    
    def _load_log_content(self, log_path: Path) -> Optional[str]:
        """Load log file content (handles compressed files)"""
        try:
            if log_path.suffix == '.gz':
                with gzip.open(log_path, 'rt', encoding='utf-8') as f:
                    return f.read()
            else:
                with open(log_path, 'r', encoding='utf-8') as f:
                    return f.read()
        except Exception as e:
            print(f"Error loading log content from {log_path}: {e}")
            return None
    
    def _collect_analytics_data(self, start_date: datetime, end_date: datetime) -> Dict[str, Any]:
        """Collect analytics data across date range"""
        data = {
            'executions': [],
            'daily_counts': defaultdict(int),
            'keywords': Counter(),
            'tools': Counter(),
            'agents': Counter(),
            'domains': Counter()
        }
        
        current_date = start_date
        while current_date <= end_date:
            daily_path = self.logs_base_path / "executions" / current_date.strftime("%Y-%m-%d")
            
            if daily_path.exists():
                index_path = daily_path / "index.json"
                
                if index_path.exists():
                    try:
                        with open(index_path, 'r', encoding='utf-8') as f:
                            daily_data = json.load(f)
                        
                        day_key = current_date.strftime("%Y-%m-%d")
                        data['daily_counts'][day_key] = len(daily_data)
                        
                        for entry in daily_data:
                            data['executions'].append(entry)
                            
                            # Count keywords
                            for keyword in entry.get('keywords', []):
                                data['keywords'][keyword] += 1
                            
                            # Count tools and agents (would need to load full log)
                            metrics = entry.get('metrics', {})
                            # Note: Tool and agent data would be extracted from full logs
                            
                    except Exception as e:
                        print(f"Error collecting data from {index_path}: {e}")
            
            current_date += timedelta(days=1)
        
        return data
    
    def _calculate_success_rate(self, executions: List[Dict[str, Any]]) -> float:
        """Calculate overall success rate"""
        if not executions:
            return 0.0
        
        successful = sum(1 for exec in executions 
                        if exec.get('metrics', {}).get('success_rate', 0) > 0.5)
        return successful / len(executions)
    
    def _calculate_average_duration(self, executions: List[Dict[str, Any]]) -> float:
        """Calculate average execution duration"""
        durations = [exec.get('metrics', {}).get('duration_seconds', 0) 
                    for exec in executions]
        durations = [d for d in durations if d > 0]
        
        return statistics.mean(durations) if durations else 0.0
    
    def _analyze_activity_patterns(self, daily_counts: Dict[str, int]) -> List[Tuple[str, int]]:
        """Analyze daily activity patterns"""
        return sorted(daily_counts.items(), key=lambda x: x[1], reverse=True)[:7]
    
    def _analyze_keyword_trends(self, keywords: Counter) -> List[Tuple[str, int]]:
        """Analyze keyword usage trends"""
        return keywords.most_common(10)
    
    def _analyze_tool_usage(self, tools: Counter) -> List[Tuple[str, int]]:
        """Analyze tool usage patterns"""
        return tools.most_common(10)
    
    def _analyze_agent_usage(self, agents: Counter) -> List[Tuple[str, int]]:
        """Analyze agent usage patterns"""
        return agents.most_common(10)
    
    def _analyze_performance_trends(self, executions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze performance trends over time"""
        # Group by day and calculate daily metrics
        daily_metrics = defaultdict(list)
        
        for exec in executions:
            timestamp = exec.get('timestamp', '')
            try:
                date = datetime.fromisoformat(timestamp).date()
                duration = exec.get('metrics', {}).get('duration_seconds', 0)
                success_rate = exec.get('metrics', {}).get('success_rate', 0)
                
                daily_metrics[str(date)].append({
                    'duration': duration,
                    'success_rate': success_rate
                })
            except:
                continue
        
        # Calculate daily averages
        trends = {}
        for date, metrics in daily_metrics.items():
            avg_duration = statistics.mean([m['duration'] for m in metrics])
            avg_success = statistics.mean([m['success_rate'] for m in metrics])
            
            trends[date] = {
                'avg_duration': avg_duration,
                'avg_success_rate': avg_success,
                'execution_count': len(metrics)
            }
        
        return trends
    
    def _analyze_usage_patterns(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze usage patterns"""
        executions = analytics_data['executions']
        
        if not executions:
            return {}
        
        # Time of day analysis
        hour_counts = defaultdict(int)
        for exec in executions:
            timestamp = exec.get('timestamp', '')
            try:
                dt = datetime.fromisoformat(timestamp)
                hour_counts[dt.hour] += 1
            except:
                continue
        
        # Most active hour
        most_active_hour = max(hour_counts.items(), key=lambda x: x[1]) if hour_counts else (0, 0)
        
        return {
            'most_active_hour': most_active_hour[0],
            'hourly_distribution': dict(hour_counts),
            'total_unique_days': len(set(
                datetime.fromisoformat(exec.get('timestamp', '')).date()
                for exec in executions if exec.get('timestamp')
            ))
        }
    
    def _generate_recommendations(self, analytics_data: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        executions = analytics_data['executions']
        
        if not executions:
            return ["Start using Claude Code to get personalized recommendations!"]
        
        # Success rate recommendations
        success_rate = self._calculate_success_rate(executions)
        if success_rate < 0.8:
            recommendations.append(f"Success rate is {success_rate:.1%}. Review failed executions for common issues.")
        
        # Duration recommendations
        avg_duration = self._calculate_average_duration(executions)
        if avg_duration > 120:  # 2 minutes
            recommendations.append("Sessions are running long. Consider breaking complex tasks into smaller steps.")
        
        # Keyword analysis
        popular_keywords = analytics_data['keywords'].most_common(5)
        if popular_keywords:
            top_keyword = popular_keywords[0][0]
            recommendations.append(f"You frequently work with '{top_keyword}'. Consider creating specialized workflows.")
        
        # Activity patterns
        if len(executions) < 5:
            recommendations.append("Try using Claude Code more regularly to build better analytics insights.")
        
        return recommendations
    
    def _calculate_similarity(self, 
                            keywords1: List[str], query1: str,
                            keywords2: List[str], query2: str) -> float:
        """Calculate similarity between two sessions"""
        # Keyword similarity
        set1 = set(keywords1)
        set2 = set(keywords2)
        
        if not set1 or not set2:
            keyword_sim = 0.0
        else:
            intersection = len(set1 & set2)
            union = len(set1 | set2)
            keyword_sim = intersection / union if union > 0 else 0.0
        
        # Query similarity (simple word overlap)
        words1 = set(query1.lower().split())
        words2 = set(query2.lower().split())
        
        if not words1 or not words2:
            query_sim = 0.0
        else:
            intersection = len(words1 & words2)
            union = len(words1 | words2)
            query_sim = intersection / union if union > 0 else 0.0
        
        # Combined similarity (weighted)
        return (keyword_sim * 0.7) + (query_sim * 0.3)
    
    def _analyze_efficiency(self, executions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze execution efficiency metrics"""
        if not executions:
            return {}
        
        durations = [exec.get('metrics', {}).get('duration_seconds', 0) for exec in executions]
        durations = [d for d in durations if d > 0]
        
        if not durations:
            return {}
        
        return {
            'median_duration': statistics.median(durations),
            'p90_duration': sorted(durations)[int(len(durations) * 0.9)],
            'fastest_execution': min(durations),
            'slowest_execution': max(durations)
        }
    
    def _identify_bottlenecks(self, executions: List[Dict[str, Any]]) -> List[str]:
        """Identify common bottlenecks"""
        bottlenecks = []
        
        # Long-running sessions
        long_sessions = [exec for exec in executions 
                        if exec.get('metrics', {}).get('duration_seconds', 0) > 300]
        
        if len(long_sessions) > len(executions) * 0.2:
            bottlenecks.append("20%+ of sessions take over 5 minutes")
        
        # Failed sessions
        failed_sessions = [exec for exec in executions 
                          if exec.get('metrics', {}).get('success_rate', 1) < 0.5]
        
        if len(failed_sessions) > len(executions) * 0.1:
            bottlenecks.append("10%+ of sessions are failing")
        
        return bottlenecks
    
    def _analyze_success_patterns(self, executions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze patterns in successful vs failed executions"""
        successful = [exec for exec in executions 
                     if exec.get('metrics', {}).get('success_rate', 0) > 0.8]
        failed = [exec for exec in executions 
                 if exec.get('metrics', {}).get('success_rate', 0) < 0.5]
        
        patterns = {
            'successful_count': len(successful),
            'failed_count': len(failed),
            'success_keywords': Counter(),
            'failure_keywords': Counter()
        }
        
        for exec in successful:
            for keyword in exec.get('keywords', []):
                patterns['success_keywords'][keyword] += 1
        
        for exec in failed:
            for keyword in exec.get('keywords', []):
                patterns['failure_keywords'][keyword] += 1
        
        return patterns
    
    def _analyze_time_patterns(self, executions: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze temporal usage patterns"""
        patterns = {
            'hourly_success_rate': defaultdict(list),
            'daily_success_rate': defaultdict(list)
        }
        
        for exec in executions:
            timestamp = exec.get('timestamp', '')
            success_rate = exec.get('metrics', {}).get('success_rate', 0)
            
            try:
                dt = datetime.fromisoformat(timestamp)
                patterns['hourly_success_rate'][dt.hour].append(success_rate)
                patterns['daily_success_rate'][dt.strftime('%A')].append(success_rate)
            except:
                continue
        
        # Calculate averages
        for hour, rates in patterns['hourly_success_rate'].items():
            patterns['hourly_success_rate'][hour] = statistics.mean(rates)
        
        for day, rates in patterns['daily_success_rate'].items():
            patterns['daily_success_rate'][day] = statistics.mean(rates)
        
        return dict(patterns)
    
    def _analyze_tool_effectiveness(self, analytics_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze tool usage effectiveness"""
        # This would require parsing full log files to get tool usage data
        # For now, return placeholder structure
        return {
            'most_effective_tools': [],
            'tool_success_rates': {},
            'tool_usage_patterns': {}
        }
    
    def _generate_markdown_report(self, analytics: AnalyticsReport) -> str:
        """Generate markdown analytics report"""
        report = f"""# Claude Code Analytics Report

**Time Period:** {analytics.time_period}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

## 📊 Executive Summary

- **Total Executions:** {analytics.total_executions}
- **Success Rate:** {analytics.success_rate:.1%}
- **Average Duration:** {analytics.average_duration:.1f} seconds

## 📈 Activity Patterns

### Most Active Days
"""
        for day, count in analytics.most_active_days[:5]:
            report += f"- **{day}:** {count} executions\n"
        
        report += f"""
## 🔍 Popular Keywords

"""
        for keyword, count in analytics.popular_keywords[:10]:
            report += f"- **{keyword}:** {count} occurrences\n"
        
        report += f"""
## 🛠 Tool Usage

"""
        if analytics.most_used_tools:
            for tool, count in analytics.most_used_tools[:10]:
                report += f"- **{tool}:** {count} times\n"
        else:
            report += "No tool usage data available.\n"
        
        report += f"""
## 🤖 Agent Usage

"""
        if analytics.most_used_agents:
            for agent, count in analytics.most_used_agents[:10]:
                report += f"- **{agent}:** {count} times\n"
        else:
            report += "No agent usage data available.\n"
        
        report += f"""
## 💡 Recommendations

"""
        for i, rec in enumerate(analytics.recommendations, 1):
            report += f"{i}. {rec}\n"
        
        return report
    
    def _generate_csv_report(self, analytics: AnalyticsReport) -> str:
        """Generate CSV analytics report"""
        csv_lines = [
            "Metric,Value",
            f"Total Executions,{analytics.total_executions}",
            f"Success Rate,{analytics.success_rate:.3f}",
            f"Average Duration,{analytics.average_duration:.2f}",
            "",
            "Most Active Days",
            "Day,Count"
        ]
        
        for day, count in analytics.most_active_days:
            csv_lines.append(f"{day},{count}")
        
        csv_lines.extend([
            "",
            "Popular Keywords",
            "Keyword,Count"
        ])
        
        for keyword, count in analytics.popular_keywords:
            csv_lines.append(f"{keyword},{count}")
        
        return "\n".join(csv_lines)

def main():
    """Command line interface for log analyzer"""
    parser = argparse.ArgumentParser(description="Claude Code Log Analyzer")
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search logs')
    search_parser.add_argument('query', help='Search query')
    search_parser.add_argument('--days', type=int, default=30, help='Days to search back')
    search_parser.add_argument('--limit', type=int, default=10, help='Maximum results')
    search_parser.add_argument('--content', action='store_true', help='Search in full content')
    
    # Analytics command
    analytics_parser = subparsers.add_parser('analytics', help='Generate analytics report')
    analytics_parser.add_argument('--days', type=int, default=30, help='Days to analyze')
    analytics_parser.add_argument('--export', help='Export to file')
    analytics_parser.add_argument('--format', choices=['json', 'markdown', 'csv'], 
                                 default='markdown', help='Export format')
    
    # Details command
    details_parser = subparsers.add_parser('details', help='Get execution details')
    details_parser.add_argument('session_id', help='Session ID')
    
    # Similar command
    similar_parser = subparsers.add_parser('similar', help='Find similar sessions')
    similar_parser.add_argument('session_id', help='Base session ID')
    similar_parser.add_argument('--limit', type=int, default=5, help='Maximum results')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        analyzer = LogAnalyzer()
        
        if args.command == 'search':
            results = analyzer.search(args.query, args.days, args.limit, args.content)
            
            print(f"Found {len(results)} results for '{args.query}':\n")
            for i, result in enumerate(results, 1):
                print(f"{i}. [{result.timestamp}] {result.user_query}")
                print(f"   Keywords: {', '.join(result.keywords)}")
                print(f"   Relevance: {result.relevance_score:.2f}")
                print(f"   Log: {result.log_filename}")
                print()
        
        elif args.command == 'analytics':
            analytics = analyzer.get_analytics(args.days)
            
            if args.export:
                success = analyzer.export_analytics(args.export, args.format, args.days)
                if success:
                    print(f"Analytics exported to {args.export}")
                else:
                    print("Export failed")
            else:
                # Print summary to console
                print("📊 Claude Code Analytics Summary")
                print(f"Time Period: {analytics.time_period}")
                print(f"Total Executions: {analytics.total_executions}")
                print(f"Success Rate: {analytics.success_rate:.1%}")
                print(f"Average Duration: {analytics.average_duration:.1f}s")
                
                if analytics.popular_keywords:
                    print(f"\nTop Keywords: {', '.join([kw for kw, _ in analytics.popular_keywords[:5]])}")
                
                if analytics.recommendations:
                    print("\n💡 Recommendations:")
                    for rec in analytics.recommendations[:3]:
                        print(f"  • {rec}")
        
        elif args.command == 'details':
            details = analyzer.get_execution_details(args.session_id)
            if details:
                entry = details['index_entry']
                print(f"Session: {entry['session_id']}")
                print(f"Timestamp: {entry['timestamp']}")
                print(f"Query: {entry['user_query']}")
                print(f"Keywords: {', '.join(entry['keywords'])}")
                print(f"Duration: {entry.get('metrics', {}).get('duration_seconds', 0):.1f}s")
                print(f"Log File: {details['log_path']}")
            else:
                print(f"Session {args.session_id} not found")
        
        elif args.command == 'similar':
            results = analyzer.find_similar_sessions(args.session_id, args.limit)
            
            if results:
                print(f"Found {len(results)} similar sessions to {args.session_id}:\n")
                for i, result in enumerate(results, 1):
                    print(f"{i}. [{result.timestamp}] {result.user_query}")
                    print(f"   Similarity: {result.relevance_score:.3f}")
                    print(f"   Keywords: {', '.join(result.keywords)}")
                    print()
            else:
                print("No similar sessions found")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()