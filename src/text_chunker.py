from typing import List, Dict
import re

class TextChunker:
    """Splits text into manageable chunks with smart sentence-based chunking."""
    
    def __init__(self, chunk_size: int = 500, chunk_overlap: int = 50):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
    
    def split_text(self, text: str, metadata: dict = None) -> List[Dict]:
        """Split text into chunks using smart sentence boundaries."""
        chunks = []
        
        # Clean the text more aggressively
        text = self._clean_text(text)
        
        if not text:
            return chunks
        
        # Split by sentences first for better chunks
        sentences = self._split_sentences(text)
        
        # Group sentences into chunks
        current_chunk = ""
        chunk_id = 0
        start_char = 0
        
        for sentence in sentences:
            # Check if adding this sentence would exceed chunk size
            if len(current_chunk) + len(sentence) > self.chunk_size and current_chunk:
                # Save current chunk
                chunk = {
                    'id': chunk_id,
                    'text': current_chunk.strip(),
                    'start_char': start_char,
                    'end_char': start_char + len(current_chunk),
                    'metadata': metadata or {}
                }
                chunks.append(chunk)
                
                # Start new chunk with overlap
                overlap_text = self._get_overlap(current_chunk)
                current_chunk = overlap_text + sentence
                start_char += len(current_chunk) - len(overlap_text)
                chunk_id += 1
            else:
                current_chunk += sentence
        
        # Add final chunk
        if current_chunk.strip():
            chunk = {
                'id': chunk_id,
                'text': current_chunk.strip(),
                'start_char': start_char,
                'end_char': start_char + len(current_chunk),
                'metadata': metadata or {}
            }
            chunks.append(chunk)
        
        print(f"✓ Created {len(chunks)} chunks (avg: {len(text) // max(len(chunks), 1)} chars/chunk)")
        return chunks
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove multiple spaces/newlines
        text = re.sub(r'\s+', ' ', text)
        # Remove control characters
        text = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]', '', text)
        return text.strip()
    
    def _split_sentences(self, text: str) -> List[str]:
        """Split text into sentences, preserving structure."""
        # Pattern for sentence boundaries
        sentence_pattern = r'(?<=[.!?])\s+(?=[A-Z])|(?<=[.!?])\s*(?=\n)'
        sentences = re.split(sentence_pattern, text)
        
        # Add back spaces and filter empty
        sentences = [s.strip() + ' ' for s in sentences if s.strip()]
        
        if not sentences:
            sentences = [text]
        
        return sentences
    
    def _get_overlap(self, text: str, overlap_size: int = None) -> str:
        """Get the last part of text for overlap with next chunk."""
        if overlap_size is None:
            overlap_size = self.chunk_overlap
        
        if len(text) <= overlap_size:
            return text
        
        # Try to break at sentence boundary
        text_tail = text[-overlap_size:]
        last_period = text_tail.rfind('.')
        
        if last_period > overlap_size // 2:
            return text_tail[last_period + 1:].strip() + ' '
        
        # Break at last space
        last_space = text_tail.rfind(' ')
        if last_space > 0:
            return text_tail[last_space:].strip() + ' '
        
        return text_tail