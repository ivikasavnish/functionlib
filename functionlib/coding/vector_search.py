"""Vector operations and similarity search (pure Python implementation)."""

import math
from typing import List, Tuple, Dict, Callable, Optional, Any

__all__ = [
    'cosine_similarity',
    'euclidean_distance',
    'manhattan_distance',
    'dot_product',
    'vector_norm',
    'normalize_vector',
    'vector_add',
    'vector_subtract',
    'vector_multiply',
    'vector_mean',
    'jaccard_similarity',
    'hamming_distance',
    'minkowski_distance',
    'pearson_correlation',
    'spearman_correlation',
    'knn_search',
    'nearest_neighbors',
    'vector_database',
    'semantic_search',
    'cluster_vectors',
    'dimension_reduce_pca',
    'vector_to_text_hash',
    'text_to_vector',
    'tfidf_vector',
    'create_embedding_index',
]

def cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Calculate cosine similarity between two vectors.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Cosine similarity (-1 to 1)
        
    Example:
        >>> v1 = [1, 2, 3]
        >>> v2 = [4, 5, 6]
        >>> cosine_similarity(v1, v2)
        0.974...
    """
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    
    if norm1 == 0 or norm2 == 0:
        return 0.0
    
    return dot / (norm1 * norm2)

def euclidean_distance(v1: List[float], v2: List[float]) -> float:
    """Calculate Euclidean distance between vectors.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Euclidean distance
        
    Example:
        >>> euclidean_distance([0, 0], [3, 4])
        5.0
    """
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(v1, v2)))

def manhattan_distance(v1: List[float], v2: List[float]) -> float:
    """Calculate Manhattan distance between vectors.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Manhattan distance
        
    Example:
        >>> manhattan_distance([0, 0], [3, 4])
        7.0
    """
    return sum(abs(a - b) for a, b in zip(v1, v2))

def dot_product(v1: List[float], v2: List[float]) -> float:
    """Calculate dot product of two vectors.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Dot product
        
    Example:
        >>> dot_product([1, 2, 3], [4, 5, 6])
        32
    """
    return sum(a * b for a, b in zip(v1, v2))

def vector_norm(v: List[float], p: int = 2) -> float:
    """Calculate p-norm of vector.
    
    Args:
        v: Vector
        p: Norm type (1=Manhattan, 2=Euclidean)
        
    Returns:
        Vector norm
        
    Example:
        >>> vector_norm([3, 4], 2)
        5.0
    """
    if p == 2:
        return math.sqrt(sum(x ** 2 for x in v))
    elif p == 1:
        return sum(abs(x) for x in v)
    else:
        return sum(abs(x) ** p for x in v) ** (1/p)

def normalize_vector(v: List[float]) -> List[float]:
    """Normalize vector to unit length.
    
    Args:
        v: Vector to normalize
        
    Returns:
        Normalized vector
        
    Example:
        >>> normalize_vector([3, 4])
        [0.6, 0.8]
    """
    norm = vector_norm(v)
    if norm == 0:
        return v
    return [x / norm for x in v]

def vector_add(v1: List[float], v2: List[float]) -> List[float]:
    """Add two vectors.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Sum vector
        
    Example:
        >>> vector_add([1, 2], [3, 4])
        [4, 6]
    """
    return [a + b for a, b in zip(v1, v2)]

def vector_subtract(v1: List[float], v2: List[float]) -> List[float]:
    """Subtract two vectors.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Difference vector
        
    Example:
        >>> vector_subtract([5, 7], [2, 3])
        [3, 4]
    """
    return [a - b for a, b in zip(v1, v2)]

def vector_multiply(v: List[float], scalar: float) -> List[float]:
    """Multiply vector by scalar.
    
    Args:
        v: Vector
        scalar: Scalar value
        
    Returns:
        Scaled vector
        
    Example:
        >>> vector_multiply([1, 2, 3], 2)
        [2, 4, 6]
    """
    return [x * scalar for x in v]

def vector_mean(vectors: List[List[float]]) -> List[float]:
    """Calculate mean of multiple vectors.
    
    Args:
        vectors: List of vectors
        
    Returns:
        Mean vector
        
    Example:
        >>> vector_mean([[1, 2], [3, 4], [5, 6]])
        [3.0, 4.0]
    """
    if not vectors:
        return []
    
    n = len(vectors)
    dim = len(vectors[0])
    
    return [sum(v[i] for v in vectors) / n for i in range(dim)]

def jaccard_similarity(s1: set, s2: set) -> float:
    """Calculate Jaccard similarity between sets.
    
    Args:
        s1: First set
        s2: Second set
        
    Returns:
        Jaccard similarity (0 to 1)
        
    Example:
        >>> jaccard_similarity({1, 2, 3}, {2, 3, 4})
        0.5
    """
    intersection = len(s1 & s2)
    union = len(s1 | s2)
    
    return intersection / union if union > 0 else 0.0

def hamming_distance(v1: List[int], v2: List[int]) -> int:
    """Calculate Hamming distance between binary vectors.
    
    Args:
        v1: First binary vector
        v2: Second binary vector
        
    Returns:
        Hamming distance
        
    Example:
        >>> hamming_distance([1, 0, 1, 1], [1, 1, 1, 0])
        2
    """
    return sum(a != b for a, b in zip(v1, v2))

def minkowski_distance(v1: List[float], v2: List[float], p: int = 2) -> float:
    """Calculate Minkowski distance.
    
    Args:
        v1: First vector
        v2: Second vector
        p: Parameter (1=Manhattan, 2=Euclidean)
        
    Returns:
        Minkowski distance
        
    Example:
        >>> minkowski_distance([0, 0], [3, 4], 2)
        5.0
    """
    return sum(abs(a - b) ** p for a, b in zip(v1, v2)) ** (1/p)

def pearson_correlation(v1: List[float], v2: List[float]) -> float:
    """Calculate Pearson correlation coefficient.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Pearson correlation (-1 to 1)
        
    Example:
        >>> pearson_correlation([1, 2, 3, 4], [2, 4, 6, 8])
        1.0
    """
    n = len(v1)
    mean1 = sum(v1) / n
    mean2 = sum(v2) / n
    
    numerator = sum((v1[i] - mean1) * (v2[i] - mean2) for i in range(n))
    denom1 = math.sqrt(sum((v1[i] - mean1) ** 2 for i in range(n)))
    denom2 = math.sqrt(sum((v2[i] - mean2) ** 2 for i in range(n)))
    
    if denom1 == 0 or denom2 == 0:
        return 0.0
    
    return numerator / (denom1 * denom2)

def spearman_correlation(v1: List[float], v2: List[float]) -> float:
    """Calculate Spearman rank correlation.
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Spearman correlation (-1 to 1)
        
    Example:
        >>> spearman_correlation([1, 2, 3, 4], [1, 3, 2, 4])
        0.8
    """
    def rank(v):
        sorted_v = sorted(enumerate(v), key=lambda x: x[1])
        ranks = [0] * len(v)
        for rank_val, (idx, _) in enumerate(sorted_v, 1):
            ranks[idx] = rank_val
        return ranks
    
    ranks1 = rank(v1)
    ranks2 = rank(v2)
    
    return pearson_correlation(ranks1, ranks2)

def knn_search(query: List[float], vectors: List[List[float]], k: int = 5,
               metric: str = 'cosine') -> List[Tuple[int, float]]:
    """Find k nearest neighbors.
    
    Args:
        query: Query vector
        vectors: Database vectors
        k: Number of neighbors
        metric: Distance metric ('cosine', 'euclidean', 'manhattan')
        
    Returns:
        List of (index, distance) tuples
        
    Example:
        >>> vectors = [[1, 0], [0, 1], [1, 1]]
        >>> knn_search([0.9, 0.1], vectors, k=2)
        [(0, ...), (2, ...)]
    """
    if metric == 'cosine':
        distances = [(i, 1 - cosine_similarity(query, v)) for i, v in enumerate(vectors)]
    elif metric == 'euclidean':
        distances = [(i, euclidean_distance(query, v)) for i, v in enumerate(vectors)]
    elif metric == 'manhattan':
        distances = [(i, manhattan_distance(query, v)) for i, v in enumerate(vectors)]
    else:
        raise ValueError(f"Unknown metric: {metric}")
    
    distances.sort(key=lambda x: x[1])
    return distances[:k]

def nearest_neighbors(query: List[float], vectors: List[List[float]],
                     threshold: float = 0.8, metric: str = 'cosine') -> List[int]:
    """Find all neighbors above similarity threshold.
    
    Args:
        query: Query vector
        vectors: Database vectors
        threshold: Similarity threshold
        metric: Similarity metric
        
    Returns:
        List of matching indices
        
    Example:
        >>> vectors = [[1, 0], [0.9, 0.1], [0, 1]]
        >>> nearest_neighbors([1, 0], vectors, threshold=0.9)
        [0, 1]
    """
    neighbors = []
    
    for i, v in enumerate(vectors):
        if metric == 'cosine':
            similarity = cosine_similarity(query, v)
            if similarity >= threshold:
                neighbors.append(i)
    
    return neighbors

def vector_database(vectors: List[List[float]], metadata: Optional[List[Dict]] = None) -> Dict:
    """Create simple vector database.
    
    Args:
        vectors: List of vectors
        metadata: Optional metadata for each vector
        
    Returns:
        Database dict
        
    Example:
        >>> db = vector_database([[1, 0], [0, 1]], [{'id': 'a'}, {'id': 'b'}])
        >>> len(db['vectors'])
        2
    """
    return {
        'vectors': vectors,
        'metadata': metadata or [{} for _ in vectors],
        'size': len(vectors),
        'dimension': len(vectors[0]) if vectors else 0
    }

def semantic_search(query: List[float], db: Dict, k: int = 5) -> List[Dict]:
    """Semantic search in vector database.
    
    Args:
        query: Query vector
        db: Vector database
        k: Number of results
        
    Returns:
        List of results with metadata and scores
        
    Example:
        >>> db = vector_database([[1, 0], [0, 1]], [{'text': 'a'}, {'text': 'b'}])
        >>> results = semantic_search([0.9, 0.1], db, k=1)
        >>> len(results) == 1
        True
    """
    neighbors = knn_search(query, db['vectors'], k=k, metric='cosine')
    
    results = []
    for idx, distance in neighbors:
        score = 1 - distance  # Convert distance to similarity
        results.append({
            'index': idx,
            'score': score,
            'metadata': db['metadata'][idx]
        })
    
    return results

def cluster_vectors(vectors: List[List[float]], n_clusters: int = 3) -> List[int]:
    """Simple k-means clustering of vectors.
    
    Args:
        vectors: List of vectors
        n_clusters: Number of clusters
        
    Returns:
        Cluster assignments
        
    Example:
        >>> vectors = [[1, 1], [1.5, 1.5], [10, 10], [10.5, 10.5]]
        >>> labels = cluster_vectors(vectors, n_clusters=2)
        >>> len(set(labels)) == 2
        True
    """
    import random
    
    # Initialize centroids randomly
    centroids = random.sample(vectors, n_clusters)
    
    for _ in range(100):  # Max iterations
        # Assign to nearest centroid
        labels = []
        for v in vectors:
            distances = [euclidean_distance(v, c) for c in centroids]
            labels.append(distances.index(min(distances)))
        
        # Update centroids
        new_centroids = []
        for i in range(n_clusters):
            cluster_vectors = [vectors[j] for j in range(len(vectors)) if labels[j] == i]
            if cluster_vectors:
                new_centroids.append(vector_mean(cluster_vectors))
            else:
                new_centroids.append(centroids[i])
        
        # Check convergence
        if all(euclidean_distance(new_centroids[i], centroids[i]) < 1e-6 
               for i in range(n_clusters)):
            break
        
        centroids = new_centroids
    
    return labels

def dimension_reduce_pca(vectors: List[List[float]], n_components: int = 2) -> List[List[float]]:
    """Simple PCA dimension reduction (approximate).
    
    Args:
        vectors: High-dimensional vectors
        n_components: Target dimensions
        
    Returns:
        Reduced vectors
        
    Example:
        >>> vectors = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
        >>> reduced = dimension_reduce_pca(vectors, n_components=2)
        >>> len(reduced[0]) == 2
        True
    """
    # Center the data
    mean = vector_mean(vectors)
    centered = [vector_subtract(v, mean) for v in vectors]
    
    # Simplified: just take first n_components dimensions
    # (Real PCA would compute covariance matrix and eigenvectors)
    return [[v[i] for i in range(min(n_components, len(v)))] for v in centered]

def vector_to_text_hash(vector: List[float], precision: int = 3) -> str:
    """Convert vector to text hash for deduplication.
    
    Args:
        vector: Vector to hash
        precision: Decimal precision
        
    Returns:
        Hash string
        
    Example:
        >>> vector_to_text_hash([1.234, 5.678])
        '1.234_5.678'
    """
    return '_'.join(f'{x:.{precision}f}' for x in vector)

def text_to_vector(text: str, dimension: int = 100) -> List[float]:
    """Simple text to vector conversion (character-based hashing).
    
    Args:
        text: Input text
        dimension: Vector dimension
        
    Returns:
        Vector representation
        
    Example:
        >>> v = text_to_vector("hello", dimension=10)
        >>> len(v) == 10
        True
    """
    vector = [0.0] * dimension
    
    for i, char in enumerate(text):
        idx = (hash(char) + i) % dimension
        vector[idx] += 1.0
    
    # Normalize
    return normalize_vector(vector)

def tfidf_vector(document: str, vocabulary: List[str], 
                 idf_scores: Dict[str, float]) -> List[float]:
    """Create TF-IDF vector for document.
    
    Args:
        document: Document text
        vocabulary: Vocabulary list
        idf_scores: IDF scores for each term
        
    Returns:
        TF-IDF vector
        
    Example:
        >>> vocab = ['hello', 'world']
        >>> idf = {'hello': 1.0, 'world': 1.5}
        >>> v = tfidf_vector('hello world hello', vocab, idf)
        >>> len(v) == 2
        True
    """
    words = document.lower().split()
    word_count = {}
    for word in words:
        word_count[word] = word_count.get(word, 0) + 1
    
    vector = []
    for term in vocabulary:
        tf = word_count.get(term, 0) / len(words) if words else 0
        idf = idf_scores.get(term, 0)
        vector.append(tf * idf)
    
    return vector

def create_embedding_index(vectors: List[List[float]], 
                           ids: Optional[List[str]] = None) -> Dict:
    """Create searchable embedding index.
    
    Args:
        vectors: Embedding vectors
        ids: Optional IDs for each vector
        
    Returns:
        Index structure
        
    Example:
        >>> vectors = [[1, 0], [0, 1]]
        >>> index = create_embedding_index(vectors, ids=['a', 'b'])
        >>> index['size']
        2
    """
    if ids is None:
        ids = [str(i) for i in range(len(vectors))]
    
    return {
        'vectors': vectors,
        'ids': ids,
        'id_to_idx': {id_: i for i, id_ in enumerate(ids)},
        'size': len(vectors),
        'dimension': len(vectors[0]) if vectors else 0
    }
