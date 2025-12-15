"""
Simple in-memory caching for embeddings and answers to reduce redundant API calls.
"""
from typing import Dict, Optional, List
import time
from functools import lru_cache

class CacheManager:
    """Manages caching of embeddings and question-answer pairs."""
    
    def __init__(self, ttl: int = 3600):
        """
        Initialize cache manager.
        
        Args:
            ttl: Time to live for cache entries in seconds (default: 1 hour)
        """
        self.ttl = ttl
        self.embedding_cache: Dict[str, tuple] = {}
        self.answer_cache: Dict[str, tuple] = {}
    
    def get_cached_embedding(self, text: str) -> Optional[List[float]]:
        """
        Get cached embedding if it exists and hasn't expired.
        
        Args:
            text: Text to look up
            
        Returns:
            Embedding vector or None if not cached/expired
        """
        if text in self.embedding_cache:
            embedding, timestamp = self.embedding_cache[text]
            if time.time() - timestamp < self.ttl:
                print(f"✓ Embedding cache hit")
                return embedding
            else:
                # Remove expired entry
                del self.embedding_cache[text]
        return None
    
    def cache_embedding(self, text: str, embedding: List[float]):
        """Cache an embedding."""
        self.embedding_cache[text] = (embedding, time.time())
    
    def get_cached_answer(self, question: str, context_hash: str) -> Optional[Dict]:
        """
        Get cached answer if it exists and hasn't expired.
        
        Args:
            question: Question text
            context_hash: Hash of context used
            
        Returns:
            Cached answer or None if not cached/expired
        """
        cache_key = f"{question}:{context_hash}"
        if cache_key in self.answer_cache:
            answer, timestamp = self.answer_cache[cache_key]
            if time.time() - timestamp < self.ttl:
                print(f"✓ Answer cache hit")
                return answer
            else:
                # Remove expired entry
                del self.answer_cache[cache_key]
        return None
    
    def cache_answer(self, question: str, context_hash: str, answer: Dict):
        """Cache an answer."""
        cache_key = f"{question}:{context_hash}"
        self.answer_cache[cache_key] = (answer, time.time())
    
    def clear_embeddings(self):
        """Clear all embedding cache."""
        self.embedding_cache.clear()
        print("✓ Embedding cache cleared")
    
    def clear_answers(self):
        """Clear all answer cache."""
        self.answer_cache.clear()
        print("✓ Answer cache cleared")
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        return {
            "embedding_cache_size": len(self.embedding_cache),
            "answer_cache_size": len(self.answer_cache),
            "ttl": self.ttl
        }
