#!/usr/bin/env python3
"""
Vector Store Embedding Script
Generate embeddings and upload to vector store
"""

import json
from typing import List, Dict

# STEP 1: Choose your embedding model
# Options: OpenAI, Cohere, Sentence Transformers, etc.

def generate_embeddings_openai(texts: List[str]) -> List[List[float]]:
    """Generate embeddings using OpenAI"""
    import openai
    
    # Set your API key
    # openai.api_key = "your-api-key"
    
    response = openai.embeddings.create(
        model="text-embedding-3-small",  # or text-embedding-3-large
        input=texts
    )
    
    return [item.embedding for item in response.data]

def generate_embeddings_sentence_transformers(texts: List[str]) -> List[List[float]]:
    """Generate embeddings using Sentence Transformers (free, local)"""
    from sentence_transformers import SentenceTransformer
    
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts)
    
    return embeddings.tolist()

# STEP 2: Load your data
def load_data():
    with open('VECTOR_STORE_DATA.json', 'r') as f:
        data = json.load(f)
    return data['entries']

# STEP 3: Upload to vector store

def upload_to_pinecone(entries: List[Dict], embeddings: List[List[float]]):
    """Upload to Pinecone"""
    import pinecone
    
    # Initialize Pinecone
    # pinecone.init(api_key="your-api-key", environment="your-environment")
    # index = pinecone.Index("function-library")
    
    # Prepare vectors
    vectors = []
    for entry, embedding in zip(entries, embeddings):
        vectors.append({
            "id": str(entry['id']),
            "values": embedding,
            "metadata": entry['metadata']
        })
    
    # Upsert in batches
    batch_size = 100
    for i in range(0, len(vectors), batch_size):
        batch = vectors[i:i+batch_size]
        # index.upsert(vectors=batch)
        print(f"Uploaded batch {i//batch_size + 1}")

def upload_to_chromadb(entries: List[Dict], embeddings: List[List[float]]):
    """Upload to ChromaDB"""
    import chromadb
    
    # Initialize ChromaDB with persistent storage
    client = chromadb.PersistentClient(path="./chroma_db")
    # Delete collection if it exists
    try:
        client.delete_collection("function_library")
    except:
        pass
    collection = client.create_collection("function_library")
    
    # Prepare data
    ids = [str(entry['id']) for entry in entries]
    documents = [entry['text'] for entry in entries]
    metadatas = [entry['metadata'] for entry in entries]
    
    # Add to collection in batches to respect max batch size
    max_batch_size = 5000  # slightly less than max to avoid errors
    for i in range(0, len(ids), max_batch_size):
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
    print(f"Uploaded {len(entries)} entries to ChromaDB")

def upload_to_weaviate(entries: List[Dict], embeddings: List[List[float]]):
    """Upload to Weaviate"""
    import weaviate
    
    # Initialize Weaviate client
    # client = weaviate.Client("http://localhost:8080")
    
    # Create schema if needed
    # schema = {
    #     "class": "Function",
    #     "properties": [...]
    # }
    # client.schema.create_class(schema)
    
    # Add objects with vectors
    with client.batch as batch:
        for entry, embedding in zip(entries, embeddings):
            batch.add_data_object(
                data_object=entry['metadata'],
                class_name="Function",
                vector=embedding,
                uuid=str(entry['id'])
            )
    print(f"Uploaded {len(entries)} entries to Weaviate")

def upload_to_qdrant(entries: List[Dict], embeddings: List[List[float]]):
    """Upload to Qdrant"""
    from qdrant_client import QdrantClient
    from qdrant_client.models import PointStruct, Distance, VectorParams
    
    # Initialize Qdrant
    client = QdrantClient(host="localhost", port=6333)
    
    # Create collection
    collection_name = "function_library"
    client.recreate_collection(
        collection_name=collection_name,
        vectors_config=VectorParams(
            size=len(embeddings[0]),
            distance=Distance.COSINE
        )
    )
    
    # Prepare points
    points = [
        PointStruct(
            id=entry['id'],
            vector=embedding,
            payload=entry['metadata']
        )
        for entry, embedding in zip(entries, embeddings)
    ]
    
    # Upload
    client.upsert(collection_name=collection_name, points=points)
    print(f"Uploaded {len(entries)} entries to Qdrant")

# MAIN EXECUTION
if __name__ == "__main__":
    print("Loading data...")
    entries = load_data()
    
    print(f"Generating embeddings for {len(entries)} entries...")
    texts = [entry['text'] for entry in entries]
    
    # Choose your embedding method
    # embeddings = generate_embeddings_openai(texts)
    embeddings = generate_embeddings_sentence_transformers(texts)
    
    print(f"Generated {len(embeddings)} embeddings")
    
    # Choose your vector store
    print("Uploading to vector store...")
    # upload_to_pinecone(entries, embeddings)
    upload_to_chromadb(entries, embeddings)
    # upload_to_weaviate(entries, embeddings)
    # upload_to_qdrant(entries, embeddings)
    
    print("✓ Complete!")
    print(f"\nYou can now query the vector store for similar functions.")
    print(f"Example: 'find functions related to sorting arrays'")
