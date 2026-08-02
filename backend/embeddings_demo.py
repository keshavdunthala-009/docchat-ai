from sentence_transformers import SentenceTransformer
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# Load the embedding model
model = SentenceTransformer('all-MiniLM-L6-v2')

print("=" * 60)
print("EMBEDDINGS DEMO - Understanding RAG Core")
print("=" * 60)

# Step 1: Convert text to embeddings
texts = [
    "Python is a programming language",
    "Python is great for data science",
    "I love playing football",
    "Machine learning uses neural networks"
]

print("\n1. Converting texts to embeddings...\n")
embeddings = []
for text in texts:
    embedding = model.encode(text)
    embeddings.append(embedding)
    print(f"Text: '{text}'")
    print(f"Embedding shape: {embedding.shape}")
    print(f"First 5 values: {embedding[:5]}\n")

# Step 2: Similarity search
print("=" * 60)
print("2. SIMILARITY SEARCH - How RAG Works\n")

query = "What is Python?"
query_embedding = model.encode(query)

print(f"Query: '{query}'\n")
print("Similarity scores with each document:\n")

for i, text in enumerate(texts):
    similarity = cosine_similarity([query_embedding], [embeddings[i]])[0][0]
    print(f"Document {i+1}: {similarity:.2f} -> '{text}'")

# Step 3: Find most similar
print("\n" + "=" * 60)
print("3. TOP-3 MOST SIMILAR DOCUMENTS\n")

similarities = []
for i, text in enumerate(texts):
    sim = cosine_similarity([query_embedding], [embeddings[i]])[0][0]
    similarities.append((sim, text, i+1))

# Sort by similarity (highest first)
similarities.sort(reverse=True)

print(f"Query: '{query}'\n")
print("Top-3 most similar:")
for rank, (score, text, doc_id) in enumerate(similarities[:3], 1):
    print(f"{rank}. (Score: {score:.2f}) Doc {doc_id}: '{text}'")

print("\n" + "=" * 60)
print("WHY THIS MATTERS FOR RAG:")
print("=" * 60)
print("""
1. User asks a question → Convert to embedding
2. We have document chunks → Each has an embedding
3. Compare question embedding to chunk embeddings
4. Find top-3 most similar chunks
5. Feed those chunks to LLM with prompt: "Answer based on these chunks"
6. LLM generates grounded answer

This is RAG in a nutshell! 🚀
""")