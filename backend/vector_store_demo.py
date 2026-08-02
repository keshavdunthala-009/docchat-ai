import chromadb
from sentence_transformers import SentenceTransformer

# Initialize Chroma (vector database)
client = chromadb.PersistentClient(path="./chroma_data")
collection = client.get_or_create_collection(name="documents")

# Load embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

print("=" * 60)
print("VECTOR STORE DEMO - Storing & Retrieving Embeddings")
print("=" * 60)

# Step 1: Add documents
documents = [
    {"id": "doc1", "text": "Python is a high-level programming language"},
    {"id": "doc2", "text": "Machine learning is a subset of artificial intelligence"},
    {"id": "doc3", "text": "FastAPI is a modern Python web framework"},
]

print("\n1. Adding documents to vector store...\n")
for doc in documents:
    embedding = model.encode(doc["text"])
    collection.add(
        ids=[doc["id"]],
        embeddings=[embedding.tolist()],
        documents=[doc["text"]],
        metadatas=[{"source": "demo"}]
    )
    print(f"✅ Added: {doc['text']}")

# Step 2: Retrieve similar documents
print("\n" + "=" * 60)
print("2. RETRIEVING SIMILAR DOCUMENTS\n")

query = "Tell me about Python"
query_embedding = model.encode(query)

results = collection.query(
    query_embeddings=[query_embedding.tolist()],
    n_results=2
)

print(f"Query: '{query}'\n")
print("Top-2 most similar documents:\n")
for i, doc in enumerate(results['documents'][0], 1):
    print(f"{i}. {doc}")

print("\n" + "=" * 60)
print("HOW CHROMA WORKS:")
print("=" * 60)
print("""
1. Store documents + embeddings in vector database
2. Query: Convert question to embedding
3. Search: Find most similar embeddings in database
4. Return: Top-K documents

This is the 'R' in RAG (Retrieval)! 🎯
""")