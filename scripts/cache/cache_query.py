#!/usr/bin/env python3
"""
Cache Query Interface for Intelligent Retrieval

Provides semantic search and intelligent querying capabilities for cached data
including Claude thinking, research sessions, and agent executions.

Author: Claude Code Research System
Version: 1.0.0
"""

import json
import sqlite3
import gzip
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import logging
import re
import argparse
from dataclasses import dataclass
import numpy as np
from difflib import SequenceMatcher

logger = logging.getLogger(__name__)

@dataclass
class CacheQueryResult:
    """Result from cache query"""
    cache_id: str
    cache_type: str
    timestamp: str
    relevance_score: float
    file_path: str
    metadata: Dict
    content_preview: str

class CacheQueryEngine:
    """Intelligent cache query engine"""
    
    def __init__(self, base_path: str = "dev/cache"):
        self.base_path = Path(base_path)
        self.db_path = self.base_path / "cache_metadata.db"
        
        if not self.db_path.exists():
            raise FileNotFoundError(f"Cache database not found: {self.db_path}")
    
    def semantic_search(self, 
                       query: str, 
                       cache_types: List[str] = None,
                       limit: int = 20,
                       min_relevance: float = 0.3,
                       time_range_days: int = None) -> List[CacheQueryResult]:
        """Perform semantic search across cached content"""
        
        if cache_types is None:
            cache_types = ['claude_thinking', 'research_sessions', 'agent_execution']
        
        # Build SQL query with filters
        where_conditions = ["cache_type IN ({})".format(','.join('?' * len(cache_types)))]
        params = cache_types
        
        if time_range_days:
            cutoff_date = (datetime.now() - timedelta(days=time_range_days)).isoformat()
            where_conditions.append("timestamp >= ?")
            params.append(cutoff_date)
        
        sql_query = f"""
            SELECT cache_id, cache_type, timestamp, file_path, quality_score, tags
            FROM cache_metadata 
            WHERE {' AND '.join(where_conditions)}
            ORDER BY timestamp DESC
        """
        
        results = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(sql_query, params)
            
            for cache_id, cache_type, timestamp, file_path, quality_score, tags_str in cursor.fetchall():
                try:
                    # Load and analyze content
                    content = self._load_cache_content(file_path)
                    if content:
                        # Calculate relevance score
                        relevance = self._calculate_relevance(query, content, cache_type)
                        
                        if relevance >= min_relevance:
                            # Generate content preview
                            preview = self._generate_preview(content, query)
                            
                            # Parse tags
                            tags = json.loads(tags_str) if tags_str else []
                            
                            result = CacheQueryResult(
                                cache_id=cache_id,
                                cache_type=cache_type,
                                timestamp=timestamp,
                                relevance_score=relevance,
                                file_path=file_path,
                                metadata={
                                    'quality_score': quality_score,
                                    'tags': tags
                                },
                                content_preview=preview
                            )
                            results.append(result)
                            
                except Exception as e:
                    logger.error(f"Error processing cache {cache_id}: {e}")
        
        # Sort by relevance score (weighted with quality and recency)
        results.sort(key=lambda x: self._calculate_final_score(x), reverse=True)
        
        return results[:limit]
    
    def find_similar_thinking(self, 
                            thinking_query: str,
                            limit: int = 10,
                            min_similarity: float = 0.4) -> List[CacheQueryResult]:
        """Find similar thinking processes"""
        
        return self.semantic_search(
            query=thinking_query,
            cache_types=['claude_thinking'],
            limit=limit,
            min_relevance=min_similarity
        )
    
    def find_research_by_domain(self,
                               domain: str,
                               limit: int = 10) -> List[CacheQueryResult]:
        """Find research sessions by domain"""
        
        results = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cache_id, timestamp, file_path, quality_score
                FROM cache_metadata 
                WHERE cache_type = 'research_sessions'
                ORDER BY quality_score DESC, timestamp DESC
                LIMIT ?
            """, (limit * 2,))  # Get more to filter
            
            for cache_id, timestamp, file_path, quality_score in cursor.fetchall():
                try:
                    content = self._load_cache_content(file_path)
                    if content and 'session_metadata' in content:
                        research_domain = content['session_metadata'].get('research_domain', '')
                        if domain.lower() in research_domain.lower():
                            preview = self._generate_research_preview(content)
                            
                            result = CacheQueryResult(
                                cache_id=cache_id,
                                cache_type='research_sessions',
                                timestamp=timestamp,
                                relevance_score=0.9,  # High relevance for domain match
                                file_path=file_path,
                                metadata={'quality_score': quality_score},
                                content_preview=preview
                            )
                            results.append(result)
                            
                            if len(results) >= limit:
                                break
                                
                except Exception as e:
                    logger.error(f"Error processing research cache {cache_id}: {e}")
        
        return results
    
    def find_agent_performance(self,
                              agent_name: str,
                              performance_metric: str = 'success_rate',
                              min_score: float = 0.8,
                              limit: int = 10) -> List[CacheQueryResult]:
        """Find best performing agent executions"""
        
        results = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cache_id, timestamp, file_path, quality_score, tags
                FROM cache_metadata 
                WHERE cache_type = 'agent_execution' AND quality_score >= ?
                ORDER BY quality_score DESC, timestamp DESC
                LIMIT ?
            """, (min_score, limit * 2))
            
            for cache_id, timestamp, file_path, quality_score, tags_str in cursor.fetchall():
                try:
                    tags = json.loads(tags_str) if tags_str else []
                    
                    # Check if agent name matches
                    if agent_name in tags or any(agent_name.lower() in tag.lower() for tag in tags):
                        content = self._load_cache_content(file_path)
                        if content:
                            preview = self._generate_agent_preview(content)
                            
                            result = CacheQueryResult(
                                cache_id=cache_id,
                                cache_type='agent_execution',
                                timestamp=timestamp,
                                relevance_score=quality_score,
                                file_path=file_path,
                                metadata={
                                    'quality_score': quality_score,
                                    'tags': tags
                                },
                                content_preview=preview
                            )
                            results.append(result)
                            
                            if len(results) >= limit:
                                break
                                
                except Exception as e:
                    logger.error(f"Error processing agent cache {cache_id}: {e}")
        
        return results
    
    def get_recent_caches(self,
                         hours: int = 24,
                         cache_types: List[str] = None,
                         limit: int = 20) -> List[CacheQueryResult]:
        """Get recent cache entries"""
        
        if cache_types is None:
            cache_types = ['claude_thinking', 'research_sessions', 'agent_execution']
        
        cutoff_time = (datetime.now() - timedelta(hours=hours)).isoformat()
        
        results = []
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT cache_id, cache_type, timestamp, file_path, quality_score, tags
                FROM cache_metadata 
                WHERE cache_type IN ({}) AND timestamp >= ?
                ORDER BY timestamp DESC
                LIMIT ?
            """.format(','.join('?' * len(cache_types))), cache_types + [cutoff_time, limit])
            
            for cache_id, cache_type, timestamp, file_path, quality_score, tags_str in cursor.fetchall():
                try:
                    content = self._load_cache_content(file_path)
                    if content:
                        preview = self._generate_preview(content, "", cache_type)
                        tags = json.loads(tags_str) if tags_str else []
                        
                        result = CacheQueryResult(
                            cache_id=cache_id,
                            cache_type=cache_type,
                            timestamp=timestamp,
                            relevance_score=quality_score,
                            file_path=file_path,
                            metadata={
                                'quality_score': quality_score,
                                'tags': tags
                            },
                            content_preview=preview
                        )
                        results.append(result)
                        
                except Exception as e:
                    logger.error(f"Error processing recent cache {cache_id}: {e}")
        
        return results
    
    def analyze_patterns(self,
                        pattern_type: str = 'thinking_patterns',
                        time_range_days: int = 30) -> Dict:
        """Analyze patterns in cached data"""
        
        cutoff_date = (datetime.now() - timedelta(days=time_range_days)).isoformat()
        patterns = {}
        
        if pattern_type == 'thinking_patterns':
            patterns = self._analyze_thinking_patterns(cutoff_date)
        elif pattern_type == 'research_trends':
            patterns = self._analyze_research_trends(cutoff_date)
        elif pattern_type == 'agent_performance':
            patterns = self._analyze_agent_performance(cutoff_date)
        
        return patterns
    
    def _load_cache_content(self, file_path: str) -> Optional[Dict]:
        """Load content from cache file"""
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                return None
            
            if file_path.endswith('.gz'):
                with open(file_path_obj, 'rb') as f:
                    compressed_data = f.read()
                    json_str = gzip.decompress(compressed_data).decode('utf-8')
                    return json.loads(json_str)
            else:
                with open(file_path_obj, 'r', encoding='utf-8') as f:
                    return json.load(f)
                    
        except Exception as e:
            logger.error(f"Failed to load cache content from {file_path}: {e}")
            return None
    
    def _calculate_relevance(self, query: str, content: Dict, cache_type: str) -> float:
        """Calculate relevance score between query and content"""
        
        # Extract searchable text based on cache type
        if cache_type == 'claude_thinking':
            searchable_text = " ".join([
                content.get('metadata', {}).get('user_query', ''),
                content.get('thinking_content', {}).get('raw_thinking', ''),
                " ".join(content.get('thinking_content', {}).get('key_insights', [])),
                " ".join(content.get('thinking_content', {}).get('decision_points', []))
            ])
        elif cache_type == 'research_sessions':
            searchable_text = " ".join([
                content.get('session_metadata', {}).get('research_domain', ''),
                content.get('session_metadata', {}).get('primary_query', ''),
                str(content.get('literature_discoveries', [])),
                str(content.get('knowledge_synthesis', {}))
            ])
        elif cache_type == 'agent_execution':
            searchable_text = " ".join([
                content.get('execution_metadata', {}).get('agent_name', ''),
                str(content.get('input_context', {})),
                str(content.get('output_results', {}))
            ])
        else:
            searchable_text = str(content)
        
        # Simple text similarity using SequenceMatcher
        similarity = SequenceMatcher(None, query.lower(), searchable_text.lower()).ratio()
        
        # Keyword matching bonus
        query_words = set(query.lower().split())
        content_words = set(searchable_text.lower().split())
        keyword_overlap = len(query_words.intersection(content_words)) / max(len(query_words), 1)
        
        # Combine scores
        final_score = (similarity * 0.6) + (keyword_overlap * 0.4)
        
        return min(1.0, final_score)
    
    def _calculate_final_score(self, result: CacheQueryResult) -> float:
        """Calculate final weighted score for ranking"""
        
        relevance = result.relevance_score
        quality = result.metadata.get('quality_score', 0.5)
        
        # Time decay factor (newer is better)
        try:
            cache_time = datetime.fromisoformat(result.timestamp.replace('Z', '+00:00'))
            hours_old = (datetime.now() - cache_time.replace(tzinfo=None)).total_seconds() / 3600
            time_factor = max(0.1, 1.0 - (hours_old / (30 * 24)))  # Decay over 30 days
        except:
            time_factor = 0.5
        
        # Weighted combination
        final_score = (relevance * 0.5) + (quality * 0.3) + (time_factor * 0.2)
        
        return final_score
    
    def _generate_preview(self, content: Dict, query: str = "", cache_type: str = "") -> str:
        """Generate content preview"""
        
        if cache_type == 'claude_thinking':
            return self._generate_thinking_preview(content)
        elif cache_type == 'research_sessions':
            return self._generate_research_preview(content)
        elif cache_type == 'agent_execution':
            return self._generate_agent_preview(content)
        else:
            # Generic preview
            return str(content)[:200] + "..." if len(str(content)) > 200 else str(content)
    
    def _generate_thinking_preview(self, content: Dict) -> str:
        """Generate thinking content preview"""
        
        metadata = content.get('metadata', {})
        thinking = content.get('thinking_content', {})
        
        preview_parts = [
            f"Query: {metadata.get('user_query', 'N/A')[:100]}",
            f"Key Insights: {'; '.join(thinking.get('key_insights', [])[:2])}",
            f"Duration: {metadata.get('thinking_duration', 0)}s"
        ]
        
        return " | ".join(filter(None, preview_parts))
    
    def _generate_research_preview(self, content: Dict) -> str:
        """Generate research session preview"""
        
        metadata = content.get('session_metadata', {})
        discoveries = content.get('literature_discoveries', [])
        
        preview_parts = [
            f"Domain: {metadata.get('research_domain', 'N/A')}",
            f"Query: {metadata.get('primary_query', 'N/A')[:100]}",
            f"Papers Found: {len(discoveries)}",
            f"Duration: {self._calculate_session_duration(metadata)}"
        ]
        
        return " | ".join(filter(None, preview_parts))
    
    def _generate_agent_preview(self, content: Dict) -> str:
        """Generate agent execution preview"""
        
        metadata = content.get('execution_metadata', {})
        metrics = content.get('performance_metrics', {})
        
        preview_parts = [
            f"Agent: {metadata.get('agent_name', 'N/A')}",
            f"Duration: {metadata.get('duration_seconds', 0)}s",
            f"Success Rate: {metrics.get('success_rate', 0):.2f}",
            f"Quality: {metrics.get('quality_score', 0):.2f}"
        ]
        
        return " | ".join(filter(None, preview_parts))
    
    def _calculate_session_duration(self, metadata: Dict) -> str:
        """Calculate research session duration"""
        try:
            start = datetime.fromisoformat(metadata.get('start_time', ''))
            end = datetime.fromisoformat(metadata.get('end_time', ''))
            duration = (end - start).total_seconds() / 60  # minutes
            return f"{duration:.1f}min"
        except:
            return "N/A"
    
    def _analyze_thinking_patterns(self, cutoff_date: str) -> Dict:
        """Analyze thinking patterns"""
        
        patterns = {
            'common_insights': {},
            'decision_patterns': {},
            'complexity_trends': [],
            'success_factors': []
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT file_path, quality_score
                FROM cache_metadata 
                WHERE cache_type = 'claude_thinking' AND timestamp >= ?
                ORDER BY timestamp DESC
            """, (cutoff_date,))
            
            for file_path, quality_score in cursor.fetchall():
                content = self._load_cache_content(file_path)
                if content:
                    # Analyze insights
                    insights = content.get('thinking_content', {}).get('key_insights', [])
                    for insight in insights:
                        patterns['common_insights'][insight] = patterns['common_insights'].get(insight, 0) + 1
                    
                    # Track complexity vs success
                    complexity = content.get('metadata', {}).get('complexity_score', 0)
                    patterns['complexity_trends'].append({'complexity': complexity, 'quality': quality_score})
        
        return patterns
    
    def _analyze_research_trends(self, cutoff_date: str) -> Dict:
        """Analyze research trends"""
        
        trends = {
            'popular_domains': {},
            'discovery_success': {},
            'search_strategies': {},
            'knowledge_evolution': []
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT file_path, quality_score, timestamp
                FROM cache_metadata 
                WHERE cache_type = 'research_sessions' AND timestamp >= ?
                ORDER BY timestamp DESC
            """, (cutoff_date,))
            
            for file_path, quality_score, timestamp in cursor.fetchall():
                content = self._load_cache_content(file_path)
                if content:
                    # Track domains
                    domain = content.get('session_metadata', {}).get('research_domain', '')
                    if domain:
                        trends['popular_domains'][domain] = trends['popular_domains'].get(domain, 0) + 1
                    
                    # Track discovery success
                    discoveries_count = len(content.get('literature_discoveries', []))
                    trends['discovery_success'][discoveries_count] = trends['discovery_success'].get(discoveries_count, 0) + 1
        
        return trends
    
    def _analyze_agent_performance(self, cutoff_date: str) -> Dict:
        """Analyze agent performance patterns"""
        
        performance = {
            'agent_rankings': {},
            'execution_efficiency': {},
            'success_patterns': {},
            'collaboration_networks': {}
        }
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT file_path, quality_score, tags
                FROM cache_metadata 
                WHERE cache_type = 'agent_execution' AND timestamp >= ?
                ORDER BY timestamp DESC
            """, (cutoff_date,))
            
            for file_path, quality_score, tags_str in cursor.fetchall():
                content = self._load_cache_content(file_path)
                if content:
                    agent_name = content.get('execution_metadata', {}).get('agent_name', '')
                    duration = content.get('execution_metadata', {}).get('duration_seconds', 0)
                    
                    # Track agent performance
                    if agent_name not in performance['agent_rankings']:
                        performance['agent_rankings'][agent_name] = []
                    performance['agent_rankings'][agent_name].append(quality_score)
                    
                    # Track efficiency
                    if agent_name not in performance['execution_efficiency']:
                        performance['execution_efficiency'][agent_name] = []
                    performance['execution_efficiency'][agent_name].append(duration)
        
        # Calculate averages
        for agent_name, scores in performance['agent_rankings'].items():
            performance['agent_rankings'][agent_name] = {
                'avg_quality': sum(scores) / len(scores),
                'executions': len(scores),
                'best_score': max(scores)
            }
        
        for agent_name, durations in performance['execution_efficiency'].items():
            performance['execution_efficiency'][agent_name] = {
                'avg_duration': sum(durations) / len(durations),
                'min_duration': min(durations),
                'max_duration': max(durations)
            }
        
        return performance


