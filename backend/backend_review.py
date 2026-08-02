# Python Review - Test Your Knowledge

# 1. Dictionaries
doc = {"title": "AI", "content": "Artificial Intelligence", "pages": 10}
print(doc["title"])  # Should print: AI

# 2. Lists
chunks = ["chunk1", "chunk2", "chunk3"]
print(chunks[0])  # Should print: chunk1

# 3. List Comprehensions
upper_chunks = [c.upper() for c in chunks]
print(upper_chunks)  # Should print: ['CHUNK1', 'CHUNK2', 'CHUNK3']

# 4. File I/O
with open("sample.txt", "w") as f:
    f.write("This is a sample document")

with open("sample.txt", "r") as f:
    content = f.read()
    print(f"File content: {content}")

# 5. Functions
def process_text(text: str) -> str:
    """Process text and return uppercase"""
    return text.upper()

result = process_text("hello world")
print(f"Processed: {result}")  # Should print: HELLO WORLD