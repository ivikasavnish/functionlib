"""
Algorithms

Common algorithm implementations including sorting, searching, and graph algorithms.
"""

from typing import List, Any, Callable, Optional, Dict, Set, Tuple
import heapq


# Sorting Algorithms

def bubble_sort(arr: List[Any]) -> List[Any]:
    """
    Bubble sort algorithm - O(n²)
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Example:
        >>> bubble_sort([64, 34, 25, 12, 22])
        [12, 22, 25, 34, 64]
    """
    arr = arr.copy()
    n = len(arr)
    
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    
    return arr


def quick_sort(arr: List[Any]) -> List[Any]:
    """
    Quick sort algorithm - O(n log n) average
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Example:
        >>> quick_sort([64, 34, 25, 12, 22])
        [12, 22, 25, 34, 64]
    """
    if len(arr) <= 1:
        return arr
    
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    
    return quick_sort(left) + middle + quick_sort(right)


def merge_sort(arr: List[Any]) -> List[Any]:
    """
    Merge sort algorithm - O(n log n)
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Example:
        >>> merge_sort([64, 34, 25, 12, 22])
        [12, 22, 25, 34, 64]
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    
    return merge(left, right)


def merge(left: List[Any], right: List[Any]) -> List[Any]:
    """Helper function for merge sort"""
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result


def insertion_sort(arr: List[Any]) -> List[Any]:
    """
    Insertion sort algorithm - O(n²)
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Example:
        >>> insertion_sort([64, 34, 25, 12, 22])
        [12, 22, 25, 34, 64]
    """
    arr = arr.copy()
    
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        
        arr[j + 1] = key
    
    return arr


def selection_sort(arr: List[Any]) -> List[Any]:
    """
    Selection sort algorithm - O(n²)
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Example:
        >>> selection_sort([64, 34, 25, 12, 22])
        [12, 22, 25, 34, 64]
    """
    arr = arr.copy()
    
    for i in range(len(arr)):
        min_idx = i
        
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j
        
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    
    return arr


def heap_sort(arr: List[Any]) -> List[Any]:
    """
    Heap sort algorithm - O(n log n)
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Example:
        >>> heap_sort([64, 34, 25, 12, 22])
        [12, 22, 25, 34, 64]
    """
    arr = arr.copy()
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]


# Searching Algorithms

def linear_search(arr: List[Any], target: Any) -> int:
    """
    Linear search - O(n)
    
    Args:
        arr: List to search
        target: Value to find
        
    Returns:
        Index of target, or -1 if not found
        
    Example:
        >>> linear_search([1, 2, 3, 4, 5], 3)
        2
    """
    for i, value in enumerate(arr):
        if value == target:
            return i
    return -1


def binary_search(arr: List[Any], target: Any) -> int:
    """
    Binary search (requires sorted array) - O(log n)
    
    Args:
        arr: Sorted list to search
        target: Value to find
        
    Returns:
        Index of target, or -1 if not found
        
    Example:
        >>> binary_search([1, 2, 3, 4, 5], 3)
        2
    """
    left, right = 0, len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1


def jump_search(arr: List[Any], target: Any) -> int:
    """
    Jump search (requires sorted array) - O(√n)
    
    Args:
        arr: Sorted list to search
        target: Value to find
        
    Returns:
        Index of target, or -1 if not found
        
    Example:
        >>> jump_search([1, 2, 3, 4, 5], 3)
        2
    """
    import math
    
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
    
    while arr[prev] < target:
        prev += 1
        if prev == min(step, n):
            return -1
    
    if arr[prev] == target:
        return prev
    
    return -1


# Graph Algorithms

def breadth_first_search(graph: Dict[Any, List[Any]], start: Any) -> List[Any]:
    """
    BFS traversal
    
    Args:
        graph: Adjacency list representation
        start: Starting vertex
        
    Returns:
        List of vertices in BFS order
        
    Example:
        >>> graph = {1: [2, 3], 2: [4], 3: [4], 4: []}
        >>> breadth_first_search(graph, 1)
        [1, 2, 3, 4]
    """
    visited = set()
    queue = [start]
    result = []
    
    while queue:
        vertex = queue.pop(0)
        if vertex not in visited:
            visited.add(vertex)
            result.append(vertex)
            queue.extend(neighbor for neighbor in graph.get(vertex, []) 
                        if neighbor not in visited)
    
    return result


def depth_first_search(graph: Dict[Any, List[Any]], start: Any) -> List[Any]:
    """
    DFS traversal
    
    Args:
        graph: Adjacency list representation
        start: Starting vertex
        
    Returns:
        List of vertices in DFS order
        
    Example:
        >>> graph = {1: [2, 3], 2: [4], 3: [4], 4: []}
        >>> depth_first_search(graph, 1)
        [1, 2, 4, 3]
    """
    visited = set()
    result = []
    
    def dfs(vertex):
        visited.add(vertex)
        result.append(vertex)
        
        for neighbor in graph.get(vertex, []):
            if neighbor not in visited:
                dfs(neighbor)
    
    dfs(start)
    return result


def dijkstra(graph: Dict[Any, Dict[Any, float]], start: Any) -> Dict[Any, float]:
    """
    Dijkstra's shortest path algorithm
    
    Args:
        graph: Adjacency dict with weights {vertex: {neighbor: weight}}
        start: Starting vertex
        
    Returns:
        Dict of shortest distances from start to each vertex
        
    Example:
        >>> graph = {1: {2: 1, 3: 4}, 2: {3: 2, 4: 5}, 3: {4: 1}, 4: {}}
        >>> dijkstra(graph, 1)
        {1: 0, 2: 1, 3: 3, 4: 4}
    """
    distances = {vertex: float('inf') for vertex in graph}
    distances[start] = 0
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        for neighbor, weight in graph.get(current, {}).items():
            distance = current_dist + weight
            
            if distance < distances.get(neighbor, float('inf')):
                distances[neighbor] = distance
                heapq.heappush(pq, (distance, neighbor))
    
    return distances


# Dynamic Programming

def fibonacci_dp(n: int) -> int:
    """
    Fibonacci using dynamic programming - O(n)
    
    Args:
        n: Fibonacci index
        
    Returns:
        nth Fibonacci number
        
    Example:
        >>> fibonacci_dp(10)
        55
    """
    if n <= 1:
        return n
    
    dp = [0] * (n + 1)
    dp[1] = 1
    
    for i in range(2, n + 1):
        dp[i] = dp[i - 1] + dp[i - 2]
    
    return dp[n]


def longest_common_subsequence(str1: str, str2: str) -> int:
    """
    Finds length of longest common subsequence
    
    Args:
        str1: First string
        str2: Second string
        
    Returns:
        Length of LCS
        
    Example:
        >>> longest_common_subsequence("ABCDGH", "AEDFHR")
        3
    """
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
    
    return dp[m][n]


def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 Knapsack problem
    
    Args:
        weights: Item weights
        values: Item values
        capacity: Knapsack capacity
        
    Returns:
        Maximum value achievable
        
    Example:
        >>> knapsack_01([2, 3, 4], [3, 4, 5], 5)
        7
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(
                    values[i - 1] + dp[i - 1][w - weights[i - 1]],
                    dp[i - 1][w]
                )
            else:
                dp[i][w] = dp[i - 1][w]
    
    return dp[n][capacity]


# String Algorithms

def levenshtein_distance(str1: str, str2: str) -> int:
    """
    Calculates edit distance between two strings
    
    Args:
        str1: First string
        str2: Second string
        
    Returns:
        Minimum edit distance
        
    Example:
        >>> levenshtein_distance("kitten", "sitting")
        3
    """
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # deletion
                    dp[i][j - 1],      # insertion
                    dp[i - 1][j - 1]   # substitution
                )
    
    return dp[m][n]


# Export all functions
__all__ = [
    'bubble_sort', 'quick_sort', 'merge_sort', 'insertion_sort',
    'selection_sort', 'heap_sort',
    'linear_search', 'binary_search', 'jump_search',
    'breadth_first_search', 'depth_first_search', 'dijkstra',
    'fibonacci_dp', 'longest_common_subsequence', 'knapsack_01',
    'levenshtein_distance',
]
