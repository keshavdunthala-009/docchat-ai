from document_handler import DocumentProcessor
from sentence_transformers import SentenceTransformer
from llm_answer import AnswerGenerator
import os
from dotenv import load_dotenv

load_dotenv()


class RAGPipeline:
    """RAG Pipeline - Full document context for resumes"""

    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.answer_gen = AnswerGenerator()
        self.full_document_text = {}  # Store full document text

    def add_document(self, pdf_path: str, document_name: str):
        """Add document and store full text"""
        # Store full text for context
        text = self.doc_processor.extract_text_from_pdf(pdf_path)
        self.full_document_text[document_name] = text
        
        # Also store in vector DB for retrieval
        result = self.doc_processor.store_document(pdf_path, document_name)
        return result

    def query(self, question: str, top_k: int = 5) -> dict:
        """RAG Pipeline - use full document as context"""

        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}\n")

        # Get full document text if available
        if self.full_document_text:
            # Use most recently uploaded document
            doc_name = list(self.full_document_text.keys())[-1]
            context = self.full_document_text[doc_name]
            print(f"Using full document: {doc_name}")
            print(f"Context length: {len(context)} characters")
        else:
            # Fallback to vector search
            print(f"Retrieving TOP 5 relevant chunks...")
            search_results = self.doc_processor.search_documents(question, top_k=5)

            if not search_results:
                return {
                    "question": question,
                    "answer": "Not found in document",
                    "sources": [],
                    "chunk_count": 0
                }

            context = "\n\n---\n\n".join([r["text"] for r in search_results])

        # Generate answer from full context
        print(f"Generating answer...")
        answer = self.answer_gen.generate(question, context)
        print(f"Answer: {answer}\n")

        return {
            "question": question,
            "answer": answer,
            "sources": [context[:150] + "..."],
            "chunk_count": 1
        }