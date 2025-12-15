from supabase import create_client, Client
from typing import List, Dict
from src.embeddings import EmbeddingManager
import os
import numpy as np

class VectorStore:
    """Manages vector database using Supabase pgvector."""
    
    def __init__(self, collection_name: str = "pdf_qa_collection"):
        print("🗄️ Initializing Supabase Vector Store...")
        
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_ANON_KEY")
        
        if not url or not key:
            raise ValueError("SUPABASE_URL and SUPABASE_ANON_KEY must be set in .env")
        
        self.client: Client = create_client(supabase_url=url, supabase_key=key)
        self.table_name = collection_name
        self.embedder = EmbeddingManager()
        
        # Create table if not exists
        self._init_table()
        print(f"✓ Connected to Supabase: {self.table_name}")
    
    def _init_table(self):
        """Create table with pgvector if not exists."""
        # Execute via SQL (do this once in Supabase SQL Editor):
        # CREATE TABLE IF NOT EXISTS pdf_qa_collection (
        #     id TEXT PRIMARY KEY,
        #     text TEXT,
        #     embedding VECTOR(384),
        #     metadata JSONB,
        #     created_at TIMESTAMP DEFAULT NOW()
        # );
        # CREATE INDEX ON pdf_qa_collection USING ivfflat (embedding vector_cosine_ops);
        pass
    
    def add_chunks(self, chunks: List[Dict]):
        """Add text chunks to vector store."""
        print(f"\n💾 Adding {len(chunks)} chunks to Supabase...")
        
        texts = [chunk['text'] for chunk in chunks]
        embeddings = self.embedder.embed_batch(texts)
        
        records = []
        for i, chunk in enumerate(chunks):
            records.append({
                'id': f"chunk_{chunk['id']}_{hash(chunk['text']) % 10000}",
                'text': chunk['text'],
                'embedding': embeddings[i],
                'metadata': chunk.get('metadata', {})
            })
        
        # Insert in batches of 100
        for i in range(0, len(records), 100):
            batch = records[i:i+100]
            self.client.table(self.table_name).upsert(batch).execute()
        
        print(f"✓ Added {len(chunks)} chunks successfully")
    
    def search(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for relevant chunks using cosine similarity."""
        print(f"🔍 Searching for: '{query}'")
        
        query_embedding = self.embedder.embed_text(query)
        
        # Use RPC function for vector search
        response = self.client.rpc(
            'match_documents',
            {
                'query_embedding': query_embedding,
                'match_count': top_k
            }
        ).execute()
        
        formatted_results = []
        for doc in response.data:
            formatted_results.append({
                'text': doc['text'],
                'metadata': doc['metadata'],
                'distance': 1 - doc['similarity'],  # Convert similarity to distance
                'id': doc['id']
            })
        
        print(f"✓ Found {len(formatted_results)} relevant chunks")
        return formatted_results
    
    def count_documents(self) -> int:
        """Get total number of chunks."""
        response = self.client.table(self.table_name).select('id', count='exact').execute()
        return response.count
    
    def clear(self):
        """Delete all documents."""
        self.client.table(self.table_name).delete().neq('id', '').execute()
        print("✓ Collection cleared")