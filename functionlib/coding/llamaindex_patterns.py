"""
Advanced LlamaIndex patterns for RAG and document processing.

Provides document loaders, index builders, query engines, and advanced RAG patterns.
Pure Python implementations compatible with LlamaIndex concepts.
"""

import json
import re
from typing import Any, Callable, Dict, List, Optional, Tuple
from collections import defaultdict
import hashlib


class Document:
    """Document with content and metadata."""
    
    def __init__(self, text: str, metadata: Optional[Dict] = None, doc_id: Optional[str] = None):
        self.text = text
        self.metadata = metadata or {}
        self.doc_id = doc_id or hashlib.md5(text.encode()).hexdigest()[:16]
        self.embedding = None
    
    def to_dict(self) -> Dict:
        """Convert to dictionary."""
        return {
            'doc_id': self.doc_id,
            'text': self.text,
            'metadata': self.metadata,
            'has_embedding': self.embedding is not None
        }


class Node:
    """A node in the index representing a text chunk."""
    
    def __init__(self, text: str, doc_id: str, metadata: Optional[Dict] = None):
        self.node_id = hashlib.md5(f"{doc_id}{text}".encode()).hexdigest()[:16]
        self.text = text
        self.doc_id = doc_id
        self.metadata = metadata or {}
        self.embedding = None
        self.relationships = {}  # prev, next, parent, child
    
    def add_relationship(self, rel_type: str, node: 'Node'):
        """Add relationship to another node."""
        self.relationships[rel_type] = node


class VectorStoreIndex:
    """Vector store index for documents."""
    
    def __init__(self, embedding_fn: Optional[Callable] = None):
        self.nodes = []
        self.embedding_fn = embedding_fn or self._simple_embedding
        self.metadata_filters = {}
    
    def _simple_embedding(self, text: str) -> List[float]:
        """Simple hash-based embedding."""
        from functionlib.coding.rag import simple_embedding
        return simple_embedding(text)
    
    @classmethod
    def from_documents(cls, documents: List[Document], chunk_size: int = 512,
                      embedding_fn: Optional[Callable] = None) -> 'VectorStoreIndex':
        """Create index from documents."""
        from functionlib.coding.rag import chunk_text
        
        index = cls(embedding_fn)
        
        for doc in documents:
            # Chunk document
            chunks = chunk_text(doc.text, chunk_size=chunk_size, overlap=50)
            
            prev_node = None
            for chunk in chunks:
                # Create node
                node = Node(chunk, doc.doc_id, doc.metadata.copy())
                node.embedding = index.embedding_fn(chunk)
                
                # Link to previous chunk
                if prev_node:
                    node.add_relationship('prev', prev_node)
                    prev_node.add_relationship('next', node)
                
                index.nodes.append(node)
                prev_node = node
        
        return index
    
    def as_query_engine(self, similarity_top_k: int = 3) -> 'QueryEngine':
        """Create a query engine from the index."""
        return QueryEngine(self, similarity_top_k=similarity_top_k)
    
    def as_retriever(self, similarity_top_k: int = 5) -> 'Retriever':
        """Create a retriever from the index."""
        return Retriever(self, similarity_top_k=similarity_top_k)
    
    def search(self, query_embedding: List[float], top_k: int = 5,
              filters: Optional[Dict] = None) -> List[Tuple[Node, float]]:
        """Search for similar nodes."""
        from functionlib.coding.rag import cosine_similarity
        
        results = []
        
        for node in self.nodes:
            # Apply metadata filters
            if filters:
                if not all(node.metadata.get(k) == v for k, v in filters.items()):
                    continue
            
            if node.embedding:
                similarity = cosine_similarity(query_embedding, node.embedding)
                results.append((node, similarity))
        
        # Sort by similarity
        results.sort(key=lambda x: x[1], reverse=True)
        
        return results[:top_k]


class QueryEngine:
    """Query engine for answering questions."""
    
    def __init__(self, index: VectorStoreIndex, similarity_top_k: int = 3,
                 llm_fn: Optional[Callable] = None):
        self.index = index
        self.similarity_top_k = similarity_top_k
        self.llm_fn = llm_fn or self._mock_llm
    
    def _mock_llm(self, prompt: str) -> str:
        """Mock LLM response."""
        return f"Answer based on context"
    
    def query(self, query: str) -> Dict[str, Any]:
        """Query the index and generate answer."""
        # Get query embedding
        query_embedding = self.index.embedding_fn(query)
        
        # Retrieve relevant nodes
        results = self.index.search(query_embedding, top_k=self.similarity_top_k)
        
        # Build context from nodes
        context = "\n\n".join([f"[{i+1}] {node.text}" for i, (node, score) in enumerate(results)])
        
        # Create prompt
        prompt = f"""Context information:
{context}

Question: {query}

Answer the question based on the context above. If the context doesn't contain relevant information, say so."""
        
        # Generate answer
        answer = self.llm_fn(prompt)
        
        return {
            'response': answer,
            'source_nodes': [node for node, _ in results],
            'metadata': {
                'query': query,
                'similarity_scores': [score for _, score in results]
            }
        }


