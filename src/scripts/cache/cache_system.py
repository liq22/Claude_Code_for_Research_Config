#!/usr/bin/env python3
"""
Intelligent Cache Management System for Claude Code Research Configuration

This system manages three layers of caching:
1. Claude thinking processes 
2. Research session data
3. Agent execution logs

Author: Claude Code Research System
Version: 1.0.0
"""

import json
import hashlib
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import logging
import gzip
import pickle
import sqlite3
from dataclasses import dataclass, asdict
import threading
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class CacheMetadata:
    """Metadata structure for cache entries"""
    timestamp: str
    cache_type: str  # 'thinking', 'research', 'agent'
    cache_id: str
    session_id: str
    query_hash: Optional[str] = None
    size_bytes: int = 0
    access_count: int = 0
    last_accessed: Optional[str] = None
    retention_days: int = 30
    quality_score: float = 0.0
    tags: List[str] = None

    def __post_init__(self):
        if self.tags is None:
            self.tags = []

class CacheSystem:
    """Main cache management system"""
    
    def __init__(self, base_path: str = "dev/cache"):
        self.base_path = Path(base_path)
        self.thinking_path = self.base_path / "claude_thinking"
        self.research_path = self.base_path / "research_sessions"  
        self.agent_path = self.base_path / "agent_execution"
        self.db_path = self.base_path / "cache_metadata.db"
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Initialize metadata database
        self._init_database()
        
        # Cache configuration
        self.config = {
            'claude_thinking': {'retention_days': 30, 'max_size_gb': 3},
            'research_sessions': {'retention_days': 90, 'max_size_gb': 4},
            'agent_execution': {'retention_days': 60, 'max_size_gb': 3},
            'compression': True,
            'auto_cleanup': True
        }
        
        # Thread lock for concurrent operations
        self._lock = threading.Lock()
        
        logger.info("Cache system initialized successfully")

    def _ensure_directories(self):
        """Ensure all cache directories exist"""
        for path in [self.thinking_path, self.research_path, self.agent_path]:
            path.mkdir(parents=True, exist_ok=True)

    def _init_database(self):
        """Initialize SQLite database for metadata"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS cache_metadata (
                    cache_id TEXT PRIMARY KEY,
                    timestamp TEXT,
                    cache_type TEXT,
                    session_id TEXT,
                    query_hash TEXT,
                    size_bytes INTEGER,
                    access_count INTEGER,
                    last_accessed TEXT,
                    retention_days INTEGER,
                    quality_score REAL,
                    tags TEXT,
                    file_path TEXT
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON cache_metadata(timestamp)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_cache_type ON cache_metadata(cache_type)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_query_hash ON cache_metadata(query_hash)')

    def _generate_cache_id(self) -> str:
        """Generate unique cache ID"""
        return str(uuid.uuid4())

    def _generate_query_hash(self, query: str) -> str:
        """Generate hash for query string"""
        return hashlib.md5(query.encode('utf-8')).hexdigest()[:12]

    def _get_timestamp(self) -> str:
        """Get formatted timestamp"""
        return datetime.now().isoformat()

    def _compress_data(self, data: Any) -> bytes:
        """Compress data using gzip"""
        json_str = json.dumps(data, ensure_ascii=False, indent=2)
        return gzip.compress(json_str.encode('utf-8'))

    def _decompress_data(self, compressed_data: bytes) -> Any:
        """Decompress data"""
        json_str = gzip.decompress(compressed_data).decode('utf-8')
        return json.loads(json_str)

    def cache_claude_thinking(self, 
                            user_query: str,
                            thinking_content: str,
                            execution_context: Dict,
                            outcome_metrics: Dict,
                            session_id: Optional[str] = None) -> str:
        """Cache Claude thinking process"""
        
        cache_id = self._generate_cache_id()
        query_hash = self._generate_query_hash(user_query)
        timestamp = self._get_timestamp()
        session_id = session_id or str(uuid.uuid4())
        
        # Structure the thinking data
        cache_data = {
            'metadata': {
                'timestamp': timestamp,
                'query_hash': query_hash,
                'session_id': session_id,
                'user_query': user_query,
                'complexity_score': len(thinking_content) / 1000,  # Simple complexity metric
                'thinking_duration': execution_context.get('duration', 0)
            },
            'thinking_content': {
                'raw_thinking': thinking_content,
                'key_insights': self._extract_insights(thinking_content),
                'decision_points': self._extract_decisions(thinking_content),
                'alternative_approaches': self._extract_alternatives(thinking_content)
            },
            'execution_context': execution_context,
            'outcome_metrics': outcome_metrics
        }
        
        # Save to file
        filename = f"{timestamp[:19].replace(':', '-')}_{query_hash}_{cache_id[:8]}.json.gz"
        file_path = self.thinking_path / filename
        
        with self._lock:
            try:
                if self.config['compression']:
                    with open(file_path, 'wb') as f:
                        f.write(self._compress_data(cache_data))
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
                # Update metadata database
                size_bytes = file_path.stat().st_size
                self._update_metadata(cache_id, 'claude_thinking', timestamp, session_id, 
                                    query_hash, size_bytes, str(file_path))
                
                logger.info(f"Cached Claude thinking: {cache_id}")
                return cache_id
                
            except Exception as e:
                logger.error(f"Failed to cache thinking: {e}")
                return None

    def cache_research_session(self,
                             session_data: Dict,
                             session_id: Optional[str] = None) -> str:
        """Cache research session data"""
        
        cache_id = self._generate_cache_id()
        timestamp = self._get_timestamp()
        session_id = session_id or str(uuid.uuid4())
        
        # Enhance session data with metadata
        cache_data = {
            'session_metadata': {
                'session_id': session_id,
                'start_time': session_data.get('start_time', timestamp),
                'end_time': timestamp,
                'research_domain': session_data.get('domain', 'unknown'),
                'primary_query': session_data.get('query', '')
            },
            'literature_discoveries': session_data.get('discoveries', []),
            'search_strategies': session_data.get('strategies', {}),
            'knowledge_synthesis': session_data.get('synthesis', {})
        }
        
        # Save to file
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"research_session_{date_str}_{session_id[:8]}_{cache_id[:8]}.json.gz"
        file_path = self.research_path / filename
        
        with self._lock:
            try:
                if self.config['compression']:
                    with open(file_path, 'wb') as f:
                        f.write(self._compress_data(cache_data))
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
                # Calculate quality score based on discoveries
                quality_score = min(1.0, len(cache_data['literature_discoveries']) / 10)
                
                size_bytes = file_path.stat().st_size
                self._update_metadata(cache_id, 'research_sessions', timestamp, session_id,
                                    None, size_bytes, str(file_path), quality_score)
                
                logger.info(f"Cached research session: {cache_id}")
                return cache_id
                
            except Exception as e:
                logger.error(f"Failed to cache research session: {e}")
                return None

    def cache_agent_execution(self,
                            agent_name: str,
                            execution_data: Dict,
                            session_id: Optional[str] = None) -> str:
        """Cache agent execution data"""
        
        cache_id = self._generate_cache_id()
        timestamp = self._get_timestamp()
        session_id = session_id or str(uuid.uuid4())
        
        # Structure execution data
        cache_data = {
            'execution_metadata': {
                'agent_name': agent_name,
                'execution_id': cache_id,
                'triggered_by': execution_data.get('triggered_by', 'user_request'),
                'start_time': execution_data.get('start_time', timestamp),
                'completion_time': timestamp,
                'duration_seconds': execution_data.get('duration', 0)
            },
            'input_context': execution_data.get('input_context', {}),
            'execution_trace': execution_data.get('execution_trace', []),
            'performance_metrics': execution_data.get('performance_metrics', {}),
            'output_results': execution_data.get('output_results', {})
        }
        
        # Save to file
        date_str = datetime.now().strftime("%Y-%m-%d")
        filename = f"agent_{agent_name}_{date_str}_{cache_id[:8]}.json.gz"
        file_path = self.agent_path / filename
        
        with self._lock:
            try:
                if self.config['compression']:
                    with open(file_path, 'wb') as f:
                        f.write(self._compress_data(cache_data))
                else:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        json.dump(cache_data, f, ensure_ascii=False, indent=2)
                
                # Calculate quality score based on success metrics
                metrics = cache_data['performance_metrics']
                quality_score = metrics.get('success_rate', 0.0) * metrics.get('quality_score', 0.5)
                
                size_bytes = file_path.stat().st_size
                tags = [agent_name, execution_data.get('triggered_by', 'unknown')]
                self._update_metadata(cache_id, 'agent_execution', timestamp, session_id,
                                    None, size_bytes, str(file_path), quality_score, tags)
                
                logger.info(f"Cached agent execution: {agent_name} -> {cache_id}")
                return cache_id
                
            except Exception as e:
                logger.error(f"Failed to cache agent execution: {e}")
                return None

    def _update_metadata(self, cache_id: str, cache_type: str, timestamp: str, 
                        session_id: str, query_hash: Optional[str], size_bytes: int,
                        file_path: str, quality_score: float = 0.0, tags: List[str] = None):
        """Update metadata in database"""
        
        tags_str = json.dumps(tags) if tags else json.dumps([])
        retention_days = self.config[cache_type]['retention_days']
        
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''
                INSERT OR REPLACE INTO cache_metadata 
                (cache_id, timestamp, cache_type, session_id, query_hash, size_bytes,
                 access_count, last_accessed, retention_days, quality_score, tags, file_path)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (cache_id, timestamp, cache_type, session_id, query_hash, size_bytes,
                  0, None, retention_days, quality_score, tags_str, file_path))

    def get_cache_stats(self) -> Dict:
        """Get cache statistics"""
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            stats = {}
            for cache_type in ['claude_thinking', 'research_sessions', 'agent_execution']:
                cursor.execute('''
                    SELECT COUNT(*), SUM(size_bytes), AVG(quality_score), MAX(timestamp)
                    FROM cache_metadata WHERE cache_type = ?
                ''', (cache_type,))
                
                count, total_size, avg_quality, latest = cursor.fetchone()
                stats[cache_type] = {
                    'count': count or 0,
                    'total_size_mb': (total_size or 0) / (1024 * 1024),
                    'avg_quality': round(avg_quality or 0, 3),
                    'latest_entry': latest
                }
            
            return stats

    def cleanup_expired_caches(self) -> Dict:
        """Clean up expired cache entries"""
        
        cleanup_stats = {'deleted_files': 0, 'freed_space': 0, 'errors': []}
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Find expired entries
            for cache_type in ['claude_thinking', 'research_sessions', 'agent_execution']:
                retention_days = self.config[cache_type]['retention_days']
                cutoff_date = (datetime.now() - timedelta(days=retention_days)).isoformat()
                
                cursor.execute('''
                    SELECT cache_id, file_path, size_bytes 
                    FROM cache_metadata 
                    WHERE cache_type = ? AND timestamp < ?
                ''', (cache_type, cutoff_date))
                
                expired_entries = cursor.fetchall()
                
                for cache_id, file_path, size_bytes in expired_entries:
                    try:
                        file_path_obj = Path(file_path)
                        if file_path_obj.exists():
                            file_path_obj.unlink()
                            cleanup_stats['freed_space'] += size_bytes
                            cleanup_stats['deleted_files'] += 1
                        
                        # Remove from database
                        cursor.execute('DELETE FROM cache_metadata WHERE cache_id = ?', (cache_id,))
                        
                    except Exception as e:
                        error_msg = f"Failed to delete {file_path}: {e}"
                        cleanup_stats['errors'].append(error_msg)
                        logger.error(error_msg)
            
            conn.commit()
        
        cleanup_stats['freed_space_mb'] = cleanup_stats['freed_space'] / (1024 * 1024)
        logger.info(f"Cleanup completed: {cleanup_stats}")
        return cleanup_stats

    def _extract_insights(self, thinking_content: str) -> List[str]:
        """Extract key insights from thinking content"""
        # Simple keyword-based extraction (can be enhanced with NLP)
        insight_keywords = ['insight:', 'key point:', 'important:', 'realize:', 'understand:']
        insights = []
        
        lines = thinking_content.split('\n')
        for line in lines:
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in insight_keywords):
                insights.append(line.strip())
                
        return insights[:5]  # Top 5 insights

    def _extract_decisions(self, thinking_content: str) -> List[str]:
        """Extract decision points from thinking content"""
        decision_keywords = ['decide:', 'choose:', 'will:', 'should:', 'need to:']
        decisions = []
        
        lines = thinking_content.split('\n')
        for line in lines:
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in decision_keywords):
                decisions.append(line.strip())
                
        return decisions[:5]  # Top 5 decisions

    def _extract_alternatives(self, thinking_content: str) -> List[str]:
        """Extract alternative approaches from thinking content"""
        alternative_keywords = ['alternatively:', 'another way:', 'could also:', 'option:', 'approach:']
        alternatives = []
        
        lines = thinking_content.split('\n')
        for line in lines:
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in alternative_keywords):
                alternatives.append(line.strip())
                
        return alternatives[:3]  # Top 3 alternatives


# Auto-cleanup background thread
class CacheCleanupThread(threading.Thread):
    """Background thread for automatic cache cleanup"""
    
    def __init__(self, cache_system: CacheSystem, interval_hours: int = 24):
        super().__init__(daemon=True)
        self.cache_system = cache_system
        self.interval_seconds = interval_hours * 3600
        self.running = True

    def run(self):
        """Run cleanup at regular intervals"""
        while self.running:
            time.sleep(self.interval_seconds)
            if self.running:  # Check again after sleep
                try:
                    self.cache_system.cleanup_expired_caches()
                except Exception as e:
                    logger.error(f"Auto-cleanup failed: {e}")

    def stop(self):
        """Stop the cleanup thread"""
        self.running = False


# Global cache system instance
_cache_system_instance = None

def get_cache_system() -> CacheSystem:
    """Get global cache system instance"""
    global _cache_system_instance
    if _cache_system_instance is None:
        _cache_system_instance = CacheSystem()
        
        # Start auto-cleanup thread if configured
        if _cache_system_instance.config['auto_cleanup']:
            cleanup_thread = CacheCleanupThread(_cache_system_instance)
            cleanup_thread.start()
            
    return _cache_system_instance


if __name__ == "__main__":
    # Test the cache system
    cache = get_cache_system()
    
    # Test thinking cache
    thinking_id = cache.cache_claude_thinking(
        user_query="Test query",
        thinking_content="This is test thinking content with key insights.",
        execution_context={"duration": 15, "tools_used": ["Read", "Edit"]},
        outcome_metrics={"success_rate": 0.9, "user_satisfaction": "high"}
    )
    
    # Test research session cache
    research_id = cache.cache_research_session({
        "domain": "machine learning",
        "query": "neural networks",
        "discoveries": [{"title": "Test paper", "authors": ["Author 1"]}],
        "strategies": {"queries": ["neural networks", "deep learning"]}
    })
    
    # Test agent execution cache
    agent_id = cache.cache_agent_execution(
        "literature-coordinator",
        {
            "triggered_by": "user_request",
            "duration": 120,
            "performance_metrics": {"success_rate": 0.95, "quality_score": 0.88},
            "output_results": {"papers_found": 10}
        }
    )
    
    # Display stats
    stats = cache.get_cache_stats()
    print("Cache Statistics:")
    print(json.dumps(stats, indent=2))
    
    logger.info("Cache system test completed successfully")