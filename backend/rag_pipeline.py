from document_handler import DocumentProcessor
from sentence_transformers import SentenceTransformer
from llm_answer import AnswerGenerator
import os
from dotenv import load_dotenv

load_dotenv()


class RAGPipeline:
    """Smart RAG Pipeline - handles any document size"""

    def __init__(self, session_id: str = "default"):
        self.session_id = session_id
        self.doc_processor = DocumentProcessor(session_id=session_id)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.answer_gen = AnswerGenerator()
        self.full_document_text = {}
        self.max_direct_chars = 20000

    def add_document(self, pdf_path: str, document_name: str):
        text = self.doc_processor.extract_text_from_pdf(pdf_path)
        self.full_document_text[document_name] = text
        result = self.doc_processor.store_document(pdf_path, document_name)
        return result

    def query(self, question: str, top_k: int = 5) -> dict:
        print(f"\n{'='*60}")
        print(f"Question: {question}")
        print(f"Session: {self.session_id}")
        print(f"{'='*60}\n")

        if self.full_document_text:
            doc_name = list(self.full_document_text.keys())[-1]
            full_text = self.full_document_text[doc_name]

            if len(full_text) <= self.max_direct_chars:
                print(f"Small doc - using full text ({len(full_text)} chars)")
                context = full_text
            else:
                print(f"Large doc - using RAG chunks ({len(full_text)} chars)")
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
        else:
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
            "chunk_count": len(self.full_document_text)
        }