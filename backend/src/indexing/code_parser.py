"""
Code parser for extracting code snippets from files.
"""

import os
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional
import ast
import re
from dataclasses import dataclass

from ..config.settings import settings


@dataclass
class CodeSnippet:
    """Represents a code snippet."""
    id: str
    content: str
    language: str
    file_path: str
    line_start: int
    line_end: int
    name: str
    type: str  # function, class, method, etc.
    complexity: str
    quality_score: float
    tags: List[str]
    description: str


class CodeParser:
    """Parser for extracting code snippets from files."""
    
    def __init__(self):
        """Initialize the code parser."""
        self.logger = logging.getLogger(__name__)
        self.supported_extensions = {
            '.py': 'python',
            '.js': 'javascript',
            '.ts': 'typescript',
            '.java': 'java',
            '.cpp': 'cpp',
            '.c': 'c',
            '.go': 'go',
            '.rs': 'rust',
            '.php': 'php',
            '.rb': 'ruby',
            '.swift': 'swift',
            '.kt': 'kotlin',
            '.scala': 'scala',
            '.r': 'r',
            '.m': 'matlab'
        }
    
    def parse_file(self, file_path: str) -> List[CodeSnippet]:
        """Parse a single file and extract code snippets."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                self.logger.warning(f"File not found: {file_path}")
                return []
            
            extension = file_path.suffix.lower()
            if extension not in self.supported_extensions:
                self.logger.debug(f"Unsupported file type: {extension}")
                return []
            
            language = self.supported_extensions[extension]
            
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if language == 'python':
                return self._parse_python_file(content, str(file_path))
            elif language in ['javascript', 'typescript']:
                return self._parse_js_file(content, str(file_path), language)
            else:
                return self._parse_generic_file(content, str(file_path), language)
                
        except Exception as e:
            self.logger.error(f"Error parsing file {file_path}: {e}")
            return []
    
    def _parse_python_file(self, content: str, file_path: str) -> List[CodeSnippet]:
        """Parse Python file using AST."""
        snippets = []
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    snippet = self._extract_python_node(node, content, file_path)
                    if snippet:
                        snippets.append(snippet)
            
            # Also extract module-level code blocks
            module_snippets = self._extract_module_snippets(tree, content, file_path)
            snippets.extend(module_snippets)
            
        except SyntaxError as e:
            self.logger.warning(f"Syntax error in {file_path}: {e}")
        
        return snippets
    
    def _extract_python_node(self, node: ast.AST, content: str, file_path: str) -> Optional[CodeSnippet]:
        """Extract a Python AST node as a code snippet."""
        try:
            lines = content.split('\n')
            start_line = node.lineno
            end_line = node.end_lineno if hasattr(node, 'end_lineno') else start_line
            
            # Get the actual code content
            snippet_content = '\n'.join(lines[start_line-1:end_line])
            
            # Determine node type and name
            if isinstance(node, ast.FunctionDef):
                node_type = 'function'
                name = node.name
            elif isinstance(node, ast.AsyncFunctionDef):
                node_type = 'async_function'
                name = node.name
            elif isinstance(node, ast.ClassDef):
                node_type = 'class'
                name = node.name
            else:
                return None
            
            # Calculate complexity
            complexity = self._calculate_complexity(node)
            
            # Calculate quality score
            quality_score = self._calculate_quality_score(snippet_content, complexity)
            
            # Extract tags
            tags = self._extract_tags(snippet_content, 'python')
            
            # Generate description
            description = self._generate_description(node, name, node_type)
            
            snippet_id = f"{file_path}:{start_line}:{end_line}"
            
            return CodeSnippet(
                id=snippet_id,
                content=snippet_content,
                language='python',
                file_path=file_path,
                line_start=start_line,
                line_end=end_line,
                name=name,
                type=node_type,
                complexity=complexity,
                quality_score=quality_score,
                tags=tags,
                description=description
            )
            
        except Exception as e:
            self.logger.error(f"Error extracting Python node: {e}")
            return None
    
    def _extract_module_snippets(self, tree: ast.AST, content: str, file_path: str) -> List[CodeSnippet]:
        """Extract module-level code blocks."""
        snippets = []
        lines = content.split('\n')
        
        # Find module-level code blocks (not inside functions/classes)
        module_lines = []
        current_block_start = 1
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('#'):
                module_lines.append((i, line))
        
        # Group consecutive lines into blocks
        if module_lines:
            block_start = module_lines[0][0]
            block_end = module_lines[0][0]
            
            for i in range(1, len(module_lines)):
                if module_lines[i][0] == module_lines[i-1][0] + 1:
                    block_end = module_lines[i][0]
                else:
                    # End of block
                    if block_end - block_start > 0:
                        snippet = self._create_module_snippet(
                            content, file_path, block_start, block_end
                        )
                        if snippet:
                            snippets.append(snippet)
                    block_start = module_lines[i][0]
                    block_end = module_lines[i][0]
            
            # Add last block
            if block_end - block_start > 0:
                snippet = self._create_module_snippet(
                    content, file_path, block_start, block_end
                )
                if snippet:
                    snippets.append(snippet)
        
        return snippets
    
    def _create_module_snippet(self, content: str, file_path: str, start_line: int, end_line: int) -> Optional[CodeSnippet]:
        """Create a snippet from module-level code."""
        lines = content.split('\n')
        snippet_content = '\n'.join(lines[start_line-1:end_line])
        
        if len(snippet_content.strip()) < 10:  # Skip very short snippets
            return None
        
        complexity = self._calculate_simple_complexity(snippet_content)
        quality_score = self._calculate_quality_score(snippet_content, complexity)
        tags = self._extract_tags(snippet_content, 'python')
        
        snippet_id = f"{file_path}:{start_line}:{end_line}"
        
        return CodeSnippet(
            id=snippet_id,
            content=snippet_content,
            language='python',
            file_path=file_path,
            line_start=start_line,
            line_end=end_line,
            name=f"module_block_{start_line}",
            type='module',
            complexity=complexity,
            quality_score=quality_score,
            tags=tags,
            description=f"Module-level code block starting at line {start_line}"
        )
    
    def _parse_js_file(self, content: str, file_path: str, language: str) -> List[CodeSnippet]:
        """Parse JavaScript/TypeScript file using regex patterns."""
        snippets = []
        
        # Function patterns
        function_patterns = [
            r'(?:export\s+)?(?:async\s+)?function\s+(\w+)\s*\([^)]*\)\s*\{[^}]*\}',
            r'(?:export\s+)?const\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>\s*\{[^}]*\}',
            r'(?:export\s+)?let\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>\s*\{[^}]*\}',
            r'(?:export\s+)?var\s+(\w+)\s*=\s*(?:async\s+)?\([^)]*\)\s*=>\s*\{[^}]*\}'
        ]
        
        # Class patterns
        class_patterns = [
            r'(?:export\s+)?class\s+(\w+)\s*\{[^}]*\}',
            r'(?:export\s+)?class\s+(\w+)\s+extends\s+\w+\s*\{[^}]*\}'
        ]
        
        lines = content.split('\n')
        
        # Find functions
        for pattern in function_patterns:
            for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
                start_pos = content[:match.start()].count('\n') + 1
                end_pos = content[:match.end()].count('\n') + 1
                
                snippet_content = match.group(0)
                function_name = match.group(1)
                
                complexity = self._calculate_simple_complexity(snippet_content)
                quality_score = self._calculate_quality_score(snippet_content, complexity)
                tags = self._extract_tags(snippet_content, language)
                
                snippet_id = f"{file_path}:{start_pos}:{end_pos}"
                
                snippet = CodeSnippet(
                    id=snippet_id,
                    content=snippet_content,
                    language=language,
                    file_path=file_path,
                    line_start=start_pos,
                    line_end=end_pos,
                    name=function_name,
                    type='function',
                    complexity=complexity,
                    quality_score=quality_score,
                    tags=tags,
                    description=f"Function {function_name}"
                )
                snippets.append(snippet)
        
        # Find classes
        for pattern in class_patterns:
            for match in re.finditer(pattern, content, re.MULTILINE | re.DOTALL):
                start_pos = content[:match.start()].count('\n') + 1
                end_pos = content[:match.end()].count('\n') + 1
                
                snippet_content = match.group(0)
                class_name = match.group(1)
                
                complexity = self._calculate_simple_complexity(snippet_content)
                quality_score = self._calculate_quality_score(snippet_content, complexity)
                tags = self._extract_tags(snippet_content, language)
                
                snippet_id = f"{file_path}:{start_pos}:{end_pos}"
                
                snippet = CodeSnippet(
                    id=snippet_id,
                    content=snippet_content,
                    language=language,
                    file_path=file_path,
                    line_start=start_pos,
                    line_end=end_pos,
                    name=class_name,
                    type='class',
                    complexity=complexity,
                    quality_score=quality_score,
                    tags=tags,
                    description=f"Class {class_name}"
                )
                snippets.append(snippet)
        
        return snippets
    
    def _parse_generic_file(self, content: str, file_path: str, language: str) -> List[CodeSnippet]:
        """Parse generic file types."""
        snippets = []
        lines = content.split('\n')
        
        # Simple approach: extract code blocks
        current_block = []
        current_start = 1
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if stripped and not stripped.startswith('//') and not stripped.startswith('/*'):
                current_block.append(line)
            else:
                if current_block:
                    # End of block
                    snippet_content = '\n'.join(current_block)
                    if len(snippet_content.strip()) > 20:  # Minimum size
                        complexity = self._calculate_simple_complexity(snippet_content)
                        quality_score = self._calculate_quality_score(snippet_content, complexity)
                        tags = self._extract_tags(snippet_content, language)
                        
                        snippet_id = f"{file_path}:{current_start}:{i-1}"
                        
                        snippet = CodeSnippet(
                            id=snippet_id,
                            content=snippet_content,
                            language=language,
                            file_path=file_path,
                            line_start=current_start,
                            line_end=i-1,
                            name=f"code_block_{current_start}",
                            type='block',
                            complexity=complexity,
                            quality_score=quality_score,
                            tags=tags,
                            description=f"Code block starting at line {current_start}"
                        )
                        snippets.append(snippet)
                    
                    current_block = []
                    current_start = i + 1
        
        # Handle last block
        if current_block:
            snippet_content = '\n'.join(current_block)
            if len(snippet_content.strip()) > 20:
                complexity = self._calculate_simple_complexity(snippet_content)
                quality_score = self._calculate_quality_score(snippet_content, complexity)
                tags = self._extract_tags(snippet_content, language)
                
                snippet_id = f"{file_path}:{current_start}:{len(lines)}"
                
                snippet = CodeSnippet(
                    id=snippet_id,
                    content=snippet_content,
                    language=language,
                    file_path=file_path,
                    line_start=current_start,
                    line_end=len(lines),
                    name=f"code_block_{current_start}",
                    type='block',
                    complexity=complexity,
                    quality_score=quality_score,
                    tags=tags,
                    description=f"Code block starting at line {current_start}"
                )
                snippets.append(snippet)
        
        return snippets
    
    def _calculate_complexity(self, node: ast.AST) -> str:
        """Calculate complexity of an AST node."""
        complexity_score = 0
        
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.For, ast.While, ast.Try, ast.ExceptHandler)):
                complexity_score += 1
            elif isinstance(child, ast.FunctionDef):
                complexity_score += 2
            elif isinstance(child, ast.ClassDef):
                complexity_score += 3
        
        if complexity_score <= 2:
            return 'low'
        elif complexity_score <= 5:
            return 'medium'
        else:
            return 'high'
    
    def _calculate_simple_complexity(self, content: str) -> str:
        """Calculate complexity using simple heuristics."""
        lines = content.split('\n')
        complexity_score = 0
        
        for line in lines:
            stripped = line.strip()
            if any(keyword in stripped for keyword in ['if ', 'for ', 'while ', 'try:', 'except', 'catch', 'switch']):
                complexity_score += 1
            if any(keyword in stripped for keyword in ['def ', 'function ', 'class ', 'method ']):
                complexity_score += 2
        
        if complexity_score <= 2:
            return 'low'
        elif complexity_score <= 5:
            return 'medium'
        else:
            return 'high'
    
    def _calculate_quality_score(self, content: str, complexity: str) -> float:
        """Calculate a simple quality score."""
        score = 7.0  # Base score
        
        # Length factor
        lines = content.split('\n')
        if 5 <= len(lines) <= 50:
            score += 1.0
        elif len(lines) > 50:
            score -= 1.0
        
        # Complexity factor
        if complexity == 'low':
            score += 0.5
        elif complexity == 'high':
            score -= 0.5
        
        # Comment factor
        comment_lines = sum(1 for line in lines if line.strip().startswith(('#', '//', '/*')))
        comment_ratio = comment_lines / len(lines) if lines else 0
        if 0.1 <= comment_ratio <= 0.3:
            score += 0.5
        elif comment_ratio > 0.5:
            score -= 0.5
        
        return max(1.0, min(10.0, score))
    
    def _extract_tags(self, content: str, language: str) -> List[str]:
        """Extract tags from code content."""
        tags = []
        
        # Language tag
        tags.append(language)
        
        # Common patterns
        patterns = {
            'function': r'\b(?:def|function|func)\s+\w+',
            'class': r'\b(?:class|interface)\s+\w+',
            'api': r'\b(?:api|endpoint|route)\b',
            'database': r'\b(?:sql|query|database|db)\b',
            'async': r'\b(?:async|await|promise)\b',
            'test': r'\b(?:test|spec|assert)\b',
            'algorithm': r'\b(?:sort|search|filter|map|reduce)\b'
        }
        
        for tag_name, pattern in patterns.items():
            if re.search(pattern, content, re.IGNORECASE):
                tags.append(tag_name)
        
        return list(set(tags))
    
    def _generate_description(self, node: ast.AST, name: str, node_type: str) -> str:
        """Generate a description for a code node."""
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            # Try to extract docstring
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                return node.body[0].value.s.strip()
            else:
                return f"{node_type.title()} {name}"
        elif isinstance(node, ast.ClassDef):
            # Try to extract docstring
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Str):
                return node.body[0].value.s.strip()
            else:
                return f"Class {name}"
        else:
            return f"{node_type.title()} {name}" 