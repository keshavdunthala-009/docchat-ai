from document_handler import DocumentProcessor
from sentence_transformers import SentenceTransformer
from llm_answer import AnswerGenerator
import os
from dotenv import load_dotenv

load_dotenv()


class RAGPipeline:
    """RAG Pipeline - Top 5 Chunks for Better Accuracy"""

    def __init__(self):
        self.doc_processor = DocumentProcessor()
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.answer_gen = AnswerGenerator()

    def add_document(self, pdf_path: str, document_name: str):
        """Add document"""
        return self.doc_processor.store_document(pdf_path, document_name)

    def query(self, question: str, top_k: int = 5) -> dict:
        """RAG Pipeline - retrieve TOP 5 chunks for better accuracy"""

        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"{'='*60}\n")

        # Retrieve TOP 5 chunks
        print(f"Retrieving TOP 5 relevant chunks...")
        search_results = self.doc_processor.search_documents(question, top_k=5)

        if not search_results:
            return {
                "question": question,
                "answer": "Not found in document",
                "sources": [],
                "chunk_count": 0
            }

        print(f"Found {len(search_results)} chunks\n")

        # Combine ALL chunks as context
        context = "\n\n---\n\n".join([r["text"] for r in search_results])

        print(f"RETRIEVED CONTEXT:")
        print(f"{context}\n")
        print(f"{'='*60}\n")

        # Generate answer from combined context
        print(f"Generating answer...")
        answer = self.answer_gen.generate(question, context)
        print(f"Answer: {answer}\n")

        return {
            "question": question,
            "answer": answer,
            "sources": [r["text"][:150] + "..." for r in search_results],
            "chunk_count": len(search_results)
        }