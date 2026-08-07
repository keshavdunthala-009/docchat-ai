from document_handler import DocumentProcessor
from sentence_transformers import SentenceTransformer
from llm_answer import AnswerGenerator
import os
from dotenv import load_dotenv

load_dotenv()

# Global document store - persists across requests
document_store = {}

class RAGPipeline:
    """Smart RAG Pipeline"""

    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.doc_processor = DocumentProcessor(session_id=session_id)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.answer_gen = AnswerGenerator()
        self.max_direct_chars = 20000

    def add_document(self, pdf_path: str, document_name: str):
        """Add document and store full text"""
        
        # Extract full text
        text = self.doc_processor.extract_text_from_pdf(pdf_path)
        
        # Store in global dict
        document_store[self.session_id] = {
            "name": document_name,
            "text": text
        }
        
        print(f"Stored document for session: {self.session_id}")
        print(f"Document: {document_name} ({len(text)} chars)")
        print(f"All sessions: {list(document_store.keys())}")
        
        # Also store chunks in ChromaDB
        result = self.doc_processor.store_document(pdf_path, document_name)
        return result

    def query(self, question: str, top_k: int = 7) -> dict:
        """Smart RAG query"""

        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"Session: {self.session_id}")
        print(f"Available sessions: {list(document_store.keys())}")
        print(f"{'='*60}\n")

        # Check if document exists for this session
        if self.session_id not in document_store:
            print(f"No document found for session: {self.session_id}")
            return {
                "question": question,
                "answer": "Please upload a document first!",
                "sources": [],
                "chunk_count": 0
            }

        doc_data = document_store[self.session_id]
        full_text = doc_data["text"]
        doc_name = doc_data["name"]

        print(f"Found document: {doc_name} ({len(full_text)} chars)")

        if len(full_text) <= self.max_direct_chars:
            # Small document - use FULL text
            print(f"FULL TEXT mode")
            context = full_text
        else:
            # Large document - use RAG chunks
            print(f"RAG CHUNKS mode")
            search_results = self.doc_processor.search_documents(
                question, top_k=top_k
            )
            if not search_results:
                return {
                    "question": question,
                    "answer": "Not found in document",
                    "sources": [],
                    "chunk_count": 0
                }
            context = "\n\n---\n\n".join([r["text"] for r in search_results])
            print(f"Retrieved {len(search_results)} chunks")

        print(f"Generating answer...")
        answer = self.answer_gen.generate(question, context)
        print(f"Answer: {answer}\n")

        return {
            "question": question,
            "answer": answer,
            "sources": [context[:150] + "..."],
            "chunk_count": 1
        }