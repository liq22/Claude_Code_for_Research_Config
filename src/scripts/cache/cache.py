#!/usr/bin/env python3
"""
Simple Cache System for Claude Code Research Configuration

Simplified caching system that only stores timestamp and content.
No complex metadata, analysis, or database operations.

Author: Claude Code Research System
Version: 2.0.0 (Simplified)
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SimpleCacheSystem:
    """Simple cache management system with only timestamp and content"""
    
    def __init__(self, base_path: str = "src/dev/cache"):
        self.base_path = Path(base_path)
        self.thinking_path = self.base_path / "claude_thinking"
        self.research_path = self.base_path / "research_sessions"
        self.agent_path = self.base_path / "agent_execution"
        
        # Ensure directories exist
        self._ensure_directories()
        
        logger.info("Simple cache system initialized")

    def _ensure_directories(self):
        """Ensure all cache directories exist"""
        for path in [self.thinking_path, self.research_path, self.agent_path]:
            path.mkdir(parents=True, exist_ok=True)

    def _get_timestamp(self) -> str:
        """Get formatted timestamp"""
        return datetime.now().isoformat()

    def _get_filename(self, timestamp: str, cache_type: str) -> str:
        """Generate simple filename from timestamp"""
        # Convert ISO timestamp to filename-safe format
        safe_timestamp = timestamp[:19].replace(':', '-')
        return f"{safe_timestamp}_{cache_type}.json"

    def _save_cache_file(self, cache_data: Dict[str, Any], file_path: Path) -> bool:
        """Save cache data to file with improved formatting"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(
                    cache_data, 
                    f, 
                    ensure_ascii=False,  # Keep Unicode characters readable
                    indent=2,
                    separators=(',', ': '),  # Clean formatting
                    sort_keys=False  # Preserve key order
                )
            return True
        except Exception as e:
            logger.error(f"Failed to save cache file {file_path}: {e}")
            return False

    def cache_thinking(self, content: Any) -> Optional[str]:
        """Cache Claude thinking process"""
        timestamp = self._get_timestamp()
        cache_data = {
            "timestamp": timestamp,
            "content": content
        }
        
        filename = self._get_filename(timestamp, "thinking")
        file_path = self.thinking_path / filename
        
        if self._save_cache_file(cache_data, file_path):
            logger.info(f"Cached thinking: {filename}")
            return str(file_path)
        return None

    def cache_research(self, content: Any) -> Optional[str]:
        """Cache research session"""
        timestamp = self._get_timestamp()
        cache_data = {
            "timestamp": timestamp,
            "content": content
        }
        
        filename = self._get_filename(timestamp, "research")
        file_path = self.research_path / filename
        
        if self._save_cache_file(cache_data, file_path):
            logger.info(f"Cached research: {filename}")
            return str(file_path)
        return None

    def cache_agent(self, content: Any) -> Optional[str]:
        """Cache agent execution"""
        timestamp = self._get_timestamp()
        cache_data = {
            "timestamp": timestamp,
            "content": content
        }
        
        filename = self._get_filename(timestamp, "agent")
        file_path = self.agent_path / filename
        
        if self._save_cache_file(cache_data, file_path):
            logger.info(f"Cached agent execution: {filename}")
            return str(file_path)
        return None
    
    def cache_conversation(self, session_id: str, prompt: str, response: str, 
                          tools_used: list = None, metadata: dict = None) -> Optional[str]:
        """Cache complete conversation with prompt and response"""
        timestamp = self._get_timestamp()
        cache_data = {
            "timestamp": timestamp,
            "content": {
                "type": "conversation",
                "session_id": session_id,
                "user_prompt": prompt,
                "claude_response": response,
                "tools_used": tools_used or [],
                "metadata": metadata or {},
                "conversation_length": len(prompt) + len(response)
            }
        }
        
        filename = self._get_filename(timestamp, "conversation")
        file_path = self.thinking_path / filename  # Store in thinking for now
        
        if self._save_cache_file(cache_data, file_path):
            logger.info(f"Cached conversation: {filename}")
            return str(file_path)
        return None
    
    def cache_tool_execution(self, tool_name: str, tool_input: dict, tool_output: dict,
                           session_id: str = None, metadata: dict = None) -> Optional[str]:
        """Cache tool execution details"""
        timestamp = self._get_timestamp()
        cache_data = {
            "timestamp": timestamp,
            "content": {
                "type": "tool_execution",
                "tool_name": tool_name,
                "session_id": session_id,
                "input_parameters": tool_input,
                "output_data": tool_output,
                "execution_time": timestamp,
                "metadata": metadata or {}
            }
        }
        
        filename = self._get_filename(timestamp, "tool")
        file_path = self.agent_path / filename  # Store tools in agent path
        
        if self._save_cache_file(cache_data, file_path):
            logger.info(f"Cached tool execution: {tool_name} -> {filename}")
            return str(file_path)
        return None
    
    def find_by_session_id(self, session_id: str) -> List[dict]:
        """Find all cache entries for a specific session"""
        results = []
        files = self.list_cache_files()
        
        for file_type, file_list in files.items():
            cache_path = getattr(self, f"{file_type}_path")
            
            for filename in file_list:
                file_path = cache_path / filename
                cache_data = self.read_cache_file(file_path)
                
                if cache_data and 'content' in cache_data:
                    content = cache_data['content']
                    # Check if session_id matches
                    if isinstance(content, dict) and content.get('session_id') == session_id:
                        results.append({
                            'file_path': str(file_path),
                            'file_type': file_type,
                            'timestamp': cache_data.get('timestamp'),
                            'content': content
                        })
        
        # Sort by timestamp
        results.sort(key=lambda x: x['timestamp'])
        return results
    
    def get_conversation_thread(self, session_id: str) -> dict:
        """Get complete conversation thread for a session"""
        session_data = self.find_by_session_id(session_id)
        
        thread = {
            'session_id': session_id,
            'messages': [],
            'tools_used': [],
            'metadata': {
                'total_interactions': len(session_data),
                'start_time': None,
                'end_time': None
            }
        }
        
        for entry in session_data:
            content = entry['content']
            entry_type = content.get('type', 'unknown')
            
            if entry_type == 'user_prompt':
                thread['messages'].append({
                    'role': 'user',
                    'content': content.get('prompt', ''),
                    'timestamp': entry['timestamp']
                })
            elif entry_type in ['conversation', 'thinking']:
                if 'claude_response' in content:
                    thread['messages'].append({
                        'role': 'assistant', 
                        'content': content.get('claude_response', ''),
                        'timestamp': entry['timestamp']
                    })
                elif 'thinking_content' in content:
                    thread['messages'].append({
                        'role': 'assistant',
                        'content': content.get('thinking_content', ''),
                        'timestamp': entry['timestamp'],
                        'type': 'thinking'
                    })
            elif entry_type == 'tool_execution':
                thread['tools_used'].append({
                    'tool_name': content.get('tool_name', ''),
                    'timestamp': entry['timestamp'],
                    'input': content.get('input_parameters', {}),
                    'output': content.get('output_data', {})
                })
            
            # Update metadata
            if not thread['metadata']['start_time'] or entry['timestamp'] < thread['metadata']['start_time']:
                thread['metadata']['start_time'] = entry['timestamp']
            if not thread['metadata']['end_time'] or entry['timestamp'] > thread['metadata']['end_time']:
                thread['metadata']['end_time'] = entry['timestamp']
        
        return thread

    def read_cache_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        """Read cache file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to read cache file {file_path}: {e}")
            return None

    def list_cache_files(self, cache_type: str = "all") -> Dict[str, list]:
        """List cache files by type"""
        files = {}
        
        if cache_type in ["all", "thinking"]:
            files["thinking"] = sorted([f.name for f in self.thinking_path.glob("*.json")])
        
        if cache_type in ["all", "research"]:
            files["research"] = sorted([f.name for f in self.research_path.glob("*.json")])
        
        if cache_type in ["all", "agent"]:
            files["agent"] = sorted([f.name for f in self.agent_path.glob("*.json")])
        
        return files

    def search_content(self, query: str, cache_type: str = "all") -> list:
        """Simple text search in cache content"""
        results = []
        cache_files = self.list_cache_files(cache_type)
        
        for file_type, file_list in cache_files.items():
            cache_path = getattr(self, f"{file_type}_path")
            
            for filename in file_list:
                file_path = cache_path / filename
                cache_data = self.read_cache_file(file_path)
                
                if cache_data and query.lower() in str(cache_data.get("content", "")).lower():
                    results.append({
                        "file": str(file_path),
                        "timestamp": cache_data.get("timestamp"),
                        "type": file_type,
                        "preview": str(cache_data.get("content", ""))[:200] + "..."
                    })
        
        return sorted(results, key=lambda x: x["timestamp"], reverse=True)

    def get_stats(self) -> Dict[str, Any]:
        """Get simple cache statistics"""
        files = self.list_cache_files()
        
        stats = {
            "timestamp": self._get_timestamp(),
            "base_path": str(self.base_path),
            "counts": {
                "thinking": len(files.get("thinking", [])),
                "research": len(files.get("research", [])),
                "agent": len(files.get("agent", []))
            },
            "total_files": sum(len(file_list) for file_list in files.values())
        }
        
        return stats

    def cleanup_old_files(self, days: int = 30) -> Dict[str, int]:
        """Remove files older than specified days"""
        from datetime import timedelta
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_counts = {"thinking": 0, "research": 0, "agent": 0}
        
        for cache_type in ["thinking", "research", "agent"]:
            cache_path = getattr(self, f"{cache_type}_path")
            
            for file_path in cache_path.glob("*.json"):
                cache_data = self.read_cache_file(file_path)
                if cache_data:
                    file_timestamp = datetime.fromisoformat(cache_data["timestamp"])
                    if file_timestamp < cutoff_date:
                        try:
                            file_path.unlink()
                            deleted_counts[cache_type] += 1
                            logger.info(f"Deleted old cache file: {file_path.name}")
                        except Exception as e:
                            logger.error(f"Failed to delete {file_path}: {e}")
        
        return deleted_counts

# Global cache system instance
_cache_system = None

def get_simple_cache_system(base_path: str = "src/dev/cache") -> SimpleCacheSystem:
    """Get global simple cache system instance"""
    global _cache_system
    if _cache_system is None:
        _cache_system = SimpleCacheSystem(base_path)
    return _cache_system

if __name__ == "__main__":
    # Simple test
    cache = get_simple_cache_system()
    
    # Test caching
    cache.cache_thinking({"query": "test query", "content": "test thinking"})
    cache.cache_research({"domain": "AI", "findings": "test findings"})
    cache.cache_agent({"agent": "test-agent", "result": "test result"})
    
    # Show stats
    print("Cache stats:", json.dumps(cache.get_stats(), indent=2))
    
    # Test search
    results = cache.search_content("test")
    print(f"Search results: {len(results)} found")