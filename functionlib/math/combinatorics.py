"""
Combinatorics Functions

Permutations, combinations, partitions, and combinatorial calculations.
"""

import math
from typing import List, Set, Iterator


def factorial(n: int) -> int:
    """
    Calculate factorial: n!
    
    Args:
        n: Non-negative integer
        
    Returns:
        Factorial of n
        
    Example:
        >>> factorial(5)
        120
    """
    if n < 0:
        raise ValueError("n must be non-negative")
    return math.factorial(n)


def permutations(n: int, r: int) -> int:
    """
    Number of permutations: P(n,r) = n! / (n-r)!
    
    Args:
        n: Total number of items
        r: Number of items to choose
        
    Returns:
        Number of permutations
        
    Example:
        >>> permutations(5, 3)
        60
    """
    if r > n or r < 0:
        return 0
    
    return math.factorial(n) // math.factorial(n - r)


def combinations(n: int, r: int) -> int:
    """
    Number of combinations: C(n,r) = n! / (r!(n-r)!)
    
    Args:
        n: Total number of items
        r: Number of items to choose
        
    Returns:
        Number of combinations
        
    Example:
        >>> combinations(5, 3)
        10
    """
    if r > n or r < 0:
        return 0
    
    return math.factorial(n) // (math.factorial(r) * math.factorial(n - r))


def combinations_with_replacement(n: int, r: int) -> int:
    """
    Combinations with replacement: C(n+r-1, r)
    
    Args:
        n: Number of types
        r: Number to choose
        
    Returns:
        Number of combinations with replacement
        
    Example:
        >>> combinations_with_replacement(3, 2)
        6
    """
    return combinations(n + r - 1, r)


def binomial_coefficient(n: int, k: int) -> int:
    """
    Binomial coefficient: (n choose k)
    
    Args:
        n: Upper index
        k: Lower index
        
    Returns:
        Binomial coefficient
        
    Example:
        >>> binomial_coefficient(5, 2)
        10
    """
    return combinations(n, k)


def multinomial_coefficient(n: int, groups: List[int]) -> int:
    """
    Multinomial coefficient: n! / (k1! * k2! * ... * km!)
    
    Args:
        n: Total number of items
        groups: Sizes of each group
        
    Returns:
        Multinomial coefficient
        
    Example:
        >>> multinomial_coefficient(10, [3, 3, 4])
        4200
    """
    if sum(groups) != n:
        raise ValueError("Sum of groups must equal n")
    
    result = math.factorial(n)
    for k in groups:
        result //= math.factorial(k)
    
    return result


