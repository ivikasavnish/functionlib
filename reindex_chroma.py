#!/usr/bin/env python3
"""
ChromaDB Re-Indexing Task
Regenerates embeddings and re-indexes the function library in ChromaDB
"""

import json
import os
from typing import List, Dict
from datetime import datetime

def log_message(message: str):
    """Log message with timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {message}")

def load_data() -> List[Dict]:
    """Load function data from ChromaDB JSON file"""
    log_message("Loading data from VECTOR_STORE_CHROMADB.json...")
    
    if not os.path.exists('VECTOR_STORE_CHROMADB.json'):
        raise FileNotFoundError("VECTOR_STORE_CHROMADB.json not found")
    
    with open('VECTOR_STORE_CHROMADB.json', 'r') as f:
        data = json.load(f)
    
    entries = data.get('entries', [])
    log_message(f"Loaded {len(entries)} entries")
    return entries

def generate_embeddings(documents: List[str]) -> List[List[float]]:
    """Generate embeddings using Sentence Transformers (local)"""
    log_message("Generating embeddings using Sentence Transformers...")
    
    try:
        from sentence_transformers import SentenceTransformer
    except ImportError:
        log_message("ERROR: sentence-transformers not installed")
        log_message("Please install: pip install sentence-transformers")
        raise
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    log_message(f"Model loaded: all-MiniLM-L6-v2")
    
    # Generate embeddings in batches for efficiency
    batch_size = 100
    all_embeddings = []
    
    for i in range(0, len(documents), batch_size):
        batch = documents[i:i+batch_size]
        log_message(f"Processing batch {i//batch_size + 1}/{(len(documents)-1)//batch_size + 1}")
        embeddings = model.encode(batch, show_progress_bar=False)
        all_embeddings.extend(embeddings.tolist())
    
    log_message(f"Generated {len(all_embeddings)} embeddings")
    return all_embeddings

def reindex_chromadb(entries: List[Dict], embeddings: List[List[float]]):
    """Delete and recreate ChromaDB collection with new embeddings"""
    log_message("Initializing ChromaDB...")
    
    try:
        import chromadb
    except ImportError:
        log_message("ERROR: chromadb not installed")
        log_message("Please install: pip install chromadb")
        raise
    
    # Initialize ChromaDB with persistent storage
    client = chromadb.PersistentClient(path="./chroma_db")
    log_message("ChromaDB client initialized")
    
    # Delete existing collection if it exists
    try:
        client.delete_collection("function_library")
        log_message("Deleted existing 'function_library' collection")
    except Exception as e:
        log_message(f"No existing collection to delete: {e}")
    
    # Create new collection
    collection = client.create_collection("function_library")
    log_message("Created new 'function_library' collection")
    
    # Prepare data for ChromaDB
    ids = [str(entry['id']) for entry in entries]
    documents = [entry['document'] for entry in entries]
    metadatas = [entry['metadata'] for entry in entries]
    
    log_message(f"Prepared {len(ids)} entries for indexing")
    
    # Add to collection in batches to respect max batch size
    max_batch_size = 5000
    total_batches = (len(ids) - 1) // max_batch_size + 1
    
    for i in range(0, len(ids), max_batch_size):
        batch_num = i // max_batch_size + 1
        log_message(f"Uploading batch {batch_num}/{total_batches}...")
        
        batch_ids = ids[i:i+max_batch_size]
        batch_embeddings = embeddings[i:i+max_batch_size]
        batch_documents = documents[i:i+max_batch_size]
        batch_metadatas = metadatas[i:i+max_batch_size]
        
        collection.add(
            ids=batch_ids,
            embeddings=batch_embeddings,
            documents=batch_documents,
            metadatas=batch_metadatas
        )
        log_message(f"Batch {batch_num} uploaded successfully")
    
    log_message(f"✓ Successfully re-indexed {len(entries)} entries in ChromaDB")
    
    # Verify the collection
    count = collection.count()
    log_message(f"Verification: Collection contains {count} items")
    
    return collection

def main():
    """Main execution function"""
    log_message("=" * 60)
    log_message("ChromaDB Re-Indexing Task Started")
    log_message("=" * 60)
    
    try:
        # Step 1: Load data
        entries = load_data()
        
        # Step 2: Generate embeddings
        documents = [entry['document'] for entry in entries]
        embeddings = generate_embeddings(documents)
        
        # Step 3: Re-index in ChromaDB
        collection = reindex_chromadb(entries, embeddings)
        
        # Step 4: Test query
        log_message("\nPerforming test query...")
        results = collection.query(
            query_texts=["sorting algorithms"],
            n_results=3
        )
        log_message(f"Test query returned {len(results['ids'][0])} results")
        if results['ids'][0]:
            log_message(f"Top result: {results['documents'][0][0]}")
        
        log_message("\n" + "=" * 60)
        log_message("✓ ChromaDB Re-Indexing Completed Successfully!")
        log_message("=" * 60)
        log_message(f"Total entries indexed: {len(entries)}")
        log_message(f"ChromaDB path: ./chroma_db")
        log_message(f"Collection name: function_library")
        
    except Exception as e:
        log_message("\n" + "=" * 60)
        log_message(f"✗ ERROR: {str(e)}")
        log_message("=" * 60)
        raise

if __name__ == "__main__":
    main()
