import os
from typing import List
from huggingface_hub import InferenceClient
import time

class EmbeddingManager:
    """Handles text embeddings via FREE HuggingFace Serverless API using InferenceClient."""
    
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        """
        Use the FREE HuggingFace Serverless Inference API.
        Model: sentence-transformers/all-MiniLM-L6-v2 (384 dimensions)
        """
        self.model_name = model_name
        self.api_token = os.getenv("HUGGINGFACE_API_KEY")
        
        if not self.api_token:
            raise ValueError(
                "HUGGINGFACE_API_KEY not found!\n"
                "Get a FREE token at: https://huggingface.co/settings/tokens\n"
                "Make sure to select 'Read' access (free tier)"
            )
        
        # Initialize HuggingFace InferenceClient (correct way for serverless)
        self.client = InferenceClient(
            token=self.api_token,
            provider="hf-inference"  # Use HuggingFace's serverless inference
        )
        
        print(f"☁️ Using FREE HuggingFace Serverless API: {model_name}")
        print(f"   Using InferenceClient with provider: hf-inference")

    def embed_text(self, text: str, max_retries: int = 3) -> List[float]:
        """Convert single text to embedding with retry logic."""
        
        for attempt in range(max_retries):
            try:
                # Use feature_extraction method (correct method for embeddings)
                embedding = self.client.feature_extraction(
                    text=text,
                    model=self.model_name
                )
                
                # Convert to list if it's a numpy array or other format
                if hasattr(embedding, 'tolist'):
                    embedding = embedding.tolist()
                
                # Handle different response formats
                if isinstance(embedding, list):
                    # If it's a nested list (batch of 1), get first element
                    if len(embedding) > 0 and isinstance(embedding[0], list):
                        return embedding[0]
                    return embedding
                
                raise Exception(f"Unexpected embedding format: {type(embedding)}")
                
            except Exception as e:
                error_msg = str(e).lower()
                
                # Model loading (503 error)
                if "503" in error_msg or "loading" in error_msg:
                    wait_time = 20
                    print(f"⏳ Model loading, waiting {wait_time}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                    continue
                
                # Rate limiting (429 error)
                if "429" in error_msg or "rate limit" in error_msg:
                    wait_time = 10
                    print(f"⏳ Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                # Last attempt - raise error
                if attempt == max_retries - 1:
                    print(f"❌ Error after {max_retries} attempts: {str(e)}")
                    raise Exception(
                        f"Failed to generate embedding: {str(e)}\n\n"
                        f"Common fixes:\n"
                        f"1. Check your token at: https://huggingface.co/settings/tokens\n"
                        f"2. Make sure token has 'Read' access\n"
                        f"3. Wait a moment for the model to load (free tier)\n"
                        f"4. Check rate limits (few hundred requests per hour for free tier)"
                    )
                
                # Retry on other errors
                print(f"⚠️ Attempt {attempt + 1} failed, retrying...")
                time.sleep(5)
        
        raise Exception(f"Failed after {max_retries} attempts")

    def embed_batch(self, texts: List[str], batch_size: int = 2) -> List[List[float]]:
        """
        Convert multiple texts to embeddings with minimal memory usage.
        Uses very small batch size (2-4) for 500MB constraint.
        """
        print(f"☁️ Embedding {len(texts)} texts via HuggingFace Serverless API (batch size: {batch_size})...")
        
        all_embeddings = []
        total_batches = (len(texts) + batch_size - 1) // batch_size
        
        # Process in minimal batch sizes for low memory
        for batch_idx in range(0, len(texts), batch_size):
            batch = texts[batch_idx:batch_idx + batch_size]
            batch_num = (batch_idx // batch_size) + 1
            print(f"   Processing batch {batch_num}/{total_batches} ({len(batch)} texts)...")
            
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Send batch
                    embeddings = self.client.feature_extraction(
                        text=batch,
                        model=self.model_name
                    )
                    
                    # Convert to list if needed
                    if hasattr(embeddings, 'tolist'):
                        embeddings = embeddings.tolist()
                    
                    # Handle response format
                    if isinstance(embeddings, list) and len(embeddings) > 0:
                        if not isinstance(embeddings[0], (list, tuple)):
                            embeddings = [embeddings]
                        
                        if len(embeddings) == len(batch):
                            all_embeddings.extend(embeddings)
                            break
                    
                    raise Exception(f"Unexpected embedding format or count mismatch")
                    
                except Exception as e:
                    error_msg = str(e).lower()
                    
                    if "503" in error_msg or "loading" in error_msg:
                        wait_time = 20
                        print(f"   ⏳ Model loading, waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    
                    if "429" in error_msg or "rate limit" in error_msg:
                        wait_time = 20 + (attempt * 10)  # Longer wait for rate limit
                        print(f"   ⏳ Rate limited, waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    
                    if attempt == max_retries - 1:
                        print(f"❌ Failed to embed batch {batch_num}: {str(e)[:100]}")
                        raise
        
        print(f"✅ Generated {len(all_embeddings)} embeddings")
        return all_embeddings