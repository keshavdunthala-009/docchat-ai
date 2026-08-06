import os
from typing import List, Dict
from sentence_transformers import SentenceTransformer
import chromadb


class DocumentProcessor:

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.client = chromadb.PersistentClient(path="/tmp/chroma_data")
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
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

    def chunk_text(self, text: str, chunk_size: int = 200, overlap: int = 40) -> List[Dict]:
        chunks = []
        sentences = text.split('.')
        current_chunk = ""
        chunk_id = 0
        for sentence in sentences:
            sentence = sentence.strip() + "."
            if len(current_chunk) + len(sentence) < chunk_size:
                current_chunk += " " + sentence
            else:
                if len(current_chunk) > 50:
                    chunks.append({
                        "id": f"chunk_{chunk_id}",
                        "text": current_chunk.strip(),
                        "chunk_index": chunk_id
                    })
                    chunk_id += 1
                current_chunk = sentence
        if len(current_chunk) > 50:
            chunks.append({
                "id": f"chunk_{chunk_id}",
                "text": current_chunk.strip(),
                "chunk_index": chunk_id
            })
        return chunks

    def store_document(self, pdf_path: str, document_name: str) -> dict:
        print(f"Processing: {document_name}")
        text = self.extract_text_from_pdf(pdf_path)
        print(f"Extracted {len(text)} characters")
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

    def search_documents(self, query: str, top_k: int = 1) -> List[Dict]:
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