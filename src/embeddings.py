import os
from typing import List
import requests
import time

class EmbeddingManager:
    """Handles text embeddings via FREE HuggingFace Inference API using direct HTTP requests."""
    
    def __init__(self, model_name: str = 'sentence-transformers/all-MiniLM-L6-v2'):
        """
        Use the FREE HuggingFace Inference API with new router endpoint.
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
        
        # Use the NEW router endpoint directly
        self.api_url = f"https://api-inference.huggingface.co/models/{model_name}"
        self.headers = {"Authorization": f"Bearer {self.api_token}"}
        
        print(f"☁️ Using FREE HuggingFace Inference API: {model_name}")

    def embed_text(self, text: str, max_retries: int = 3) -> List[float]:
        """Convert single text to embedding with retry logic."""
        
        for attempt in range(max_retries):
            try:
                # Direct HTTP POST request to HuggingFace Inference API
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json={"inputs": text}
                )
                
                if response.status_code == 200:
                    embedding = response.json()
                    
                    # Handle different response formats
                    if isinstance(embedding, list):
                        # If it's a nested list (batch of 1), get first element
                        if len(embedding) > 0 and isinstance(embedding[0], list):
                            return embedding[0]
                        return embedding
                    
                    raise Exception(f"Unexpected response format: {type(embedding)}")
                
                # Handle specific error codes
                elif response.status_code == 503:
                    wait_time = 20
                    print(f"⏳ Model loading, waiting {wait_time}s (attempt {attempt + 1}/{max_retries})...")
                    time.sleep(wait_time)
                    continue
                
                elif response.status_code == 429:
                    wait_time = 10
                    print(f"⏳ Rate limited, waiting {wait_time}s...")
                    time.sleep(wait_time)
                    continue
                
                else:
                    response.raise_for_status()
                    
            except requests.exceptions.HTTPError as e:
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
            
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                print(f"⚠️ Attempt {attempt + 1} failed, retrying...")
                time.sleep(5)
        
        raise Exception(f"Failed after {max_retries} attempts")

    def embed_batch(self, texts: List[str], batch_size: int = 2) -> List[List[float]]:
        """
        Convert multiple texts to embeddings with minimal memory usage.
        Uses very small batch size (2-4) for 500MB constraint.
        """
        print(f"☁️ Embedding {len(texts)} texts via HuggingFace Inference API (batch size: {batch_size})...")
        
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
                    # Direct HTTP POST request
                    response = requests.post(
                        self.api_url,
                        headers=self.headers,
                        json={"inputs": batch}
                    )
                    
                    if response.status_code == 200:
                        embeddings = response.json()
                        
                        # Handle response format
                        if isinstance(embeddings, list) and len(embeddings) > 0:
                            if not isinstance(embeddings[0], (list, tuple)):
                                embeddings = [embeddings]
                            
                            if len(embeddings) == len(batch):
                                all_embeddings.extend(embeddings)
                                break
                        
                        raise Exception(f"Unexpected embedding format or count mismatch")
                    
                    elif response.status_code == 503:
                        wait_time = 20
                        print(f"   ⏳ Model loading, waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    
                    elif response.status_code == 429:
                        wait_time = 20 + (attempt * 10)  # Longer wait for rate limit
                        print(f"   ⏳ Rate limited, waiting {wait_time}s...")
                        time.sleep(wait_time)
                        continue
                    
                    else:
                        response.raise_for_status()
                    
                except Exception as e:
                    if attempt == max_retries - 1:
                        print(f"❌ Failed to embed batch {batch_num}: {str(e)[:100]}")
                        raise
                    time.sleep(5)
        
        print(f"✅ Generated {len(all_embeddings)} embeddings")
        return all_embeddings