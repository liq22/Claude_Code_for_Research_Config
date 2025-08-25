#!/usr/bin/env python3
"""
Cache Statistics Dashboard

Interactive dashboard showing cache system statistics and analytics.

Author: Claude Code Research System
Version: 1.0.0
"""

import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import sys
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

# Add cache system to path
sys.path.append(str(Path(__file__).parent))
from cache import get_simple_cache_system

class CacheDashboard:
    """Cache system dashboard and analytics"""
    
    def __init__(self):
        self.cache = get_simple_cache_system()
        
    def generate_statistics(self) -> Dict:
        """Generate comprehensive cache statistics"""
        stats = self.cache.get_stats()
        
        # Enhanced analytics
        enhanced_stats = {
            **stats,
            'activity_patterns': self._analyze_activity_patterns(),
            'content_analytics': self._analyze_content_types(),
            'performance_metrics': self._calculate_performance_metrics(),
            'growth_trends': self._analyze_growth_trends()
        }
        
        return enhanced_stats
    
    def _analyze_activity_patterns(self) -> Dict:
        """Analyze activity patterns by time"""
        patterns = {
            'hourly': defaultdict(int),
            'daily': defaultdict(int),
            'weekly': defaultdict(int),
            'peak_hours': [],
            'peak_days': []
        }
        
        files = self.cache.list_cache_files()
        
        for file_type, file_list in files.items():
            cache_path = getattr(self.cache, f"{file_type}_path")
            
            for filename in file_list:
                file_path = cache_path / filename
                cache_data = self.cache.read_cache_file(file_path)
                
                if cache_data and 'timestamp' in cache_data:
                    try:
                        dt = datetime.fromisoformat(cache_data['timestamp'])
                        patterns['hourly'][dt.hour] += 1
                        patterns['daily'][dt.strftime('%Y-%m-%d')] += 1
                        patterns['weekly'][dt.strftime('%A')] += 1
                    except:
                        continue
        
        # Find peak times
        if patterns['hourly']:
            peak_hour = max(patterns['hourly'], key=patterns['hourly'].get)
            patterns['peak_hours'] = [peak_hour, patterns['hourly'][peak_hour]]
        
        if patterns['weekly']:
            peak_day = max(patterns['weekly'], key=patterns['weekly'].get)
            patterns['peak_days'] = [peak_day, patterns['weekly'][peak_day]]
        
        return patterns
    
    def _analyze_content_types(self) -> Dict:
        """Analyze content types and patterns"""
        content_stats = {
            'thinking_topics': Counter(),
            'agent_types': Counter(),
            'research_domains': Counter(),
            'tool_usage': Counter(),
            'common_queries': Counter()
        }
        
        files = self.cache.list_cache_files()
        
        for file_type, file_list in files.items():
            cache_path = getattr(self.cache, f"{file_type}_path")
            
            for filename in file_list:
                file_path = cache_path / filename
                cache_data = self.cache.read_cache_file(file_path)
                
                if cache_data and 'content' in cache_data:
                    content = cache_data['content']
                    
                    if file_type == 'thinking':
                        if 'user_query' in content:
                            query = content['user_query'].lower()
                            # Extract key words
                            words = [w for w in query.split() if len(w) > 3][:3]
                            content_stats['common_queries'].update(words)
                        
                        if 'tools_used' in content:
                            content_stats['tool_usage'].update(content['tools_used'])
                    
                    elif file_type == 'agent':
                        if 'agent_name' in content:
                            content_stats['agent_types'][content['agent_name']] += 1
                    
                    elif file_type == 'research':
                        if 'domain' in content:
                            content_stats['research_domains'][content['domain']] += 1
        
        return {k: dict(v.most_common(10)) for k, v in content_stats.items()}
    
    def _calculate_performance_metrics(self) -> Dict:
        """Calculate cache performance metrics"""
        files = self.cache.list_cache_files()
        total_files = sum(len(file_list) for file_list in files.values())
        
        if total_files == 0:
            return {'avg_daily_cache': 0, 'cache_efficiency': 0, 'storage_usage': 0}
        
        # Calculate storage usage
        total_size = 0
        oldest_date = None
        newest_date = None
        
        for file_type, file_list in files.items():
            cache_path = getattr(self.cache, f"{file_type}_path")
            
            for filename in file_list:
                file_path = cache_path / filename
                
                try:
                    total_size += file_path.stat().st_size
                    
                    cache_data = self.cache.read_cache_file(file_path)
                    if cache_data and 'timestamp' in cache_data:
                        dt = datetime.fromisoformat(cache_data['timestamp'])
                        if oldest_date is None or dt < oldest_date:
                            oldest_date = dt
                        if newest_date is None or dt > newest_date:
                            newest_date = dt
                except:
                    continue
        
        # Calculate metrics
        metrics = {
            'storage_usage_mb': round(total_size / (1024 * 1024), 2),
            'avg_file_size_kb': round(total_size / max(total_files, 1) / 1024, 2),
            'total_files': total_files
        }
        
        if oldest_date and newest_date:
            days_span = max((newest_date - oldest_date).days, 1)
            metrics['avg_daily_cache'] = round(total_files / days_span, 2)
            metrics['days_active'] = days_span
        
        return metrics
    
    def _analyze_growth_trends(self) -> Dict:
        """Analyze cache growth trends"""
        daily_counts = defaultdict(int)
        files = self.cache.list_cache_files()
        
        for file_type, file_list in files.items():
            cache_path = getattr(self.cache, f"{file_type}_path")
            
            for filename in file_list:
                file_path = cache_path / filename
                cache_data = self.cache.read_cache_file(file_path)
                
                if cache_data and 'timestamp' in cache_data:
                    try:
                        dt = datetime.fromisoformat(cache_data['timestamp'])
                        date_key = dt.strftime('%Y-%m-%d')
                        daily_counts[date_key] += 1
                    except:
                        continue
        
        # Calculate trends
        if len(daily_counts) >= 2:
            dates = sorted(daily_counts.keys())
            recent_days = dates[-3:] if len(dates) >= 3 else dates
            early_days = dates[:3] if len(dates) >= 3 else dates
            
            recent_avg = sum(daily_counts[d] for d in recent_days) / len(recent_days)
            early_avg = sum(daily_counts[d] for d in early_days) / len(early_days)
            
            growth_rate = ((recent_avg - early_avg) / max(early_avg, 1)) * 100
        else:
            growth_rate = 0
        
        return {
            'daily_counts': dict(daily_counts),
            'growth_rate_percent': round(growth_rate, 1),
            'total_days': len(daily_counts)
        }
    
    def print_dashboard(self):
        """Print formatted dashboard"""
        stats = self.generate_statistics()
        
        print("=" * 80)
        print(" " * 25 + "CLAUDE CODE CACHE DASHBOARD")
        print("=" * 80)
        print()
        
        # Basic stats
        print("📊 CACHE OVERVIEW")
        print("-" * 40)
        print(f"Base Path: {stats['base_path']}")
        print(f"Total Files: {stats['total_files']}")
        print(f"Last Updated: {stats['timestamp'][:19]}")
        print()
        
        # File counts by type
        print("📁 FILES BY TYPE")
        print("-" * 40)
        for cache_type, count in stats['counts'].items():
            print(f"  {cache_type.capitalize()}: {count} files")
        print()
        
        # Performance metrics
        perf = stats['performance_metrics']
        print("⚡ PERFORMANCE METRICS")
        print("-" * 40)
        print(f"Storage Usage: {perf.get('storage_usage_mb', 0)} MB")
        print(f"Average File Size: {perf.get('avg_file_size_kb', 0)} KB")
        if 'avg_daily_cache' in perf:
            print(f"Average Daily Cache: {perf['avg_daily_cache']} files/day")
        if 'days_active' in perf:
            print(f"Days Active: {perf['days_active']} days")
        print()
        
        # Activity patterns
        patterns = stats['activity_patterns']
        print("📈 ACTIVITY PATTERNS")
        print("-" * 40)
        if patterns['peak_hours']:
            print(f"Peak Hour: {patterns['peak_hours'][0]}:00 ({patterns['peak_hours'][1]} files)")
        if patterns['peak_days']:
            print(f"Most Active Day: {patterns['peak_days'][0]} ({patterns['peak_days'][1]} files)")
        print()
        
        # Growth trends
        growth = stats['growth_trends']
        print("📊 GROWTH TRENDS")
        print("-" * 40)
        print(f"Growth Rate: {growth['growth_rate_percent']}%")
        print(f"Active Days: {growth['total_days']}")
        print()
        
        # Content analytics
        content = stats['content_analytics']
        print("🔍 CONTENT ANALYTICS")
        print("-" * 40)
        
        if content['agent_types']:
            print("Top Agents:")
            for agent, count in list(content['agent_types'].items())[:3]:
                print(f"  • {agent}: {count} executions")
        
        if content['common_queries']:
            print("Common Query Terms:")
            for term, count in list(content['common_queries'].items())[:5]:
                print(f"  • {term}: {count} occurrences")
        
        if content['tool_usage']:
            print("Tools Used:")
            for tool, count in list(content['tool_usage'].items())[:3]:
                print(f"  • {tool}: {count} times")
        
        print()
        print("=" * 80)
    
    def export_to_json(self, filename: str = None):
        """Export statistics to JSON"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"cache_stats_{timestamp}.json"
        
        stats = self.generate_statistics()
        
        with open(filename, 'w') as f:
            json.dump(stats, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📄 Statistics exported to: {filename}")
        return filename

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Cache Dashboard")
    parser.add_argument("--export", metavar="FILE", help="Export stats to JSON file")
    parser.add_argument("--format", choices=["json", "dashboard"], default="dashboard", 
                       help="Output format")
    
    args = parser.parse_args()
    
    dashboard = CacheDashboard()
    
    try:
        if args.export:
            dashboard.export_to_json(args.export)
        elif args.format == "json":
            stats = dashboard.generate_statistics()
            print(json.dumps(stats, indent=2, ensure_ascii=False, default=str))
        else:
            dashboard.print_dashboard()
            
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()