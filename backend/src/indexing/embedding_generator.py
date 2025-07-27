"""
Embedding generator for creating semantic embeddings of code snippets.
"""

import numpy as np
from typing import List, Dict, Any, Optional, Union
from transformers import AutoTokenizer, AutoModel
import torch
from sentence_transformers import SentenceTransformer
import hashlib
import json
from datetime import datetime

from ..config.settings import settings
from ..models.code_snippet import CodeSnippet


class EmbeddingGenerator:
    """Generator for creating semantic embeddings of code snippets."""
    
    def __init__(self):
        """Initialize the embedding generator with models."""
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.models = {}
        self.tokenizers = {}
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models for code embedding."""
        try:
            # Load CodeBERT model for code-specific embeddings
            self.models['codebert'] = AutoModel.from_pretrained('microsoft/codebert-base')
            self.tokenizers['codebert'] = AutoTokenizer.from_pretrained('microsoft/codebert-base')
            self.models['codebert'].to(self.device)
            
            # Load GraphCodeBERT for graph-based code embeddings
            self.models['graphcodebert'] = AutoModel.from_pretrained('microsoft/graphcodebert-base')
            self.tokenizers['graphcodebert'] = AutoTokenizer.from_pretrained('microsoft/graphcodebert-base')
            self.models['graphcodebert'].to(self.device)
            
            # Load general-purpose sentence transformer
            self.models['sentence'] = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
            
            # Load language-specific models
            self.models['python'] = SentenceTransformer('microsoft/DialoGPT-medium')
            self.models['javascript'] = SentenceTransformer('microsoft/DialoGPT-medium')
            
        except Exception as e:
            print(f"Error loading models: {e}")
            # Fallback to basic sentence transformer
            self.models['sentence'] = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
    
    def generate_embedding(self, snippet: CodeSnippet, model_type: str = 'codebert') -> Optional[List[float]]:
        """Generate embedding for a code snippet."""
        try:
            if model_type == 'codebert':
                return self._generate_codebert_embedding(snippet)
            elif model_type == 'graphcodebert':
                return self._generate_graphcodebert_embedding(snippet)
            elif model_type == 'sentence':
                return self._generate_sentence_embedding(snippet)
            elif model_type == 'hybrid':
                return self._generate_hybrid_embedding(snippet)
            else:
                return self._generate_codebert_embedding(snippet)
        except Exception as e:
            print(f"Error generating embedding: {e}")
            return None
    
    def _generate_codebert_embedding(self, snippet: CodeSnippet) -> Optional[List[float]]:
        """Generate embedding using CodeBERT."""
        try:
            model = self.models.get('codebert')
            tokenizer = self.tokenizers.get('codebert')
            
            if not model or not tokenizer:
                return None
            
            # Prepare input text
            input_text = self._prepare_code_text(snippet)
            
            # Tokenize
            inputs = tokenizer(
                input_text,
                return_tensors='pt',
                max_length=512,
                truncation=True,
                padding=True
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embeddings
            with torch.no_grad():
                outputs = model(**inputs)
                # Use [CLS] token embedding
                embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()[0]
            
            return embedding.tolist()
            
        except Exception as e:
            print(f"Error in CodeBERT embedding: {e}")
            return None
    
    def _generate_graphcodebert_embedding(self, snippet: CodeSnippet) -> Optional[List[float]]:
        """Generate embedding using GraphCodeBERT."""
        try:
            model = self.models.get('graphcodebert')
            tokenizer = self.tokenizers.get('graphcodebert')
            
            if not model or not tokenizer:
                return None
            
            # Prepare input text with data flow information
            input_text = self._prepare_code_text_with_flow(snippet)
            
            # Tokenize
            inputs = tokenizer(
                input_text,
                return_tensors='pt',
                max_length=512,
                truncation=True,
                padding=True
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embeddings
            with torch.no_grad():
                outputs = model(**inputs)
                embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()[0]
            
            return embedding.tolist()
            
        except Exception as e:
            print(f"Error in GraphCodeBERT embedding: {e}")
            return None
    
    def _generate_sentence_embedding(self, snippet: CodeSnippet) -> Optional[List[float]]:
        """Generate embedding using sentence transformer."""
        try:
            model = self.models.get('sentence')
            
            if not model:
                return None
            
            # Prepare input text
            input_text = self._prepare_code_text(snippet)
            
            # Generate embedding
            embedding = model.encode(input_text, convert_to_tensor=True)
            embedding = embedding.cpu().numpy()
            
            return embedding.tolist()
            
        except Exception as e:
            print(f"Error in sentence embedding: {e}")
            return None
    
    def _generate_hybrid_embedding(self, snippet: CodeSnippet) -> Optional[List[float]]:
        """Generate hybrid embedding combining multiple models."""
        try:
            embeddings = []
            
            # Get embeddings from different models
            codebert_emb = self._generate_codebert_embedding(snippet)
            if codebert_emb:
                embeddings.append(codebert_emb)
            
            sentence_emb = self._generate_sentence_embedding(snippet)
            if sentence_emb:
                embeddings.append(sentence_emb)
            
            if not embeddings:
                return None
            
            # Combine embeddings (simple concatenation or averaging)
            if len(embeddings) == 1:
                return embeddings[0]
            else:
                # Average the embeddings
                combined = np.mean(embeddings, axis=0)
                return combined.tolist()
                
        except Exception as e:
            print(f"Error in hybrid embedding: {e}")
            return None
    
    def _prepare_code_text(self, snippet: CodeSnippet) -> str:
        """Prepare code text for embedding generation."""
        text_parts = []
        
        # Add code content
        text_parts.append(snippet.content)
        
        # Add function/class name if available
        if snippet.name:
            text_parts.append(f"Name: {snippet.name}")
        
        # Add docstring if available
        if snippet.docstring:
            text_parts.append(f"Documentation: {snippet.docstring}")
        
        # Add parameters if available
        if snippet.parameters:
            text_parts.append(f"Parameters: {', '.join(snippet.parameters)}")
        
        # Add return type if available
        if snippet.return_type:
            text_parts.append(f"Returns: {snippet.return_type}")
        
        # Add keywords
        if snippet.keywords:
            text_parts.append(f"Keywords: {', '.join(snippet.keywords)}")
        
        # Add language information
        text_parts.append(f"Language: {snippet.language}")
        text_parts.append(f"Type: {snippet.code_type.value}")
        
        return " ".join(text_parts)
    
    def _prepare_code_text_with_flow(self, snippet: CodeSnippet) -> str:
        """Prepare code text with data flow information for GraphCodeBERT."""
        text_parts = []
        
        # Add code content
        text_parts.append(snippet.content)
        
        # Add data flow information
        if snippet.called_functions:
            text_parts.append(f"Calls: {', '.join(snippet.called_functions)}")
        
        if snippet.variables_used:
            text_parts.append(f"Variables: {', '.join(snippet.variables_used)}")
        
        if snippet.dependencies:
            text_parts.append(f"Dependencies: {', '.join(snippet.dependencies)}")
        
        # Add other metadata
        if snippet.name:
            text_parts.append(f"Name: {snippet.name}")
        
        if snippet.docstring:
            text_parts.append(f"Documentation: {snippet.docstring}")
        
        return " ".join(text_parts)
    
    def generate_batch_embeddings(self, snippets: List[CodeSnippet], model_type: str = 'codebert') -> Dict[str, List[float]]:
        """Generate embeddings for a batch of snippets."""
        embeddings = {}
        
        for snippet in snippets:
            embedding = self.generate_embedding(snippet, model_type)
            if embedding:
                embeddings[snippet.id] = embedding
        
        return embeddings
    
    def generate_query_embedding(self, query: str, model_type: str = 'codebert') -> Optional[List[float]]:
        """Generate embedding for a search query."""
        try:
            if model_type == 'codebert':
                return self._generate_codebert_query_embedding(query)
            elif model_type == 'sentence':
                return self._generate_sentence_query_embedding(query)
            else:
                return self._generate_sentence_query_embedding(query)
        except Exception as e:
            print(f"Error generating query embedding: {e}")
            return None
    
    def _generate_codebert_query_embedding(self, query: str) -> Optional[List[float]]:
        """Generate embedding for query using CodeBERT."""
        try:
            model = self.models.get('codebert')
            tokenizer = self.tokenizers.get('codebert')
            
            if not model or not tokenizer:
                return None
            
            # Tokenize query
            inputs = tokenizer(
                query,
                return_tensors='pt',
                max_length=512,
                truncation=True,
                padding=True
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate embedding
            with torch.no_grad():
                outputs = model(**inputs)
                embedding = outputs.last_hidden_state[:, 0, :].cpu().numpy()[0]
            
            return embedding.tolist()
            
        except Exception as e:
            print(f"Error in CodeBERT query embedding: {e}")
            return None
    
    def _generate_sentence_query_embedding(self, query: str) -> Optional[List[float]]:
        """Generate embedding for query using sentence transformer."""
        try:
            model = self.models.get('sentence')
            
            if not model:
                return None
            
            # Generate embedding
            embedding = model.encode(query, convert_to_tensor=True)
            embedding = embedding.cpu().numpy()
            
            return embedding.tolist()
            
        except Exception as e:
            print(f"Error in sentence query embedding: {e}")
            return None
    
    def calculate_similarity(self, embedding1: List[float], embedding2: List[float]) -> float:
        """Calculate cosine similarity between two embeddings."""
        try:
            vec1 = np.array(embedding1)
            vec2 = np.array(embedding2)
            
            # Normalize vectors
            vec1_norm = vec1 / np.linalg.norm(vec1)
            vec2_norm = vec2 / np.linalg.norm(vec2)
            
            # Calculate cosine similarity
            similarity = np.dot(vec1_norm, vec2_norm)
            
            return float(similarity)
            
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0
    
    def find_similar_snippets(self, query_embedding: List[float], snippet_embeddings: Dict[str, List[float]], 
                            top_k: int = 10, threshold: float = 0.7) -> List[tuple]:
        """Find similar snippets based on embedding similarity."""
        similarities = []
        
        for snippet_id, embedding in snippet_embeddings.items():
            similarity = self.calculate_similarity(query_embedding, embedding)
            if similarity >= threshold:
                similarities.append((snippet_id, similarity))
        
        # Sort by similarity score (descending)
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return similarities[:top_k]
    
    def get_embedding_dimension(self, model_type: str = 'codebert') -> int:
        """Get the dimension of embeddings for a specific model."""
        dimensions = {
            'codebert': 768,
            'graphcodebert': 768,
            'sentence': 384,
            'hybrid': 768  # Default to CodeBERT dimension
        }
        
        return dimensions.get(model_type, 768)
    
    def create_embedding_hash(self, snippet: CodeSnippet) -> str:
        """Create a hash for caching embeddings."""
        content_hash = hashlib.md5(snippet.content.encode()).hexdigest()
        metadata = {
            'language': snippet.language,
            'code_type': snippet.code_type.value,
            'name': snippet.name,
            'parameters': snippet.parameters,
            'return_type': snippet.return_type,
            'keywords': snippet.keywords
        }
        metadata_hash = hashlib.md5(json.dumps(metadata, sort_keys=True).encode()).hexdigest()
        
        return f"{content_hash}_{metadata_hash}"
    
    def update_snippet_embedding(self, snippet: CodeSnippet, embedding: List[float], model_type: str = 'codebert'):
        """Update a snippet with its embedding."""
        snippet.embedding = embedding
        snippet.embedding_model = model_type
        snippet.updated_at = datetime.utcnow() 