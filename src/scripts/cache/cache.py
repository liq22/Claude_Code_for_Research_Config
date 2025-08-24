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
from typing import Dict, Any, Optional
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
        """Save cache data to file"""
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(cache_data, f, ensure_ascii=False, indent=2)
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