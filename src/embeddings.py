import os
from typing import List
import cohere

class EmbeddingManager:
    """Handles text embeddings using Cohere's FREE API (generous free tier)."""
    
    def __init__(self, model_name: str = 'embed-english-light-v3.0'):
        """
        Use Cohere's FREE embedding API.
        Model: embed-english-light-v3.0 (384 dimensions, optimized for speed)
        Free tier: 100 API calls/minute, plenty for our use case.
        """
        self.model_name = model_name
        api_key = os.getenv("COHERE_API_KEY", "TRIAL_KEY")  # Trial key works for testing
        
        # Initialize Cohere client
        self.client = cohere.Client(api_key)
        print(f"☁️ Using Cohere FREE API: {model_name}")
    
    def embed_text(self, text: str, max_retries: int = 3) -> List[float]:
        """Convert single text to embedding using Cohere API."""
        try:
            response = self.client.embed(
                texts=[text],
                model=self.model_name,
                input_type="search_document"
            )
            return response.embeddings[0]

    def embed_batch(self, texts: List[str], batch_size: int = 96) -> List[List[float]]:
        """
        Convert multiple texts to embeddings using Cohere API.
        Cohere supports up to 96 texts per API call.
        """
        print(f"📊 Embedding {len(texts)} texts using Cohere API...")
        
        try:
            all_embeddings = []
            
            # Process in batches (Cohere max: 96 texts per call)
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i+batch_size]
                
                response = self.client.embed(
                    texts=batch,
                    model=self.model_name,
                    input_type="search_document"
                )
                
                all_embeddings.extend(response.embeddings)
            
            print(f"✅ Generated {len(all_embeddings)} embeddings")
            return all_embeddings
            
        except Exception as e:
            print(f"❌ Failed to embed batch: {str(e)}")
            raise