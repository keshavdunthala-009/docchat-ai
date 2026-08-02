import PyPDF2
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb

class DocumentProcessor:
    """Process documents, chunk them, and store in vector database"""
    
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path="./chroma_data")
        self.collection = self.client.get_or_create_collection(name="documents")
    
    def extract_text_from_pdf(self, pdf_path: str) -> str:
        """Extract text from PDF"""
        text = ""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                for page_num, page in enumerate(reader.pages):
                    page_text = page.extract_text()
                    text += f"--- Page {page_num + 1} ---\n{page_text}\n"
        except Exception as e:
            print(f"Error reading PDF: {e}")
        return text
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[Dict]:
        """Split text into chunks with metadata"""
        chunks = []
        start = 0
        chunk_id = 0
        
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            
            chunks.append({
                "id": f"chunk_{chunk_id}",
                "text": chunk,
                "chunk_index": chunk_id,
                "char_start": start,
                "char_end": end
            })
            
            start = end - overlap
            chunk_id += 1
        
        return chunks
    
    def store_document(self, pdf_path: str, document_name: str) -> dict:
        """
        Complete pipeline: Extract → Chunk → Embed → Store
        
        Args:
            pdf_path: Path to PDF file
            document_name: Name for this document
            
        Returns:
            Status dict
        """
        print(f"\n{'='*60}")
        print(f"Processing: {document_name}")
        print(f"{'='*60}\n")
        
        # Step 1: Extract text
        print(f"1. Extracting text from PDF...")
        text = self.extract_text_from_pdf(pdf_path)
        print(f"   ✅ Extracted {len(text)} characters")
        
        # Step 2: Chunk text
        print(f"\n2. Chunking text...")
        chunks = self.chunk_text(text, chunk_size=500, overlap=50)
        print(f"   ✅ Created {len(chunks)} chunks")
        
        # Step 3: Embed and store
        print(f"\n3. Embedding and storing in vector database...")
        for i, chunk in enumerate(chunks):
            embedding = self.model.encode(chunk["text"])
            chunk_id = f"{document_name}_{chunk['id']}"
            
            self.collection.add(
                ids=[chunk_id],
                embeddings=[embedding.tolist()],
                documents=[chunk["text"]],
                metadatas={
                    "document": document_name,
                    "chunk_index": chunk["chunk_index"],
                    "char_start": chunk["char_start"],
                    "char_end": chunk["char_end"]
                }
            )
            
            if (i + 1) % 10 == 0:
                print(f"   ✅ Stored {i + 1}/{len(chunks)} chunks")
        
        print(f"   ✅ All chunks stored successfully!")
        
        return {
            "status": "success",
            "document": document_name,
            "chunks": len(chunks),
            "total_chars": len(text)
        }
    
    def search_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Search for similar documents"""
        query_embedding = self.model.encode(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        
        search_results = []
        for i, doc in enumerate(results['documents'][0]):
            search_results.append({
                "rank": i + 1,
                "text": doc,
                "metadata": results['metadatas'][0][i] if results['metadatas'] else {}
            })
        
        return search_results

# Test it
if __name__ == "__main__":
    processor = DocumentProcessor()
    
    # Create a sample text file to test (since we don't have a PDF yet)
    sample_text = """
    Python is a high-level, interpreted programming language.
    It's known for its simplicity and readability.
    Python is used in data science, web development, and AI.
    
    Machine Learning is a subset of artificial intelligence.
    It allows computers to learn from data without being explicitly programmed.
    
    FastAPI is a modern Python web framework for building APIs.
    It's fast, easy to use, and great for microservices.
    """
    
    # Save as sample file
    with open("sample_doc.txt", "w") as f:
        f.write(sample_text * 5)  # Repeat to make it longer
    
    print("Document Processor Demo")
    print("=" * 60)
    
    # In real scenario, you'd use: processor.store_document("file.pdf", "My Document")
    # For now, we'll just test the components
    
    # Test chunking
    chunks = processor.chunk_text(sample_text * 5)
    print(f"✅ Created {len(chunks)} chunks from sample text")
    
    # Test searching
    query = "What is Python?"
    results = processor.search_documents(query)
    print(f"\nSearch Results for: '{query}'")
    for result in results:
        print(f"{result['rank']}. {result['text'][:100]}...")