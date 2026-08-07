from document_handler import DocumentProcessor
from sentence_transformers import SentenceTransformer
from llm_answer import AnswerGenerator
from supabase_handler import SupabaseHandler
import os
from dotenv import load_dotenv

load_dotenv()


class RAGPipeline:
    """Smart RAG Pipeline with Supabase persistence"""

    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.doc_processor = DocumentProcessor(session_id=session_id)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.answer_gen = AnswerGenerator()
        self.supabase = SupabaseHandler()
        self.max_direct_chars = 100000

    def add_document(self, pdf_path: str, document_name: str):
        """Add document - store in Supabase permanently"""

        text = self.doc_processor.extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(text)} characters")

        # Save to Supabase permanently
        self.supabase.save_document(
            session_id=self.session_id,
            document_name=document_name,
            full_text=text
        )
        print(f"Saved to Supabase - Session: {self.session_id}")

        # Store chunks in ChromaDB for large doc RAG
        result = self.doc_processor.store_document(pdf_path, document_name)
        return result

    def query(self, question: str, top_k: int = 7) -> dict:
        """Smart RAG query with Supabase"""

        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"Session: {self.session_id}")
        print(f"{'='*60}\n")

        # Get document from Supabase
        doc_data = self.supabase.get_document(self.session_id)

        if not doc_data:
            print(f"No document in Supabase for session: {self.session_id}")
            return {
                "question": question,
                "answer": "Please upload a document first!",
                "sources": [],
                "chunk_count": 0
            }

        full_text = doc_data["full_text"]
        doc_name = doc_data["document_name"]
        print(f"Found: {doc_name} ({len(full_text)} chars)")

        if len(full_text) <= self.max_direct_chars:
            print(f"FULL TEXT mode")
            context = full_text
        else:
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

        print(f"Generating answer...")
        answer = self.answer_gen.generate(question, context)
        print(f"Answer: {answer}\n")

        return {
            "question": question,
            "answer": answer,
            "sources": [context[:150] + "..."],
            "chunk_count": 1
        }