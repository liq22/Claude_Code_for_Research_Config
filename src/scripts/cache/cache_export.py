#!/usr/bin/env python3
"""
Cache Export Tool

Export cache data in various formats for analysis and backup.

Author: Claude Code Research System
Version: 1.0.0
"""

import json
import csv
import argparse
from datetime import datetime
from pathlib import Path
import sys
from typing import Dict, List

# Add cache system to path
sys.path.append(str(Path(__file__).parent))
from cache import get_simple_cache_system

class CacheExporter:
    """Cache data exporter with multiple format support"""
    
    def __init__(self):
        self.cache = get_simple_cache_system()
    
    def export_to_json(self, output_file: str = None, filter_type: str = "all", 
                      include_content: bool = True) -> str:
        """Export cache to JSON format"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"cache_export_{timestamp}.json"
        
        files = self.cache.list_cache_files(filter_type)
        export_data = {
            'export_info': {
                'timestamp': datetime.now().isoformat(),
                'cache_type': filter_type,
                'total_files': sum(len(file_list) for file_list in files.values()),
                'include_content': include_content
            },
            'cache_data': {}
        }
        
        for file_type, file_list in files.items():
            cache_path = getattr(self.cache, f"{file_type}_path")
            export_data['cache_data'][file_type] = []
            
            for filename in file_list:
                file_path = cache_path / filename
                cache_data = self.cache.read_cache_file(file_path)
                
                if cache_data:
                    export_item = {
                        'filename': filename,
                        'timestamp': cache_data.get('timestamp'),
                        'file_path': str(file_path)
                    }
                    
                    if include_content:
                        export_item['content'] = cache_data.get('content')
                    else:
                        # Only include summary for space efficiency
                        content = cache_data.get('content', {})
                        if isinstance(content, dict):
                            export_item['content_summary'] = {
                                k: str(v)[:100] + "..." if len(str(v)) > 100 else str(v)
                                for k, v in content.items()
                            }
                        else:
                            export_item['content_summary'] = str(content)[:200] + "..."
                    
                    export_data['cache_data'][file_type].append(export_item)
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        return output_file
    
    def export_to_csv(self, output_file: str = None, filter_type: str = "all") -> str:
        """Export cache metadata to CSV format"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"cache_metadata_{timestamp}.csv"
        
        files = self.cache.list_cache_files(filter_type)
        
        # Prepare CSV data
        csv_data = []
        for file_type, file_list in files.items():
            cache_path = getattr(self.cache, f"{file_type}_path")
            
            for filename in file_list:
                file_path = cache_path / filename
                cache_data = self.cache.read_cache_file(file_path)
                
                if cache_data:
                    row = {
                        'filename': filename,
                        'type': file_type,
                        'timestamp': cache_data.get('timestamp'),
                        'file_path': str(file_path),
                        'file_size_bytes': file_path.stat().st_size if file_path.exists() else 0
                    }
                    
                    # Add type-specific fields
                    content = cache_data.get('content', {})
                    if file_type == 'thinking':
                        row['user_query'] = content.get('user_query', '')[:200]
                        row['tools_used'] = ','.join(content.get('tools_used', []))
                    elif file_type == 'agent':
                        row['agent_name'] = content.get('agent_name', '')
                        row['status'] = content.get('status', '')
                    elif file_type == 'research':
                        row['domain'] = content.get('domain', '')
                        row['query'] = content.get('query', '')[:200]
                    
                    csv_data.append(row)
        
        # Write CSV
        if csv_data:
            fieldnames = csv_data[0].keys()
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(csv_data)
        
        return output_file
    
    def export_to_markdown(self, output_file: str = None, filter_type: str = "all") -> str:
        """Export cache to Markdown format for documentation"""
        if not output_file:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            output_file = f"cache_report_{timestamp}.md"
        
        files = self.cache.list_cache_files(filter_type)
        stats = self.cache.get_stats()
        
        # Generate markdown content
        md_content = []
        md_content.append("# Claude Code Cache Report")
        md_content.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        md_content.append("")
        
        # Summary
        md_content.append("## Summary")
        md_content.append(f"- **Base Path:** `{stats['base_path']}`")
        md_content.append(f"- **Total Files:** {stats['total_files']}")
        md_content.append(f"- **Cache Types:** {filter_type}")
        md_content.append("")
        
        # Files by type
        md_content.append("## Files by Type")
        for cache_type, count in stats['counts'].items():
            if filter_type == "all" or filter_type == cache_type:
                md_content.append(f"- **{cache_type.capitalize()}:** {count} files")
        md_content.append("")
        
        # Detailed file listing
        for file_type, file_list in files.items():
            if not file_list:
                continue
                
            md_content.append(f"## {file_type.capitalize()} Files")
            cache_path = getattr(self.cache, f"{file_type}_path")
            
            for filename in file_list:
                file_path = cache_path / filename
                cache_data = self.cache.read_cache_file(file_path)
                
                if cache_data:
                    md_content.append(f"### {filename}")
                    md_content.append(f"- **Timestamp:** {cache_data.get('timestamp')}")
                    md_content.append(f"- **Path:** `{file_path}`")
                    
                    content = cache_data.get('content', {})
                    if isinstance(content, dict):
                        for key, value in content.items():
                            if key in ['user_query', 'agent_name', 'domain', 'query']:
                                md_content.append(f"- **{key.replace('_', ' ').title()}:** {str(value)[:200]}")
                    
                    md_content.append("")
        
        # Write markdown file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(md_content))
        
        return output_file
    
    def backup_cache(self, backup_dir: str = None) -> str:
        """Create a complete backup of the cache system"""
        if not backup_dir:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_dir = f"cache_backup_{timestamp}"
        
        backup_path = Path(backup_dir)
        backup_path.mkdir(exist_ok=True)
        
        # Copy all cache files
        import shutil
        
        for cache_type in ['thinking', 'research', 'agent']:
            cache_path = getattr(self.cache, f"{cache_type}_path")
            if cache_path.exists():
                type_backup_dir = backup_path / cache_type
                type_backup_dir.mkdir(exist_ok=True)
                
                for file_path in cache_path.glob("*.json"):
                    shutil.copy2(file_path, type_backup_dir / file_path.name)
        
        # Create backup metadata
        backup_info = {
            'backup_timestamp': datetime.now().isoformat(),
            'original_cache_path': str(self.cache.base_path),
            'backup_path': str(backup_path),
            'stats': self.cache.get_stats()
        }
        
        with open(backup_path / "backup_info.json", 'w') as f:
            json.dump(backup_info, f, indent=2)
        
        return str(backup_path)
    
    def print_export_summary(self, export_files: List[str]):
        """Print summary of exported files"""
        print("📦 EXPORT SUMMARY")
        print("-" * 50)
        for file_path in export_files:
            file_size = Path(file_path).stat().st_size if Path(file_path).exists() else 0
            print(f"✅ {file_path} ({file_size:,} bytes)")
        print()