def main():
    """Command line interface for cache queries"""
    
    parser = argparse.ArgumentParser(description='Query cached Claude Code data')
    parser.add_argument('command', choices=['search', 'similar', 'recent', 'patterns', 'agent'], 
                       help='Query command to execute')
    parser.add_argument('--query', '-q', help='Search query text')
    parser.add_argument('--agent', '-a', help='Agent name for agent-specific queries')
    parser.add_argument('--domain', '-d', help='Research domain filter')
    parser.add_argument('--limit', '-l', type=int, default=10, help='Maximum results')
    parser.add_argument('--days', type=int, help='Time range in days')
    parser.add_argument('--type', choices=['thinking', 'research', 'agent'], help='Cache type filter')
    parser.add_argument('--format', choices=['json', 'text'], default='text', help='Output format')
    
    args = parser.parse_args()
    
    # Initialize query engine
    try:
        query_engine = CacheQueryEngine()
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print("Make sure the cache system has been initialized.")
        return
    
    # Execute command
    results = []
    
    if args.command == 'search':
        if not args.query:
            print("Error: --query is required for search command")
            return
        cache_types = [f"{args.type}_{'sessions' if args.type == 'research' else args.type}"] if args.type else None
        results = query_engine.semantic_search(
            query=args.query,
            cache_types=cache_types,
            limit=args.limit,
            time_range_days=args.days
        )
    
    elif args.command == 'similar':
        if not args.query:
            print("Error: --query is required for similar command")
            return
        results = query_engine.find_similar_thinking(
            thinking_query=args.query,
            limit=args.limit
        )
    
    elif args.command == 'recent':
        cache_types = [f"{args.type}_{'sessions' if args.type == 'research' else args.type}"] if args.type else None
        hours = (args.days or 1) * 24
        results = query_engine.get_recent_caches(
            hours=hours,
            cache_types=cache_types,
            limit=args.limit
        )
    
    elif args.command == 'agent':
        if not args.agent:
            print("Error: --agent is required for agent command")
            return
        results = query_engine.find_agent_performance(
            agent_name=args.agent,
            limit=args.limit
        )
    
    elif args.command == 'patterns':
        pattern_type = f"{args.type}_patterns" if args.type else "thinking_patterns"
        patterns = query_engine.analyze_patterns(
            pattern_type=pattern_type,
            time_range_days=args.days or 30
        )
        
        if args.format == 'json':
            print(json.dumps(patterns, indent=2, ensure_ascii=False))
        else:
            print(f"Pattern Analysis ({pattern_type}):")
            print("=" * 50)
            for key, value in patterns.items():
                print(f"{key}: {value}")
        return
    
    # Format and display results
    if args.format == 'json':
        output = [
            {
                'cache_id': r.cache_id,
                'cache_type': r.cache_type,
                'timestamp': r.timestamp,
                'relevance_score': r.relevance_score,
                'preview': r.content_preview
            }
            for r in results
        ]
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        print(f"Found {len(results)} results:")
        print("=" * 80)
        for i, result in enumerate(results, 1):
            print(f"{i}. [{result.cache_type}] {result.timestamp}")
            print(f"   Relevance: {result.relevance_score:.3f}")
            print(f"   Preview: {result.content_preview}")
            print(f"   ID: {result.cache_id}")
            print("-" * 80)


if __name__ == "__main__":
    main()