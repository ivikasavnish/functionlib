#!/usr/bin/env python3
"""
Query Vector Store - Search for similar functions
"""

import sys
import chromadb

def query_chromadb(query_text: str, n_results: int = 5):
    """Query ChromaDB for similar functions"""
    client = chromadb.PersistentClient(path="./chroma_db")
    collection = client.get_collection("function_library")
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    print(f"\nTop {n_results} results for: '{query_text}'")
    print("=" * 80)
    
    for i, (metadata, distance) in enumerate(zip(
        results['metadatas'][0],
        results['distances'][0]
    )):
        print(f"\n{i+1}. {metadata['function_name']}")
        print(f"   Category: {metadata['category']}/{metadata['subcategory']}")
        print(f"   Purpose: {metadata['purpose']}")
        print(f"   Similarity: {1 - distance:.4f}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 vector_store_query.py '<query>' [num_results]")
        sys.exit(1)
    
    query = sys.argv[1]
    n_results = int(sys.argv[2]) if len(sys.argv) > 2 else 5
    
    query_chromadb(query, n_results)