def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description="Cache Export Tool")
    parser.add_argument("--format", choices=["json", "csv", "markdown", "all"], 
                       default="json", help="Export format")
    parser.add_argument("--type", choices=["all", "thinking", "research", "agent"], 
                       default="all", help="Cache type to export")
    parser.add_argument("--output", help="Output file/directory name")
    parser.add_argument("--no-content", action="store_true", 
                       help="Exclude content from JSON export (metadata only)")
    parser.add_argument("--backup", action="store_true", 
                       help="Create complete backup instead of export")
    
    args = parser.parse_args()
    
    exporter = CacheExporter()
    exported_files = []
    
    try:
        if args.backup:
            backup_dir = exporter.backup_cache(args.output)
            print(f"🗄️  Complete cache backup created: {backup_dir}")
            return
        
        if args.format == "json" or args.format == "all":
            json_file = exporter.export_to_json(
                args.output if args.format == "json" else None,
                args.type,
                not args.no_content
            )
            exported_files.append(json_file)
            print(f"📄 JSON export: {json_file}")
        
        if args.format == "csv" or args.format == "all":
            csv_file = exporter.export_to_csv(
                args.output if args.format == "csv" else None,
                args.type
            )
            exported_files.append(csv_file)
            print(f"📊 CSV export: {csv_file}")
        
        if args.format == "markdown" or args.format == "all":
            md_file = exporter.export_to_markdown(
                args.output if args.format == "markdown" else None,
                args.type
            )
            exported_files.append(md_file)
            print(f"📝 Markdown report: {md_file}")
        
        if args.format == "all":
            exporter.print_export_summary(exported_files)
            
    except Exception as e:
        print(f"❌ Export failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()