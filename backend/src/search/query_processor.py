"""
Query processor for handling search queries and intent classification.
"""

import re
from typing import List, Dict, Any, Optional
import logging
from transformers import pipeline

from ..models.search_result import SearchQuery, SearchType, SearchIntent
from ..config.settings import settings


class QueryProcessor:
    """Processor for handling and analyzing search queries."""
    
    def __init__(self):
        """Initialize the query processor."""
        self.logger = logging.getLogger(__name__)
        self.intent_classifier = None
        self._load_models()
    
    def _load_models(self):
        """Load NLP models for query processing."""
        try:
            # Load intent classification model
            self.intent_classifier = pipeline(
                "text-classification",
                model="facebook/bart-large-mnli",
                device=-1  # Use CPU
            )
        except Exception as e:
            self.logger.warning(f"Could not load intent classifier: {e}")
    
    def process_query(self, query: SearchQuery) -> SearchQuery:
        """Process and enhance a search query."""
        try:
            # Extract keywords
            query.query_keywords = self._extract_keywords(query.query)
            
            # Detect intent
            query.intent = self._detect_intent(query.query)
            
            # Expand query
            if query.expand_query:
                expanded_terms = self._expand_query(query.query)
                query.query = f"{query.query} {' '.join(expanded_terms)}"
            
            # Extract topics
            query.query_topics = self._extract_topics(query.query)
            
            # Normalize query
            query.query = self._normalize_query(query.query)
            
            return query
            
        except Exception as e:
            self.logger.error(f"Error processing query: {e}")
            return query
    
    def _extract_keywords(self, query: str) -> List[str]:
        """Extract keywords from query."""
        keywords = []
        
        # Remove common stop words
        stop_words = {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
            'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'can', 'this', 'that', 'these', 'those'
        }
        
        # Extract words
        words = re.findall(r'\b\w+\b', query.lower())
        
        # Filter out stop words and short words
        keywords = [word for word in words if word not in stop_words and len(word) > 2]
        
        # Add programming-specific keywords
        programming_keywords = self._get_programming_keywords()
        keywords.extend([word for word in words if word in programming_keywords])
        
        return list(set(keywords))
    
    def _get_programming_keywords(self) -> set:
        """Get programming-specific keywords."""
        keywords = set()
        
        # Add common programming terms for all supported languages
        common_terms = {
            'function', 'class', 'method', 'variable', 'constant', 'import',
            'export', 'module', 'package', 'library', 'framework', 'api',
            'algorithm', 'data structure', 'sorting', 'searching', 'recursion',
            'iteration', 'loop', 'condition', 'exception', 'error', 'debug',
            'test', 'unit', 'integration', 'database', 'query', 'sql',
            'http', 'rest', 'graphql', 'authentication', 'authorization',
            'encryption', 'security', 'performance', 'optimization', 'cache',
            'memory', 'cpu', 'thread', 'process', 'async', 'await', 'promise',
            'callback', 'event', 'listener', 'middleware', 'router', 'controller',
            'model', 'view', 'template', 'component', 'service', 'repository'
        }
        keywords.update(common_terms)
        
        # Add language-specific terms for supported languages
        for language in settings.SUPPORTED_LANGUAGES:
            if language == 'python':
                keywords.update({'def', 'class', 'import', 'from', 'as', 'if', 'else', 'elif', 'for', 'while', 'try', 'except', 'finally', 'with', 'lambda', 'yield', 'async', 'await'})
            elif language == 'javascript':
                keywords.update({'function', 'const', 'let', 'var', 'if', 'else', 'for', 'while', 'try', 'catch', 'finally', 'async', 'await', 'export', 'import', 'class', 'extends', 'super'})
            elif language == 'typescript':
                keywords.update({'interface', 'type', 'enum', 'namespace', 'module', 'declare', 'function', 'const', 'let', 'var', 'if', 'else', 'for', 'while', 'try', 'catch', 'finally', 'async', 'await', 'export', 'import', 'class', 'extends', 'super'})
            elif language == 'java':
                keywords.update({'public', 'private', 'protected', 'static', 'final', 'class', 'interface', 'extends', 'implements', 'import', 'package', 'try', 'catch', 'finally', 'throw', 'throws', 'new', 'this', 'super'})
            elif language == 'cpp':
                keywords.update({'class', 'struct', 'enum', 'namespace', 'template', 'typename', 'const', 'static', 'virtual', 'public', 'private', 'protected', 'friend', 'inline', 'explicit', 'operator', 'new', 'delete', 'this', 'super'})
        
        return keywords
    
    def _detect_intent(self, query: str) -> Optional[SearchIntent]:
        """Detect search intent from query."""
        if not self.intent_classifier:
            return self._rule_based_intent_detection(query)
        
        try:
            # Define intent labels
            intent_labels = {
                'find_function': 'function search',
                'find_class': 'class search',
                'find_algorithm': 'algorithm search',
                'find_example': 'example search',
                'find_pattern': 'pattern search',
                'find_api': 'api search',
                'debug_error': 'error debugging',
                'learn_concept': 'learning concept',
                'compare_implementations': 'implementation comparison'
            }
            
            # Classify intent
            result = self.intent_classifier(query, candidate_labels=list(intent_labels.values()))
            
            # Map back to intent enum
            for intent, label in intent_labels.items():
                if label == result['labels'][0]:
                    return SearchIntent(intent)
            
            return None
            
        except Exception as e:
            self.logger.error(f"Error in intent detection: {e}")
            return self._rule_based_intent_detection(query)
    
    def _rule_based_intent_detection(self, query: str) -> Optional[SearchIntent]:
        """Rule-based intent detection fallback."""
        query_lower = query.lower()
        
        # Function search patterns
        if any(term in query_lower for term in ['function', 'def ', 'func ', 'method']):
            return SearchIntent.FIND_FUNCTION
        
        # Class search patterns
        if any(term in query_lower for term in ['class', 'struct', 'interface']):
            return SearchIntent.FIND_CLASS
        
        # Algorithm search patterns
        if any(term in query_lower for term in ['algorithm', 'sort', 'search', 'binary', 'quick', 'merge']):
            return SearchIntent.FIND_ALGORITHM
        
        # Example search patterns
        if any(term in query_lower for term in ['example', 'sample', 'how to', 'tutorial']):
            return SearchIntent.FIND_EXAMPLE
        
        # API search patterns
        if any(term in query_lower for term in ['api', 'endpoint', 'rest', 'graphql']):
            return SearchIntent.FIND_API
        
        # Error debugging patterns
        if any(term in query_lower for term in ['error', 'exception', 'bug', 'fix', 'debug']):
            return SearchIntent.DEBUG_ERROR
        
        # Learning patterns
        if any(term in query_lower for term in ['learn', 'understand', 'explain', 'what is']):
            return SearchIntent.LEARN_CONCEPT
        
        # Comparison patterns
        if any(term in query_lower for term in ['compare', 'difference', 'vs', 'versus']):
            return SearchIntent.COMPARE_IMPLEMENTATIONS
        
        return None
    
    def _expand_query(self, query: str) -> List[str]:
        """Expand query with synonyms and related terms."""
        synonyms = {
            'sort': ['sorting', 'order', 'arrange'],
            'search': ['finding', 'lookup', 'query'],
            'function': ['method', 'procedure', 'routine'],
            'class': ['type', 'object', 'struct'],
            'error': ['exception', 'bug', 'issue', 'problem'],
            'api': ['endpoint', 'service', 'interface'],
            'database': ['db', 'storage', 'repository'],
            'authentication': ['auth', 'login', 'security'],
            'performance': ['speed', 'efficiency', 'optimization'],
            'test': ['testing', 'unit test', 'integration test'],
            'algorithm': ['algo', 'procedure', 'method'],
            'data structure': ['ds', 'container', 'collection'],
            'recursion': ['recursive', 'recursively'],
            'iteration': ['loop', 'iterate', 'for loop'],
            'async': ['asynchronous', 'non-blocking'],
            'cache': ['caching', 'memoization'],
            'middleware': ['interceptor', 'filter'],
            'template': ['template', 'view', 'component']
        }
        
        expanded_terms = []
        query_lower = query.lower()
        
        for term, synonyms_list in synonyms.items():
            if term in query_lower:
                expanded_terms.extend(synonyms_list)
        
        return expanded_terms[:5]  # Limit to 5 additional terms
    
    def _extract_topics(self, query: str) -> List[str]:
        """Extract topics from query."""
        topics = []
        
        # Programming language detection
        languages = list(SUPPORTED_LANGUAGES.keys())
        for lang in languages:
            if lang in query.lower():
                topics.append(f"language:{lang}")
        
        # Framework detection
        frameworks = {
            'react': 'frontend',
            'vue': 'frontend',
            'angular': 'frontend',
            'django': 'backend',
            'flask': 'backend',
            'express': 'backend',
            'spring': 'backend',
            'tensorflow': 'machine_learning',
            'pytorch': 'machine_learning',
            'scikit': 'machine_learning',
            'pandas': 'data_analysis',
            'numpy': 'data_analysis',
            'matplotlib': 'data_visualization'
        }
        
        for framework, category in frameworks.items():
            if framework in query.lower():
                topics.append(f"framework:{framework}")
                topics.append(f"category:{category}")
        
        # Domain detection
        domains = {
            'web': ['web', 'http', 'html', 'css', 'javascript'],
            'mobile': ['mobile', 'ios', 'android', 'react native'],
            'data': ['data', 'database', 'sql', 'nosql', 'analytics'],
            'ai': ['ai', 'machine learning', 'ml', 'neural', 'deep learning'],
            'security': ['security', 'cryptography', 'encryption', 'authentication'],
            'devops': ['devops', 'docker', 'kubernetes', 'ci/cd', 'deployment']
        }
        
        for domain, keywords in domains.items():
            if any(keyword in query.lower() for keyword in keywords):
                topics.append(f"domain:{domain}")
        
        return topics
    
    def _normalize_query(self, query: str) -> str:
        """Normalize query text."""
        # Remove extra whitespace
        query = re.sub(r'\s+', ' ', query.strip())
        
        # Convert to lowercase
        query = query.lower()
        
        # Remove special characters but keep programming syntax
        query = re.sub(r'[^\w\s\-_\.]', ' ', query)
        
        # Remove extra whitespace again
        query = re.sub(r'\s+', ' ', query.strip())
        
        return query
    
    def get_suggestions(self, partial_query: str, limit: int = 10) -> List[str]:
        """Get search suggestions based on partial query."""
        suggestions = []
        
        # Common programming patterns
        common_patterns = [
            "sorting algorithm",
            "binary search",
            "quick sort",
            "merge sort",
            "bubble sort",
            "function definition",
            "class constructor",
            "error handling",
            "try catch",
            "async await",
            "promise handling",
            "database query",
            "api endpoint",
            "authentication",
            "unit test",
            "integration test",
            "data structure",
            "linked list",
            "binary tree",
            "hash table",
            "stack implementation",
            "queue implementation",
            "recursive function",
            "iterative solution",
            "design pattern",
            "singleton pattern",
            "factory pattern",
            "observer pattern",
            "middleware function",
            "route handler"
        ]
        
        # Filter suggestions based on partial query
        partial_lower = partial_query.lower()
        for pattern in common_patterns:
            if partial_lower in pattern.lower():
                suggestions.append(pattern)
        
        # Add language-specific suggestions
        for lang, config in SUPPORTED_LANGUAGES.items():
            if lang in partial_lower:
                for keyword in config.get('keywords', [])[:5]:
                    suggestions.append(f"{keyword} in {lang}")
        
        return suggestions[:limit]
    
    def analyze_query_complexity(self, query: str) -> Dict[str, Any]:
        """Analyze query complexity and characteristics."""
        analysis = {
            'length': len(query),
            'word_count': len(query.split()),
            'keyword_count': len(self._extract_keywords(query)),
            'has_code_syntax': bool(re.search(r'[{}()\[\]]', query)),
            'has_quotes': '"' in query or "'" in query,
            'has_operators': bool(re.search(r'[+\-*/=<>!&|]', query)),
            'intent': self._detect_intent(query),
            'topics': self._extract_topics(query),
            'languages_mentioned': [],
            'complexity_score': 0.0
        }
        
        # Detect mentioned languages
        for lang in SUPPORTED_LANGUAGES.keys():
            if lang in query.lower():
                analysis['languages_mentioned'].append(lang)
        
        # Calculate complexity score
        score = 0.0
        score += min(analysis['word_count'] / 10.0, 1.0) * 0.3
        score += min(analysis['keyword_count'] / 5.0, 1.0) * 0.3
        score += 0.2 if analysis['has_code_syntax'] else 0.0
        score += 0.1 if analysis['has_operators'] else 0.0
        score += 0.1 if analysis['intent'] else 0.0
        
        analysis['complexity_score'] = min(score, 1.0)
        
        return analysis 