import os
from typing import List
from sentence_transformers import SentenceTransformer
import time

class EmbeddingManager:
    """Handles text embeddings using LOCAL SentenceTransformer model (80MB, runs on CPU)."""
    
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        """
        Use SentenceTransformer locally - downloads model once (80MB).
        Model: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
        Runs on CPU, optimized for low memory (500MB).
        """
        self.model_name = model_name
        
        # Download and load model locally (cached after first run)
        print(f"📥 Loading embedding model: {model_name}")
        self.model = SentenceTransformer(model_name)
        print(f"✅ Embedding model loaded (running on CPU)")

    def embed_text(self, text: str, max_retries: int = 3) -> List[float]:
        """Convert single text to embedding using local model."""
        try:
            # Generate embedding using local model (runs on CPU)
            embedding = self.model.encode(text, convert_to_numpy=True)
            return embedding.tolist()
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {e}")

    def embed_batch(self, texts: List[str], batch_size: int = 8) -> List[List[float]]:
        """
        Convert multiple texts to embeddings using local model.
        Batch size of 8 is efficient for CPU processing.
        """
        print(f"📊 Embedding {len(texts)} texts using local model (batch size: {batch_size})...")
        
        try:
            # Process all texts in batches (SentenceTransformer handles batching internally)
            embeddings = self.model.encode(
                texts,
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=False
            )
            
            result = [emb.tolist() for emb in embeddings]
            print(f"✅ Generated {len(result)} embeddings")
            return result
            
        except Exception as e:
            print(f"❌ Failed to embed batch: {str(e)}")
            raise