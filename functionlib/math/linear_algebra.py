"""
Linear Algebra Functions

Vectors, matrices, and linear algebra operations.
"""

import math
from typing import List, Tuple, Optional


# Type aliases
Vector = List[float]
Matrix = List[List[float]]


def vector_add(v1: Vector, v2: Vector) -> Vector:
    """
    Adds two vectors
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Sum vector
        
    Example:
        >>> vector_add([1, 2, 3], [4, 5, 6])
        [5, 7, 9]
    """
    if len(v1) != len(v2):
        raise ValueError("Vectors must have same dimension")
    
    return [a + b for a, b in zip(v1, v2)]


def vector_subtract(v1: Vector, v2: Vector) -> Vector:
    """
    Subtracts two vectors
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Difference vector
        
    Example:
        >>> vector_subtract([5, 7, 9], [1, 2, 3])
        [4, 5, 6]
    """
    if len(v1) != len(v2):
        raise ValueError("Vectors must have same dimension")
    
    return [a - b for a, b in zip(v1, v2)]


def vector_scalar_multiply(v: Vector, scalar: float) -> Vector:
    """
    Multiplies vector by scalar
    
    Args:
        v: Vector
        scalar: Scalar value
        
    Returns:
        Scaled vector
        
    Example:
        >>> vector_scalar_multiply([1, 2, 3], 2)
        [2, 4, 6]
    """
    return [scalar * x for x in v]


def dot_product(v1: Vector, v2: Vector) -> float:
    """
    Computes dot product of two vectors
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Dot product
        
    Example:
        >>> dot_product([1, 2, 3], [4, 5, 6])
        32
    """
    if len(v1) != len(v2):
        raise ValueError("Vectors must have same dimension")
    
    return sum(a * b for a, b in zip(v1, v2))


def vector_magnitude(v: Vector) -> float:
    """
    Computes magnitude (length) of vector
    
    Args:
        v: Vector
        
    Returns:
        Magnitude
        
    Example:
        >>> vector_magnitude([3, 4])
        5.0
    """
    return math.sqrt(sum(x ** 2 for x in v))


def vector_normalize(v: Vector) -> Vector:
    """
    Normalizes vector to unit length
    
    Args:
        v: Vector
        
    Returns:
        Unit vector
        
    Example:
        >>> vector_normalize([3, 4])
        [0.6, 0.8]
    """
    mag = vector_magnitude(v)
    
    if mag == 0:
        raise ValueError("Cannot normalize zero vector")
    
    return [x / mag for x in v]


def cross_product(v1: Vector, v2: Vector) -> Vector:
    """
    Computes cross product of two 3D vectors
    
    Args:
        v1: First 3D vector
        v2: Second 3D vector
        
    Returns:
        Cross product vector
        
    Example:
        >>> cross_product([1, 0, 0], [0, 1, 0])
        [0, 0, 1]
    """
    if len(v1) != 3 or len(v2) != 3:
        raise ValueError("Cross product requires 3D vectors")
    
    return [
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0]
    ]


def vector_angle(v1: Vector, v2: Vector) -> float:
    """
    Computes angle between two vectors (in radians)
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Angle in radians
        
    Example:
        >>> angle = vector_angle([1, 0], [0, 1])
        >>> abs(angle - 1.5708) < 0.001  # ~π/2
        True
    """
    dot = dot_product(v1, v2)
    mag1 = vector_magnitude(v1)
    mag2 = vector_magnitude(v2)
    
    if mag1 == 0 or mag2 == 0:
        raise ValueError("Cannot compute angle with zero vector")
    
    cos_angle = dot / (mag1 * mag2)
    cos_angle = max(-1, min(1, cos_angle))  # Clamp to [-1, 1]
    
    return math.acos(cos_angle)


def vector_projection(v: Vector, onto: Vector) -> Vector:
    """
    Projects vector v onto vector 'onto'
    
    Args:
        v: Vector to project
        onto: Vector to project onto
        
    Returns:
        Projection vector
        
    Example:
        >>> vector_projection([3, 4], [1, 0])
        [3.0, 0.0]
    """
    dot_prod = dot_product(v, onto)
    onto_mag_sq = sum(x ** 2 for x in onto)
    
    if onto_mag_sq == 0:
        raise ValueError("Cannot project onto zero vector")
    
    scalar = dot_prod / onto_mag_sq
    
    return [scalar * x for x in onto]


