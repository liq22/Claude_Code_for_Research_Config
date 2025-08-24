#!/usr/bin/env python3
"""
Simple Cache System Starter
Starts the simplified auto-cache system for Claude Code

Author: Claude Code Research System
Version: 2.0.0 (Simplified)
"""

import os
import sys
import time
import signal
from datetime import datetime
from pathlib import Path

# Add cache modules to path
sys.path.append(str(Path(__file__).parent))
from cache import get_simple_cache_system
from auto_hook import get_simple_auto_hook

class SimpleCacheStarter:
    """Simple cache system starter"""
    
    def __init__(self):
        self.cache = None
        self.auto_hook = None
        self.running = False
        
    def initialize(self):
        """Initialize cache system"""
        print("🔧 Initializing simple cache system...")
        
        try:
            self.cache = get_simple_cache_system()
            self.auto_hook = get_simple_auto_hook()
            print("✅ Simple cache system initialized")
            return True
        except Exception as e:
            print(f"❌ Failed to initialize: {e}")
            return False
    
    def start(self):
        """Start the cache system"""
        print("🚀 Starting simple cache system...")
        
        try:
            self.auto_hook.start()
            self.running = True
            print("✅ Simple auto-cache hook started")
            print("🎉 Simple cache system operational!")
            return True
        except Exception as e:
            print(f"❌ Failed to start: {e}")
            return False
    
    def status_report(self):
        """Show status report"""
        print("\n📊 Simple Cache System Status")
        print("=" * 50)
        print(f"🕐 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        if self.cache:
            stats = self.cache.get_stats()
            print(f"📁 Cache Directory: {stats['base_path']}")
            print(f"📦 Total Files: {stats['total_files']}")
            for cache_type, count in stats['counts'].items():
                print(f"   • {cache_type.capitalize()}: {count} files")
        
        print(f"🧠 Auto-hook: {'✅ Running' if self.running else '❌ Not started'}")
        print(f"💾 Cache system: {'✅ Running' if self.cache else '❌ Not started'}")
        
        print("\n💡 Usage:")
        print("  - Search: python src/scripts/cache/simple_cache_query.py search 'query'")
        print("  - Stats: python src/scripts/cache/simple_cache_query.py stats")
        print("  - List: python src/scripts/cache/simple_cache_query.py list")
        print("  - Stop: Ctrl+C")
    
    def setup_signal_handlers(self):
        """Setup graceful shutdown handlers"""
        def signal_handler(signum, frame):
            print(f"\n🛑 Received signal {signum}, shutting down...")
            self.shutdown()
            sys.exit(0)
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def shutdown(self):
        """Gracefully shutdown cache system"""
        print("\n🔄 Shutting down simple cache system...")
        self.running = False
        
        if self.auto_hook:
            try:
                self.auto_hook.stop()
                print("✅ Auto-hook stopped")
            except Exception as e:
                print(f"⚠️  Error stopping auto-hook: {e}")
        
        print("🛑 Simple cache system shutdown complete")
    
    def run_interactive(self):
        """Run in interactive mode"""
        self.status_report()
        
        try:
            print("\n⚡ Running in interactive mode (Ctrl+C to stop)")
            while self.running:
                time.sleep(1)
        except KeyboardInterrupt:
            self.shutdown()
    
    def run_daemon(self):
        """Run in daemon mode"""
        print("👤 Running in daemon mode...")
        try:
            while self.running:
                time.sleep(10)
        except KeyboardInterrupt:
            self.shutdown()

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple Cache System Starter")
    parser.add_argument("--daemon", action="store_true", help="Run in daemon mode")
    parser.add_argument("--status", action="store_true", help="Show status only")
    parser.add_argument("--test", action="store_true", help="Run system test")
    
    args = parser.parse_args()
    
    starter = SimpleCacheStarter()
    
    if args.status:
        if starter.initialize():
            starter.status_report()
        return
    
    if args.test:
        print("🧪 Running simple cache system test...")
        success = starter.initialize() and starter.start()
        if success:
            # Quick test
            hook = get_simple_auto_hook()
            test_file = hook.cache_thinking("test query", "test thinking content")
            if test_file:
                print("✅ Simple cache system test passed!")
            else:
                print("❌ Test failed - no file created")
                success = False
            starter.shutdown()
        
        if not success:
            print("❌ Simple cache system test failed!")
            sys.exit(1)
        return
    
    # Normal startup
    print("🎯 Starting Simple Cache System")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Setup signal handlers
    starter.setup_signal_handlers()
    
    # Initialize and start
    if not starter.initialize():
        sys.exit(1)
        
    if not starter.start():
        sys.exit(1)
    
    # Run mode
    if args.daemon:
        starter.run_daemon()
    else:
        starter.run_interactive()

if __name__ == "__main__":
    main()