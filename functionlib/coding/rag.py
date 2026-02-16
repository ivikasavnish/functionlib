"""
RAG (Retrieval Augmented Generation) utilities.

Pure Python implementations of RAG components including vector stores,
embeddings, document chunking, and retrieval strategies.
"""

import json
import math
import re
from collections import defaultdict
from typing import List, Dict, Any, Tuple, Optional, Callable
import hashlib


def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    """Calculate cosine similarity between two vectors."""
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have same length")
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = math.sqrt(sum(a * a for a in vec1))
    magnitude2 = math.sqrt(sum(b * b for b in vec2))
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)


def euclidean_distance(vec1: List[float], vec2: List[float]) -> float:
    """Calculate Euclidean distance between two vectors."""
    if len(vec1) != len(vec2):
        raise ValueError("Vectors must have same length")
    
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(vec1, vec2)))


def simple_embedding(text: str, dimensions: int = 384) -> List[float]:
    """
    Create a simple deterministic embedding from text.
    
    This is a basic implementation using character frequencies and n-grams.
    For production, use sentence-transformers or OpenAI embeddings.
    """
    # Normalize text
    text = text.lower().strip()
    
    # Create hash-based embedding
    embedding = [0.0] * dimensions
    
    # Character frequency features
    for i, char in enumerate(text):
        idx = (ord(char) + i) % dimensions
        embedding[idx] += 1.0
    
    # Bigram features
    for i in range(len(text) - 1):
        bigram = text[i:i+2]
        hash_val = int(hashlib.md5(bigram.encode()).hexdigest(), 16)
        idx = hash_val % dimensions
        embedding[idx] += 0.5
    
    # Normalize
    magnitude = math.sqrt(sum(x * x for x in embedding))
    if magnitude > 0:
        embedding = [x / magnitude for x in embedding]
    
    return embedding


def chunk_text(text: str, chunk_size: int = 512, overlap: int = 50) -> List[str]:
    """Split text into overlapping chunks."""
    if chunk_size <= 0:
        raise ValueError("chunk_size must be positive")
    
    chunks = []
    words = text.split()
    
    for i in range(0, len(words), chunk_size - overlap):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk:
            chunks.append(chunk)
    
    return chunks


def chunk_by_sentences(text: str, max_chunk_size: int = 512) -> List[str]:
    """Split text into chunks by sentences, respecting max size."""
    # Simple sentence splitting
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    chunks = []
    current_chunk = []
    current_size = 0
    
    for sentence in sentences:
        sentence_len = len(sentence.split())
        
        if current_size + sentence_len > max_chunk_size and current_chunk:
            chunks.append(" ".join(current_chunk))
            current_chunk = []
            current_size = 0
        
        current_chunk.append(sentence)
        current_size += sentence_len
    
    if current_chunk:
        chunks.append(" ".join(current_chunk))
    
    return chunks


class InMemoryVectorStore:
    """Simple in-memory vector store for RAG applications."""
    
    def __init__(self, embedding_dim: int = 384):
        self.embedding_dim = embedding_dim
        self.documents = []
        self.embeddings = []
        self.metadata = []
    
    def add_document(self, text: str, embedding: List[float], metadata: Optional[Dict] = None):
        """Add a document with its embedding."""
        if len(embedding) != self.embedding_dim:
            raise ValueError(f"Embedding dimension mismatch: expected {self.embedding_dim}, got {len(embedding)}")
        
        self.documents.append(text)
        self.embeddings.append(embedding)
        self.metadata.append(metadata or {})
    
    def add_documents(self, documents: List[str], embeddings: List[List[float]], metadata: Optional[List[Dict]] = None):
        """Add multiple documents at once."""
        if len(documents) != len(embeddings):
            raise ValueError("Number of documents must match number of embeddings")
        
        metadata = metadata or [{}] * len(documents)
        
        for doc, emb, meta in zip(documents, embeddings, metadata):
            self.add_document(doc, emb, meta)
    
    def search(self, query_embedding: List[float], top_k: int = 5, threshold: float = 0.0) -> List[Dict[str, Any]]:
        """Search for similar documents using cosine similarity."""
        if len(query_embedding) != self.embedding_dim:
            raise ValueError(f"Query embedding dimension mismatch")
        
        results = []
        
        for i, doc_embedding in enumerate(self.embeddings):
            similarity = cosine_similarity(query_embedding, doc_embedding)
            
            if similarity >= threshold:
                results.append({
                    'document': self.documents[i],
                    'score': similarity,
                    'metadata': self.metadata[i],
                    'index': i
                })
        
        # Sort by score descending
        results.sort(key=lambda x: x['score'], reverse=True)
        
        return results[:top_k]
    
    def delete_document(self, index: int):
        """Delete a document by index."""
        if 0 <= index < len(self.documents):
            del self.documents[index]
            del self.embeddings[index]
            del self.metadata[index]
    
    def clear(self):
        """Clear all documents."""
        self.documents.clear()
        self.embeddings.clear()
        self.metadata.clear()
    
    def size(self) -> int:
        """Return number of documents."""
        return len(self.documents)
    
    def save(self, filepath: str):
        """Save vector store to file."""
        data = {
            'embedding_dim': self.embedding_dim,
            'documents': self.documents,
            'embeddings': self.embeddings,
            'metadata': self.metadata
        }
        with open(filepath, 'w') as f:
            json.dump(data, f)
    
    def load(self, filepath: str):
        """Load vector store from file."""
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        self.embedding_dim = data['embedding_dim']
        self.documents = data['documents']
        self.embeddings = data['embeddings']
        self.metadata = data['metadata']


