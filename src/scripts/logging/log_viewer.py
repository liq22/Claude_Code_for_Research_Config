#!/usr/bin/env python3
"""
Claude Code Interactive Log Viewer

User-friendly interactive interface for browsing and exploring Claude Code execution logs.
Provides various viewing modes: recent logs, search interface, detailed analysis.

Features:
- Recent executions browser
- Interactive search
- Detailed log inspection
- Performance visualization
- Session comparison
- Export utilities

Author: Claude Code Research System
Version: 1.0.0
"""

import os
import sys
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import re

# Add parent directory for imports
sys.path.append(str(Path(__file__).parent))
from log_analyzer import LogAnalyzer, SearchResult, AnalyticsReport

class LogViewer:
    """Interactive log viewer with multiple viewing modes"""
    
    def __init__(self, logs_base_path: str = "logs"):
        self.analyzer = LogAnalyzer(logs_base_path)
        self.logs_base_path = Path(logs_base_path)
    
    def interactive_mode(self):
        """Start interactive browsing mode"""
        print("🚀 Claude Code Log Viewer")
        print("=" * 50)
        
        while True:
            try:
                self._display_main_menu()
                choice = input("\nEnter your choice (1-8, or 'q' to quit): ").strip().lower()
                
                if choice == 'q' or choice == 'quit':
                    print("Goodbye! 👋")
                    break
                elif choice == '1':
                    self._view_recent_logs()
                elif choice == '2':
                    self._interactive_search()
                elif choice == '3':
                    self._view_analytics_summary()
                elif choice == '4':
                    self._detailed_log_inspector()
                elif choice == '5':
                    self._find_similar_sessions()
                elif choice == '6':
                    self._performance_insights()
                elif choice == '7':
                    self._export_data()
                elif choice == '8':
                    self._show_help()
                else:
                    print("❌ Invalid choice. Please try again.")
                    
                input("\nPress Enter to continue...")
                self._clear_screen()
                
            except KeyboardInterrupt:
                print("\n\nGoodbye! 👋")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                input("\nPress Enter to continue...")
    
    def _display_main_menu(self):
        """Display the main menu"""
        print("\n📋 Main Menu:")
        print("1. 📅 View Recent Executions")
        print("2. 🔍 Search Logs")
        print("3. 📊 Analytics Summary")
        print("4. 🔍 Detailed Log Inspector") 
        print("5. 🔗 Find Similar Sessions")
        print("6. ⚡ Performance Insights")
        print("7. 📤 Export Data")
        print("8. ❓ Help")
        print("q. Quit")
    
    def _view_recent_logs(self):
        """View recent execution logs"""
        print("\n📅 Recent Executions")
        print("=" * 50)
        
        days = self._get_number_input("How many days back to look? (default: 7): ", 7)
        limit = self._get_number_input("How many results to show? (default: 20): ", 20)
        
        # Get recent logs by searching with empty query
        results = self.analyzer.search("", days=days, limit=limit)
        
        if not results:
            print("No recent executions found.")
            return
        
        print(f"\nFound {len(results)} recent executions:\n")
        
        for i, result in enumerate(results, 1):
            timestamp = datetime.fromisoformat(result.timestamp)
            formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
            
            # Truncate query for display
            query_display = result.user_query[:60] + "..." if len(result.user_query) > 60 else result.user_query
            
            print(f"{i:2}. [{formatted_time}] {query_display}")
            print(f"    🏷️  Keywords: {', '.join(result.keywords[:5])}")
            print(f"    📄 Log: {result.log_filename}")
            print()
        
        # Option to view details of a specific log
        while True:
            choice = input("Enter number to view details (or Enter to continue): ").strip()
            if not choice:
                break
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(results):
                    self._show_log_details(results[index].session_id)
                    break
                else:
                    print("❌ Invalid number. Please try again.")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def _interactive_search(self):
        """Interactive search interface"""
        print("\n🔍 Interactive Search")
        print("=" * 50)
        
        while True:
            query = input("\nEnter search query (or 'back' to return): ").strip()
            
            if query.lower() == 'back' or not query:
                break
            
            print("🔍 Searching...")
            
            days = self._get_number_input("Search how many days back? (default: 30): ", 30)
            limit = self._get_number_input("Maximum results? (default: 15): ", 15)
            
            results = self.analyzer.search(query, days=days, limit=limit, include_content=True)
            
            if not results:
                print(f"No results found for '{query}'.")
                continue
            
            print(f"\n📋 Found {len(results)} results for '{query}':")
            print("-" * 60)
            
            for i, result in enumerate(results, 1):
                timestamp = datetime.fromisoformat(result.timestamp)
                formatted_time = timestamp.strftime("%Y-%m-%d %H:%M")
                
                print(f"{i:2}. [{formatted_time}] Score: {result.relevance_score:.2f}")
                print(f"    💬 Query: {result.user_query[:80]}{'...' if len(result.user_query) > 80 else ''}")
                print(f"    🏷️  Keywords: {', '.join(result.keywords)}")
                print(f"    ✨ Matched: {', '.join(result.matched_terms)}")
                print(f"    📄 Log: {result.log_filename}")
                print()
            
            # Option to view details
            while True:
                choice = input("Enter number to view details (or Enter for new search): ").strip()
                if not choice:
                    break
                
                try:
                    index = int(choice) - 1
                    if 0 <= index < len(results):
                        self._show_log_details(results[index].session_id)
                        break
                    else:
                        print("❌ Invalid number.")
                except ValueError:
                    print("❌ Please enter a valid number.")
    
    def _view_analytics_summary(self):
        """View analytics summary"""
        print("\n📊 Analytics Summary")
        print("=" * 50)
        
        days = self._get_number_input("Analyze how many days? (default: 30): ", 30)
        
        print("📊 Generating analytics report...")
        analytics = self.analyzer.get_analytics(days)
        
        # Display summary
        print(f"\n📈 Summary for {analytics.time_period}")
        print("-" * 50)
        print(f"Total Executions: {analytics.total_executions}")
        print(f"Success Rate: {analytics.success_rate:.1%}")
        print(f"Average Duration: {analytics.average_duration:.1f} seconds")
        
        # Most active days
        if analytics.most_active_days:
            print(f"\n📅 Most Active Days:")
            for day, count in analytics.most_active_days[:5]:
                print(f"  • {day}: {count} executions")
        
        # Popular keywords
        if analytics.popular_keywords:
            print(f"\n🏷️  Popular Keywords:")
            for keyword, count in analytics.popular_keywords[:10]:
                print(f"  • {keyword}: {count} times")
        
        # Tool usage
        if analytics.most_used_tools:
            print(f"\n🛠️  Most Used Tools:")
            for tool, count in analytics.most_used_tools[:8]:
                print(f"  • {tool}: {count} times")
        
        # Agent usage
        if analytics.most_used_agents:
            print(f"\n🤖 Most Used Agents:")
            for agent, count in analytics.most_used_agents[:8]:
                print(f"  • {agent}: {count} times")
        
        # Recommendations
        if analytics.recommendations:
            print(f"\n💡 Recommendations:")
            for i, rec in enumerate(analytics.recommendations, 1):
                print(f"  {i}. {rec}")
        
        # Option to export
        export_choice = input("\n📤 Export this report? (y/n): ").strip().lower()
        if export_choice == 'y':
            format_choice = input("Format (json/markdown/csv): ").strip().lower()
            if format_choice in ['json', 'markdown', 'csv']:
                filename = f"analytics_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_choice}"
                output_path = self.logs_base_path / "analytics" / filename
                output_path.parent.mkdir(exist_ok=True)
                
                if self.analyzer.export_analytics(str(output_path), format_choice, days):
                    print(f"✅ Report exported to: {output_path}")
                else:
                    print("❌ Export failed.")
    
    def _detailed_log_inspector(self):
        """Detailed log file inspector"""
        print("\n🔍 Detailed Log Inspector")
        print("=" * 50)
        
        session_id = input("Enter session ID: ").strip()
        
        if not session_id:
            print("❌ Session ID is required.")
            return
        
        self._show_log_details(session_id)
    
    def _show_log_details(self, session_id: str):
        """Show detailed information for a session"""
        print(f"\n🔍 Detailed View: {session_id}")
        print("=" * 60)
        
        details = self.analyzer.get_execution_details(session_id)
        
        if not details:
            print("❌ Session not found.")
            return
        
        entry = details['index_entry']
        
        # Basic information
        timestamp = datetime.fromisoformat(entry.get('timestamp', ''))
        print(f"📅 Timestamp: {timestamp.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"💬 User Query: {entry.get('user_query', 'N/A')}")
        print(f"🏷️  Keywords: {', '.join(entry.get('keywords', []))}")
        print(f"📄 Log File: {entry.get('log_filename', 'N/A')}")
        
        # Metrics
        metrics = entry.get('metrics', {})
        if metrics:
            print(f"\n📊 Execution Metrics:")
            print(f"  • Duration: {metrics.get('duration_seconds', 0):.1f} seconds")
            print(f"  • Success Rate: {metrics.get('success_rate', 0):.1%}")
            print(f"  • Tools Used: {metrics.get('tools_count', 0)}")
            print(f"  • Files Accessed: {metrics.get('files_accessed_count', 0)}")
            print(f"  • Agents Invoked: {metrics.get('agents_invoked_count', 0)}")
            print(f"  • Execution Steps: {metrics.get('execution_steps', 0)}")
        
        # Show full log content option
        show_content = input("\n📄 View full log content? (y/n): ").strip().lower()
        if show_content == 'y':
            content = details.get('full_content', '')
            if content:
                print("\n" + "="*60)
                print("📄 FULL LOG CONTENT")
                print("="*60)
                print(content)
                print("="*60)
            else:
                print("❌ Could not load log content.")
        
        # Find similar sessions option
        find_similar = input("\n🔗 Find similar sessions? (y/n): ").strip().lower()
        if find_similar == 'y':
            print("🔍 Finding similar sessions...")
            similar = self.analyzer.find_similar_sessions(session_id, limit=5)
            
            if similar:
                print(f"\n🔗 Found {len(similar)} similar sessions:")
                for i, result in enumerate(similar, 1):
                    timestamp = datetime.fromisoformat(result.timestamp)
                    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M")
                    print(f"  {i}. [{formatted_time}] Similarity: {result.relevance_score:.3f}")
                    print(f"     💬 {result.user_query[:60]}{'...' if len(result.user_query) > 60 else ''}")
            else:
                print("No similar sessions found.")
    
    def _find_similar_sessions(self):
        """Find similar sessions interface"""
        print("\n🔗 Find Similar Sessions")
        print("=" * 50)
        
        session_id = input("Enter base session ID: ").strip()
        
        if not session_id:
            print("❌ Session ID is required.")
            return
        
        limit = self._get_number_input("How many similar sessions to find? (default: 10): ", 10)
        
        print("🔍 Finding similar sessions...")
        similar = self.analyzer.find_similar_sessions(session_id, limit=limit)
        
        if not similar:
            print("No similar sessions found.")
            return
        
        print(f"\n🔗 Found {len(similar)} similar sessions to {session_id}:")
        print("-" * 60)
        
        for i, result in enumerate(similar, 1):
            timestamp = datetime.fromisoformat(result.timestamp)
            formatted_time = timestamp.strftime("%Y-%m-%d %H:%M")
            
            print(f"{i:2}. [{formatted_time}] Similarity: {result.relevance_score:.3f}")
            print(f"    💬 Query: {result.user_query[:70]}{'...' if len(result.user_query) > 70 else ''}")
            print(f"    🏷️  Keywords: {', '.join(result.keywords[:6])}")
            print(f"    📄 Log: {result.log_filename}")
            print()
        
        # Option to view details
        while True:
            choice = input("Enter number to view details (or Enter to continue): ").strip()
            if not choice:
                break
            
            try:
                index = int(choice) - 1
                if 0 <= index < len(similar):
                    self._show_log_details(similar[index].session_id)
                    break
                else:
                    print("❌ Invalid number.")
            except ValueError:
                print("❌ Please enter a valid number.")
    
    def _performance_insights(self):
        """Show performance insights"""
        print("\n⚡ Performance Insights")
        print("=" * 50)
        
        days = self._get_number_input("Analyze how many days? (default: 30): ", 30)
        
        print("⚡ Analyzing performance patterns...")
        insights = self.analyzer.get_performance_insights(days)
        
        # Efficiency metrics
        efficiency = insights.get('efficiency_metrics', {})
        if efficiency:
            print("\n📈 Efficiency Metrics:")
            print(f"  • Median Duration: {efficiency.get('median_duration', 0):.1f}s")
            print(f"  • 90th Percentile: {efficiency.get('p90_duration', 0):.1f}s")
            print(f"  • Fastest Execution: {efficiency.get('fastest_execution', 0):.1f}s")
            print(f"  • Slowest Execution: {efficiency.get('slowest_execution', 0):.1f}s")
        
        # Bottlenecks
        bottlenecks = insights.get('bottlenecks', [])
        if bottlenecks:
            print("\n🚨 Identified Bottlenecks:")
            for bottleneck in bottlenecks:
                print(f"  ⚠️  {bottleneck}")
        else:
            print("\n✅ No major bottlenecks identified!")
        
        # Success patterns
        success_patterns = insights.get('success_patterns', {})
        if success_patterns:
            successful_count = success_patterns.get('successful_count', 0)
            failed_count = success_patterns.get('failed_count', 0)
            total_count = successful_count + failed_count
            
            if total_count > 0:
                print(f"\n✅ Success Patterns:")
                print(f"  • Successful: {successful_count} ({successful_count/total_count:.1%})")
                print(f"  • Failed: {failed_count} ({failed_count/total_count:.1%})")
                
                # Show success keywords
                success_keywords = success_patterns.get('success_keywords', {})
                if success_keywords:
                    top_success = success_keywords.most_common(5)
                    print("  • Success Keywords:", ", ".join([kw for kw, _ in top_success]))
                
                # Show failure keywords
                failure_keywords = success_patterns.get('failure_keywords', {})
                if failure_keywords:
                    top_failure = failure_keywords.most_common(5)
                    print("  • Failure Keywords:", ", ".join([kw for kw, _ in top_failure]))
        
        # Time patterns
        time_patterns = insights.get('time_patterns', {})
        if time_patterns:
            hourly_success = time_patterns.get('hourly_success_rate', {})
            if hourly_success:
                best_hour = max(hourly_success.items(), key=lambda x: x[1])
                worst_hour = min(hourly_success.items(), key=lambda x: x[1])
                
                print(f"\n🕐 Time Patterns:")
                print(f"  • Best Performance Hour: {best_hour[0]}:00 ({best_hour[1]:.1%} success)")
                print(f"  • Worst Performance Hour: {worst_hour[0]}:00 ({worst_hour[1]:.1%} success)")
    
    def _export_data(self):
        """Export data interface"""
        print("\n📤 Export Data")
        print("=" * 50)
        
        print("What would you like to export?")
        print("1. Analytics Report")
        print("2. Search Results") 
        print("3. Raw Log Data")
        
        choice = input("Enter choice (1-3): ").strip()
        
        if choice == '1':
            self._export_analytics()
        elif choice == '2':
            self._export_search_results()
        elif choice == '3':
            self._export_raw_logs()
        else:
            print("❌ Invalid choice.")
    
    def _export_analytics(self):
        """Export analytics report"""
        days = self._get_number_input("How many days to analyze? (default: 30): ", 30)
        format_choice = input("Format (json/markdown/csv): ").strip().lower()
        
        if format_choice not in ['json', 'markdown', 'csv']:
            print("❌ Invalid format.")
            return
        
        filename = f"analytics_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.{format_choice}"
        output_path = self.logs_base_path / "analytics" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        if self.analyzer.export_analytics(str(output_path), format_choice, days):
            print(f"✅ Analytics exported to: {output_path}")
        else:
            print("❌ Export failed.")
    
    def _export_search_results(self):
        """Export search results"""
        query = input("Enter search query: ").strip()
        if not query:
            print("❌ Query is required.")
            return
        
        days = self._get_number_input("Search how many days? (default: 30): ", 30)
        results = self.analyzer.search(query, days=days, limit=1000)
        
        if not results:
            print("No results to export.")
            return
        
        # Export as JSON
        filename = f"search_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        output_path = self.logs_base_path / "analytics" / filename
        output_path.parent.mkdir(exist_ok=True)
        
        try:
            export_data = []
            for result in results:
                export_data.append({
                    'session_id': result.session_id,
                    'timestamp': result.timestamp,
                    'user_query': result.user_query,
                    'keywords': result.keywords,
                    'log_filename': result.log_filename,
                    'relevance_score': result.relevance_score,
                    'matched_terms': result.matched_terms
                })
            
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Search results exported to: {output_path}")
            print(f"📊 Exported {len(results)} results for query '{query}'")
            
        except Exception as e:
            print(f"❌ Export failed: {e}")
    
    def _export_raw_logs(self):
        """Export raw log data"""
        print("Raw log export not yet implemented.")
        print("Use individual log files in the logs/executions/ directory.")
    
    def _show_help(self):
        """Show help information"""
        print("\n❓ Claude Code Log Viewer Help")
        print("=" * 50)
        
        help_text = """
🚀 Welcome to Claude Code Log Viewer!

This interactive tool helps you explore and analyze your Claude Code execution logs.

📋 Main Features:

1. 📅 Recent Executions: View your most recent Claude Code sessions
2. 🔍 Search Logs: Find specific executions by keywords or content
3. 📊 Analytics Summary: Get insights into your usage patterns
4. 🔍 Detailed Inspector: Deep dive into specific execution details
5. 🔗 Similar Sessions: Find executions similar to a reference session
6. ⚡ Performance Insights: Analyze efficiency and identify bottlenecks
7. 📤 Export Data: Export analytics and search results for external analysis

💡 Tips:
- Use descriptive search terms for better results
- Check performance insights regularly to optimize your workflow
- Export analytics to track your productivity over time
- Use similar session search to find reusable patterns

📄 Log File Naming:
Your logs are automatically saved with smart names like:
• 2025-01-23_10-30-45_literature_review_transformers.log
• 2025-01-23_14-15-22_debug_pytorch_model.log

The system extracts keywords from your queries to create meaningful filenames!

🔍 Search Tips:
- Use specific technical terms for better matches
- Try searching for tool names, file types, or domains
- Use quotes for exact phrases: "neural network training"

📊 Analytics Insights:
- Success rate shows how often your executions complete successfully
- Duration metrics help identify slow operations
- Keyword trends show your most common work patterns
- Tool usage helps optimize your workflow

For more help, visit the documentation or check the logs/README.md file.
"""
        print(help_text)
    
    # Utility methods
    
    def _get_number_input(self, prompt: str, default: int) -> int:
        """Get number input with default"""
        try:
            value = input(prompt).strip()
            return int(value) if value else default
        except ValueError:
            return default
    
    def _clear_screen(self):
        """Clear the screen (platform-independent)"""
        os.system('cls' if os.name == 'nt' else 'clear')

def main():
    """Command line interface for log viewer"""
    parser = argparse.ArgumentParser(description="Claude Code Interactive Log Viewer")
    
    parser.add_argument('--logs-path', default='logs', 
                       help='Path to logs directory (default: logs)')
    parser.add_argument('--recent', type=int, metavar='N',
                       help='Show N recent executions and exit')
    parser.add_argument('--search', metavar='QUERY',
                       help='Search logs and exit')
    parser.add_argument('--analytics', action='store_true',
                       help='Show analytics summary and exit')
    parser.add_argument('--days', type=int, default=30,
                       help='Number of days for analytics/search (default: 30)')
    
    args = parser.parse_args()
    
    try:
        viewer = LogViewer(args.logs_path)
        
        if args.recent:
            # Show recent executions and exit
            results = viewer.analyzer.search("", days=7, limit=args.recent)
            
            if results:
                print(f"📅 Last {len(results)} executions:")
                for i, result in enumerate(results, 1):
                    timestamp = datetime.fromisoformat(result.timestamp)
                    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                    print(f"{i:2}. [{formatted_time}] {result.user_query[:60]}")
            else:
                print("No recent executions found.")
        
        elif args.search:
            # Search logs and exit
            results = viewer.analyzer.search(args.search, days=args.days, limit=20)
            
            if results:
                print(f"🔍 Found {len(results)} results for '{args.search}':")
                for i, result in enumerate(results, 1):
                    timestamp = datetime.fromisoformat(result.timestamp)
                    formatted_time = timestamp.strftime("%Y-%m-%d %H:%M")
                    print(f"{i:2}. [{formatted_time}] Score: {result.relevance_score:.2f}")
                    print(f"    {result.user_query[:70]}")
            else:
                print(f"No results found for '{args.search}'.")
        
        elif args.analytics:
            # Show analytics and exit
            analytics = viewer.analyzer.get_analytics(args.days)
            
            print(f"📊 Analytics Summary ({analytics.time_period})")
            print(f"Total Executions: {analytics.total_executions}")
            print(f"Success Rate: {analytics.success_rate:.1%}")
            print(f"Average Duration: {analytics.average_duration:.1f}s")
            
            if analytics.popular_keywords:
                keywords = [kw for kw, _ in analytics.popular_keywords[:5]]
                print(f"Top Keywords: {', '.join(keywords)}")
        
        else:
            # Start interactive mode
            viewer.interactive_mode()
            
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure the logs directory exists and contains execution logs.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()