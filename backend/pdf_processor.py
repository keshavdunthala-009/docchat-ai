import PyPDF2
from typing import List, Dict

def extract_text_from_pdf(pdf_path: str) -> str:
    """Extract all text from a PDF file"""
    text = ""
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            print(f"Total pages: {len(reader.pages)}\n")
            
            for page_num, page in enumerate(reader.pages):
                page_text = page.extract_text()
                text += f"--- Page {page_num + 1} ---\n{page_text}\n"
    except Exception as e:
        print(f"Error reading PDF: {e}")
    
    return text

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
    """Split text into chunks with overlap"""
    chunks = []
    start = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start = end - overlap
    
    return chunks

def chunk_text_with_metadata(text: str, filename: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
    """Chunks with metadata for later retrieval"""
    chunks = []
    start = 0
    chunk_id = 0
    
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        
        chunks.append({
            "id": f"{filename}_chunk_{chunk_id}",
            "text": chunk,
            "filename": filename,
            "chunk_index": chunk_id,
            "char_start": start,
            "char_end": end
        })
        
        start = end - overlap
        chunk_id += 1
    
    return chunks

# Test it
if __name__ == "__main__":
    print("=" * 60)
    print("PDF PROCESSOR - Document Chunking Demo")
    print("=" * 60)
    
    # Sample text
    sample_text = "Python is a programming language. " * 50
    
    # Test chunking
    chunks = chunk_text(sample_text, chunk_size=200, overlap=30)
    
    print(f"\nOriginal text length: {len(sample_text)} characters")
    print(f"Number of chunks: {len(chunks)}")
    print(f"\nFirst chunk:\n{chunks[0][:100]}...")
    print(f"\nSecond chunk:\n{chunks[1][:100]}...")
    
    # Test with metadata
    chunks_with_meta = chunk_text_with_metadata(sample_text, "demo.pdf", chunk_size=200, overlap=30)
    
    print(f"\n\nChunk with metadata:")
    print(f"ID: {chunks_with_meta[0]['id']}")
    print(f"Filename: {chunks_with_meta[0]['filename']}")
    print(f"Chunk index: {chunks_with_meta[0]['chunk_index']}")