def bm25_score(query_terms: List[str], document: str, corpus: List[str], k1: float = 1.5, b: float = 0.75) -> float:
    """
    Calculate BM25 score for a document given query terms.
    
    BM25 is a ranking function used in information retrieval.
    """
    doc_terms = document.lower().split()
    doc_len = len(doc_terms)
    
    # Calculate average document length
    avg_doc_len = sum(len(doc.split()) for doc in corpus) / len(corpus) if corpus else 1
    
    # Calculate document frequency for each term
    df = {}
    for term in set(query_terms):
        df[term] = sum(1 for doc in corpus if term in doc.lower())
    
    # Calculate BM25 score
    score = 0.0
    N = len(corpus)
    
    for term in query_terms:
        term = term.lower()
        if term not in doc_terms:
            continue
        
        # Term frequency
        tf = doc_terms.count(term)
        
        # Inverse document frequency
        n = df.get(term, 0)
        idf = math.log((N - n + 0.5) / (n + 0.5) + 1.0)
        
        # BM25 formula
        numerator = tf * (k1 + 1)
        denominator = tf + k1 * (1 - b + b * (doc_len / avg_doc_len))
        
        score += idf * (numerator / denominator)
    
    return score


def hybrid_search(query: str, query_embedding: List[float], vector_store: InMemoryVectorStore,
                  alpha: float = 0.5, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Hybrid search combining vector similarity and BM25 keyword matching.
    
    alpha: weight for vector search (1-alpha for BM25)
    """
    # Vector search
    vector_results = vector_store.search(query_embedding, top_k=top_k * 2)
    
    # BM25 search
    query_terms = query.lower().split()
    corpus = vector_store.documents
    
    bm25_scores = {}
    for i, doc in enumerate(corpus):
        bm25_scores[i] = bm25_score(query_terms, doc, corpus)
    
    # Combine scores
    combined_results = []
    for result in vector_results:
        idx = result['index']
        vector_score = result['score']
        bm25_score_val = bm25_scores.get(idx, 0.0)
        
        # Normalize BM25 score (simple min-max normalization)
        max_bm25 = max(bm25_scores.values()) if bm25_scores else 1.0
        normalized_bm25 = bm25_score_val / max_bm25 if max_bm25 > 0 else 0.0
        
        combined_score = alpha * vector_score + (1 - alpha) * normalized_bm25
        
        combined_results.append({
            'document': result['document'],
            'score': combined_score,
            'vector_score': vector_score,
            'bm25_score': bm25_score_val,
            'metadata': result['metadata'],
            'index': idx
        })
    
    # Sort by combined score
    combined_results.sort(key=lambda x: x['score'], reverse=True)
    
    return combined_results[:top_k]


def rerank_results(query: str, results: List[Dict[str, Any]], strategy: str = 'cross_encoder') -> List[Dict[str, Any]]:
    """
    Rerank search results using various strategies.
    
    Strategies: 'cross_encoder', 'keyword_boost', 'metadata_boost'
    """
    if strategy == 'keyword_boost':
        # Boost documents containing exact query terms
        query_terms = set(query.lower().split())
        
        for result in results:
            doc_terms = set(result['document'].lower().split())
            overlap = len(query_terms & doc_terms)
            boost = 1.0 + (overlap / len(query_terms)) * 0.3
            result['score'] *= boost
    
    elif strategy == 'metadata_boost':
        # Boost documents with certain metadata properties
        for result in results:
            metadata = result.get('metadata', {})
            if metadata.get('important'):
                result['score'] *= 1.2
            if metadata.get('recent'):
                result['score'] *= 1.1
    
    # Resort after reranking
    results.sort(key=lambda x: x['score'], reverse=True)
    
    return results


def create_rag_context(query: str, results: List[Dict[str, Any]], max_length: int = 2000) -> str:
    """
    Create a context string from search results for LLM prompting.
    """
    context_parts = []
    current_length = 0
    
    for i, result in enumerate(results):
        doc = result['document']
        score = result['score']
        
        # Format result
        part = f"[{i+1}] (Score: {score:.3f})\n{doc}\n"
        part_length = len(part)
        
        if current_length + part_length > max_length:
            break
        
        context_parts.append(part)
        current_length += part_length
    
    return "\n".join(context_parts)


def extract_keywords(text: str, top_k: int = 10) -> List[Tuple[str, float]]:
    """
    Extract keywords from text using TF-IDF-like scoring.
    """
    # Tokenize and clean
    words = re.findall(r'\b[a-zA-Z]{3,}\b', text.lower())
    
    # Calculate term frequency
    tf = defaultdict(int)
    for word in words:
        tf[word] += 1
    
    # Simple scoring based on frequency and length
    scores = {}
    for word, freq in tf.items():
        # Longer words and higher frequency get higher scores
        score = freq * math.log(len(word))
        scores[word] = score
    
    # Sort by score
    sorted_keywords = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    
    return sorted_keywords[:top_k]


def query_expansion(query: str, method: str = 'synonyms') -> List[str]:
    """
    Expand query with related terms.
    
    Methods: 'synonyms', 'related', 'misspellings'
    """
    expanded = [query]
    
    # Simple expansion rules (in production, use WordNet or embeddings)
    if method == 'synonyms':
        # Add common synonyms for technical terms
        synonym_map = {
            'error': ['bug', 'issue', 'problem', 'exception'],
            'function': ['method', 'procedure', 'routine'],
            'data': ['information', 'dataset', 'records'],
            'fast': ['quick', 'rapid', 'speedy'],
            'large': ['big', 'huge', 'massive']
        }
        
        for term, synonyms in synonym_map.items():
            if term in query.lower():
                for syn in synonyms[:2]:  # Add top 2 synonyms
                    expanded.append(query.replace(term, syn))
    
    elif method == 'related':
        # Add related technical terms
        query_lower = query.lower()
        if 'python' in query_lower:
            expanded.append(query + ' programming')
        if 'database' in query_lower:
            expanded.extend([query + ' SQL', query + ' query'])
    
    return expanded


class DocumentStore:
    """Store and manage documents for RAG."""
    
    def __init__(self):
        self.documents = {}
        self.next_id = 0
    
    def add_document(self, text: str, metadata: Optional[Dict] = None) -> str:
        """Add a document and return its ID."""
        doc_id = str(self.next_id)
        self.next_id += 1
        
        self.documents[doc_id] = {
            'text': text,
            'metadata': metadata or {},
            'created_at': None  # Would use datetime in production
        }
        
        return doc_id
    
    def get_document(self, doc_id: str) -> Optional[Dict]:
        """Retrieve a document by ID."""
        return self.documents.get(doc_id)
    
    def update_document(self, doc_id: str, text: str, metadata: Optional[Dict] = None):
        """Update an existing document."""
        if doc_id in self.documents:
            self.documents[doc_id]['text'] = text
            if metadata:
                self.documents[doc_id]['metadata'].update(metadata)
    
    def delete_document(self, doc_id: str):
        """Delete a document."""
        self.documents.pop(doc_id, None)
    
    def list_documents(self) -> List[str]:
        """List all document IDs."""
        return list(self.documents.keys())
    
    def search_by_metadata(self, key: str, value: Any) -> List[str]:
        """Search documents by metadata."""
        results = []
        for doc_id, doc in self.documents.items():
            if doc['metadata'].get(key) == value:
                results.append(doc_id)
        return results


def reciprocal_rank_fusion(results_list: List[List[Dict]], k: int = 60) -> List[Dict]:
    """
    Combine multiple ranking lists using Reciprocal Rank Fusion.
    
    Used to merge results from different retrieval strategies.
    """
    # Track scores for each document
    fusion_scores = defaultdict(float)
    doc_data = {}
    
    for results in results_list:
        for rank, result in enumerate(results):
            doc_key = result['document']
            
            # RRF formula
            score = 1.0 / (k + rank + 1)
            fusion_scores[doc_key] += score
            
            # Keep document data
            if doc_key not in doc_data:
                doc_data[doc_key] = result
    
    # Convert back to list format
    fused_results = []
    for doc_key, score in fusion_scores.items():
        result = doc_data[doc_key].copy()
        result['fusion_score'] = score
        fused_results.append(result)
    
    # Sort by fusion score
    fused_results.sort(key=lambda x: x['fusion_score'], reverse=True)
    
    return fused_results


__all__ = [
    'cosine_similarity',
    'euclidean_distance',
    'simple_embedding',
    'chunk_text',
    'chunk_by_sentences',
    'InMemoryVectorStore',
    'bm25_score',
    'hybrid_search',
    'rerank_results',
    'create_rag_context',
    'extract_keywords',
    'query_expansion',
    'DocumentStore',
    'reciprocal_rank_fusion'
]
