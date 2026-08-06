import os
import re
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb


class DocumentProcessor:

    def __init__(self, session_id: str = "default"):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path="/tmp/chroma_data")
        self.collection = self.client.get_or_create_collection(
            name=f"documents_{session_id}",
            metadata={"hnsw:space": "cosine"}
        )
        # Separate collection for full documents
        self.full_docs = self.client.get_or_create_collection(
            name=f"full_docs_{session_id}"
        )

    def extract_text_from_pdf(self, pdf_path: str) -> str:
        try:
            import PyPDF2
            text = ""
            with open(pdf_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() + "\n"
            return text
        except Exception as e:
            with open(pdf_path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()

    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 100) -> List[Dict]:
        chunks = []
        chunk_id = 0

        sections = re.split(r'\n(?=[A-Z][A-Z\s]+\n)', text)

        for section in sections:
            section = section.strip()
            if len(section) > 50:
                if len(section) > chunk_size:
                    start = 0
                    while start < len(section):
                        end = start + chunk_size
                        chunk = section[start:end].strip()
                        if len(chunk) > 50:
                            chunks.append({
                                "id": f"chunk_{chunk_id}",
                                "text": chunk,
                                "chunk_index": chunk_id
                            })
                            chunk_id += 1
                        start = end - overlap
                else:
                    chunks.append({
                        "id": f"chunk_{chunk_id}",
                        "text": section,
                        "chunk_index": chunk_id
                    })
                    chunk_id += 1

        if len(chunks) == 0:
            start = 0
            while start < len(text):
                end = start + chunk_size
                chunk = text[start:end].strip()
                if len(chunk) > 50:
                    chunks.append({
                        "id": f"chunk_{chunk_id}",
                        "text": chunk,
                        "chunk_index": chunk_id
                    })
                    chunk_id += 1
                start = end - overlap

        return chunks

    def store_document(self, pdf_path: str, document_name: str) -> dict:
        print(f"Processing: {document_name}")
        text = self.extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(text)} characters")

        # Store FULL text in separate collection
        try:
            self.full_docs.add(
                ids=[document_name],
                documents=[text],
                metadatas=[{"document": document_name, "length": len(text)}]
            )
            print(f"Stored full text ({len(text)} chars)")
        except Exception as e:
            print(f"Full text already exists: {e}")

        # Store chunks for RAG
        chunks = self.chunk_text(text)
        print(f"Created {len(chunks)} chunks")
        chunk_texts = [chunk["text"] for chunk in chunks]

        embeddings = self.model.encode(
            chunk_texts,
            batch_size=32,
            convert_to_numpy=True
        )
        print(f"Embedded {len(embeddings)} chunks")

        ids = [f"{document_name}_chunk_{i}" for i in range(len(chunks))]
        metadatas = [{"document": document_name, "chunk_index": i} for i in range(len(chunks))]

        self.collection.add(
            ids=ids,
            embeddings=embeddings.tolist(),
            documents=chunk_texts,
            metadatas=metadatas
        )
        print(f"Stored all {len(chunks)} chunks!")
        return {"chunks": len(chunks), "document": document_name}

    def get_full_text(self, document_name: str) -> str:
        """Get full document text from ChromaDB"""
        try:
            result = self.full_docs.get(ids=[document_name])
            if result and result['documents']:
                return result['documents'][0]
        except Exception as e:
            print(f"Error getting full text: {e}")
        return None

    def get_latest_document(self) -> str:
        """Get the latest uploaded document name"""
        try:
            result = self.full_docs.get()
            if result and result['ids']:
                return result['ids'][-1]
        except Exception as e:
            print(f"Error getting latest doc: {e}")
        return None

    def search_documents(self, query: str, top_k: int = 7) -> List[Dict]:
        query_embedding = self.model.encode(query)
        results = self.collection.query(
            query_embeddings=[query_embedding.tolist()],
            n_results=top_k
        )
        search_results = []
        for i, doc in enumerate(results['documents'][0]):
            search_results.append({
                "text": doc,
                "metadata": results['metadatas'][0][i],
                "rank": i + 1
            })
        return search_results