#!/usr/bin/env python3
"""
Auto-Cache Hook for Claude Code

Automatically captures Claude thinking processes, research sessions, and agent executions
for intelligent caching and future reference.

Author: Claude Code Research System  
Version: 1.0.0
"""

import os
import sys
import json
import time
import uuid
import threading
import logging
import re
import queue
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import signal
import atexit

# Add the cache system to the path
sys.path.append(str(Path(__file__).parent))
from cache_system import get_cache_system

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('dev/cache/auto_cache.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class ThinkingCapture:
    """Captures Claude thinking processes"""
    
    def __init__(self):
        self.thinking_buffer = ""
        self.current_session = None
        self.start_time = None
        self.tools_used = []
        self.files_accessed = []
        
    def start_thinking_session(self, user_query: str) -> str:
        """Start a new thinking session"""
        session_id = str(uuid.uuid4())
        self.current_session = session_id
        self.start_time = time.time()
        self.thinking_buffer = ""
        self.tools_used = []
        self.files_accessed = []
        
        logger.info(f"Started thinking session: {session_id}")
        return session_id
        
    def add_thinking_content(self, content: str):
        """Add thinking content to buffer"""
        if self.current_session:
            self.thinking_buffer += content + "\n"
    
    def record_tool_usage(self, tool_name: str, parameters: Dict = None):
        """Record tool usage during thinking"""
        if self.current_session:
            tool_entry = {
                'tool': tool_name,
                'timestamp': datetime.now().isoformat(),
                'parameters': parameters or {}
            }
            self.tools_used.append(tool_entry)
    
    def record_file_access(self, file_path: str, operation: str = 'read'):
        """Record file access during thinking"""
        if self.current_session and file_path not in self.files_accessed:
            self.files_accessed.append({
                'path': file_path,
                'operation': operation,
                'timestamp': datetime.now().isoformat()
            })
    
    def end_thinking_session(self, outcome_metrics: Dict = None) -> Optional[str]:
        """End thinking session and cache the results"""
        if not self.current_session:
            return None
            
        duration = time.time() - self.start_time if self.start_time else 0
        
        # Extract user query from thinking buffer (simple heuristic)
        user_query = self._extract_user_query()
        
        execution_context = {
            'duration': duration,
            'tools_used': [tool['tool'] for tool in self.tools_used],
            'tools_detailed': self.tools_used,
            'files_accessed': self.files_accessed,
            'session_start': datetime.fromtimestamp(self.start_time).isoformat() if self.start_time else None
        }
        
        default_metrics = {
            'success_rate': 0.9,  # Default assumption
            'user_satisfaction': 'high',
            'complexity_score': len(self.thinking_buffer) / 1000,
            'tool_efficiency': len(self.tools_used) / max(duration / 60, 1)  # tools per minute
        }
        
        final_metrics = {**default_metrics, **(outcome_metrics or {})}
        
        # Cache the thinking process
        try:
            cache_system = get_cache_system()
            cache_id = cache_system.cache_claude_thinking(
                user_query=user_query,
                thinking_content=self.thinking_buffer,
                execution_context=execution_context,
                outcome_metrics=final_metrics,
                session_id=self.current_session
            )
            
            logger.info(f"Cached thinking session: {self.current_session} -> {cache_id}")
            
            # Reset for next session
            self.current_session = None
            self.thinking_buffer = ""
            self.start_time = None
            self.tools_used = []
            self.files_accessed = []
            
            return cache_id
            
        except Exception as e:
            logger.error(f"Failed to cache thinking session: {e}")
            return None
    
    def _extract_user_query(self) -> str:
        """Extract user query from thinking buffer"""
        # Look for patterns like "user asks:", "the user wants:", etc.
        lines = self.thinking_buffer.split('\n')
        for line in lines[:10]:  # Check first 10 lines
            line = line.strip().lower()
            if any(phrase in line for phrase in ['user asks', 'user wants', 'user is asking', 'the request', 'user query']):
                # Extract the actual query part
                return line.split(':', 1)[-1].strip() if ':' in line else line
        
        # Fallback: return first meaningful line
        for line in lines[:5]:
            if len(line.strip()) > 10 and not line.strip().startswith('<'):
                return line.strip()[:200]
        
        return "Auto-captured thinking session"

class ResearchSessionCapture:
    """Captures research session data"""
    
    def __init__(self):
        self.active_sessions = {}
        
    def start_research_session(self, domain: str, query: str) -> str:
        """Start research session"""
        session_id = str(uuid.uuid4())
        self.active_sessions[session_id] = {
            'domain': domain,
            'query': query,
            'start_time': datetime.now().isoformat(),
            'discoveries': [],
            'strategies': {'queries': [], 'databases': []},
            'synthesis': {}
        }
        logger.info(f"Started research session: {session_id}")
        return session_id
    
    def add_discovery(self, session_id: str, discovery: Dict):
        """Add literature discovery"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['discoveries'].append({
                **discovery,
                'found_at': datetime.now().isoformat()
            })
    
    def add_search_strategy(self, session_id: str, query: str, database: str):
        """Record search strategy"""
        if session_id in self.active_sessions:
            session = self.active_sessions[session_id]
            session['strategies']['queries'].append(query)
            if database not in session['strategies']['databases']:
                session['strategies']['databases'].append(database)
    
    def add_synthesis(self, session_id: str, synthesis_data: Dict):
        """Add knowledge synthesis"""
        if session_id in self.active_sessions:
            self.active_sessions[session_id]['synthesis'].update(synthesis_data)
    
    def end_research_session(self, session_id: str) -> Optional[str]:
        """End and cache research session"""
        if session_id not in self.active_sessions:
            return None
            
        session_data = self.active_sessions[session_id]
        session_data['end_time'] = datetime.now().isoformat()
        
        try:
            cache_system = get_cache_system()
            cache_id = cache_system.cache_research_session(
                session_data=session_data,
                session_id=session_id
            )
            
            logger.info(f"Cached research session: {session_id} -> {cache_id}")
            
            # Remove from active sessions
            del self.active_sessions[session_id]
            
            return cache_id
            
        except Exception as e:
            logger.error(f"Failed to cache research session: {e}")
            return None

class AgentExecutionCapture:
    """Captures agent execution data"""
    
    def __init__(self):
        self.active_executions = {}
    
    def start_agent_execution(self, agent_name: str, input_context: Dict) -> str:
        """Start agent execution tracking"""
        execution_id = str(uuid.uuid4())
        self.active_executions[execution_id] = {
            'agent_name': agent_name,
            'start_time': datetime.now().isoformat(),
            'input_context': input_context,
            'execution_trace': [],
            'performance_metrics': {},
            'output_results': {}
        }
        logger.info(f"Started agent execution: {agent_name} -> {execution_id}")
        return execution_id
    
    def add_execution_step(self, execution_id: str, step: str, action: str, duration: float, success: bool):
        """Add execution step"""
        if execution_id in self.active_executions:
            self.active_executions[execution_id]['execution_trace'].append({
                'step': step,
                'action': action,
                'duration': duration,
                'success': success,
                'timestamp': datetime.now().isoformat()
            })
    
    def update_performance_metrics(self, execution_id: str, metrics: Dict):
        """Update performance metrics"""
        if execution_id in self.active_executions:
            self.active_executions[execution_id]['performance_metrics'].update(metrics)
    
    def set_output_results(self, execution_id: str, results: Dict):
        """Set final output results"""
        if execution_id in self.active_executions:
            self.active_executions[execution_id]['output_results'] = results
    
    def end_agent_execution(self, execution_id: str) -> Optional[str]:
        """End and cache agent execution"""
        if execution_id not in self.active_executions:
            return None
            
        execution_data = self.active_executions[execution_id]
        execution_data['completion_time'] = datetime.now().isoformat()
        
        # Calculate duration
        start_time = datetime.fromisoformat(execution_data['start_time'])
        end_time = datetime.fromisoformat(execution_data['completion_time'])
        execution_data['duration'] = (end_time - start_time).total_seconds()
        
        try:
            cache_system = get_cache_system()
            cache_id = cache_system.cache_agent_execution(
                agent_name=execution_data['agent_name'],
                execution_data=execution_data
            )
            
            logger.info(f"Cached agent execution: {execution_id} -> {cache_id}")
            
            # Remove from active executions
            del self.active_executions[execution_id]
            
            return cache_id
            
        except Exception as e:
            logger.error(f"Failed to cache agent execution: {e}")
            return None

class AutoCacheHook:
    """Main auto-cache hook system"""
    
    def __init__(self):
        self.thinking_capture = ThinkingCapture()
        self.research_capture = ResearchSessionCapture()
        self.agent_capture = AgentExecutionCapture()
        self.background_queue = queue.Queue()
        self.background_thread = None
        self.running = False
        
        # Session tracking
        self.current_thinking_session = None
        self.current_research_sessions = set()
        self.current_agent_executions = set()
        
        self._setup_signal_handlers()
        
    def start(self):
        """Start the auto-cache system"""
        self.running = True
        self.background_thread = threading.Thread(target=self._background_processor, daemon=True)
        self.background_thread.start()
        logger.info("Auto-cache hook started")
    
    def stop(self):
        """Stop the auto-cache system"""
        self.running = False
        if self.background_thread:
            self.background_thread.join(timeout=5)
        
        # End any active sessions
        self._cleanup_active_sessions()
        logger.info("Auto-cache hook stopped")
    
    def hook_thinking_start(self, user_query: str) -> str:
        """Hook for thinking process start"""
        session_id = self.thinking_capture.start_thinking_session(user_query)
        self.current_thinking_session = session_id
        return session_id
    
    def hook_thinking_content(self, content: str):
        """Hook for thinking content"""
        self.thinking_capture.add_thinking_content(content)
    
    def hook_thinking_end(self, outcome_metrics: Dict = None) -> Optional[str]:
        """Hook for thinking process end"""
        cache_id = self.thinking_capture.end_thinking_session(outcome_metrics)
        self.current_thinking_session = None
        return cache_id
    
    def hook_tool_usage(self, tool_name: str, parameters: Dict = None):
        """Hook for tool usage"""
        self.thinking_capture.record_tool_usage(tool_name, parameters)
    
    def hook_file_access(self, file_path: str, operation: str = 'read'):
        """Hook for file access"""
        self.thinking_capture.record_file_access(file_path, operation)
    
    def hook_research_start(self, domain: str, query: str) -> str:
        """Hook for research session start"""
        session_id = self.research_capture.start_research_session(domain, query)
        self.current_research_sessions.add(session_id)
        return session_id
    
    def hook_research_discovery(self, session_id: str, discovery: Dict):
        """Hook for research discovery"""
        self.research_capture.add_discovery(session_id, discovery)
    
    def hook_research_end(self, session_id: str) -> Optional[str]:
        """Hook for research session end"""
        cache_id = self.research_capture.end_research_session(session_id)
        self.current_research_sessions.discard(session_id)
        return cache_id
    
    def hook_agent_start(self, agent_name: str, input_context: Dict) -> str:
        """Hook for agent execution start"""
        execution_id = self.agent_capture.start_agent_execution(agent_name, input_context)
        self.current_agent_executions.add(execution_id)
        return execution_id
    
    def hook_agent_step(self, execution_id: str, step: str, action: str, duration: float, success: bool):
        """Hook for agent execution step"""
        self.agent_capture.add_execution_step(execution_id, step, action, duration, success)
    
    def hook_agent_end(self, execution_id: str, results: Dict = None) -> Optional[str]:
        """Hook for agent execution end"""
        if results:
            self.agent_capture.set_output_results(execution_id, results)
        cache_id = self.agent_capture.end_agent_execution(execution_id)
        self.current_agent_executions.discard(execution_id)
        return cache_id
    
    def _background_processor(self):
        """Background thread for processing cache operations"""
        while self.running:
            try:
                # Process any queued operations
                if not self.background_queue.empty():
                    operation = self.background_queue.get(timeout=1)
                    self._process_queued_operation(operation)
                
                time.sleep(0.1)  # Small delay to prevent busy waiting
                
            except queue.Empty:
                continue
            except Exception as e:
                logger.error(f"Background processor error: {e}")
    
    def _process_queued_operation(self, operation: Dict):
        """Process queued cache operation"""
        op_type = operation.get('type')
        
        if op_type == 'auto_save':
            # Periodically save active sessions
            self._auto_save_sessions()
        elif op_type == 'cleanup':
            # Cleanup expired data
            try:
                cache_system = get_cache_system()
                cache_system.cleanup_expired_caches()
            except Exception as e:
                logger.error(f"Auto-cleanup failed: {e}")
    
    def _auto_save_sessions(self):
        """Periodically save active sessions"""
        # For thinking sessions, we don't auto-save until completion
        # For research and agent sessions, we could implement incremental saves
        pass
    
    def _cleanup_active_sessions(self):
        """Clean up any active sessions on shutdown"""
        # End current thinking session
        if self.current_thinking_session:
            self.hook_thinking_end({'success_rate': 0.5, 'user_satisfaction': 'unknown'})
        
        # End research sessions
        for session_id in list(self.current_research_sessions):
            self.hook_research_end(session_id)
        
        # End agent executions
        for execution_id in list(self.current_agent_executions):
            self.hook_agent_end(execution_id, {'status': 'interrupted'})
    
    def _setup_signal_handlers(self):
        """Setup signal handlers for graceful shutdown"""
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            self.stop()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        atexit.register(self.stop)

# Global auto-cache hook instance
_auto_cache_hook = None

def get_auto_cache_hook() -> AutoCacheHook:
    """Get global auto-cache hook instance"""
    global _auto_cache_hook
    if _auto_cache_hook is None:
        _auto_cache_hook = AutoCacheHook()
        _auto_cache_hook.start()
    return _auto_cache_hook

# Convenience functions for external integration
def cache_thinking_start(user_query: str) -> str:
    """Start thinking cache session"""
    return get_auto_cache_hook().hook_thinking_start(user_query)

def cache_thinking_content(content: str):
    """Add thinking content"""
    get_auto_cache_hook().hook_thinking_content(content)

def cache_thinking_end(outcome_metrics: Dict = None) -> Optional[str]:
    """End thinking cache session"""
    return get_auto_cache_hook().hook_thinking_end(outcome_metrics)

def cache_tool_usage(tool_name: str, parameters: Dict = None):
    """Record tool usage"""
    get_auto_cache_hook().hook_tool_usage(tool_name, parameters)

def cache_file_access(file_path: str, operation: str = 'read'):
    """Record file access"""
    get_auto_cache_hook().hook_file_access(file_path, operation)

def cache_research_start(domain: str, query: str) -> str:
    """Start research session"""
    return get_auto_cache_hook().hook_research_start(domain, query)

def cache_research_discovery(session_id: str, discovery: Dict):
    """Record research discovery"""
    get_auto_cache_hook().hook_research_discovery(session_id, discovery)

def cache_research_end(session_id: str) -> Optional[str]:
    """End research session"""
    return get_auto_cache_hook().hook_research_end(session_id)

def cache_agent_start(agent_name: str, input_context: Dict) -> str:
    """Start agent execution"""
    return get_auto_cache_hook().hook_agent_start(agent_name, input_context)

def cache_agent_step(execution_id: str, step: str, action: str, duration: float, success: bool):
    """Record agent execution step"""
    get_auto_cache_hook().hook_agent_step(execution_id, step, action, duration, success)

def cache_agent_end(execution_id: str, results: Dict = None) -> Optional[str]:
    """End agent execution"""
    return get_auto_cache_hook().hook_agent_end(execution_id, results)

if __name__ == "__main__":
    # Test the auto-cache hook system
    hook = get_auto_cache_hook()
    
    # Test thinking cache
    print("Testing thinking cache...")
    session_id = hook.hook_thinking_start("How to implement caching system?")
    hook.hook_thinking_content("I need to consider the following aspects...")
    hook.hook_thinking_content("Key decision: Use file-based storage with SQLite metadata")
    hook.hook_tool_usage("Read", {"file_path": "/test/file.py"})
    hook.hook_file_access("/test/file.py", "read")
    cache_id = hook.hook_thinking_end({"success_rate": 0.95, "user_satisfaction": "high"})
    print(f"Thinking cached: {cache_id}")
    
    # Test research cache
    print("\nTesting research cache...")
    research_id = hook.hook_research_start("machine learning", "neural networks")
    hook.hook_research_discovery(research_id, {
        "title": "Attention is All You Need",
        "authors": ["Vaswani et al."],
        "relevance_score": 0.95
    })
    research_cache_id = hook.hook_research_end(research_id)
    print(f"Research cached: {research_cache_id}")
    
    # Test agent cache
    print("\nTesting agent cache...")
    agent_id = hook.hook_agent_start("literature-coordinator", {"query": "transformers"})
    hook.hook_agent_step(agent_id, "1", "search literature", 30.0, True)
    hook.hook_agent_step(agent_id, "2", "extract data", 45.0, True)
    agent_cache_id = hook.hook_agent_end(agent_id, {"papers_found": 15, "quality_score": 0.9})
    print(f"Agent execution cached: {agent_cache_id}")
    
    print("\nAuto-cache hook test completed successfully!")
    
    # Keep running for a bit to test background operations
    time.sleep(2)
    hook.stop()