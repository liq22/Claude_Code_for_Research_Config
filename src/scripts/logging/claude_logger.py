#!/usr/bin/env python3
"""
Claude Code Automatic Execution Logger

Captures all Claude Code executions with intelligent naming based on keywords
from user queries. Provides comprehensive logging with timing, tools used,
and performance metrics.

Format: YYYY-MM-DD_HH-MM-SS_keywords.log

Author: Claude Code Research System
Version: 1.0.0
"""

import os
import sys
import json
import uuid
import re
import threading
import gzip
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
import logging
import time
import hashlib
from dataclasses import dataclass, asdict
from collections import defaultdict

# Add parent directory to path for keyword extraction
sys.path.append(str(Path(__file__).parent))

@dataclass
class ExecutionLog:
    """Structure for execution log entries"""
    session_id: str
    timestamp: str
    user_query: str
    keywords: List[str]
    log_filename: str
    execution: Dict[str, Any]
    response: str
    metrics: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

class ClaudeLogger:
    """Main Claude Code execution logger"""
    
    def __init__(self, config_path: str = ".claude/config.yaml", logs_base_path: str = "logs"):
        self.logs_base_path = Path(logs_base_path)
        self.config_path = Path(config_path)
        
        # Ensure directories exist
        self._ensure_directories()
        
        # Load configuration
        self.config = self._load_config()
        
        # Active session tracking
        self.active_sessions = {}
        self.current_session_id = None
        
        # Thread safety
        self._lock = threading.Lock()
        
        # Initialize logging
        self._setup_logging()
        
        # Performance tracking
        self.session_start_time = None
        self.tools_used = []
        self.files_accessed = []
        self.agents_invoked = []
        
        self.logger.info("Claude Logger initialized successfully")

    def _ensure_directories(self):
        """Ensure all required directories exist"""
        directories = [
            self.logs_base_path / "executions",
            self.logs_base_path / "sessions", 
            self.logs_base_path / "agents",
            self.logs_base_path / "analytics"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from YAML file"""
        default_config = {
            'logging': {
                'enabled': True,
                'auto_capture': True,
                'log_path': 'logs/executions',
                'retention_days': 90,
                'compression': True,
                'keyword_extraction': True,
                'real_time': True,
                'max_keywords': 5,
                'min_keyword_length': 3,
                'file_rotation_mb': 10
            }
        }
        
        try:
            if self.config_path.exists():
                import yaml
                with open(self.config_path, 'r') as f:
                    config = yaml.safe_load(f)
                    # Merge with defaults
                    default_config.update(config)
        except Exception as e:
            self.logger.warning(f"Failed to load config: {e}, using defaults")
            
        return default_config['logging']
    
    def _setup_logging(self):
        """Setup internal logging system"""
        log_level = logging.INFO
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        
        # Create logger
        self.logger = logging.getLogger('claude_logger')
        self.logger.setLevel(log_level)
        
        # File handler
        log_file = self.logs_base_path / "analytics" / "claude_logger.log"
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        # Console handler (optional)
        if self.config.get('verbose', False):
            console_handler = logging.StreamHandler()
            console_handler.setFormatter(formatter)
            self.logger.addHandler(console_handler)

    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from user query using simple NLP"""
        if not self.config.get('keyword_extraction', True):
            return ['session']
            
        # Clean and normalize text
        text = re.sub(r'[^\w\s]', ' ', text.lower())
        words = text.split()
        
        # Filter out common words (stopwords)
        stopwords = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among', 'i', 'you',
            'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their', 'this', 'that',
            'these', 'those', 'is', 'was', 'are', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'can', 'please', 'help', 'how',
            'what', 'when', 'where', 'why', 'who', 'which', 'agent', 'claude'
        }
        
        # Extract meaningful keywords
        keywords = []
        for word in words:
            if (len(word) >= self.config.get('min_keyword_length', 3) and 
                word not in stopwords and
                not word.isdigit()):
                keywords.append(word)
        
        # Remove duplicates while preserving order
        unique_keywords = list(dict.fromkeys(keywords))
        
        # Limit number of keywords
        max_keywords = self.config.get('max_keywords', 5)
        return unique_keywords[:max_keywords] if unique_keywords else ['session']

    def generate_log_filename(self, user_query: str, timestamp: datetime = None) -> str:
        """Generate smart log filename based on keywords and timestamp"""
        if timestamp is None:
            timestamp = datetime.now()
            
        # Extract keywords
        keywords = self.extract_keywords(user_query)
        
        # Format timestamp
        time_str = timestamp.strftime("%Y-%m-%d_%H-%M-%S")
        
        # Create keywords part (limit length for filesystem)
        keywords_str = "_".join(keywords[:3])  # Max 3 keywords
        if len(keywords_str) > 50:  # Limit total length
            keywords_str = keywords_str[:50]
        
        # Sanitize for filesystem
        keywords_str = re.sub(r'[^\w\-_]', '_', keywords_str)
        
        return f"{time_str}_{keywords_str}.log"

    def start_execution_session(self, user_query: str) -> str:
        """Start a new execution logging session"""
        with self._lock:
            # Generate session ID and filename
            session_id = str(uuid.uuid4())
            timestamp = datetime.now()
            log_filename = self.generate_log_filename(user_query, timestamp)
            
            # Initialize session data
            session_data = {
                'session_id': session_id,
                'start_time': timestamp.isoformat(),
                'user_query': user_query,
                'keywords': self.extract_keywords(user_query),
                'log_filename': log_filename,
                'tools_used': [],
                'files_accessed': [],
                'agents_invoked': [],
                'execution_trace': [],
                'status': 'active'
            }
            
            # Store active session
            self.active_sessions[session_id] = session_data
            self.current_session_id = session_id
            self.session_start_time = time.time()
            
            # Create log file
            log_path = self._get_daily_log_path(timestamp) / log_filename
            self._create_log_file(log_path, session_data)
            
            self.logger.info(f"Started execution session: {session_id} -> {log_filename}")
            return session_id

    def log_tool_usage(self, tool_name: str, parameters: Dict = None, duration: float = None):
        """Log tool usage during execution"""
        if not self.current_session_id:
            return
            
        with self._lock:
            tool_entry = {
                'tool': tool_name,
                'timestamp': datetime.now().isoformat(),
                'parameters': parameters or {},
                'duration': duration
            }
            
            if self.current_session_id in self.active_sessions:
                session = self.active_sessions[self.current_session_id]
                session['tools_used'].append(tool_entry)
                session['execution_trace'].append(f"TOOL: {tool_name}")
                
                # Real-time logging to file
                if self.config.get('real_time', True):
                    self._append_to_log(tool_entry, 'TOOL_USAGE')

    def log_file_access(self, file_path: str, operation: str = 'read'):
        """Log file access during execution"""
        if not self.current_session_id:
            return
            
        with self._lock:
            file_entry = {
                'path': file_path,
                'operation': operation,
                'timestamp': datetime.now().isoformat()
            }
            
            if self.current_session_id in self.active_sessions:
                session = self.active_sessions[self.current_session_id]
                session['files_accessed'].append(file_entry)
                session['execution_trace'].append(f"FILE: {operation} {file_path}")
                
                # Real-time logging to file
                if self.config.get('real_time', True):
                    self._append_to_log(file_entry, 'FILE_ACCESS')

    def log_agent_invocation(self, agent_name: str, parameters: Dict = None, duration: float = None):
        """Log agent invocation during execution"""
        if not self.current_session_id:
            return
            
        with self._lock:
            agent_entry = {
                'agent': agent_name,
                'timestamp': datetime.now().isoformat(),
                'parameters': parameters or {},
                'duration': duration
            }
            
            if self.current_session_id in self.active_sessions:
                session = self.active_sessions[self.current_session_id]
                session['agents_invoked'].append(agent_entry)
                session['execution_trace'].append(f"AGENT: {agent_name}")
                
                # Real-time logging to file
                if self.config.get('real_time', True):
                    self._append_to_log(agent_entry, 'AGENT_INVOCATION')

    def log_response(self, response: str, tokens_used: int = None):
        """Log Claude's response"""
        if not self.current_session_id:
            return
            
        with self._lock:
            response_entry = {
                'response': response,
                'timestamp': datetime.now().isoformat(),
                'tokens_used': tokens_used,
                'length': len(response)
            }
            
            if self.current_session_id in self.active_sessions:
                session = self.active_sessions[self.current_session_id]
                session['response'] = response_entry
                
                # Real-time logging to file
                if self.config.get('real_time', True):
                    self._append_to_log(response_entry, 'RESPONSE')

    def end_execution_session(self, success: bool = True, error_message: str = None) -> Optional[str]:
        """End current execution session and finalize log"""
        if not self.current_session_id:
            return None
            
        with self._lock:
            session_id = self.current_session_id
            
            if session_id not in self.active_sessions:
                return None
                
            session = self.active_sessions[session_id]
            
            # Calculate session metrics
            end_time = datetime.now()
            duration = time.time() - self.session_start_time if self.session_start_time else 0
            
            # Finalize session data
            session.update({
                'end_time': end_time.isoformat(),
                'duration_seconds': duration,
                'success': success,
                'error_message': error_message,
                'status': 'completed',
                'metrics': {
                    'tools_count': len(session['tools_used']),
                    'files_accessed_count': len(session['files_accessed']),
                    'agents_invoked_count': len(session['agents_invoked']),
                    'execution_steps': len(session['execution_trace']),
                    'duration_seconds': duration,
                    'success_rate': 1.0 if success else 0.0
                }
            })
            
            # Create final execution log
            execution_log = ExecutionLog(
                session_id=session_id,
                timestamp=session['start_time'],
                user_query=session['user_query'],
                keywords=session['keywords'],
                log_filename=session['log_filename'],
                execution={
                    'tools_used': session['tools_used'],
                    'files_accessed': session['files_accessed'],
                    'agents_invoked': session['agents_invoked'],
                    'execution_trace': session['execution_trace'],
                    'duration_seconds': duration
                },
                response=session.get('response', ''),
                metrics=session['metrics']
            )
            
            # Write final log to file
            self._finalize_log_file(execution_log)
            
            # Update index
            self._update_index(execution_log)
            
            # Cleanup
            del self.active_sessions[session_id]
            self.current_session_id = None
            self.session_start_time = None
            
            self.logger.info(f"Completed execution session: {session_id}")
            return session['log_filename']

    def _get_daily_log_path(self, timestamp: datetime) -> Path:
        """Get daily log directory path"""
        daily_path = self.logs_base_path / "executions" / timestamp.strftime("%Y-%m-%d")
        daily_path.mkdir(parents=True, exist_ok=True)
        return daily_path

    def _create_log_file(self, log_path: Path, session_data: Dict):
        """Create initial log file"""
        try:
            with open(log_path, 'w', encoding='utf-8') as f:
                f.write(f"=== Claude Code Execution Log ===\n")
                f.write(f"Session ID: {session_data['session_id']}\n")
                f.write(f"Start Time: {session_data['start_time']}\n")
                f.write(f"User Query: {session_data['user_query']}\n")
                f.write(f"Keywords: {', '.join(session_data['keywords'])}\n")
                f.write(f"{'='*50}\n\n")
                
        except Exception as e:
            self.logger.error(f"Failed to create log file {log_path}: {e}")

    def _append_to_log(self, entry: Dict, entry_type: str):
        """Append entry to current log file in real-time"""
        if not self.current_session_id or not self.config.get('real_time', True):
            return
            
        try:
            session = self.active_sessions[self.current_session_id]
            log_filename = session['log_filename']
            timestamp = datetime.fromisoformat(session['start_time'])
            log_path = self._get_daily_log_path(timestamp) / log_filename
            
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(f"\n[{entry.get('timestamp', datetime.now().isoformat())}] {entry_type}:\n")
                f.write(json.dumps(entry, indent=2, ensure_ascii=False))
                f.write(f"\n{'-'*30}\n")
                
        except Exception as e:
            self.logger.error(f"Failed to append to log: {e}")

    def _finalize_log_file(self, execution_log: ExecutionLog):
        """Finalize log file with complete execution data"""
        try:
            timestamp = datetime.fromisoformat(execution_log.timestamp)
            log_path = self._get_daily_log_path(timestamp) / execution_log.log_filename
            
            # Append final summary
            with open(log_path, 'a', encoding='utf-8') as f:
                f.write(f"\n{'='*50}\n")
                f.write(f"=== EXECUTION SUMMARY ===\n")
                f.write(f"{'='*50}\n")
                f.write(json.dumps(execution_log.to_dict(), indent=2, ensure_ascii=False))
                f.write(f"\n{'='*50}\n")
            
            # Compress if configured
            if self.config.get('compression', True) and timestamp.date() < datetime.now().date():
                self._compress_log_file(log_path)
                
        except Exception as e:
            self.logger.error(f"Failed to finalize log: {e}")

    def _compress_log_file(self, log_path: Path):
        """Compress log file to save space"""
        try:
            compressed_path = log_path.with_suffix('.log.gz')
            
            with open(log_path, 'rb') as f_in:
                with gzip.open(compressed_path, 'wb') as f_out:
                    f_out.writelines(f_in)
            
            # Remove original file
            log_path.unlink()
            self.logger.info(f"Compressed log file: {compressed_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to compress log file: {e}")

    def _update_index(self, execution_log: ExecutionLog):
        """Update searchable index"""
        try:
            timestamp = datetime.fromisoformat(execution_log.timestamp)
            index_path = self._get_daily_log_path(timestamp) / "index.json"
            
            # Load existing index
            index_data = []
            if index_path.exists():
                with open(index_path, 'r', encoding='utf-8') as f:
                    index_data = json.load(f)
            
            # Add new entry
            index_entry = {
                'session_id': execution_log.session_id,
                'timestamp': execution_log.timestamp,
                'user_query': execution_log.user_query,
                'keywords': execution_log.keywords,
                'log_filename': execution_log.log_filename,
                'metrics': execution_log.metrics
            }
            
            index_data.append(index_entry)
            
            # Save updated index
            with open(index_path, 'w', encoding='utf-8') as f:
                json.dump(index_data, f, indent=2, ensure_ascii=False)
                
        except Exception as e:
            self.logger.error(f"Failed to update index: {e}")

    def search_logs(self, query: str, days: int = 7) -> List[Dict]:
        """Search logs by query"""
        results = []
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        current_date = start_date
        while current_date <= end_date:
            index_path = self._get_daily_log_path(current_date) / "index.json"
            
            if index_path.exists():
                try:
                    with open(index_path, 'r', encoding='utf-8') as f:
                        index_data = json.load(f)
                    
                    for entry in index_data:
                        # Simple text search in user_query and keywords
                        searchable_text = f"{entry['user_query']} {' '.join(entry['keywords'])}".lower()
                        if query.lower() in searchable_text:
                            results.append(entry)
                            
                except Exception as e:
                    self.logger.error(f"Failed to search in {index_path}: {e}")
            
            current_date += timedelta(days=1)
        
        return sorted(results, key=lambda x: x['timestamp'], reverse=True)

    def get_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Generate usage analytics"""
        analytics = {
            'total_executions': 0,
            'successful_executions': 0,
            'failed_executions': 0,
            'total_duration': 0,
            'avg_duration': 0,
            'most_used_tools': defaultdict(int),
            'most_used_agents': defaultdict(int),
            'popular_keywords': defaultdict(int),
            'daily_activity': defaultdict(int)
        }
        
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        current_date = start_date
        while current_date <= end_date:
            index_path = self._get_daily_log_path(current_date) / "index.json"
            
            if index_path.exists():
                try:
                    with open(index_path, 'r', encoding='utf-8') as f:
                        index_data = json.load(f)
                    
                    day_key = current_date.strftime("%Y-%m-%d")
                    analytics['daily_activity'][day_key] = len(index_data)
                    
                    for entry in index_data:
                        analytics['total_executions'] += 1
                        
                        if entry.get('metrics', {}).get('success_rate', 0) > 0:
                            analytics['successful_executions'] += 1
                        else:
                            analytics['failed_executions'] += 1
                        
                        duration = entry.get('metrics', {}).get('duration_seconds', 0)
                        analytics['total_duration'] += duration
                        
                        # Count keywords
                        for keyword in entry.get('keywords', []):
                            analytics['popular_keywords'][keyword] += 1
                            
                except Exception as e:
                    self.logger.error(f"Failed to analyze {index_path}: {e}")
            
            current_date += timedelta(days=1)
        
        # Calculate averages
        if analytics['total_executions'] > 0:
            analytics['avg_duration'] = analytics['total_duration'] / analytics['total_executions']
            
        # Convert defaultdicts to regular dicts for JSON serialization
        analytics['most_used_tools'] = dict(analytics['most_used_tools'])
        analytics['most_used_agents'] = dict(analytics['most_used_agents'])
        analytics['popular_keywords'] = dict(analytics['popular_keywords'])
        analytics['daily_activity'] = dict(analytics['daily_activity'])
        
        return analytics

# Global logger instance
_claude_logger = None

def get_claude_logger() -> ClaudeLogger:
    """Get global Claude logger instance"""
    global _claude_logger
    if _claude_logger is None:
        _claude_logger = ClaudeLogger()
    return _claude_logger

# Convenience functions for external integration
def start_logging_session(user_query: str) -> str:
    """Start execution logging session"""
    return get_claude_logger().start_execution_session(user_query)

def log_tool_usage(tool_name: str, parameters: Dict = None, duration: float = None):
    """Log tool usage"""
    get_claude_logger().log_tool_usage(tool_name, parameters, duration)

def log_file_access(file_path: str, operation: str = 'read'):
    """Log file access"""
    get_claude_logger().log_file_access(file_path, operation)

def log_agent_invocation(agent_name: str, parameters: Dict = None, duration: float = None):
    """Log agent invocation"""
    get_claude_logger().log_agent_invocation(agent_name, parameters, duration)

def log_response(response: str, tokens_used: int = None):
    """Log Claude response"""
    get_claude_logger().log_response(response, tokens_used)

def end_logging_session(success: bool = True, error_message: str = None) -> Optional[str]:
    """End execution logging session"""
    return get_claude_logger().end_execution_session(success, error_message)

def search_execution_logs(query: str, days: int = 7) -> List[Dict]:
    """Search execution logs"""
    return get_claude_logger().search_logs(query, days)

def get_usage_analytics(days: int = 30) -> Dict[str, Any]:
    """Get usage analytics"""
    return get_claude_logger().get_analytics(days)

if __name__ == "__main__":
    # Test the logger system
    logger = get_claude_logger()
    
    print("Testing Claude Logger...")
    
    # Test session
    session_id = logger.start_execution_session("Search for papers on quantum computing optimization")
    logger.log_tool_usage("WebSearch", {"query": "quantum computing"}, 5.2)
    logger.log_file_access("/tmp/paper.md", "write")
    logger.log_agent_invocation("research-literature", {"topic": "quantum"}, 30.5)
    logger.log_response("Found 15 relevant papers on quantum computing optimization", 245)
    filename = logger.end_execution_session(True)
    
    print(f"Test session logged to: {filename}")
    
    # Test search
    results = logger.search_logs("quantum", 1)
    print(f"Search results: {len(results)} found")
    
    # Test analytics
    analytics = logger.get_analytics(1)
    print(f"Analytics: {analytics['total_executions']} executions")
    
    print("Claude Logger test completed successfully!")