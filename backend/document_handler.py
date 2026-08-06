def store_document(self, pdf_path: str, document_name: str) -> dict:
    """Store document with BATCH embedding for speed"""
    
    print(f"\n{'='*60}")
    print(f"Processing: {document_name}")
    print(f"{'='*60}\n")
    
    # Step 1: Extract text
    print("1. Extracting text from PDF...")
    text = self.extract_text_from_pdf(pdf_path)
    print(f"✅ Extracted {len(text)} characters\n")
    
    # Step 2: Chunk text
    print("2. Chunking text...")
    chunks = self.chunk_text(text)
    print(f"✅ Created {len(chunks)} chunks\n")
    
    # Step 3: BATCH embed ALL chunks at once
    print("3. Embedding ALL chunks at once (batch)...")
    chunk_texts = [chunk["text"] for chunk in chunks]
    
    # Batch encode - much faster than one by one!
    embeddings = self.model.encode(
        chunk_texts, 
        batch_size=32,        # Process 32 at once
        show_progress_bar=True,
        convert_to_numpy=True
    )
    print(f"✅ Embedded {len(embeddings)} chunks\n")
    
    # Step 4: Store ALL in ChromaDB at once
    print("4. Storing in vector database...")
    ids = [f"{document_name}_chunk_{i}" for i in range(len(chunks))]
    metadatas = [{"document": document_name, "chunk_index": i} for i in range(len(chunks))]
    
    self.collection.add(
        ids=ids,
        embeddings=embeddings.tolist(),
        documents=chunk_texts,
        metadatas=metadatas
    )
    print(f"✅ Stored all {len(chunks)} chunks at once!\n")
    
    return {"chunks": len(chunks), "document": document_name}