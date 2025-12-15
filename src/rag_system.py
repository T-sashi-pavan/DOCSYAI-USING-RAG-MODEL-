from src.pdf_loader import PDFLoader
from src.text_chunker import TextChunker
from src.vector_store import VectorStore
from src.llm_manager import LLMManager
from typing import Dict, List
import time
import gc

class RAGSystem:
    """Complete RAG system optimized for 500MB memory constraint."""
    
    def __init__(self, 
                 collection_name: str = "pdf_qa",
                 llm_model: str = "llama-3.1-8b-instant",
                 chunk_size: int = 300):  # Smaller chunks for low memory
        print("🚀 Initializing RAG System (LOW MEMORY MODE - 500MB)...")
        
        self.vector_store = VectorStore(collection_name)
        self.llm = LLMManager(llm_model)
        self.chunker = TextChunker(chunk_size=chunk_size)
        
        print("✓ RAG System ready (memory optimized)!\n")
    
    def ingest_pdf(self, pdf_path: str):
        """Process and store PDF with memory-efficient streaming."""
        print(f"\n📚 Processing PDF: {pdf_path}")
        print(f"⚙️  Memory mode: LOW (500MB) - using streaming\n")
        
        start_time = time.time()
        loader = PDFLoader(pdf_path)
        
        # Process pages in streaming fashion
        total_chars = 0
        total_chunks = 0
        chunks_buffer = []
        buffer_size = 20  # Process chunks in small batches
        
        for page_num, page_text in enumerate(loader.load_streaming(), 1):
            if not page_text:
                continue
            
            # Add page marker
            text_with_marker = f"\n--- Page {page_num} ---\n{page_text}"
            total_chars += len(text_with_marker)
            
            # Chunk this page
            metadata = {'page': page_num, 'source': pdf_path}
            page_chunks = self.chunker.split_text(text_with_marker, metadata=metadata)
            
            # Add to buffer
            chunks_buffer.extend(page_chunks)
            total_chunks += len(page_chunks)
            
            # Process buffer when it reaches a threshold
            if len(chunks_buffer) >= buffer_size:
                self._add_chunks_batch(chunks_buffer)
                chunks_buffer = []
                gc.collect()  # Free memory
        
        # Process remaining chunks
        if chunks_buffer:
            self._add_chunks_batch(chunks_buffer)
        
        processing_time = time.time() - start_time
        
        # Summary
        print(f"\n⏱️  Processing Summary:")
        print(f"   📄 Total Pages: {page_num if page_num > 0 else 0}")
        print(f"   📊 Total Characters: {total_chars}")
        print(f"   ✂️  Total Chunks: {total_chunks}")
        print(f"   ⏳ Time: {processing_time:.2f}s")
        print(f"   💾 Memory mode: Streaming (low usage)")
        print(f"✓ PDF processing complete")
    
    def _add_chunks_batch(self, chunks: List[Dict]):
        """Add a batch of chunks to vector store."""
        if not chunks:
            return
        
        print(f"   💾 Adding {len(chunks)} chunks to database...")
        self.vector_store.add_chunks(chunks)
    
    def ask(self, question: str, top_k: int = 5, threshold: float = 0.7) -> Dict:
        """
        Ask a question with enhanced response formatting.
        
        Args:
            question: User's question
            top_k: Number of chunks to retrieve
            threshold: Relevance threshold (0-1, lower distance = more relevant)
            
        Returns:
            Enhanced response dictionary
        """
        print(f"\n❓ Question: {question}")
        
        # Retrieve relevant chunks
        results = self.vector_store.search(question, top_k=top_k)
        
        # Determine if we have relevant context
        has_relevant_context = False
        filtered_results = []
        
        if results:
            # Filter by relevance threshold
            for result in results:
                # Distance < threshold means high relevance
                if result['distance'] < threshold:
                    has_relevant_context = True
                    filtered_results.append(result)
        
        # Generate response based on context availability
        if has_relevant_context:
            # Use PDF context
            context_chunks = [result['text'] for result in filtered_results]
            response_data = self.llm.generate_answer(question, context_chunks, mode="pdf")
            response_data['sources'] = filtered_results
            response_data['mode'] = 'pdf'
        else:
            # Use general knowledge
            print("⚠️  No highly relevant content found in PDF. Using general knowledge...")
            response_data = self.llm.generate_answer(question, [], mode="general")
            response_data['sources'] = results[:3] if results else []  # Show closest matches anyway
            response_data['mode'] = 'general'
        
        return response_data
    
    def generate_summary(self, pdf_path: str = None) -> str:
        """Generate a summary of uploaded PDF(s)."""
        # Get some representative chunks
        # This is a simplified version
        return "Summary feature - to be implemented"
    
    def get_stats(self) -> Dict:
        """Get system statistics."""
        return {
            'total_chunks': self.vector_store.count_documents(),
            'collection': self.vector_store.table_name
        }