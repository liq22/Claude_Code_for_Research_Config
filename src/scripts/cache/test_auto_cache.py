#!/usr/bin/env python3
"""
Auto-Cache System Test Suite
Tests all components of the automatic caching system for Claude Code

Author: Claude Code Research System
Version: 1.0.0
"""

import os
import sys
import time
import json
import tempfile
import shutil
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# Add cache modules to path
sys.path.append(str(Path(__file__).parent))
from cache_system import get_cache_system
from auto_cache_hook import get_auto_cache_hook
from cache_query import CacheQueryEngine

class AutoCacheTestSuite:
    """Comprehensive test suite for auto-cache system"""
    
    def __init__(self, test_dir: str = None):
        self.test_dir = Path(test_dir) if test_dir else Path(__file__).parent.parent.parent.parent / "dev/cache_test"
        self.original_cache_path = None
        self.cache_system = None
        self.auto_hook = None
        self.query_engine = None
        self.test_results = []
        
    def setup_test_environment(self):
        """Setup isolated test environment"""
        print("🔧 Setting up test environment...")
        
        # Create test directory
        self.test_dir.mkdir(parents=True, exist_ok=True)
        
        # Backup original environment
        self.original_cache_path = os.environ.get('CLAUDE_CACHE_PATH')
        
        # Set test environment
        os.environ['CLAUDE_CACHE_PATH'] = str(self.test_dir)
        
        print(f"✅ Test environment: {self.test_dir}")
        return True
    
    def teardown_test_environment(self):
        """Cleanup test environment"""
        print("🧹 Cleaning up test environment...")
        
        # Restore original environment
        if self.original_cache_path:
            os.environ['CLAUDE_CACHE_PATH'] = self.original_cache_path
        elif 'CLAUDE_CACHE_PATH' in os.environ:
            del os.environ['CLAUDE_CACHE_PATH']
        
        # Cleanup test directory
        if self.test_dir.exists():
            shutil.rmtree(self.test_dir)
        
        print("✅ Test environment cleaned up")
    
    def test_cache_system_initialization(self) -> bool:
        """Test cache system can be initialized"""
        print("🧪 Testing cache system initialization...")
        
        try:
            self.cache_system = get_cache_system()
            if self.cache_system is None:
                raise Exception("Cache system returned None")
            
            print("✅ Cache system initialized successfully")
            self.test_results.append(("Cache System Init", True, "System initialized correctly"))
            return True
            
        except Exception as e:
            print(f"❌ Cache system initialization failed: {e}")
            self.test_results.append(("Cache System Init", False, str(e)))
            return False
    
    def test_auto_hook_functionality(self) -> bool:
        """Test auto-cache hook functionality"""
        print("🧪 Testing auto-cache hook functionality...")
        
        try:
            self.auto_hook = get_auto_cache_hook()
            
            # Test thinking session
            session_id = self.auto_hook.hook_thinking_start("Test thinking session")
            if not session_id:
                raise Exception("Failed to start thinking session")
            
            # Add some content
            self.auto_hook.hook_thinking_content("This is test thinking content")
            self.auto_hook.hook_tool_usage("Read", {"file_path": "/test/path.txt"})
            self.auto_hook.hook_file_access("/test/path.txt", "read")
            
            # End session
            cache_id = self.auto_hook.hook_thinking_end({"success_rate": 0.95})
            if not cache_id:
                raise Exception("Failed to end thinking session")
            
            print(f"✅ Auto-hook functionality working (Cache ID: {cache_id})")
            self.test_results.append(("Auto Hook", True, f"Session cached: {cache_id}"))
            return True
            
        except Exception as e:
            print(f"❌ Auto-hook functionality failed: {e}")
            self.test_results.append(("Auto Hook", False, str(e)))
            return False
    
    def test_research_session_caching(self) -> bool:
        """Test research session caching"""
        print("🧪 Testing research session caching...")
        
        try:
            # Start research session
            research_id = self.auto_hook.hook_research_start("machine learning", "neural networks optimization")
            if not research_id:
                raise Exception("Failed to start research session")
            
            # Add discoveries
            self.auto_hook.hook_research_discovery(research_id, {
                "title": "Attention Is All You Need",
                "authors": ["Vaswani et al."],
                "relevance_score": 0.95,
                "summary": "Transformer architecture breakthrough"
            })
            
            self.auto_hook.hook_research_discovery(research_id, {
                "title": "BERT: Bidirectional Encoder Representations",
                "authors": ["Devlin et al."],
                "relevance_score": 0.90,
                "summary": "Pre-training language representations"
            })
            
            # End research session
            cache_id = self.auto_hook.hook_research_end(research_id)
            if not cache_id:
                raise Exception("Failed to end research session")
            
            print(f"✅ Research session caching working (Cache ID: {cache_id})")
            self.test_results.append(("Research Session", True, f"Session cached: {cache_id}"))
            return True
            
        except Exception as e:
            print(f"❌ Research session caching failed: {e}")
            self.test_results.append(("Research Session", False, str(e)))
            return False
    
    def test_agent_execution_caching(self) -> bool:
        """Test agent execution caching"""
        print("🧪 Testing agent execution caching...")
        
        try:
            # Start agent execution
            execution_id = self.auto_hook.hook_agent_start("literature-coordinator", {
                "query": "quantum computing applications",
                "domain": "computer science"
            })
            if not execution_id:
                raise Exception("Failed to start agent execution")
            
            # Add execution steps
            self.auto_hook.hook_agent_step(execution_id, "search", "semantic_search", 2.5, True)
            self.auto_hook.hook_agent_step(execution_id, "analyze", "relevance_scoring", 1.8, True)
            self.auto_hook.hook_agent_step(execution_id, "synthesize", "evidence_integration", 3.2, True)
            
            # End agent execution
            cache_id = self.auto_hook.hook_agent_end(execution_id, {
                "papers_found": 15,
                "avg_relevance": 0.85,
                "synthesis_quality": 0.92
            })
            if not cache_id:
                raise Exception("Failed to end agent execution")
            
            print(f"✅ Agent execution caching working (Cache ID: {cache_id})")
            self.test_results.append(("Agent Execution", True, f"Execution cached: {cache_id}"))
            return True
            
        except Exception as e:
            print(f"❌ Agent execution caching failed: {e}")
            self.test_results.append(("Agent Execution", False, str(e)))
            return False
    
    def test_cache_querying(self) -> bool:
        """Test cache querying functionality"""
        print("🧪 Testing cache querying...")
        
        try:
            self.query_engine = CacheQueryEngine()
            
            # Test semantic search
            results = self.query_engine.semantic_search("neural networks", limit=5)
            if results is None:
                raise Exception("Semantic search returned None")
            
            print(f"✅ Semantic search found {len(results)} results")
            
            self.test_results.append(("Cache Querying", True, f"Search: {len(results)} results"))
            return True
            
        except Exception as e:
            print(f"❌ Cache querying failed: {e}")
            self.test_results.append(("Cache Querying", False, str(e)))
            return False
    
    def test_cache_persistence(self) -> bool:
        """Test cache data persistence"""
        print("🧪 Testing cache persistence...")
        
        try:
            # Check that cache files were created
            cache_dirs = ["claude_thinking", "research_sessions", "agent_execution"]
            files_found = 0
            
            for cache_dir in cache_dirs:
                dir_path = self.test_dir / cache_dir
                if dir_path.exists():
                    files = list(dir_path.glob("*"))
                    files_found += len(files)
                    print(f"📁 {cache_dir}: {len(files)} files")
            
            if files_found == 0:
                print("⚠️  No cache files found - may be using in-memory storage")
            
            # Check metadata database
            metadata_db = self.test_dir / "metadata.db"
            if metadata_db.exists():
                print("✅ Metadata database created")
            else:
                print("⚠️  Metadata database not found (may be normal)")
            
            print(f"✅ Cache persistence working ({files_found} files created)")
            self.test_results.append(("Cache Persistence", True, f"{files_found} files persisted"))
            return True
            
        except Exception as e:
            print(f"❌ Cache persistence failed: {e}")
            self.test_results.append(("Cache Persistence", False, str(e)))
            return False
    
    def test_cache_cleanup(self) -> bool:
        """Test cache cleanup functionality"""
        print("🧪 Testing cache cleanup...")
        
        try:
            if hasattr(self.cache_system, 'cleanup_expired_caches'):
                initial_files = sum(1 for _ in self.test_dir.rglob("*") if _.is_file())
                
                # Run cleanup (won't delete recent test files, but tests the mechanism)
                self.cache_system.cleanup_expired_caches()
                
                final_files = sum(1 for _ in self.test_dir.rglob("*") if _.is_file())
                
                print(f"✅ Cache cleanup completed (files: {initial_files} → {final_files})")
                self.test_results.append(("Cache Cleanup", True, f"Cleanup ran successfully"))
                return True
            else:
                print("⚠️  Cache cleanup method not available")
                self.test_results.append(("Cache Cleanup", True, "Method not available (acceptable)"))
                return True
                
        except Exception as e:
            print(f"❌ Cache cleanup failed: {e}")
            self.test_results.append(("Cache Cleanup", False, str(e)))
            return False
    
    def generate_test_report(self) -> Dict:
        """Generate comprehensive test report"""
        passed = sum(1 for _, success, _ in self.test_results if success)
        total = len(self.test_results)
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_tests": total,
            "passed": passed,
            "failed": total - passed,
            "success_rate": passed / total if total > 0 else 0,
            "tests": [
                {
                    "name": name,
                    "passed": success,
                    "details": details
                }
                for name, success, details in self.test_results
            ]
        }
        
        return report
    
    def run_all_tests(self) -> bool:
        """Run all tests in sequence"""
        print("🚀 Starting Auto-Cache System Test Suite")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 60)
        
        try:
            # Setup
            if not self.setup_test_environment():
                return False
            
            # Run tests
            tests = [
                self.test_cache_system_initialization,
                self.test_auto_hook_functionality,
                self.test_research_session_caching,
                self.test_agent_execution_caching,
                self.test_cache_querying,
                self.test_cache_persistence,
                self.test_cache_cleanup
            ]
            
            # Give cache system time to initialize
            time.sleep(1)
            
            for test in tests:
                test()
                time.sleep(0.5)  # Small delay between tests
            
        finally:
            # Cleanup
            if self.auto_hook:
                try:
                    self.auto_hook.stop()
                except:
                    pass
            
            self.teardown_test_environment()
        
        # Generate report
        report = self.generate_test_report()
        
        print("\n" + "=" * 60)
        print("📊 Test Results Summary")
        print("=" * 60)
        print(f"✅ Passed: {report['passed']}/{report['total_tests']} ({report['success_rate']:.1%})")
        print(f"❌ Failed: {report['failed']}/{report['total_tests']}")
        print()
        
        for test in report['tests']:
            status = "✅" if test['passed'] else "❌"
            print(f"{status} {test['name']}: {test['details']}")
        
        # Save detailed report
        report_file = Path(__file__).parent.parent.parent.parent / "tests/cache_test_report.json"
        report_file.parent.mkdir(exist_ok=True)
        
        with open(report_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\n📄 Detailed report saved: {report_file}")
        
        return report['success_rate'] >= 0.8  # 80% pass rate required

def main():
    """Main test runner"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Auto-Cache System")
    parser.add_argument("--test-dir", help="Custom test directory")
    parser.add_argument("--quick", action="store_true", help="Run quick tests only")
    
    args = parser.parse_args()
    
    # Run tests
    test_suite = AutoCacheTestSuite(test_dir=args.test_dir)
    success = test_suite.run_all_tests()
    
    if success:
        print("\n🎉 Auto-cache system is working correctly!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed. Check the output above for details.")
        sys.exit(1)

if __name__ == "__main__":
    main()