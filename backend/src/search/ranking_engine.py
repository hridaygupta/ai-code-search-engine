"""
Ranking engine for scoring and ranking search results.
"""

from typing import List, Dict, Any, Optional
import math
import logging
from datetime import datetime, timedelta

from ..models.search_result import SearchResult, SearchQuery
from ..config.settings import settings


class RankingEngine:
    """Engine for ranking search results based on multiple factors."""
    
    def __init__(self):
        """Initialize the ranking engine."""
        self.logger = logging.getLogger(__name__)
        self.weights = settings.SEARCH_WEIGHTS
    
    def rank_results(self, results: List[SearchResult], query: SearchQuery) -> List[SearchResult]:
        """Rank search results based on multiple factors."""
        try:
            # Calculate individual scores
            for result in results:
                result.relevance_score = self._calculate_relevance_score(result, query)
            
            # Sort by relevance score
            results.sort(key=lambda x: x.relevance_score, reverse=True)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error ranking results: {e}")
            return results
    
    def _calculate_relevance_score(self, result: SearchResult, query: SearchQuery) -> float:
        """Calculate overall relevance score for a result."""
        try:
            # Get individual component scores
            semantic_score = result.similarity_score
            keyword_score = self._calculate_keyword_score(result, query)
            quality_score = self._calculate_quality_score(result)
            popularity_score = self._calculate_popularity_score(result)
            recency_score = self._calculate_recency_score(result)
            documentation_score = self._calculate_documentation_score(result)
            
            # Apply weights and combine scores
            final_score = (
                semantic_score * self.weights['semantic_similarity'] +
                keyword_score * self.weights['keyword_match'] +
                quality_score * self.weights['code_quality'] +
                popularity_score * self.weights['popularity'] +
                recency_score * self.weights['recency'] +
                documentation_score * self.weights['documentation']
            )
            
            # Apply boosts
            final_score *= result.quality_boost
            final_score *= result.popularity_boost
            final_score *= result.recency_boost
            final_score *= result.documentation_boost
            
            return min(final_score, 1.0)  # Cap at 1.0
            
        except Exception as e:
            self.logger.error(f"Error calculating relevance score: {e}")
            return result.similarity_score
    
    def _calculate_keyword_score(self, result: SearchResult, query: SearchQuery) -> float:
        """Calculate keyword matching score."""
        try:
            if not query.query_keywords:
                return 0.0
            
            snippet_keywords = set(result.snippet.keywords)
            query_keywords = set(query.query_keywords)
            
            if not query_keywords:
                return 0.0
            
            # Calculate keyword overlap
            overlap = len(snippet_keywords.intersection(query_keywords))
            total_query_keywords = len(query_keywords)
            
            # Also check content for keyword matches
            content_lower = result.snippet.content.lower()
            content_matches = sum(1 for keyword in query_keywords if keyword.lower() in content_lower)
            
            # Combine overlap and content matches
            keyword_score = (overlap + content_matches * 0.5) / (total_query_keywords * 1.5)
            
            return min(keyword_score, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating keyword score: {e}")
            return 0.0
    
    def _calculate_quality_score(self, result: SearchResult) -> float:
        """Calculate code quality score."""
        try:
            # Base quality score from snippet
            base_quality = result.snippet.quality_score
            
            # Complexity penalty
            complexity_penalty = 0.0
            if result.snippet.complexity_score > 15:
                complexity_penalty = min((result.snippet.complexity_score - 15) / 20, 0.3)
            
            # Readability bonus
            readability_bonus = result.snippet.readability_score * 0.2
            
            # Documentation bonus
            doc_bonus = 0.0
            if result.snippet.docstring:
                doc_bonus = 0.1
            
            # Calculate final quality score
            quality_score = base_quality - complexity_penalty + readability_bonus + doc_bonus
            
            return max(min(quality_score, 1.0), 0.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating quality score: {e}")
            return 0.5
    
    def _calculate_popularity_score(self, result: SearchResult) -> float:
        """Calculate popularity score."""
        try:
            # Repository popularity (stars, forks)
            repo_popularity = 0.0
            if hasattr(result.snippet, 'repository') and result.snippet.repository:
                repo = result.snippet.repository
                if repo.stars > 0:
                    repo_popularity = min(math.log10(repo.stars + 1) / 5, 1.0)
            
            # Snippet usage
            usage_score = min(result.snippet.usage_count / 100, 1.0)
            
            # View count
            view_score = min(result.view_count / 50, 1.0)
            
            # Combine popularity factors
            popularity_score = (repo_popularity * 0.5 + usage_score * 0.3 + view_score * 0.2)
            
            return popularity_score
            
        except Exception as e:
            self.logger.error(f"Error calculating popularity score: {e}")
            return 0.0
    
    def _calculate_recency_score(self, result: SearchResult) -> float:
        """Calculate recency score."""
        try:
            # Get snippet creation date
            created_at = result.snippet.created_at
            if not created_at:
                return 0.5
            
            # Calculate days since creation
            days_old = (datetime.utcnow() - created_at).days
            
            # Recency decay function
            if days_old <= 30:
                recency_score = 1.0
            elif days_old <= 90:
                recency_score = 0.8
            elif days_old <= 365:
                recency_score = 0.6
            elif days_old <= 730:
                recency_score = 0.4
            else:
                recency_score = 0.2
            
            return recency_score
            
        except Exception as e:
            self.logger.error(f"Error calculating recency score: {e}")
            return 0.5
    
    def _calculate_documentation_score(self, result: SearchResult) -> float:
        """Calculate documentation score."""
        try:
            doc_score = 0.0
            
            # Docstring presence
            if result.snippet.docstring:
                doc_score += 0.4
            
            # Function/class name clarity
            if result.snippet.name and len(result.snippet.name) > 2:
                doc_score += 0.2
            
            # Parameter documentation
            if result.snippet.parameters and len(result.snippet.parameters) > 0:
                doc_score += 0.2
            
            # Return type documentation
            if result.snippet.return_type:
                doc_score += 0.1
            
            # Comments in code
            content = result.snippet.content
            comment_lines = sum(1 for line in content.split('\n') if line.strip().startswith(('#', '//', '/*', '*/')))
            total_lines = len(content.split('\n'))
            if total_lines > 0:
                comment_ratio = comment_lines / total_lines
                doc_score += min(comment_ratio * 0.3, 0.1)
            
            return min(doc_score, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error calculating documentation score: {e}")
            return 0.0
    
    def apply_boosts(self, results: List[SearchResult], query: SearchQuery) -> List[SearchResult]:
        """Apply query-specific boosts to results."""
        try:
            for result in results:
                # Language boost
                if query.languages and result.snippet.language in query.languages:
                    result.quality_boost *= 1.2
                
                # Repository boost
                if query.repositories and result.snippet.repository_id in query.repositories:
                    result.quality_boost *= 1.1
                
                # Intent-based boost
                if query.intent:
                    intent_boost = self._get_intent_boost(result, query.intent)
                    result.quality_boost *= intent_boost
                
                # Complexity boost
                if query.complexity_levels:
                    if result.snippet.complexity_level.value in query.complexity_levels:
                        result.quality_boost *= 1.1
                
                # Cap boosts to reasonable limits
                result.quality_boost = min(result.quality_boost, 2.0)
                result.popularity_boost = min(result.popularity_boost, 1.5)
                result.recency_boost = min(result.recency_boost, 1.3)
                result.documentation_boost = min(result.documentation_boost, 1.2)
            
            return results
            
        except Exception as e:
            self.logger.error(f"Error applying boosts: {e}")
            return results
    
    def _get_intent_boost(self, result: SearchResult, intent) -> float:
        """Get boost based on search intent."""
        try:
            intent_boosts = {
                'find_function': 1.2 if result.snippet.code_type.value in ['function', 'method'] else 0.8,
                'find_class': 1.2 if result.snippet.code_type.value == 'class' else 0.8,
                'find_algorithm': 1.3 if 'algorithm' in result.snippet.keywords else 1.0,
                'find_example': 1.1 if result.snippet.docstring else 1.0,
                'find_pattern': 1.2 if len(result.snippet.keywords) > 3 else 1.0,
                'find_api': 1.2 if 'api' in result.snippet.keywords else 1.0,
                'debug_error': 1.1 if 'error' in result.snippet.keywords or 'exception' in result.snippet.keywords else 1.0,
                'learn_concept': 1.2 if result.snippet.docstring else 1.0,
                'compare_implementations': 1.1 if result.snippet.complexity_score > 5 else 1.0
            }
            
            return intent_boosts.get(intent.value, 1.0)
            
        except Exception as e:
            self.logger.error(f"Error getting intent boost: {e}")
            return 1.0
    
    def filter_results(self, results: List[SearchResult], query: SearchQuery) -> List[SearchResult]:
        """Filter results based on query criteria."""
        try:
            filtered_results = []
            
            for result in results:
                # Apply similarity threshold
                if result.similarity_score < query.similarity_threshold:
                    continue
                
                # Apply language filter
                if query.languages and result.snippet.language not in query.languages:
                    continue
                
                # Apply repository filter
                if query.repositories and result.snippet.repository_id not in query.repositories:
                    continue
                
                # Apply complexity filter
                if query.complexity_levels and result.snippet.complexity_level.value not in query.complexity_levels:
                    continue
                
                # Apply date range filter
                if query.date_range:
                    created_at = result.snippet.created_at
                    if created_at:
                        start_date = query.date_range.get('start')
                        end_date = query.date_range.get('end')
                        
                        if start_date and created_at < start_date:
                            continue
                        if end_date and created_at > end_date:
                            continue
                
                filtered_results.append(result)
            
            return filtered_results
            
        except Exception as e:
            self.logger.error(f"Error filtering results: {e}")
            return results
    
    def get_ranking_explanation(self, result: SearchResult, query: SearchQuery) -> Dict[str, Any]:
        """Get explanation of ranking factors for a result."""
        try:
            explanation = {
                'similarity_score': result.similarity_score,
                'keyword_score': self._calculate_keyword_score(result, query),
                'quality_score': self._calculate_quality_score(result),
                'popularity_score': self._calculate_popularity_score(result),
                'recency_score': self._calculate_recency_score(result),
                'documentation_score': self._calculate_documentation_score(result),
                'final_score': result.relevance_score,
                'boosts': {
                    'quality_boost': result.quality_boost,
                    'popularity_boost': result.popularity_boost,
                    'recency_boost': result.recency_boost,
                    'documentation_boost': result.documentation_boost
                },
                'factors': {
                    'has_documentation': bool(result.snippet.docstring),
                    'complexity_level': result.snippet.complexity_level.value,
                    'code_type': result.snippet.code_type.value,
                    'language': result.snippet.language,
                    'usage_count': result.snippet.usage_count,
                    'view_count': result.view_count
                }
            }
            
            return explanation
            
        except Exception as e:
            self.logger.error(f"Error getting ranking explanation: {e}")
            return {} 