def stirling_first_kind(n: int, k: int) -> int:
    """
    Stirling number of the first kind (unsigned)
    
    Args:
        n: Number of elements
        k: Number of cycles
        
    Returns:
        Stirling number
        
    Example:
        >>> stirling_first_kind(4, 2)
        11
    """
    if n == 0 and k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    
    # Use dynamic programming
    s = [[0] * (k + 1) for _ in range(n + 1)]
    s[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            s[i][j] = s[i-1][j-1] + (i-1) * s[i-1][j]
    
    return s[n][k]


def stirling_second_kind(n: int, k: int) -> int:
    """
    Stirling number of the second kind
    
    Args:
        n: Number of elements
        k: Number of non-empty subsets
        
    Returns:
        Stirling number
        
    Example:
        >>> stirling_second_kind(4, 2)
        7
    """
    if n == 0 and k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    
    # Use dynamic programming
    s = [[0] * (k + 1) for _ in range(n + 1)]
    s[0][0] = 1
    
    for i in range(1, n + 1):
        for j in range(1, min(i, k) + 1):
            s[i][j] = j * s[i-1][j] + s[i-1][j-1]
    
    return s[n][k]


def bell_number(n: int) -> int:
    """
    Bell number: number of partitions of a set
    
    Args:
        n: Size of set
        
    Returns:
        Bell number
        
    Example:
        >>> bell_number(3)
        5
    """
    if n == 0:
        return 1
    
    return sum(stirling_second_kind(n, k) for k in range(n + 1))


def catalan_number(n: int) -> int:
    """
    Catalan number: C(n) = C(2n,n) / (n+1)
    
    Args:
        n: Index
        
    Returns:
        Catalan number
        
    Example:
        >>> catalan_number(3)
        5
    """
    return combinations(2*n, n) // (n + 1)


def fibonacci(n: int) -> int:
    """
    Fibonacci number (combinatorial interpretation)
    
    Args:
        n: Index (0-based)
        
    Returns:
        Fibonacci number
        
    Example:
        >>> fibonacci(7)
        13
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def lucas_number(n: int) -> int:
    """
    Lucas number
    
    Args:
        n: Index
        
    Returns:
        Lucas number
        
    Example:
        >>> lucas_number(5)
        11
    """
    if n == 0:
        return 2
    if n == 1:
        return 1
    
    a, b = 2, 1
    for _ in range(2, n + 1):
        a, b = b, a + b
    
    return b


def partition_count(n: int) -> int:
    """
    Number of integer partitions of n
    
    Args:
        n: Positive integer
        
    Returns:
        Number of partitions
        
    Example:
        >>> partition_count(5)
        7
    """
    if n < 0:
        return 0
    if n == 0:
        return 1
    
    # Use dynamic programming
    p = [0] * (n + 1)
    p[0] = 1
    
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            p[j] += p[j - i]
    
    return p[n]


def generate_permutations(items: List) -> List[List]:
    """
    Generate all permutations of a list
    
    Args:
        items: List of items
        
    Returns:
        List of all permutations
        
    Example:
        >>> generate_permutations([1, 2, 3])
        [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    """
    if len(items) <= 1:
        return [items]
    
    result = []
    for i, item in enumerate(items):
        remaining = items[:i] + items[i+1:]
        for perm in generate_permutations(remaining):
            result.append([item] + perm)
    
    return result


def generate_combinations(items: List, r: int) -> List[List]:
    """
    Generate all combinations of r items
    
    Args:
        items: List of items
        r: Number to choose
        
    Returns:
        List of all combinations
        
    Example:
        >>> generate_combinations([1, 2, 3], 2)
        [[1, 2], [1, 3], [2, 3]]
    """
    if r > len(items):
        return []
    if r == 0:
        return [[]]
    if r == len(items):
        return [items]
    
    result = []
    for i in range(len(items) - r + 1):
        for combo in generate_combinations(items[i+1:], r - 1):
            result.append([items[i]] + combo)
    
    return result


def generate_subsets(items: List) -> List[List]:
    """
    Generate all subsets (power set)
    
    Args:
        items: List of items
        
    Returns:
        List of all subsets
        
    Example:
        >>> generate_subsets([1, 2])
        [[], [1], [2], [1, 2]]
    """
    result = [[]]
    
    for item in items:
        result.extend([subset + [item] for subset in result])
    
    return result


def derangements(n: int) -> int:
    """
    Number of derangements (permutations with no fixed points)
    
    Args:
        n: Number of items
        
    Returns:
        Number of derangements
        
    Example:
        >>> derangements(3)
        2
    """
    if n == 0:
        return 1
    if n == 1:
        return 0
    
    # Use recurrence: D(n) = (n-1)[D(n-1) + D(n-2)]
    d = [0] * (n + 1)
    d[0] = 1
    d[1] = 0
    
    for i in range(2, n + 1):
        d[i] = (i - 1) * (d[i-1] + d[i-2])
    
    return d[n]


def partitions_into_k_parts(n: int, k: int) -> int:
    """
    Number of ways to partition n into exactly k parts
    
    Args:
        n: Integer to partition
        k: Number of parts
        
    Returns:
        Number of partitions
        
    Example:
        >>> partitions_into_k_parts(5, 2)
        2
    """
    if k > n or k < 1:
        return 0
    if k == 1 or k == n:
        return 1
    
    # Use dynamic programming
    p = [[0] * (k + 1) for _ in range(n + 1)]
    
    for i in range(n + 1):
        p[i][1] = 1
    
    for i in range(1, n + 1):
        for j in range(2, min(i, k) + 1):
            p[i][j] = p[i-1][j-1] + p[i-j][j]
    
    return p[n][k]


def necklace_count(n: int, k: int) -> int:
    """
    Number of distinct necklaces (cyclic arrangements)
    
    Args:
        n: Number of beads
        k: Number of colors
        
    Returns:
        Number of distinct necklaces
        
    Example:
        >>> necklace_count(4, 2)
        6
    """
    if n == 0:
        return 0
    
    # Use Burnside's lemma / Pólya enumeration
    from math import gcd
    
    total = 0
    for d in range(1, n + 1):
        if n % d == 0:
            total += euler_phi(d) * (k ** (n // d))
    
    return total // n


def euler_phi(n: int) -> int:
    """
    Euler's totient function (for necklace_count)
    
    Args:
        n: Positive integer
        
    Returns:
        Number of integers ≤ n that are coprime to n
        
    Example:
        >>> euler_phi(9)
        6
    """
    result = n
    p = 2
    
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    
    if n > 1:
        result -= result // n
    
    return result


def compositions(n: int, k: int) -> int:
    """
    Number of compositions (ordered partitions) of n into k parts
    
    Args:
        n: Integer to partition
        k: Number of parts
        
    Returns:
        Number of compositions
        
    Example:
        >>> compositions(5, 3)
        6
    """
    if k > n or k < 1:
        return 0
    
    return combinations(n - 1, k - 1)


def weak_compositions(n: int, k: int) -> int:
    """
    Number of weak compositions (parts can be 0)
    
    Args:
        n: Integer to partition
        k: Number of parts
        
    Returns:
        Number of weak compositions
        
    Example:
        >>> weak_compositions(5, 3)
        21
    """
    return combinations(n + k - 1, k - 1)


def pentagonal_number(n: int) -> int:
    """
    Pentagonal number: n(3n-1)/2
    
    Args:
        n: Index
        
    Returns:
        Pentagonal number
        
    Example:
        >>> pentagonal_number(3)
        12
    """
    return n * (3*n - 1) // 2


def triangular_number(n: int) -> int:
    """
    Triangular number: n(n+1)/2
    
    Args:
        n: Index
        
    Returns:
        Triangular number
        
    Example:
        >>> triangular_number(4)
        10
    """
    return n * (n + 1) // 2


def tetrahedral_number(n: int) -> int:
    """
    Tetrahedral number: n(n+1)(n+2)/6
    
    Args:
        n: Index
        
    Returns:
        Tetrahedral number
        
    Example:
        >>> tetrahedral_number(3)
        10
    """
    return n * (n + 1) * (n + 2) // 6


# Export all functions
__all__ = [
    'factorial', 'permutations', 'combinations', 'combinations_with_replacement',
    'binomial_coefficient', 'multinomial_coefficient',
    'stirling_first_kind', 'stirling_second_kind', 'bell_number', 'catalan_number',
    'fibonacci', 'lucas_number', 'partition_count',
    'generate_permutations', 'generate_combinations', 'generate_subsets',
    'derangements', 'partitions_into_k_parts', 'necklace_count',
    'compositions', 'weak_compositions',
    'pentagonal_number', 'triangular_number', 'tetrahedral_number',
]