class Retriever:
    """Retriever for getting relevant documents."""
    
    def __init__(self, index: VectorStoreIndex, similarity_top_k: int = 5):
        self.index = index
        self.similarity_top_k = similarity_top_k
    
    def retrieve(self, query: str) -> List[Node]:
        """Retrieve relevant nodes."""
        query_embedding = self.index.embedding_fn(query)
        results = self.index.search(query_embedding, top_k=self.similarity_top_k)
        return [node for node, _ in results]


class SentenceWindowRetriever(Retriever):
    """Retriever that expands to surrounding sentences."""
    
    def __init__(self, index: VectorStoreIndex, similarity_top_k: int = 5,
                 window_size: int = 1):
        super().__init__(index, similarity_top_k)
        self.window_size = window_size
    
    def retrieve(self, query: str) -> List[Node]:
        """Retrieve with sentence window expansion."""
        base_nodes = super().retrieve(query)
        
        expanded_nodes = []
        for node in base_nodes:
            # Add previous nodes
            current = node
            for _ in range(self.window_size):
                prev = current.relationships.get('prev')
                if prev:
                    expanded_nodes.append(prev)
                    current = prev
            
            expanded_nodes.append(node)
            
            # Add next nodes
            current = node
            for _ in range(self.window_size):
                next_node = current.relationships.get('next')
                if next_node:
                    expanded_nodes.append(next_node)
                    current = next_node
        
        # Remove duplicates while preserving order
        seen = set()
        unique_nodes = []
        for node in expanded_nodes:
            if node.node_id not in seen:
                seen.add(node.node_id)
                unique_nodes.append(node)
        
        return unique_nodes


class HybridRetriever(Retriever):
    """Combines multiple retrieval strategies."""
    
    def __init__(self, retrievers: List[Retriever], weights: Optional[List[float]] = None):
        self.retrievers = retrievers
        self.weights = weights or [1.0] * len(retrievers)
    
    def retrieve(self, query: str) -> List[Node]:
        """Retrieve using multiple strategies and combine."""
        all_results = []
        
        for retriever, weight in zip(self.retrievers, self.weights):
            nodes = retriever.retrieve(query)
            for i, node in enumerate(nodes):
                # Score based on rank and weight
                score = weight * (1.0 / (i + 1))
                all_results.append((node, score))
        
        # Aggregate scores for same nodes
        node_scores = defaultdict(float)
        node_map = {}
        for node, score in all_results:
            node_scores[node.node_id] += score
            node_map[node.node_id] = node
        
        # Sort by aggregated score
        sorted_nodes = sorted(
            node_scores.items(),
            key=lambda x: x[1],
            reverse=True
        )
        
        return [node_map[node_id] for node_id, _ in sorted_nodes]


class ResponseSynthesizer:
    """Synthesize responses from retrieved nodes."""
    
    def __init__(self, llm_fn: Optional[Callable] = None, response_mode: str = "compact"):
        self.llm_fn = llm_fn or self._mock_llm
        self.response_mode = response_mode  # compact, tree_summarize, refine
    
    def _mock_llm(self, prompt: str) -> str:
        return "Synthesized response"
    
    def synthesize(self, query: str, nodes: List[Node]) -> str:
        """Synthesize response from nodes."""
        if self.response_mode == "compact":
            return self._compact_synthesis(query, nodes)
        elif self.response_mode == "tree_summarize":
            return self._tree_summarize(query, nodes)
        elif self.response_mode == "refine":
            return self._refine_synthesis(query, nodes)
        else:
            return self._compact_synthesis(query, nodes)
    
    def _compact_synthesis(self, query: str, nodes: List[Node]) -> str:
        """Compact all context into one prompt."""
        context = "\n\n".join([node.text for node in nodes])
        prompt = f"Context:\n{context}\n\nQuestion: {query}\n\nAnswer:"
        return self.llm_fn(prompt)
    
    def _tree_summarize(self, query: str, nodes: List[Node]) -> str:
        """Hierarchical summarization."""
        # Group nodes and summarize in batches
        batch_size = 3
        summaries = []
        
        for i in range(0, len(nodes), batch_size):
            batch = nodes[i:i+batch_size]
            context = "\n\n".join([node.text for node in batch])
            prompt = f"Summarize this context:\n{context}"
            summary = self.llm_fn(prompt)
            summaries.append(summary)
        
        # Final synthesis
        final_context = "\n\n".join(summaries)
        final_prompt = f"Context:\n{final_context}\n\nQuestion: {query}\n\nAnswer:"
        return self.llm_fn(final_prompt)
    
    def _refine_synthesis(self, query: str, nodes: List[Node]) -> str:
        """Iteratively refine answer with each node."""
        answer = "No information available."
        
        for node in nodes:
            prompt = f"""Current Answer: {answer}

New Context: {node.text}

Question: {query}

Refine the answer based on the new context:"""
            
            answer = self.llm_fn(prompt)
        
        return answer