def matrix_add(m1: Matrix, m2: Matrix) -> Matrix:
    """
    Adds two matrices
    
    Args:
        m1: First matrix
        m2: Second matrix
        
    Returns:
        Sum matrix
        
    Example:
        >>> matrix_add([[1, 2], [3, 4]], [[5, 6], [7, 8]])
        [[6, 8], [10, 12]]
    """
    if len(m1) != len(m2) or len(m1[0]) != len(m2[0]):
        raise ValueError("Matrices must have same dimensions")
    
    return [[a + b for a, b in zip(row1, row2)] for row1, row2 in zip(m1, m2)]


def matrix_scalar_multiply(m: Matrix, scalar: float) -> Matrix:
    """
    Multiplies matrix by scalar
    
    Args:
        m: Matrix
        scalar: Scalar value
        
    Returns:
        Scaled matrix
        
    Example:
        >>> matrix_scalar_multiply([[1, 2], [3, 4]], 2)
        [[2, 4], [6, 8]]
    """
    return [[scalar * x for x in row] for row in m]


def matrix_multiply(m1: Matrix, m2: Matrix) -> Matrix:
    """
    Multiplies two matrices
    
    Args:
        m1: First matrix (m×n)
        m2: Second matrix (n×p)
        
    Returns:
        Product matrix (m×p)
        
    Example:
        >>> matrix_multiply([[1, 2], [3, 4]], [[5, 6], [7, 8]])
        [[19, 22], [43, 50]]
    """
    if len(m1[0]) != len(m2):
        raise ValueError("Matrix dimensions incompatible for multiplication")
    
    result = [[0] * len(m2[0]) for _ in range(len(m1))]
    
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            for k in range(len(m2)):
                result[i][j] += m1[i][k] * m2[k][j]
    
    return result


def matrix_transpose(m: Matrix) -> Matrix:
    """
    Transposes matrix
    
    Args:
        m: Matrix
        
    Returns:
        Transposed matrix
        
    Example:
        >>> matrix_transpose([[1, 2, 3], [4, 5, 6]])
        [[1, 4], [2, 5], [3, 6]]
    """
    return [[m[j][i] for j in range(len(m))] for i in range(len(m[0]))]


def identity_matrix(n: int) -> Matrix:
    """
    Creates n×n identity matrix
    
    Args:
        n: Matrix dimension
        
    Returns:
        Identity matrix
        
    Example:
        >>> identity_matrix(3)
        [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    """
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]


def zero_matrix(rows: int, cols: int) -> Matrix:
    """
    Creates matrix of zeros
    
    Args:
        rows: Number of rows
        cols: Number of columns
        
    Returns:
        Zero matrix
        
    Example:
        >>> zero_matrix(2, 3)
        [[0, 0, 0], [0, 0, 0]]
    """
    return [[0 for _ in range(cols)] for _ in range(rows)]


def determinant_2x2(m: Matrix) -> float:
    """
    Computes determinant of 2×2 matrix
    
    Args:
        m: 2×2 matrix
        
    Returns:
        Determinant
        
    Example:
        >>> determinant_2x2([[1, 2], [3, 4]])
        -2.0
    """
    if len(m) != 2 or len(m[0]) != 2:
        raise ValueError("Matrix must be 2×2")
    
    return m[0][0] * m[1][1] - m[0][1] * m[1][0]


def determinant_3x3(m: Matrix) -> float:
    """
    Computes determinant of 3×3 matrix
    
    Args:
        m: 3×3 matrix
        
    Returns:
        Determinant
        
    Example:
        >>> determinant_3x3([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        0.0
    """
    if len(m) != 3 or len(m[0]) != 3:
        raise ValueError("Matrix must be 3×3")
    
    return (
        m[0][0] * (m[1][1] * m[2][2] - m[1][2] * m[2][1]) -
        m[0][1] * (m[1][0] * m[2][2] - m[1][2] * m[2][0]) +
        m[0][2] * (m[1][0] * m[2][1] - m[1][1] * m[2][0])
    )


def matrix_trace(m: Matrix) -> float:
    """
    Computes trace (sum of diagonal elements)
    
    Args:
        m: Square matrix
        
    Returns:
        Trace
        
    Example:
        >>> matrix_trace([[1, 2], [3, 4]])
        5.0
    """
    if len(m) != len(m[0]):
        raise ValueError("Matrix must be square")
    
    return sum(m[i][i] for i in range(len(m)))


