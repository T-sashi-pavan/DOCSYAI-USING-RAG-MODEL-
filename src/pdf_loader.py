import pypdf
from typing import Dict, Generator
import gc

class PDFLoader:
    """Extracts text from PDF files with memory-efficient streaming."""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = ""
        self.pages = []
    
    def load_streaming(self) -> Generator[str, None, None]:
        """Stream text from PDF pages one at a time (memory efficient)."""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                print(f"📄 Found {num_pages} pages (streaming mode - low memory)")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    # Yield one page at a time instead of accumulating
                    yield page_text
                    
                    # Force garbage collection every 10 pages
                    if (page_num + 1) % 10 == 0:
                        gc.collect()
                        print(f"   Processed {page_num + 1}/{num_pages} pages")
                
                print(f"✓ Streamed all {num_pages} pages successfully")
                
        except FileNotFoundError:
            print(f"✗ Error: File not found at {self.pdf_path}")
        except Exception as e:
            print(f"✗ Error reading PDF: {str(e)}")
    
    def load(self) -> str:
        """Load entire PDF (use only for small PDFs < 50MB)."""
        text = ""
        for page_text in self.load_streaming():
            text += f"\n--- Page {len(self.pages) + 1} ---\n"
            text += page_text
            self.pages.append({
                'page_number': len(self.pages) + 1,
                'text': page_text
            })
        
        print(f"✓ Loaded {len(text)} characters")
        return text
    
    def get_metadata(self) -> dict:
        """Get PDF metadata."""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                metadata = pdf_reader.metadata
                return {
                    'title': metadata.get('/Title', 'Unknown') if metadata else 'Unknown',
                    'author': metadata.get('/Author', 'Unknown') if metadata else 'Unknown',
                    'pages': len(pdf_reader.pages)
                }
        except:
            return {'title': 'Unknown', 'author': 'Unknown', 'pages': 0}