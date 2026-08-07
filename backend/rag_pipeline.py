from document_handler import DocumentProcessor
from sentence_transformers import SentenceTransformer
from llm_answer import AnswerGenerator
import os
from dotenv import load_dotenv

load_dotenv()

# Global storage - persists across requests in same session
document_store = {}

class RAGPipeline:
    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.doc_processor = DocumentProcessor(session_id=session_id)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.answer_gen = AnswerGenerator()
        self.max_direct_chars = 20000

    def add_document(self, pdf_path: str, document_name: str):
        """Add document and store full text globally"""
        text = self.doc_processor.extract_text_from_pdf(pdf_path)
        
        # Store in global dict with session_id
        document_store[self.session_id] = {
            "name": document_name,
            "text": text
        }
        print(f"Stored full text: {len(text)} chars for session {self.session_id}")
        
        result = self.doc_processor.store_document(pdf_path, document_name)
        return result

    def query(self, question: str, top_k: int = 7) -> dict:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"Session: {self.session_id}")
        print(f"{'='*60}\n")

        # Check global store first
        if self.session_id in document_store:
            doc_data = document_store[self.session_id]
            full_text = doc_data["text"]
            doc_name = doc_data["name"]
            
            print(f"Found document: {doc_name} ({len(full_text)} chars)")

            if len(full_text) <= self.max_direct_chars:
                # Small doc - send FULL text to LLM
                print(f"Using FULL text mode")
                context = full_text
            else:
                # Large doc - use RAG
                print(f"Using RAG mode")
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
        else:
            return {
                "question": question,
                "answer": "Please upload a document first!",
                "sources": [],
                "chunk_count": 0
            }

        print(f"Generating answer...")
        answer = self.answer_gen.generate(question, context)
        print(f"Answer: {answer}\n")

        return {
            "question": question,
            "answer": answer,
            "sources": [context[:150] + "..."],
            "chunk_count": 1
        }