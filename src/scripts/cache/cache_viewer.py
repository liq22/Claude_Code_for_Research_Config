#!/usr/bin/env python3
"""
Cache Viewer - Human-Friendly Cache Browser

Provides easy-to-read access to cached conversations and data.
Supports both JSON cache and Markdown conversation logs.

Author: Claude Code Research System  
Version: 1.0.0
"""

import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
import sys
from collections import defaultdict
from typing import Dict, List, Tuple, Any

# Add cache system to path
sys.path.append(str(Path(__file__).parent))
from cache import get_simple_cache_system
from conversation_logger import get_conversation_logger

class CacheViewer:
    """Human-friendly cache viewer and browser"""
    
    def __init__(self):
        self.cache = get_simple_cache_system()
        self.logger = get_conversation_logger()
        
    def show_recent_conversations(self, days: int = 7, format: str = "summary"):
        """Show recent conversations in human-readable format"""
        print(f"📅 Recent Conversations (Last {days} days)")
        print("=" * 60)
        
        # Get recent conversation files
        recent_files = self.logger.get_recent_conversations(days)
        
        if not recent_files:
            print(f"No conversations found in the last {days} days")
            return
        
        for file_info in recent_files:
            file_path = file_info['path']
            days_ago = file_info['days_ago']
            size_kb = file_info['size'] / 1024
            
            date_str = file_info['date'].strftime('%Y-%m-%d (%A)')
            
            if days_ago == 0:
                age_str = "Today"
            elif days_ago == 1:
                age_str = "Yesterday"
            else:
                age_str = f"{days_ago} days ago"
            
            print(f"\n📝 **{date_str}** - {age_str}")
            print(f"   Size: {size_kb:.1f} KB | File: {file_path.name}")
            
            if format == "preview":
                self._show_conversation_preview(file_path)
            elif format == "full":
                self._show_conversation_full(file_path)
    
    def _show_conversation_preview(self, file_path: Path, max_lines: int = 10):
        """Show preview of conversation file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Find conversation entries (lines starting with ##)
            conversation_lines = [line for line in lines if line.strip().startswith('##')]
            
            if conversation_lines:
                print("   Preview:")
                for line in conversation_lines[:max_lines]:
                    clean_line = line.strip().replace('##', '  →')
                    print(f"     {clean_line}")
                
                if len(conversation_lines) > max_lines:
                    print(f"     ... and {len(conversation_lines) - max_lines} more entries")
                    
        except Exception as e:
            print(f"   Error reading file: {e}")
    
    def _show_conversation_full(self, file_path: Path):
        """Show full conversation file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print("\n" + "─" * 60)
            print(content)
            print("─" * 60)
                    
        except Exception as e:
            print(f"   Error reading file: {e}")
    
    def search_conversations(self, query: str, days: int = 30, context_lines: int = 2):
        """Search through conversation files"""
        print(f"🔍 Searching for '{query}' in conversations (last {days} days)")
        print("=" * 60)
        
        recent_files = self.logger.get_recent_conversations(days)
        results = []
        
        for file_info in recent_files:
            file_path = file_info['path']
            
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                
                # Search for query in lines
                for i, line in enumerate(lines):
                    if query.lower() in line.lower():
                        # Get context around the match
                        start = max(0, i - context_lines)
                        end = min(len(lines), i + context_lines + 1)
                        context = lines[start:end]
                        
                        results.append({
                            'file': file_path,
                            'line_number': i + 1,
                            'match_line': line.strip(),
                            'context': context,
                            'date': file_info['date']
                        })
                        
            except Exception as e:
                print(f"Error searching {file_path}: {e}")
        
        if not results:
            print("No matches found")
            return
        
        print(f"Found {len(results)} matches:\n")
        
        for i, result in enumerate(results[:10]):  # Show first 10 results
            date_str = result['date'].strftime('%Y-%m-%d')
            print(f"{i+1}. **{result['file'].name}** (Line {result['line_number']}) - {date_str}")
            print(f"   Match: {result['match_line']}")
            
            # Show context
            print("   Context:")
            for ctx_line in result['context']:
                marker = ">>> " if query.lower() in ctx_line.lower() else "    "
                print(f"   {marker}{ctx_line.rstrip()}")
            print()
        
        if len(results) > 10:
            print(f"... and {len(results) - 10} more matches")
    
    def show_cache_summary(self):
        """Show summary of both JSON cache and conversation logs"""
        print("📊 Cache System Summary")
        print("=" * 60)
        
        # JSON Cache stats
        cache_stats = self.cache.get_stats()
        print(f"\n🗃️  JSON Cache:")
        print(f"   Path: {cache_stats['base_path']}")
        print(f"   Total Files: {cache_stats['total_files']}")
        print(f"   File Types:")
        for cache_type, count in cache_stats['counts'].items():
            print(f"     • {cache_type.capitalize()}: {count} files")
        
        # Conversation logs stats  
        logger_stats = self.logger.get_stats()
        print(f"\n📝 Conversation Logs:")
        print(f"   Path: {logger_stats['conversations_path']}")
        print(f"   Total Files: {logger_stats['total_conversation_files']}")
        print(f"   Total Size: {logger_stats['total_size_mb']} MB")
        print(f"   Recent (7 days): {logger_stats['recent_files_7days']} files")
        
        # Recent activity
        recent_files = self.logger.get_recent_conversations(7)
        if recent_files:
            print(f"\n🕐 Recent Activity:")
            for file_info in recent_files[:3]:
                age = file_info['days_ago']
                age_str = "Today" if age == 0 else f"{age} days ago"
                print(f"   • {file_info['path'].name} - {age_str}")
    
    def show_session_thread(self, session_id: str):
        """Show complete conversation thread for a session"""
        print(f"🧵 Session Thread: {session_id}")
        print("=" * 60)
        
        thread = self.cache.get_conversation_thread(session_id)
        
        if not thread['messages']:
            print("No messages found for this session")
            return
        
        print(f"Session Overview:")
        metadata = thread['metadata']
        print(f"   • Total Interactions: {metadata['total_interactions']}")
        print(f"   • Start Time: {metadata.get('start_time', 'Unknown')}")
        print(f"   • End Time: {metadata.get('end_time', 'Unknown')}")
        print(f"   • Tools Used: {len(thread['tools_used'])}")
        
        print(f"\nConversation:")
        print("-" * 40)
        
        for i, message in enumerate(thread['messages']):
            role = message['role']
            content = message['content']
            timestamp = message.get('timestamp', '')
            
            if timestamp:
                time_str = datetime.fromisoformat(timestamp).strftime('%H:%M:%S')
            else:
                time_str = f"#{i+1}"
            
            role_icon = "👤" if role == "user" else "🤖"
            print(f"\n{time_str} - {role_icon} {role.title()}:")
            
            # Format content nicely
            if len(content) > 200:
                lines = content.split('\n')
                for line in lines[:5]:
                    print(f"   {line}")
                if len(lines) > 5:
                    print(f"   ... ({len(lines) - 5} more lines)")
            else:
                for line in content.split('\n'):
                    print(f"   {line}")
        
        # Show tools used
        if thread['tools_used']:
            print(f"\nTools Used:")
            print("-" * 40)
            for tool in thread['tools_used']:
                tool_time = datetime.fromisoformat(tool['timestamp']).strftime('%H:%M:%S')
                print(f"{tool_time} - 🔧 {tool['tool_name']}")
    
    def export_conversation(self, date: str, output_file: str = None):
        """Export a specific day's conversation to file"""
        try:
            date_obj = datetime.strptime(date, '%Y-%m-%d')
            conv_file = self.logger.conversations_path / f"{date}.md"
            
            if not conv_file.exists():
                print(f"No conversation found for {date}")
                return
            
            if not output_file:
                output_file = f"conversation_{date}_export.md"
            
            # Copy with some processing
            with open(conv_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Add export header
            export_content = f"""# 📤 Exported Conversation - {date}

> Exported from Claude Code Cache System on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
> Original file: {conv_file}

---

{content}

---

*End of exported conversation*
"""
            
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(export_content)
            
            print(f"✅ Conversation exported to: {output_file}")
            
        except Exception as e:
            print(f"❌ Export failed: {e}")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Human-friendly cache viewer")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Recent conversations
    recent_parser = subparsers.add_parser("recent", help="Show recent conversations")
    recent_parser.add_argument("--days", type=int, default=7, help="Number of days to look back")
    recent_parser.add_argument("--format", choices=["summary", "preview", "full"], 
                              default="summary", help="Display format")
    
    # Search conversations
    search_parser = subparsers.add_parser("search", help="Search conversations")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--days", type=int, default=30, help="Days to search back")
    search_parser.add_argument("--context", type=int, default=2, help="Context lines around matches")
    
    # Summary
    subparsers.add_parser("summary", help="Show cache system summary")
    
    # Session thread
    session_parser = subparsers.add_parser("session", help="Show session conversation thread")
    session_parser.add_argument("session_id", help="Session ID to display")
    
    # Export conversation
    export_parser = subparsers.add_parser("export", help="Export conversation for a specific date")
    export_parser.add_argument("date", help="Date in YYYY-MM-DD format")
    export_parser.add_argument("--output", help="Output filename")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    viewer = CacheViewer()
    
    try:
        if args.command == "recent":
            viewer.show_recent_conversations(args.days, args.format)
        elif args.command == "search":
            viewer.search_conversations(args.query, args.days, args.context)
        elif args.command == "summary":
            viewer.show_cache_summary()
        elif args.command == "session":
            viewer.show_session_thread(args.session_id)
        elif args.command == "export":
            viewer.export_conversation(args.date, args.output)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()