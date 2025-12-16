import os
from typing import List
from optimum.onnxruntime import ORTModelForFeatureExtraction
from transformers import AutoTokenizer
import numpy as np

class EmbeddingManager:
    """Handles text embeddings using ONNX Runtime (CPU-only, ~50MB, fast)."""
    
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        """
        Use ONNX Runtime for embeddings - much lighter than PyTorch.
        Model: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
        Runs on CPU with ONNX optimization (~50MB total).
        """
        self.model_name = model_name
        
        # Load ONNX model and tokenizer (CPU-only, optimized)
        print(f"📥 Loading ONNX embedding model: {model_name}")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = ORTModelForFeatureExtraction.from_pretrained(
            model_name,
            export=True  # Auto-convert to ONNX if needed
        )
        print(f"✅ ONNX model loaded (CPU-optimized, low memory)")

    def _mean_pooling(self, model_output, attention_mask):
        """Apply mean pooling to get sentence embeddings."""
        token_embeddings = model_output[0]
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return (token_embeddings * input_mask_expanded).sum(1) / input_mask_expanded.sum(1).clamp(min=1e-9)
    
    def embed_text(self, text: str, max_retries: int = 3) -> List[float]:
        """Convert single text to embedding using ONNX model."""
        try:
            # Tokenize
            inputs = self.tokenizer(text, return_tensors="pt", padding=True, truncation=True, max_length=512)
            
            # Generate embeddings with ONNX model
            outputs = self.model(**inputs)
            
            # Apply mean pooling
            embeddings = self._mean_pooling(outputs, inputs['attention_mask'])
            
            # Normalize
            embeddings = embeddings / embeddings.norm(dim=1, keepdim=True)
            
            return embeddings[0].detach().numpy().tolist()
        except Exception as e:
            raise Exception(f"Failed to generate embedding: {e}")

    def embed_batch(self, texts: List[str], batch_size: int = 8) -> List[List[float]]:
        """
        Convert multiple texts to embeddings using ONNX model.
        Batch size of 8 is efficient for CPU processing.
        """
        print(f"📊 Embedding {len(texts)} texts using ONNX model (batch size: {batch_size})...")
        
        try:
            all_embeddings = []
            
            # Process in batches
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                
                # Tokenize batch
                inputs = self.tokenizer(batch, return_tensors="pt", padding=True, truncation=True, max_length=512)
                
                # Generate embeddings
                outputs = self.model(**inputs)
                
                # Apply mean pooling
                embeddings = self._mean_pooling(outputs, inputs['attention_mask'])
                
                # Normalize
                embeddings = embeddings / embeddings.norm(dim=1, keepdim=True)
                
                # Convert to list
                all_embeddings.extend([emb.detach().numpy().tolist() for emb in embeddings])
            
            print(f"✅ Generated {len(all_embeddings)} embeddings")
            return all_embeddings
            
        except Exception as e:
            print(f"❌ Failed to embed batch: {str(e)}")
            raise