"""
Semantic search implementation for code snippets.
"""

import os
import logging
from typing import List, Dict, Any, Optional
from pathlib import Path
import re
from dataclasses import dataclass

from ..indexing.code_parser import CodeParser, CodeSnippet
from ..config.settings import settings


@dataclass
class SearchResult:
    """Represents a search result."""
    snippet: CodeSnippet
    score: float
    match_type: str
    highlighted_content: str


class SemanticSearch:
    """Semantic search engine for code snippets."""
    
    def __init__(self):
        """Initialize the semantic search engine."""
        self.logger = logging.getLogger(__name__)
        self.code_parser = CodeParser()
        self.indexed_snippets: List[CodeSnippet] = []
        self._load_sample_data()
    
    def _load_sample_data(self):
        """Load sample code data for demonstration."""
        # Create some sample code files for testing
        self._create_sample_files()
        
        # Index the sample files
        sample_dir = Path("sample_code")
        if sample_dir.exists():
            self._index_directory(sample_dir)
    
    def _create_sample_files(self):
        """Create sample code files for testing."""
        sample_dir = Path("sample_code")
        sample_dir.mkdir(exist_ok=True)
        
        # Python sample
        python_code = '''"""
Sample Python code for testing search functionality.
"""

import os
import json
from typing import List, Dict, Any

def bubble_sort(arr: List[int]) -> List[int]:
    """
    Sort a list using bubble sort algorithm.
    
    Args:
        arr: List of integers to sort
        
    Returns:
        Sorted list
    """
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def binary_search(arr: List[int], target: int) -> int:
    """
    Search for target in sorted array using binary search.
    
    Args:
        arr: Sorted list of integers
        target: Value to search for
        
    Returns:
        Index of target if found, -1 otherwise
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1

class DataProcessor:
    """Process and analyze data."""
    
    def __init__(self, data: List[Dict[str, Any]]):
        self.data = data
        self.processed = False
    
    def process_data(self) -> Dict[str, Any]:
        """Process the input data and return statistics."""
        if not self.data:
            return {"error": "No data to process"}
        
        total_items = len(self.data)
        numeric_fields = []
        
        for item in self.data:
            for value in item.values():
                if isinstance(value, (int, float)):
                    numeric_fields.append(value)
        
        return {
            "total_items": total_items,
            "numeric_count": len(numeric_fields),
            "average": sum(numeric_fields) / len(numeric_fields) if numeric_fields else 0
        }
    
    def filter_by_field(self, field: str, value: Any) -> List[Dict[str, Any]]:
        """Filter data by field and value."""
        return [item for item in self.data if item.get(field) == value]

def main():
    """Main function demonstrating the code."""
    # Test sorting
    numbers = [64, 34, 25, 12, 22, 11, 90]
    sorted_numbers = bubble_sort(numbers.copy())
    print(f"Original: {numbers}")
    print(f"Sorted: {sorted_numbers}")
    
    # Test searching
    target = 25
    index = binary_search(sorted_numbers, target)
    print(f"Found {target} at index: {index}")
    
    # Test data processing
    sample_data = [
        {"id": 1, "name": "Alice", "age": 30, "score": 85.5},
        {"id": 2, "name": "Bob", "age": 25, "score": 92.0},
        {"id": 3, "name": "Charlie", "age": 35, "score": 78.5}
    ]
    
    processor = DataProcessor(sample_data)
    stats = processor.process_data()
    print(f"Data statistics: {stats}")
    
    filtered = processor.filter_by_field("age", 30)
    print(f"People aged 30: {filtered}")

if __name__ == "__main__":
    main()
'''
        
        with open(sample_dir / "algorithms.py", "w") as f:
            f.write(python_code)
        
        # JavaScript sample
        js_code = '''/**
 * Sample JavaScript code for testing search functionality.
 */

// Utility functions for array operations
function quickSort(arr) {
    if (arr.length <= 1) return arr;
    
    const pivot = arr[Math.floor(arr.length / 2)];
    const left = arr.filter(x => x < pivot);
    const middle = arr.filter(x => x === pivot);
    const right = arr.filter(x => x > pivot);
    
    return [...quickSort(left), ...middle, ...quickSort(right)];
}

function linearSearch(arr, target) {
    for (let i = 0; i < arr.length; i++) {
        if (arr[i] === target) {
            return i;
        }
    }
    return -1;
}

// API handling class
class ApiHandler {
    constructor(baseUrl) {
        this.baseUrl = baseUrl;
        this.endpoints = new Map();
    }
    
    async get(endpoint) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`);
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
    
    async post(endpoint, data) {
        try {
            const response = await fetch(`${this.baseUrl}${endpoint}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            return await response.json();
        } catch (error) {
            console.error('API request failed:', error);
            throw error;
        }
    }
}

// Database operations
class DatabaseManager {
    constructor(connectionString) {
        this.connectionString = connectionString;
        this.connected = false;
    }
    
    async connect() {
        // Simulate database connection
        this.connected = true;
        console.log('Connected to database');
    }
    
    async query(sql) {
        if (!this.connected) {
            throw new Error('Not connected to database');
        }
        
        // Simulate query execution
        console.log(`Executing query: ${sql}`);
        return { rows: [], count: 0 };
    }
    
    async close() {
        this.connected = false;
        console.log('Database connection closed');
    }
}

// Main execution
async function main() {
    // Test sorting
    const numbers = [64, 34, 25, 12, 22, 11, 90];
    const sorted = quickSort([...numbers]);
    console.log('Original:', numbers);
    console.log('Sorted:', sorted);
    
    // Test searching
    const target = 25;
    const index = linearSearch(sorted, target);
    console.log(`Found ${target} at index: ${index}`);
    
    // Test API handling
    const api = new ApiHandler('https://api.example.com');
    try {
        const data = await api.get('/users');
        console.log('API data:', data);
    } catch (error) {
        console.log('API error handled');
    }
    
    // Test database operations
    const db = new DatabaseManager('postgresql://localhost:5432/mydb');
    await db.connect();
    const result = await db.query('SELECT * FROM users');
    console.log('Database result:', result);
    await db.close();
}

// Export for module usage
module.exports = {
    quickSort,
    linearSearch,
    ApiHandler,
    DatabaseManager
};
'''
        
        with open(sample_dir / "utils.js", "w") as f:
            f.write(js_code)
    
    def _index_directory(self, directory: Path):
        """Index all code files in a directory."""
        self.logger.info(f"Indexing directory: {directory}")
        
        for file_path in directory.rglob("*"):
            if file_path.is_file():
                extension = file_path.suffix.lower()
                if extension in self.code_parser.supported_extensions:
                    try:
                        snippets = self.code_parser.parse_file(str(file_path))
                        self.indexed_snippets.extend(snippets)
                        self.logger.debug(f"Indexed {len(snippets)} snippets from {file_path}")
                    except Exception as e:
                        self.logger.error(f"Error indexing {file_path}: {e}")
        
        self.logger.info(f"Total indexed snippets: {len(self.indexed_snippets)}")
    
    def search(self, query: str, max_results: int = 20, similarity_threshold: float = 0.1) -> List[SearchResult]:
        """Search for code snippets matching the query."""
        self.logger.info(f"Searching for: {query}")
        
        if not self.indexed_snippets:
            self.logger.warning("No indexed snippets available")
            return []
        
        results = []
        query_lower = query.lower()
        
        for snippet in self.indexed_snippets:
            score = self._calculate_relevance_score(snippet, query_lower)
            
            if score >= similarity_threshold:
                match_type = self._determine_match_type(snippet, query_lower)
                highlighted_content = self._highlight_matches(snippet.content, query_lower)
                
                result = SearchResult(
                    snippet=snippet,
                    score=score,
                    match_type=match_type,
                    highlighted_content=highlighted_content
                )
                results.append(result)
        
        # Sort by relevance score (descending)
        results.sort(key=lambda x: x.score, reverse=True)
        
        # Limit results
        results = results[:max_results]
        
        self.logger.info(f"Found {len(results)} results")
        return results
    
    def _calculate_relevance_score(self, snippet: CodeSnippet, query: str) -> float:
        """Calculate relevance score between snippet and query."""
        score = 0.0
        
        # Content match
        content_lower = snippet.content.lower()
        if query in content_lower:
            score += 0.8
        
        # Name match
        if query in snippet.name.lower():
            score += 0.9
        
        # Description match
        if query in snippet.description.lower():
            score += 0.7
        
        # Tags match
        for tag in snippet.tags:
            if query in tag.lower():
                score += 0.6
        
        # Language match
        if query in snippet.language.lower():
            score += 0.5
        
        # Type match
        if query in snippet.type.lower():
            score += 0.4
        
        # File path match
        if query in snippet.file_path.lower():
            score += 0.3
        
        # Keyword matching
        keywords = query.split()
        for keyword in keywords:
            if keyword in content_lower:
                score += 0.1
            if keyword in snippet.name.lower():
                score += 0.2
            if keyword in snippet.description.lower():
                score += 0.15
        
        # Quality bonus
        score += snippet.quality_score * 0.01
        
        return min(1.0, score)
    
    def _determine_match_type(self, snippet: CodeSnippet, query: str) -> str:
        """Determine the type of match."""
        if query in snippet.name.lower():
            return "exact_name"
        elif query in snippet.content.lower():
            return "content_match"
        elif query in snippet.description.lower():
            return "description_match"
        elif any(query in tag.lower() for tag in snippet.tags):
            return "tag_match"
        else:
            return "keyword_match"
    
    def _highlight_matches(self, content: str, query: str) -> str:
        """Highlight query matches in content."""
        if not query:
            return content
        
        # Simple highlighting - replace query with highlighted version
        highlighted = content
        query_parts = query.split()
        
        for part in query_parts:
            if len(part) > 2:  # Only highlight meaningful parts
                pattern = re.compile(re.escape(part), re.IGNORECASE)
                highlighted = pattern.sub(f'<mark>{part}</mark>', highlighted)
        
        return highlighted
    
    def find_similar_snippets(self, snippet_id: str, top_k: int = 10, threshold: float = 0.1) -> List[SearchResult]:
        """Find similar snippets to a given snippet."""
        # Find the target snippet
        target_snippet = None
        for snippet in self.indexed_snippets:
            if snippet.id == snippet_id:
                target_snippet = snippet
                break
        
        if not target_snippet:
            return []
        
        # Calculate similarity with all other snippets
        results = []
        for snippet in self.indexed_snippets:
            if snippet.id != snippet_id:
                similarity = self._calculate_snippet_similarity(target_snippet, snippet)
                if similarity >= threshold:
                    result = SearchResult(
                        snippet=snippet,
                        score=similarity,
                        match_type="similarity",
                        highlighted_content=snippet.content
                    )
                    results.append(result)
        
        # Sort by similarity and return top k
        results.sort(key=lambda x: x.score, reverse=True)
        return results[:top_k]
    
    def _calculate_snippet_similarity(self, snippet1: CodeSnippet, snippet2: CodeSnippet) -> float:
        """Calculate similarity between two snippets."""
        similarity = 0.0
        
        # Language similarity
        if snippet1.language == snippet2.language:
            similarity += 0.2
        
        # Type similarity
        if snippet1.type == snippet2.type:
            similarity += 0.2
        
        # Tag similarity
        common_tags = set(snippet1.tags) & set(snippet2.tags)
        if common_tags:
            similarity += 0.3 * (len(common_tags) / max(len(snippet1.tags), len(snippet2.tags)))
        
        # Content similarity (simple keyword overlap)
        content1_words = set(snippet1.content.lower().split())
        content2_words = set(snippet2.content.lower().split())
        
        if content1_words and content2_words:
            word_overlap = len(content1_words & content2_words)
            total_words = len(content1_words | content2_words)
            similarity += 0.3 * (word_overlap / total_words)
        
        return similarity
    
    def get_statistics(self) -> Dict[str, Any]:
        """Get search statistics."""
        if not self.indexed_snippets:
            return {
                "total_snippets": 0,
                "languages": {},
                "types": {},
                "average_quality": 0.0
            }
        
        languages = {}
        types = {}
        total_quality = 0.0
        
        for snippet in self.indexed_snippets:
            # Count languages
            languages[snippet.language] = languages.get(snippet.language, 0) + 1
            
            # Count types
            types[snippet.type] = types.get(snippet.type, 0) + 1
            
            # Sum quality scores
            total_quality += snippet.quality_score
        
        return {
            "total_snippets": len(self.indexed_snippets),
            "languages": languages,
            "types": types,
            "average_quality": total_quality / len(self.indexed_snippets) if self.indexed_snippets else 0.0
        } 