def matrix_inverse_2x2(m: Matrix) -> Matrix:
    """
    Computes inverse of 2×2 matrix
    
    Args:
        m: 2×2 matrix
        
    Returns:
        Inverse matrix
        
    Example:
        >>> matrix_inverse_2x2([[1, 2], [3, 4]])
        [[-2.0, 1.0], [1.5, -0.5]]
    """
    det = determinant_2x2(m)
    
    if abs(det) < 1e-10:
        raise ValueError("Matrix is singular (not invertible)")
    
    return [
        [m[1][1] / det, -m[0][1] / det],
        [-m[1][0] / det, m[0][0] / det]
    ]


def matrix_power(m: Matrix, n: int) -> Matrix:
    """
    Computes matrix to the power n
    
    Args:
        m: Square matrix
        n: Exponent (non-negative)
        
    Returns:
        Matrix power
        
    Example:
        >>> matrix_power([[1, 1], [0, 1]], 3)
        [[1, 3], [0, 1]]
    """
    if len(m) != len(m[0]):
        raise ValueError("Matrix must be square")
    
    if n < 0:
        raise ValueError("Exponent must be non-negative")
    
    if n == 0:
        return identity_matrix(len(m))
    
    result = m
    for _ in range(n - 1):
        result = matrix_multiply(result, m)
    
    return result


def vector_distance(v1: Vector, v2: Vector) -> float:
    """
    Computes Euclidean distance between two vectors
    
    Args:
        v1: First vector
        v2: Second vector
        
    Returns:
        Distance
        
    Example:
        >>> vector_distance([0, 0], [3, 4])
        5.0
    """
    diff = vector_subtract(v1, v2)
    return vector_magnitude(diff)


def gram_schmidt(vectors: List[Vector]) -> List[Vector]:
    """
    Gram-Schmidt orthogonalization process
    
    Args:
        vectors: List of vectors
        
    Returns:
        Orthogonal vectors
        
    Example:
        >>> gram_schmidt([[1, 1], [1, -1]])
        [[0.7071067811865475, 0.7071067811865475], [0.7071067811865475, -0.7071067811865475]]
    """
    orthogonal = []
    
    for v in vectors:
        # Subtract projections onto previous vectors
        w = v[:]
        for u in orthogonal:
            proj = vector_projection(v, u)
            w = vector_subtract(w, proj)
        
        # Normalize
        if vector_magnitude(w) > 1e-10:
            orthogonal.append(vector_normalize(w))
    
    return orthogonal


def is_orthogonal(v1: Vector, v2: Vector, tolerance: float = 1e-10) -> bool:
    """
    Checks if two vectors are orthogonal
    
    Args:
        v1: First vector
        v2: Second vector
        tolerance: Tolerance for dot product
        
    Returns:
        True if orthogonal
        
    Example:
        >>> is_orthogonal([1, 0], [0, 1])
        True
    """
    return abs(dot_product(v1, v2)) < tolerance


def linear_combination(vectors: List[Vector], coefficients: List[float]) -> Vector:
    """
    Computes linear combination of vectors
    
    Args:
        vectors: List of vectors
        coefficients: List of coefficients
        
    Returns:
        Linear combination
        
    Example:
        >>> linear_combination([[1, 0], [0, 1]], [2, 3])
        [2.0, 3.0]
    """
    if len(vectors) != len(coefficients):
        raise ValueError("Number of vectors and coefficients must match")
    
    if not vectors:
        raise ValueError("Need at least one vector")
    
    result = [0.0] * len(vectors[0])
    
    for v, c in zip(vectors, coefficients):
        scaled = vector_scalar_multiply(v, c)
        result = vector_add(result, scaled)
    
    return result


# Export all functions
__all__ = [
    'Vector', 'Matrix',
    'vector_add', 'vector_subtract', 'vector_scalar_multiply',
    'dot_product', 'vector_magnitude', 'vector_normalize',
    'cross_product', 'vector_angle', 'vector_projection',
    'matrix_add', 'matrix_scalar_multiply', 'matrix_multiply',
    'matrix_transpose', 'identity_matrix', 'zero_matrix',
    'determinant_2x2', 'determinant_3x3', 'matrix_trace',
    'matrix_inverse_2x2', 'matrix_power', 'vector_distance',
    'gram_schmidt', 'is_orthogonal', 'linear_combination',
]