class SubQuestionQueryEngine:
    """Break down complex queries into sub-questions."""
    
    def __init__(self, query_engines: Dict[str, QueryEngine], llm_fn: Optional[Callable] = None):
        self.query_engines = query_engines
        self.llm_fn = llm_fn or self._mock_llm
    
    def _mock_llm(self, prompt: str) -> str:
        return "Mock response"
    
    def query(self, query: str) -> Dict[str, Any]:
        """Break query into sub-questions and answer each."""
        # Generate sub-questions
        sub_questions = self._generate_sub_questions(query)
        
        # Answer each sub-question
        sub_answers = []
        for sub_q in sub_questions:
            # Route to appropriate engine
            engine = self._route_question(sub_q)
            result = engine.query(sub_q)
            sub_answers.append({
                'question': sub_q,
                'answer': result['response']
            })
        
        # Synthesize final answer
        final_answer = self._synthesize_final_answer(query, sub_answers)
        
        return {
            'response': final_answer,
            'sub_questions': sub_questions,
            'sub_answers': sub_answers
        }
    
    def _generate_sub_questions(self, query: str) -> List[str]:
        """Generate sub-questions from main query."""
        prompt = f"""Break down this complex question into 2-3 simpler sub-questions:

Question: {query}

Sub-questions:
1."""
        
        response = self.llm_fn(prompt)
        
        # Parse sub-questions (simplified)
        lines = response.split('\n')
        sub_questions = [line.strip() for line in lines if line.strip() and any(c.isalnum() for c in line)]
        
        return sub_questions[:3] if sub_questions else [query]
    
    def _route_question(self, question: str) -> QueryEngine:
        """Route question to appropriate query engine."""
        # Simple keyword-based routing
        question_lower = question.lower()
        
        for key, engine in self.query_engines.items():
            if key.lower() in question_lower:
                return engine
        
        # Default to first engine
        return list(self.query_engines.values())[0]
    
    def _synthesize_final_answer(self, query: str, sub_answers: List[Dict]) -> str:
        """Synthesize final answer from sub-answers."""
        context = "\n\n".join([
            f"Q: {sa['question']}\nA: {sa['answer']}"
            for sa in sub_answers
        ])
        
        prompt = f"""Based on these sub-question answers:

{context}

Provide a comprehensive answer to: {query}"""
        
        return self.llm_fn(prompt)


class ContextualCompressionRetriever:
    """Compress retrieved context to most relevant parts."""
    
    def __init__(self, base_retriever: Retriever, llm_fn: Optional[Callable] = None):
        self.base_retriever = base_retriever
        self.llm_fn = llm_fn or self._mock_llm
    
    def _mock_llm(self, prompt: str) -> str:
        return "Compressed content"
    
    def retrieve(self, query: str) -> List[Node]:
        """Retrieve and compress context."""
        # Get base results
        nodes = self.base_retriever.retrieve(query)
        
        # Compress each node
        compressed_nodes = []
        for node in nodes:
            compressed_text = self._compress_node(query, node)
            
            # Create new node with compressed content
            compressed_node = Node(compressed_text, node.doc_id, node.metadata)
            compressed_node.embedding = node.embedding
            compressed_nodes.append(compressed_node)
        
        return compressed_nodes
    
    def _compress_node(self, query: str, node: Node) -> str:
        """Compress node content to relevant parts."""
        prompt = f"""Extract only the parts relevant to the question.

Question: {query}

Content: {node.text}

Relevant excerpts:"""
        
        return self.llm_fn(prompt)


def create_document_summary_index(documents: List[Document], llm_fn: Optional[Callable] = None) -> Dict:
    """Create an index of document summaries."""
    summaries = {}
    
    llm = llm_fn or (lambda p: "Summary of document")
    
    for doc in documents:
        prompt = f"Summarize this document in 2-3 sentences:\n\n{doc.text[:1000]}"
        summary = llm(prompt)
        summaries[doc.doc_id] = {
            'summary': summary,
            'metadata': doc.metadata,
            'full_text': doc.text
        }
    
    return summaries


def create_knowledge_graph(documents: List[Document]) -> Dict:
    """Extract entities and relationships to create knowledge graph."""
    graph = {
        'entities': {},
        'relationships': []
    }
    
    for doc in documents:
        # Extract entities (simplified - use NER in production)
        entities = re.findall(r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*\b', doc.text)
        
        for entity in entities:
            if entity not in graph['entities']:
                graph['entities'][entity] = {
                    'name': entity,
                    'mentions': 0,
                    'documents': []
                }
            
            graph['entities'][entity]['mentions'] += 1
            if doc.doc_id not in graph['entities'][entity]['documents']:
                graph['entities'][entity]['documents'].append(doc.doc_id)
    
    return graph


__all__ = [
    'Document',
    'Node',
    'VectorStoreIndex',
    'QueryEngine',
    'Retriever',
    'SentenceWindowRetriever',
    'HybridRetriever',
    'ResponseSynthesizer',
    'SubQuestionQueryEngine',
    'ContextualCompressionRetriever',
    'create_document_summary_index',
    'create_knowledge_graph'
]
