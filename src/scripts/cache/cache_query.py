#!/usr/bin/env python3
"""
Simple Cache Query Tool
Simple searching and viewing of cached content.

Author: Claude Code Research System
Version: 2.0.0 (Simplified)
"""

import json
import argparse
from datetime import datetime
from pathlib import Path
import sys

# Add cache system to path
sys.path.append(str(Path(__file__).parent))
from cache import get_simple_cache_system

def search_cache(query: str, cache_type: str = "all", limit: int = 10):
    """Search cache content"""
    cache = get_simple_cache_system()
    results = cache.search_content(query, cache_type)
    
    print(f"\n🔍 Search Results for '{query}' ({len(results)} found)")
    print("=" * 60)
    
    for i, result in enumerate(results[:limit]):
        print(f"\n{i+1}. [{result['type'].upper()}] {result['timestamp']}")
        print(f"   File: {Path(result['file']).name}")
        print(f"   Preview: {result['preview']}")
        print("-" * 60)
    
    if len(results) > limit:
        print(f"\n... and {len(results) - limit} more results")

def list_files(cache_type: str = "all"):
    """List cache files"""
    cache = get_simple_cache_system()
    files = cache.list_cache_files(cache_type)
    
    print(f"\n📁 Cache Files ({cache_type})")
    print("=" * 60)
    
    for file_type, file_list in files.items():
        if file_list:
            print(f"\n{file_type.upper()} ({len(file_list)} files):")
            for filename in file_list[-10:]:  # Show last 10
                print(f"  • {filename}")
            if len(file_list) > 10:
                print(f"  ... and {len(file_list) - 10} more")

def show_stats():
    """Show cache statistics"""
    cache = get_simple_cache_system()
    stats = cache.get_stats()
    
    print(f"\n📊 Cache Statistics")
    print("=" * 60)
    print(f"Base Path: {stats['base_path']}")
    print(f"Last Updated: {stats['timestamp']}")
    print(f"Total Files: {stats['total_files']}")
    print("\nBy Type:")
    for cache_type, count in stats['counts'].items():
        print(f"  • {cache_type.capitalize()}: {count} files")

def view_file(filename: str):
    """View specific cache file"""
    cache = get_simple_cache_system()
    
    # Try to find the file in any cache directory
    for cache_type in ["thinking", "research", "agent"]:
        cache_path = getattr(cache, f"{cache_type}_path")
        file_path = cache_path / filename
        
        if file_path.exists():
            cache_data = cache.read_cache_file(file_path)
            if cache_data:
                print(f"\n📄 Cache File: {filename}")
                print("=" * 60)
                print(f"Timestamp: {cache_data.get('timestamp')}")
                print(f"Type: {cache_type}")
                print("\nContent:")
                print(json.dumps(cache_data.get('content', {}), indent=2, ensure_ascii=False))
                return
    
    print(f"❌ File not found: {filename}")

def cleanup_old_files(days: int = 30):
    """Clean up old cache files"""
    cache = get_simple_cache_system()
    deleted = cache.cleanup_old_files(days)
    
    print(f"\n🧹 Cleanup Results (older than {days} days)")
    print("=" * 60)
    total_deleted = sum(deleted.values())
    
    if total_deleted > 0:
        for cache_type, count in deleted.items():
            if count > 0:
                print(f"  • {cache_type.capitalize()}: {count} files deleted")
        print(f"\nTotal: {total_deleted} files cleaned up")
    else:
        print("No old files found to clean up")

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Simple Cache Query Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Search command
    search_parser = subparsers.add_parser("search", help="Search cache content")
    search_parser.add_argument("query", help="Search query")
    search_parser.add_argument("--type", choices=["all", "thinking", "research", "agent"], 
                              default="all", help="Cache type to search")
    search_parser.add_argument("--limit", type=int, default=10, help="Maximum results")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List cache files")
    list_parser.add_argument("--type", choices=["all", "thinking", "research", "agent"],
                            default="all", help="Cache type to list")
    
    # Stats command
    subparsers.add_parser("stats", help="Show cache statistics")
    
    # View command
    view_parser = subparsers.add_parser("view", help="View specific cache file")
    view_parser.add_argument("filename", help="Filename to view")
    
    # Cleanup command
    cleanup_parser = subparsers.add_parser("cleanup", help="Clean up old cache files")
    cleanup_parser.add_argument("--days", type=int, default=30, 
                               help="Delete files older than N days (default: 30)")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    try:
        if args.command == "search":
            search_cache(args.query, args.type, args.limit)
        elif args.command == "list":
            list_files(args.type)
        elif args.command == "stats":
            show_stats()
        elif args.command == "view":
            view_file(args.filename)
        elif args.command == "cleanup":
            cleanup_old_files(args.days)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()