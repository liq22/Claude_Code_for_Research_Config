#!/usr/bin/env python3
"""
Cache System Starter and Integrator
Initializes and starts the auto-cache system for Claude Code Research Configuration

Author: Claude Code Research System
Version: 1.0.0
"""

import os
import sys
import json
import time
import signal
import subprocess
import threading
from datetime import datetime
from pathlib import Path

# Add cache modules to path
sys.path.append(str(Path(__file__).parent))
from cache_system import get_cache_system
from auto_cache_hook import get_auto_cache_hook

class CacheSystemStarter:
    """Main class for starting and managing the cache system"""
    
    def __init__(self, config_path: str = None):
        self.project_root = Path(__file__).parent.parent.parent.parent
        self.config_path = config_path or Path(__file__).parent / "config.json"
        self.config = self._load_config()
        self.cache_system = None
        self.auto_hook = None
        self.running = False
        
    def _load_config(self) -> dict:
        """Load cache system configuration"""
        try:
            with open(self.config_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"❌ Config file not found: {self.config_path}")
            return self._default_config()
        except json.JSONDecodeError as e:
            print(f"❌ Invalid JSON in config: {e}")
            return self._default_config()
    
    def _default_config(self) -> dict:
        """Return default configuration"""
        return {
            "system": {"auto_start": True},
            "cache": {"enabled_types": ["thinking", "research", "agent"]},
            "logging": {"level": "INFO", "console_output": True}
        }
    
    def initialize_environment(self):
        """Initialize cache system environment"""
        print("🔧 Initializing cache system environment...")
        
        # Create cache directories
        cache_base = self.project_root / self.config.get("cache", {}).get("base_path", "src/dev/cache")
        for cache_type in self.config.get("cache", {}).get("enabled_types", []):
            cache_dir = cache_base / {
                "thinking": "claude_thinking",
                "research": "research_sessions", 
                "agent": "agent_execution"
            }.get(cache_type, cache_type)
            cache_dir.mkdir(parents=True, exist_ok=True)
            
        # Create log directory
        log_dir = cache_base / "logs"
        log_dir.mkdir(exist_ok=True)
        
        # Set environment variables
        os.environ['CLAUDE_CACHE_ENABLED'] = '1'
        os.environ['CLAUDE_CACHE_PATH'] = str(cache_base)
        os.environ['CLAUDE_CACHE_CONFIG'] = str(self.config_path)
        
        print("✅ Environment initialized")
        return True
    
    def start_cache_system(self):
        """Start the cache system components"""
        print("🚀 Starting cache system components...")
        
        try:
            # Initialize cache system
            self.cache_system = get_cache_system()
            print("✅ Cache system initialized")
            
            # Start auto-cache hook if enabled
            if self.config.get("capture", {}).get("thinking", {}).get("auto_capture", True):
                self.auto_hook = get_auto_cache_hook()
                print("✅ Auto-cache hook started")
            
            # Start background monitoring
            if self.config.get("performance", {}).get("background_processing", True):
                self._start_background_monitoring()
                print("✅ Background monitoring started")
            
            self.running = True
            print("🎉 Cache system fully operational!")
            return True
            
        except Exception as e:
            print(f"❌ Failed to start cache system: {e}")
            return False
    
    def _start_background_monitoring(self):
        """Start background monitoring thread"""
        def monitor():
            while self.running:
                try:
                    # Periodic cleanup
                    if hasattr(self.cache_system, 'cleanup_expired_caches'):
                        self.cache_system.cleanup_expired_caches()
                    
                    # Sleep for monitoring interval
                    interval = self.config.get("performance", {}).get("metrics", {}).get("report_interval_minutes", 60)
                    time.sleep(interval * 60)
                    
                except Exception as e:
                    print(f"⚠️  Background monitoring error: {e}")
                    time.sleep(60)  # Wait before retry
        
        monitor_thread = threading.Thread(target=monitor, daemon=True)
        monitor_thread.start()
    
    def setup_signal_handlers(self):
        """Setup graceful shutdown handlers"""
        def signal_handler(signum, frame):
            print(f"\n🛑 Received signal {signum}, shutting down gracefully...")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def status_report(self):
        """Generate and display status report"""
        print("\n📊 Cache System Status Report")
        print("=" * 50)
        print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Cache Directory: {os.environ.get('CLAUDE_CACHE_PATH', 'Not Set')}")
        print(f"⚙️  Config File: {self.config_path}")
        
        # Check cache directories
        cache_base = Path(os.environ.get('CLAUDE_CACHE_PATH', ''))
        if cache_base.exists():
            for cache_type in ["claude_thinking", "research_sessions", "agent_execution"]:
                cache_dir = cache_base / cache_type
                if cache_dir.exists():
                    file_count = len(list(cache_dir.glob('*')))
                    print(f"📦 {cache_type}: {file_count} cached items")
        
        # Component status
        print(f"🧠 Auto-cache hook: {'✅ Running' if self.auto_hook else '❌ Not started'}")
        print(f"💾 Cache system: {'✅ Running' if self.cache_system else '❌ Not started'}")
        print(f"🔄 Background monitoring: {'✅ Active' if self.running else '❌ Inactive'}")
        
        print("\n💡 Usage:")
        print("  - Query cache: python src/scripts/cache/cache_query.py search --query 'your search'")
        print("  - Cache manager: /agent writer-cache-manager")
        print("  - Stop system: Ctrl+C or kill process")
        print()
    
    def shutdown(self):
        """Gracefully shutdown cache system"""
        print("\n🔄 Shutting down cache system...")
        self.running = False
        
        if self.auto_hook:
            try:
                self.auto_hook.stop()
                print("✅ Auto-cache hook stopped")
            except Exception as e:
                print(f"⚠️  Error stopping auto-cache hook: {e}")
        
        print("🛑 Cache system shutdown complete")
    
    def run_interactive(self):
        """Run in interactive mode"""
        self.status_report()
        
        try:
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()
    
    def run_daemon(self):
        """Run in daemon mode (background)"""
        print("👤 Running in daemon mode...")
        try:
            while self.running:
                time.sleep(10)
        except KeyboardInterrupt:
            self.shutdown()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Start Claude Code Cache System")
    parser.add_argument("--config", help="Path to config file")
    parser.add_argument("--daemon", action="store_true", help="Run in background daemon mode")
    parser.add_argument("--status", action="store_true", help="Show status only")
    parser.add_argument("--test", action="store_true", help="Run system test")
    
    args = parser.parse_args()
    
    # Initialize starter
    starter = CacheSystemStarter(config_path=args.config)
    
    if args.status:
        starter.initialize_environment()
        starter.status_report()
        return
    
    if args.test:
        print("🧪 Running cache system test...")
        success = starter.initialize_environment() and starter.start_cache_system()
        if success:
            print("✅ Cache system test passed!")
            starter.shutdown()
        else:
            print("❌ Cache system test failed!")
            sys.exit(1)
        return
    
    # Normal startup
    print("🎯 Starting Claude Code Cache System")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Setup signal handlers
    starter.setup_signal_handlers()
    
    # Initialize and start
    if not starter.initialize_environment():
        sys.exit(1)
        
    if not starter.start_cache_system():
        sys.exit(1)
    
    # Run mode
    if args.daemon:
        starter.run_daemon()
    else:
        starter.run_interactive()

if __name__ == "__main__":
    main()