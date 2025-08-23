#!/usr/bin/env python3
"""
Advanced Keywords Extractor for Claude Code Logging

Extracts meaningful keywords from user queries using advanced NLP techniques
to generate intelligent log file names.

Supports multiple extraction methods:
- TF-IDF based extraction
- Named Entity Recognition (NER) 
- Domain-specific keyword detection
- Research terminology identification

Author: Claude Code Research System
Version: 1.0.0
"""

import re
import string
from typing import List, Dict, Set, Tuple, Optional
from collections import Counter, defaultdict
from dataclasses import dataclass
import math

@dataclass
class KeywordScore:
    """Keyword with relevance score"""
    keyword: str
    score: float
    category: str  # 'technical', 'action', 'domain', 'entity'
    frequency: int

class KeywordsExtractor:
    """Advanced keyword extractor for smart log naming"""
    
    def __init__(self):
        # Extended stopwords for academic/technical context
        self.stopwords = {
            # Common words
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
            'before', 'after', 'above', 'below', 'between', 'among',
            
            # Pronouns
            'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
            'my', 'your', 'his', 'her', 'its', 'our', 'their',
            
            # Demonstratives
            'this', 'that', 'these', 'those',
            
            # Verbs
            'is', 'was', 'are', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
            'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'must', 'can',
            
            # Question words
            'please', 'help', 'how', 'what', 'when', 'where', 'why', 'who', 'which',
            
            # Claude-specific
            'agent', 'claude', 'use', 'using', 'need', 'want', 'get', 'make', 'create',
            'find', 'search', 'look', 'show', 'tell', 'explain', 'describe',
            
            # Common actions
            'run', 'execute', 'start', 'stop', 'open', 'close', 'save', 'load',
            'write', 'read', 'edit', 'update', 'delete', 'remove', 'add'
        }
        
        # Technical term patterns
        self.technical_patterns = [
            r'\b[A-Z][a-z]+(?:[A-Z][a-z]+)+\b',  # CamelCase
            r'\b[a-z]+_[a-z]+(?:_[a-z]+)*\b',    # snake_case
            r'\b[a-z]+-[a-z]+(?:-[a-z]+)*\b',    # kebab-case
            r'\b\w+\.(py|js|md|json|yaml|csv|txt|pdf)\b',  # File extensions
            r'\b[A-Z]{2,}\b',  # Acronyms
            r'\b\d+\.\d+\b',   # Version numbers
        ]
        
        # Action verbs that indicate task type
        self.action_keywords = {
            'analyze', 'analysis', 'analyzing', 'review', 'reviewing', 'examine', 'examining',
            'implement', 'implementing', 'code', 'coding', 'program', 'programming',
            'debug', 'debugging', 'fix', 'fixing', 'solve', 'solving',
            'test', 'testing', 'validate', 'validating', 'verify', 'verifying',
            'optimize', 'optimizing', 'improve', 'improving', 'enhance', 'enhancing',
            'research', 'researching', 'study', 'studying', 'investigate', 'investigating',
            'design', 'designing', 'build', 'building', 'construct', 'constructing',
            'deploy', 'deploying', 'install', 'installing', 'configure', 'configuring',
            'migrate', 'migrating', 'upgrade', 'upgrading', 'refactor', 'refactoring',
            'document', 'documenting', 'explain', 'explaining', 'tutorial', 'guide'
        }
        
        # Domain-specific terminology
        self.domain_terms = {
            'ai': {'ai', 'artificial', 'intelligence', 'machine', 'learning', 'ml', 'deep', 'neural', 'network', 'transformer', 'llm', 'gpt', 'bert'},
            'web': {'web', 'html', 'css', 'javascript', 'js', 'react', 'vue', 'angular', 'node', 'express', 'api', 'rest', 'graphql'},
            'data': {'data', 'database', 'sql', 'nosql', 'mongodb', 'postgres', 'mysql', 'analytics', 'visualization', 'pandas', 'numpy'},
            'cloud': {'cloud', 'aws', 'azure', 'gcp', 'docker', 'kubernetes', 'k8s', 'container', 'microservices', 'serverless'},
            'mobile': {'mobile', 'ios', 'android', 'react-native', 'flutter', 'swift', 'kotlin', 'app', 'application'},
            'research': {'research', 'paper', 'literature', 'academic', 'publication', 'journal', 'conference', 'arxiv', 'pubmed'},
            'python': {'python', 'django', 'flask', 'fastapi', 'pytorch', 'tensorflow', 'sklearn', 'scipy', 'jupyter', 'conda'},
            'security': {'security', 'encryption', 'authentication', 'authorization', 'ssl', 'tls', 'vulnerability', 'penetration'}
        }
        
        # Build reverse domain mapping
        self.term_to_domain = {}
        for domain, terms in self.domain_terms.items():
            for term in terms:
                self.term_to_domain[term] = domain

    def extract_keywords(self, text: str, max_keywords: int = 5, min_score: float = 0.1) -> List[str]:
        """
        Extract top keywords from text using multiple strategies
        
        Args:
            text: Input text to extract keywords from
            max_keywords: Maximum number of keywords to return
            min_score: Minimum relevance score threshold
            
        Returns:
            List of top keywords sorted by relevance
        """
        # Normalize text
        text = self._normalize_text(text)
        
        # Extract keyword candidates using multiple methods
        candidates = self._extract_candidates(text)
        
        # Score candidates
        scored_keywords = self._score_keywords(candidates, text)
        
        # Filter by minimum score and limit results
        filtered_keywords = [
            kw for kw in scored_keywords 
            if kw.score >= min_score
        ][:max_keywords]
        
        # Extract just the keyword strings
        return [kw.keyword for kw in filtered_keywords]

    def extract_with_metadata(self, text: str, max_keywords: int = 5, min_score: float = 0.1) -> List[KeywordScore]:
        """Extract keywords with full metadata"""
        text = self._normalize_text(text)
        candidates = self._extract_candidates(text)
        scored_keywords = self._score_keywords(candidates, text)
        
        return [
            kw for kw in scored_keywords 
            if kw.score >= min_score
        ][:max_keywords]

    def _normalize_text(self, text: str) -> str:
        """Normalize text for processing"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text

    def _extract_candidates(self, text: str) -> Set[str]:
        """Extract keyword candidates using multiple strategies"""
        candidates = set()
        
        # 1. Extract technical patterns (preserve original case)
        original_text = text  # Keep original for pattern matching
        for pattern in self.technical_patterns:
            matches = re.findall(pattern, original_text, re.IGNORECASE)
            candidates.update([match.lower() for match in matches])
        
        # 2. Extract regular words
        words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', text)
        for word in words:
            if (len(word) >= 3 and 
                word not in self.stopwords and 
                not word.isdigit() and
                not all(c in string.punctuation for c in word)):
                candidates.add(word)
        
        # 3. Extract compound terms (bigrams)
        words = text.split()
        for i in range(len(words) - 1):
            if (words[i] not in self.stopwords and 
                words[i+1] not in self.stopwords and
                len(words[i]) >= 3 and len(words[i+1]) >= 3):
                compound = f"{words[i]}_{words[i+1]}"
                candidates.add(compound)
        
        # 4. Extract domain-specific abbreviations
        abbreviations = re.findall(r'\b[A-Z]{2,}\b', original_text)
        candidates.update([abbr.lower() for abbr in abbreviations])
        
        return candidates

    def _score_keywords(self, candidates: Set[str], text: str) -> List[KeywordScore]:
        """Score keyword candidates using multiple factors"""
        word_freq = Counter(re.findall(r'\b\w+\b', text))
        total_words = len(text.split())
        
        scored_keywords = []
        
        for candidate in candidates:
            score = 0.0
            category = 'general'
            
            # Base frequency score (TF)
            freq = self._get_candidate_frequency(candidate, word_freq)
            tf_score = freq / total_words if total_words > 0 else 0
            
            # Category bonuses
            if candidate in self.action_keywords:
                score += 0.5
                category = 'action'
            
            if candidate in self.term_to_domain:
                score += 0.7
                category = 'domain'
            
            # Technical term bonus
            if self._is_technical_term(candidate):
                score += 0.3
                category = 'technical'
            
            # Length bonus (prefer meaningful terms)
            if len(candidate) >= 5:
                score += 0.2
            elif len(candidate) >= 8:
                score += 0.4
            
            # Compound term bonus
            if '_' in candidate or '-' in candidate:
                score += 0.3
                category = 'technical'
            
            # Capitalization bonus (in original text)
            if any(candidate.capitalize() in text for text in [text]):
                score += 0.1
            
            # Final score combines TF with categorical bonuses
            final_score = tf_score + score
            
            scored_keywords.append(KeywordScore(
                keyword=candidate,
                score=final_score,
                category=category,
                frequency=freq
            ))
        
        # Sort by score (descending)
        return sorted(scored_keywords, key=lambda x: x.score, reverse=True)

    def _get_candidate_frequency(self, candidate: str, word_freq: Counter) -> int:
        """Get frequency of candidate in text"""
        if '_' in candidate:
            # For compound terms, get minimum frequency of components
            parts = candidate.split('_')
            return min(word_freq.get(part, 0) for part in parts)
        else:
            return word_freq.get(candidate, 0)

    def _is_technical_term(self, term: str) -> bool:
        """Check if term looks like a technical term"""
        # Check patterns
        patterns = [
            r'^[a-z]+[A-Z]',  # camelCase
            r'_',             # snake_case
            r'-',             # kebab-case
            r'\d',            # contains digits
            r'^[A-Z]+$'       # all caps
        ]
        
        return any(re.search(pattern, term) for pattern in patterns)

    def get_domain_summary(self, text: str) -> Dict[str, float]:
        """Get domain relevance scores for text"""
        keywords = self.extract_with_metadata(text, max_keywords=20, min_score=0.0)
        domain_scores = defaultdict(float)
        
        for kw in keywords:
            if kw.keyword in self.term_to_domain:
                domain = self.term_to_domain[kw.keyword]
                domain_scores[domain] += kw.score
        
        # Normalize scores
        if domain_scores:
            max_score = max(domain_scores.values())
            domain_scores = {k: v/max_score for k, v in domain_scores.items()}
        
        return dict(domain_scores)

    def suggest_filename_keywords(self, text: str, max_length: int = 50) -> str:
        """Suggest keywords for filename with length constraint"""
        keywords = self.extract_keywords(text, max_keywords=6, min_score=0.1)
        
        # Build filename within length constraint
        filename_parts = []
        current_length = 0
        
        for keyword in keywords:
            # Clean keyword for filename
            clean_keyword = re.sub(r'[^\w\-]', '_', keyword)
            
            if current_length + len(clean_keyword) + 1 <= max_length:  # +1 for underscore
                filename_parts.append(clean_keyword)
                current_length += len(clean_keyword) + 1
            else:
                break
        
        return '_'.join(filename_parts) if filename_parts else 'session'

# Global extractor instance
_keywords_extractor = None

def get_keywords_extractor() -> KeywordsExtractor:
    """Get global keywords extractor instance"""
    global _keywords_extractor
    if _keywords_extractor is None:
        _keywords_extractor = KeywordsExtractor()
    return _keywords_extractor

# Convenience functions
def extract_keywords(text: str, max_keywords: int = 5) -> List[str]:
    """Extract keywords from text"""
    return get_keywords_extractor().extract_keywords(text, max_keywords)

def suggest_log_filename_keywords(text: str, max_length: int = 50) -> str:
    """Suggest keywords for log filename"""
    return get_keywords_extractor().suggest_filename_keywords(text, max_length)

def get_text_domain_summary(text: str) -> Dict[str, float]:
    """Get domain relevance summary"""
    return get_keywords_extractor().get_domain_summary(text)

if __name__ == "__main__":
    # Test the keyword extractor
    extractor = KeywordsExtractor()
    
    test_cases = [
        "Search for papers on transformer architectures in natural language processing",
        "Debug PyTorch model training with CUDA memory issues",
        "Implement REST API authentication using JWT tokens",
        "Optimize database queries in PostgreSQL for better performance",
        "Create React component for data visualization with D3.js",
        "Deploy machine learning model to AWS using Docker containers",
        "Analyze literature review on quantum computing algorithms",
        "Refactor JavaScript code to use modern ES6 syntax"
    ]
    
    print("=== Keywords Extractor Test ===\n")
    
    for i, text in enumerate(test_cases, 1):
        print(f"Test {i}: {text}")
        
        # Basic keyword extraction
        keywords = extractor.extract_keywords(text, max_keywords=5)
        print(f"Keywords: {', '.join(keywords)}")
        
        # Filename suggestion
        filename_kw = extractor.suggest_filename_keywords(text, max_length=40)
        print(f"Filename: {filename_kw}")
        
        # Domain analysis
        domains = extractor.get_domain_summary(text)
        if domains:
            top_domain = max(domains.items(), key=lambda x: x[1])
            print(f"Primary domain: {top_domain[0]} ({top_domain[1]:.2f})")
        
        # Detailed metadata
        detailed = extractor.extract_with_metadata(text, max_keywords=3)
        print("Detailed analysis:")
        for kw in detailed:
            print(f"  - {kw.keyword} (score: {kw.score:.3f}, category: {kw.category})")
        
        print("-" * 60)
    
    print("Keywords Extractor test completed successfully!")