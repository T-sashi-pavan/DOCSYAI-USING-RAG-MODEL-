import pypdf
from typing import List, Dict

class PDFLoader:
    """Extracts text from PDF files."""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.text = ""
        self.pages = []
    
    def load(self) -> str:
        """Extract text from all pages."""
        try:
            with open(self.pdf_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                num_pages = len(pdf_reader.pages)
                
                print(f"📄 Found {num_pages} pages")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    page_text = page.extract_text()
                    
                    self.pages.append({
                        'page_number': page_num + 1,
                        'text': page_text
                    })
                    
                    self.text += f"\n--- Page {page_num + 1} ---\n"
                    self.text += page_text
                
                print(f"✓ Extracted {len(self.text)} characters")
                return self.text
                
        except FileNotFoundError:
            print(f"✗ Error: File not found at {self.pdf_path}")
            return ""
        except Exception as e:
            print(f"✗ Error reading PDF: {str(e)}")
            return ""
    
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