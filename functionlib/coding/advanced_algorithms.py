"""
Advanced Algorithms

String search, graph algorithms, advanced data structures, and optimization.
"""

from typing import List, Dict, Any, Optional, Tuple, Set, Callable
from collections import defaultdict, deque
import heapq

__all__ = [
    # String Search Algorithms
    'kmp_search', 'boyer_moore_search', 'rabin_karp_search', 
    'naive_string_search', 'find_all_occurrences',
    
    # Pattern Matching
    'longest_common_subsequence', 'longest_common_substring',
    'edit_distance', 'hamming_distance', 'fuzzy_match',
    
    # Graph Algorithms - Shortest Path
    'dijkstra_shortest_path', 'bellman_ford', 'floyd_warshall',
    'a_star_search', 'bfs_shortest_path',
    
    # Graph Algorithms - Traversal
    'depth_first_search', 'breadth_first_search', 'topological_sort',
    'strongly_connected_components', 'detect_cycle',
    
    # Graph Algorithms - Spanning Trees
    'kruskals_mst', 'prims_mst', 'is_connected',
    
    # Advanced Sorting
    'heap_sort', 'counting_sort', 'radix_sort', 'bucket_sort',
    'shell_sort', 'tim_sort_merge',
    
    # Dynamic Programming
    'knapsack_01', 'knapsack_unbounded', 'coin_change',
    'longest_increasing_subsequence', 'matrix_chain_multiplication',
    
    # Greedy Algorithms
    'activity_selection', 'fractional_knapsack', 'huffman_encoding',
    
    # Searching & Selection
    'binary_search_recursive', 'exponential_search', 'jump_search',
    'interpolation_search', 'kth_smallest', 'kth_largest',
    
    # Array Algorithms
    'kadanes_max_subarray', 'sliding_window_max', 'two_pointer_sum',
    'dutch_national_flag', 'rotate_array',
    
    # Bit Manipulation
    'count_set_bits', 'power_of_two', 'find_missing_number',
    'single_number', 'reverse_bits'
]

# ============================================================================
# STRING SEARCH ALGORITHMS
# ============================================================================

def kmp_search(text: str, pattern: str) -> int:
    """
    Knuth-Morris-Pratt string search algorithm.
    
    Args:
        text: Text to search in
        pattern: Pattern to find
        
    Returns:
        Index of first occurrence, -1 if not found
        
    Example:
        >>> kmp_search("ABABDABACDABABCABAB", "ABABCABAB")
        10
    """
    if not pattern:
        return 0
    
    # Build failure function
    def build_failure_function(p: str) -> List[int]:
        m = len(p)
        failure = [0] * m
        j = 0
        
        for i in range(1, m):
            while j > 0 and p[i] != p[j]:
                j = failure[j - 1]
            if p[i] == p[j]:
                j += 1
            failure[i] = j
        
        return failure
    
    failure = build_failure_function(pattern)
    n, m = len(text), len(pattern)
    j = 0
    
    for i in range(n):
        while j > 0 and text[i] != pattern[j]:
            j = failure[j - 1]
        if text[i] == pattern[j]:
            j += 1
        if j == m:
            return i - m + 1
    
    return -1


def boyer_moore_search(text: str, pattern: str) -> int:
    """
    Boyer-Moore string search algorithm.
    
    Args:
        text: Text to search in
        pattern: Pattern to find
        
    Returns:
        Index of first occurrence, -1 if not found
        
    Example:
        >>> boyer_moore_search("ABAAABCD", "ABC")
        5
    """
    if not pattern:
        return 0
    
    n, m = len(text), len(pattern)
    
    # Bad character heuristic
    bad_char = {}
    for i in range(m):
        bad_char[pattern[i]] = i
    
    shift = 0
    while shift <= n - m:
        j = m - 1
        
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1
        
        if j < 0:
            return shift
        else:
            shift += max(1, j - bad_char.get(text[shift + j], -1))
    
    return -1


def rabin_karp_search(text: str, pattern: str, prime: int = 101) -> int:
    """
    Rabin-Karp string search using rolling hash.
    
    Args:
        text: Text to search in
        pattern: Pattern to find
        prime: Prime number for hashing
        
    Returns:
        Index of first occurrence, -1 if not found
        
    Example:
        >>> rabin_karp_search("GEEKS FOR GEEKS", "GEEK")
        0
    """
    if not pattern:
        return 0
    
    n, m = len(text), len(pattern)
    d = 256  # Number of characters
    
    pattern_hash = 0
    text_hash = 0
    h = pow(d, m - 1, prime)
    
    # Calculate initial hashes
    for i in range(m):
        pattern_hash = (d * pattern_hash + ord(pattern[i])) % prime
        text_hash = (d * text_hash + ord(text[i])) % prime
    
    # Slide the pattern
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text[i:i+m] == pattern:
                return i
        
        if i < n - m:
            text_hash = (d * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            if text_hash < 0:
                text_hash += prime
    
    return -1


def naive_string_search(text: str, pattern: str) -> int:
    """
    Naive string search algorithm.
    
    Args:
        text: Text to search in
        pattern: Pattern to find
        
    Returns:
        Index of first occurrence, -1 if not found
        
    Example:
        >>> naive_string_search("hello world", "world")
        6
    """
    n, m = len(text), len(pattern)
    for i in range(n - m + 1):
        if text[i:i+m] == pattern:
            return i
    return -1


def find_all_occurrences(text: str, pattern: str) -> List[int]:
    """
    Find all occurrences of pattern in text.
    
    Args:
        text: Text to search in
        pattern: Pattern to find
        
    Returns:
        List of starting indices
        
    Example:
        >>> find_all_occurrences("AABAACAADAABAAABAA", "AABA")
        [0, 9, 13]
    """
    occurrences = []
    start = 0
    
    while True:
        pos = text.find(pattern, start)
        if pos == -1:
            break
        occurrences.append(pos)
        start = pos + 1
    
    return occurrences


# ============================================================================
# PATTERN MATCHING
# ============================================================================

def longest_common_subsequence(str1: str, str2: str) -> int:
    """
    Find length of longest common subsequence.
    
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
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    
    return dp[m][n]


def longest_common_substring(str1: str, str2: str) -> int:
    """
    Find length of longest common substring.
    
    Args:
        str1: First string
        str2: Second string
        
    Returns:
        Length of longest common substring
        
    Example:
        >>> longest_common_substring("ABCDGH", "ACDGHR")
        4
    """
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    max_length = 0
    
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
                max_length = max(max_length, dp[i][j])
    
    return max_length


def edit_distance(str1: str, str2: str) -> int:
    """
    Calculate Levenshtein edit distance.
    
    Args:
        str1: First string
        str2: Second string
        
    Returns:
        Minimum number of edits
        
    Example:
        >>> edit_distance("kitten", "sitting")
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
            if str1[i-1] == str2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                dp[i][j] = 1 + min(dp[i-1][j], dp[i][j-1], dp[i-1][j-1])
    
    return dp[m][n]


def hamming_distance(str1: str, str2: str) -> int:
    """
    Calculate Hamming distance between two strings.
    
    Args:
        str1: First string
        str2: Second string
        
    Returns:
        Number of positions with different characters
        
    Example:
        >>> hamming_distance("karolin", "kathrin")
        3
    """
    if len(str1) != len(str2):
        raise ValueError("Strings must be same length")
    
    return sum(c1 != c2 for c1, c2 in zip(str1, str2))


def fuzzy_match(text: str, pattern: str, max_distance: int = 2) -> List[int]:
    """
    Fuzzy string matching with maximum edit distance.
    
    Args:
        text: Text to search in
        pattern: Pattern to find
        max_distance: Maximum allowed edit distance
        
    Returns:
        List of positions with fuzzy matches
        
    Example:
        >>> matches = fuzzy_match("hello world", "helo", max_distance=1)
        >>> len(matches) > 0
        True
    """
    matches = []
    m = len(pattern)
    
    for i in range(len(text) - m + max_distance + 1):
        for length in range(m - max_distance, m + max_distance + 1):
            if i + length <= len(text):
                substring = text[i:i+length]
                if edit_distance(substring, pattern) <= max_distance:
                    matches.append(i)
                    break
    
    return matches


# ============================================================================
# GRAPH ALGORITHMS - SHORTEST PATH
# ============================================================================

def dijkstra_shortest_path(graph: Dict[Any, List[Tuple[Any, int]]], 
                          start: Any, end: Any) -> Tuple[List[Any], int]:
    """
    Dijkstra's shortest path algorithm.
    
    Args:
        graph: Adjacency list {node: [(neighbor, weight), ...]}
        start: Start node
        end: End node
        
    Returns:
        Tuple of (path, distance)
        
    Example:
        >>> graph = {'A': [('B', 1), ('C', 4)], 'B': [('C', 2)], 'C': []}
        >>> path, dist = dijkstra_shortest_path(graph, 'A', 'C')
        >>> dist
        3
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    pq = [(0, start)]
    visited = set()
    
    while pq:
        current_dist, current = heapq.heappop(pq)
        
        if current in visited:
            continue
        
        visited.add(current)
        
        if current == end:
            break
        
        for neighbor, weight in graph.get(current, []):
            distance = current_dist + weight
            
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current
                heapq.heappush(pq, (distance, neighbor))
    
    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    
    return path, distances[end]


def bellman_ford(graph: Dict[Any, List[Tuple[Any, int]]], 
                 start: Any) -> Dict[Any, int]:
    """
    Bellman-Ford algorithm (handles negative weights).
    
    Args:
        graph: Adjacency list
        start: Start node
        
    Returns:
        Dictionary of shortest distances
        
    Example:
        >>> graph = {'A': [('B', 1)], 'B': [('C', -1)], 'C': []}
        >>> distances = bellman_ford(graph, 'A')
        >>> distances['C']
        0
    """
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    
    # Relax edges V-1 times
    for _ in range(len(graph) - 1):
        for node in graph:
            for neighbor, weight in graph[node]:
                if distances[node] + weight < distances[neighbor]:
                    distances[neighbor] = distances[node] + weight
    
    # Check for negative cycles
    for node in graph:
        for neighbor, weight in graph[node]:
            if distances[node] + weight < distances[neighbor]:
                raise ValueError("Graph contains negative cycle")
    
    return distances


def floyd_warshall(graph: Dict[Any, Dict[Any, int]]) -> Dict[Any, Dict[Any, int]]:
    """
    Floyd-Warshall all-pairs shortest path.
    
    Args:
        graph: Adjacency matrix {node: {neighbor: weight}}
        
    Returns:
        Distance matrix
        
    Example:
        >>> graph = {'A': {'B': 3, 'C': 8}, 'B': {'C': 1}, 'C': {}}
        >>> dist = floyd_warshall(graph)
        >>> dist['A']['C']
        4
    """
    nodes = list(graph.keys())
    dist = {i: {j: float('inf') for j in nodes} for i in nodes}
    
    # Initialize
    for node in nodes:
        dist[node][node] = 0
        for neighbor, weight in graph.get(node, {}).items():
            dist[node][neighbor] = weight
    
    # Floyd-Warshall
    for k in nodes:
        for i in nodes:
            for j in nodes:
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    
    return dist


def a_star_search(graph: Dict[Any, List[Tuple[Any, int]]], 
                  start: Any, goal: Any,
                  heuristic: Callable[[Any], int]) -> Tuple[List[Any], int]:
    """
    A* pathfinding algorithm.
    
    Args:
        graph: Adjacency list
        start: Start node
        goal: Goal node
        heuristic: Heuristic function h(node) -> estimated distance to goal
        
    Returns:
        Tuple of (path, distance)
        
    Example:
        >>> graph = {'A': [('B', 1)], 'B': [('C', 1)], 'C': []}
        >>> path, dist = a_star_search(graph, 'A', 'C', lambda n: 0)
        >>> len(path)
        3
    """
    open_set = [(heuristic(start), 0, start)]
    came_from = {}
    g_score = {start: 0}
    
    while open_set:
        _, current_g, current = heapq.heappop(open_set)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path, g_score[goal]
        
        for neighbor, weight in graph.get(current, []):
            tentative_g = current_g + weight
            
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor)
                heapq.heappush(open_set, (f_score, tentative_g, neighbor))
    
    return [], float('inf')


def bfs_shortest_path(graph: Dict[Any, List[Any]], 
                      start: Any, end: Any) -> List[Any]:
    """
    BFS shortest path (unweighted graph).
    
    Args:
        graph: Adjacency list (unweighted)
        start: Start node
        end: End node
        
    Returns:
        Shortest path
        
    Example:
        >>> graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
        >>> path = bfs_shortest_path(graph, 'A', 'D')
        >>> len(path)
        3
    """
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        node, path = queue.popleft()
        
        if node == end:
            return path
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor]))
    
    return []


# ============================================================================
# GRAPH ALGORITHMS - TRAVERSAL
# ============================================================================

def depth_first_search(graph: Dict[Any, List[Any]], 
                       start: Any) -> List[Any]:
    """
    Depth-first search traversal.
    
    Args:
        graph: Adjacency list
        start: Start node
        
    Returns:
        List of nodes in DFS order
        
    Example:
        >>> graph = {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}
        >>> dfs = depth_first_search(graph, 'A')
        >>> dfs[0]
        'A'
    """
    visited = []
    stack = [start]
    seen = set()
    
    while stack:
        node = stack.pop()
        if node not in seen:
            seen.add(node)
            visited.append(node)
            stack.extend(reversed(graph.get(node, [])))
    
    return visited


def breadth_first_search(graph: Dict[Any, List[Any]], 
                        start: Any) -> List[Any]:
    """
    Breadth-first search traversal.
    
    Args:
        graph: Adjacency list
        start: Start node
        
    Returns:
        List of nodes in BFS order
        
    Example:
        >>> graph = {'A': ['B', 'C'], 'B': ['D'], 'C': [], 'D': []}
        >>> bfs = breadth_first_search(graph, 'A')
        >>> bfs[0]
        'A'
    """
    visited = []
    queue = deque([start])
    seen = {start}
    
    while queue:
        node = queue.popleft()
        visited.append(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in seen:
                seen.add(neighbor)
                queue.append(neighbor)
    
    return visited


def topological_sort(graph: Dict[Any, List[Any]]) -> List[Any]:
    """
    Topological sort of directed acyclic graph.
    
    Args:
        graph: Adjacency list
        
    Returns:
        Topologically sorted list
        
    Example:
        >>> graph = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
        >>> sorted_nodes = topological_sort(graph)
        >>> sorted_nodes.index('A') < sorted_nodes.index('D')
        True
    """
    in_degree = {node: 0 for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
    
    queue = deque([node for node in graph if in_degree[node] == 0])
    result = []
    
    while queue:
        node = queue.popleft()
        result.append(node)
        
        for neighbor in graph.get(node, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    if len(result) != len(graph):
        raise ValueError("Graph has a cycle")
    
    return result


def strongly_connected_components(graph: Dict[Any, List[Any]]) -> List[List[Any]]:
    """
    Find strongly connected components using Kosaraju's algorithm.
    
    Args:
        graph: Adjacency list
        
    Returns:
        List of SCCs
        
    Example:
        >>> graph = {'A': ['B'], 'B': ['C'], 'C': ['A'], 'D': ['C']}
        >>> sccs = strongly_connected_components(graph)
        >>> len(sccs) >= 1
        True
    """
    # First DFS to get finish times
    visited = set()
    stack = []
    
    def dfs1(node):
        visited.add(node)
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                dfs1(neighbor)
        stack.append(node)
    
    for node in graph:
        if node not in visited:
            dfs1(node)
    
    # Reverse graph
    reversed_graph = {node: [] for node in graph}
    for node in graph:
        for neighbor in graph[node]:
            reversed_graph[neighbor].append(node)
    
    # Second DFS on reversed graph
    visited = set()
    sccs = []
    
    def dfs2(node, component):
        visited.add(node)
        component.append(node)
        for neighbor in reversed_graph.get(node, []):
            if neighbor not in visited:
                dfs2(neighbor, component)
    
    while stack:
        node = stack.pop()
        if node not in visited:
            component = []
            dfs2(node, component)
            sccs.append(component)
    
    return sccs


def detect_cycle(graph: Dict[Any, List[Any]]) -> bool:
    """
    Detect cycle in directed graph.
    
    Args:
        graph: Adjacency list
        
    Returns:
        True if cycle exists
        
    Example:
        >>> graph = {'A': ['B'], 'B': ['C'], 'C': ['A']}
        >>> detect_cycle(graph)
        True
    """
    visited = set()
    rec_stack = set()
    
    def dfs(node):
        visited.add(node)
        rec_stack.add(node)
        
        for neighbor in graph.get(node, []):
            if neighbor not in visited:
                if dfs(neighbor):
                    return True
            elif neighbor in rec_stack:
                return True
        
        rec_stack.remove(node)
        return False
    
    for node in graph:
        if node not in visited:
            if dfs(node):
                return True
    
    return False


# ============================================================================
# GRAPH ALGORITHMS - SPANNING TREES
# ============================================================================

def kruskals_mst(edges: List[Tuple[Any, Any, int]], 
                 nodes: Set[Any]) -> List[Tuple[Any, Any, int]]:
    """
    Kruskal's Minimum Spanning Tree algorithm.
    
    Args:
        edges: List of (node1, node2, weight)
        nodes: Set of all nodes
        
    Returns:
        List of edges in MST
        
    Example:
        >>> edges = [('A', 'B', 1), ('B', 'C', 2), ('A', 'C', 3)]
        >>> nodes = {'A', 'B', 'C'}
        >>> mst = kruskals_mst(edges, nodes)
        >>> len(mst)
        2
    """
    # Union-Find
    parent = {node: node for node in nodes}
    rank = {node: 0 for node in nodes}
    
    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]
    
    def union(x, y):
        px, py = find(x), find(y)
        if px == py:
            return False
        if rank[px] < rank[py]:
            parent[px] = py
        elif rank[px] > rank[py]:
            parent[py] = px
        else:
            parent[py] = px
            rank[px] += 1
        return True
    
    mst = []
    for u, v, weight in sorted(edges, key=lambda e: e[2]):
        if union(u, v):
            mst.append((u, v, weight))
    
    return mst


def prims_mst(graph: Dict[Any, List[Tuple[Any, int]]]) -> List[Tuple[Any, Any, int]]:
    """
    Prim's Minimum Spanning Tree algorithm.
    
    Args:
        graph: Adjacency list with weights
        
    Returns:
        List of edges in MST
        
    Example:
        >>> graph = {'A': [('B', 1), ('C', 3)], 'B': [('C', 2)], 'C': []}
        >>> mst = prims_mst(graph)
        >>> len(mst)
        2
    """
    if not graph:
        return []
    
    start = next(iter(graph))
    visited = {start}
    mst = []
    edges = [(weight, start, neighbor) for neighbor, weight in graph[start]]
    heapq.heapify(edges)
    
    while edges:
        weight, u, v = heapq.heappop(edges)
        
        if v not in visited:
            visited.add(v)
            mst.append((u, v, weight))
            
            for neighbor, w in graph.get(v, []):
                if neighbor not in visited:
                    heapq.heappush(edges, (w, v, neighbor))
    
    return mst


def is_connected(graph: Dict[Any, List[Any]]) -> bool:
    """
    Check if undirected graph is connected.
    
    Args:
        graph: Adjacency list
        
    Returns:
        True if connected
        
    Example:
        >>> graph = {'A': ['B'], 'B': ['A', 'C'], 'C': ['B']}
        >>> is_connected(graph)
        True
    """
    if not graph:
        return True
    
    start = next(iter(graph))
    visited = set(breadth_first_search(graph, start))
    return len(visited) == len(graph)


# ============================================================================
# ADVANCED SORTING
# ============================================================================

def heap_sort(arr: List[int]) -> List[int]:
    """
    Heap sort algorithm.
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Example:
        >>> heap_sort([3, 1, 4, 1, 5, 9, 2, 6])
        [1, 1, 2, 3, 4, 5, 6, 9]
    """
    result = arr.copy()
    heapq.heapify(result)
    return [heapq.heappop(result) for _ in range(len(result))]


def counting_sort(arr: List[int], max_val: Optional[int] = None) -> List[int]:
    """
    Counting sort for non-negative integers.
    
    Args:
        arr: List to sort
        max_val: Maximum value (auto-detected if None)
        
    Returns:
        Sorted list
        
    Example:
        >>> counting_sort([4, 2, 2, 8, 3, 3, 1])
        [1, 2, 2, 3, 3, 4, 8]
    """
    if not arr:
        return []
    
    if max_val is None:
        max_val = max(arr)
    
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    
    result = []
    for num, freq in enumerate(count):
        result.extend([num] * freq)
    
    return result


def radix_sort(arr: List[int]) -> List[int]:
    """
    Radix sort for non-negative integers.
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Example:
        >>> radix_sort([170, 45, 75, 90, 802, 24, 2, 66])
        [2, 24, 45, 66, 75, 90, 170, 802]
    """
    if not arr:
        return []
    
    max_val = max(arr)
    exp = 1
    result = arr.copy()
    
    while max_val // exp > 0:
        counting = [[] for _ in range(10)]
        
        for num in result:
            digit = (num // exp) % 10
            counting[digit].append(num)
        
        result = []
        for bucket in counting:
            result.extend(bucket)
        
        exp *= 10
    
    return result


def bucket_sort(arr: List[float], num_buckets: int = 10) -> List[float]:
    """
    Bucket sort for floating point numbers.
    
    Args:
        arr: List to sort
        num_buckets: Number of buckets
        
    Returns:
        Sorted list
        
    Example:
        >>> bucket_sort([0.42, 0.32, 0.23, 0.52, 0.25, 0.47, 0.51])
        [0.23, 0.25, 0.32, 0.42, 0.47, 0.51, 0.52]
    """
    if not arr:
        return []
    
    buckets = [[] for _ in range(num_buckets)]
    
    min_val, max_val = min(arr), max(arr)
    range_val = max_val - min_val
    
    for num in arr:
        if range_val == 0:
            idx = 0
        else:
            idx = min(int((num - min_val) / range_val * num_buckets), num_buckets - 1)
        buckets[idx].append(num)
    
    result = []
    for bucket in buckets:
        result.extend(sorted(bucket))
    
    return result


def shell_sort(arr: List[int]) -> List[int]:
    """
    Shell sort algorithm.
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Example:
        >>> shell_sort([12, 34, 54, 2, 3])
        [2, 3, 12, 34, 54]
    """
    result = arr.copy()
    n = len(result)
    gap = n // 2
    
    while gap > 0:
        for i in range(gap, n):
            temp = result[i]
            j = i
            while j >= gap and result[j - gap] > temp:
                result[j] = result[j - gap]
                j -= gap
            result[j] = temp
        gap //= 2
    
    return result


def tim_sort_merge(arr: List[int]) -> List[int]:
    """
    Simple Tim sort-like merge sort.
    
    Args:
        arr: List to sort
        
    Returns:
        Sorted list
        
    Example:
        >>> tim_sort_merge([5, 2, 8, 1, 9])
        [1, 2, 5, 8, 9]
    """
    if len(arr) <= 1:
        return arr.copy()
    
    mid = len(arr) // 2
    left = tim_sort_merge(arr[:mid])
    right = tim_sort_merge(arr[mid:])
    
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


# ============================================================================
# DYNAMIC PROGRAMMING
# ============================================================================

def knapsack_01(weights: List[int], values: List[int], capacity: int) -> int:
    """
    0/1 Knapsack problem.
    
    Args:
        weights: Item weights
        values: Item values
        capacity: Knapsack capacity
        
    Returns:
        Maximum value
        
    Example:
        >>> knapsack_01([2, 3, 4], [3, 4, 5], 5)
        7
    """
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            if weights[i-1] <= w:
                dp[i][w] = max(dp[i-1][w], values[i-1] + dp[i-1][w - weights[i-1]])
            else:
                dp[i][w] = dp[i-1][w]
    
    return dp[n][capacity]


def knapsack_unbounded(weights: List[int], values: List[int], capacity: int) -> int:
    """
    Unbounded Knapsack problem.
    
    Args:
        weights: Item weights
        values: Item values
        capacity: Knapsack capacity
        
    Returns:
        Maximum value
        
    Example:
        >>> knapsack_unbounded([1, 3, 4], [10, 40, 50], 8)
        110
    """
    dp = [0] * (capacity + 1)
    
    for w in range(capacity + 1):
        for i in range(len(weights)):
            if weights[i] <= w:
                dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
    
    return dp[capacity]


def coin_change(coins: List[int], amount: int) -> int:
    """
    Minimum coins needed to make amount.
    
    Args:
        coins: Available coin denominations
        amount: Target amount
        
    Returns:
        Minimum number of coins (-1 if impossible)
        
    Example:
        >>> coin_change([1, 2, 5], 11)
        3
    """
    dp = [float('inf')] * (amount + 1)
    dp[0] = 0
    
    for i in range(1, amount + 1):
        for coin in coins:
            if coin <= i:
                dp[i] = min(dp[i], dp[i - coin] + 1)
    
    return dp[amount] if dp[amount] != float('inf') else -1


def longest_increasing_subsequence(arr: List[int]) -> int:
    """
    Length of longest increasing subsequence.
    
    Args:
        arr: Input array
        
    Returns:
        Length of LIS
        
    Example:
        >>> longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18])
        4
    """
    if not arr:
        return 0
    
    dp = [1] * len(arr)
    
    for i in range(1, len(arr)):
        for j in range(i):
            if arr[j] < arr[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    
    return max(dp)


def matrix_chain_multiplication(dimensions: List[int]) -> int:
    """
    Minimum scalar multiplications for matrix chain.
    
    Args:
        dimensions: Matrix dimensions [p0, p1, ..., pn]
                   where matrix i has dimensions p[i-1] x p[i]
        
    Returns:
        Minimum number of multiplications
        
    Example:
        >>> matrix_chain_multiplication([10, 20, 30, 40])
        18000
    """
    n = len(dimensions) - 1
    dp = [[0] * n for _ in range(n)]
    
    for length in range(2, n + 1):
        for i in range(n - length + 1):
            j = i + length - 1
            dp[i][j] = float('inf')
            
            for k in range(i, j):
                cost = (dp[i][k] + dp[k+1][j] + 
                       dimensions[i] * dimensions[k+1] * dimensions[j+1])
                dp[i][j] = min(dp[i][j], cost)
    
    return dp[0][n-1]


# ============================================================================
# GREEDY ALGORITHMS
# ============================================================================

def activity_selection(start_times: List[int], 
                       end_times: List[int]) -> List[int]:
    """
    Select maximum non-overlapping activities.
    
    Args:
        start_times: Activity start times
        end_times: Activity end times
        
    Returns:
        Indices of selected activities
        
    Example:
        >>> activity_selection([1, 3, 0, 5, 8], [2, 4, 6, 7, 9])
        [0, 1, 3, 4]
    """
    activities = sorted(enumerate(zip(start_times, end_times)), 
                       key=lambda x: x[1][1])
    
    selected = [activities[0][0]]
    last_end = activities[0][1][1]
    
    for idx, (start, end) in activities[1:]:
        if start >= last_end:
            selected.append(idx)
            last_end = end
    
    return sorted(selected)


def fractional_knapsack(weights: List[float], values: List[float], 
                        capacity: float) -> float:
    """
    Fractional knapsack problem.
    
    Args:
        weights: Item weights
        values: Item values
        capacity: Knapsack capacity
        
    Returns:
        Maximum value achievable
        
    Example:
        >>> fractional_knapsack([10, 20, 30], [60, 100, 120], 50)
        240.0
    """
    items = sorted(zip(values, weights), key=lambda x: x[0]/x[1], reverse=True)
    total_value = 0
    remaining = capacity
    
    for value, weight in items:
        if weight <= remaining:
            total_value += value
            remaining -= weight
        else:
            total_value += value * (remaining / weight)
            break
    
    return total_value


def huffman_encoding(frequencies: Dict[str, int]) -> Dict[str, str]:
    """
    Generate Huffman codes for characters.
    
    Args:
        frequencies: Character frequencies
        
    Returns:
        Dictionary of character: code
        
    Example:
        >>> codes = huffman_encoding({'a': 5, 'b': 9, 'c': 12})
        >>> len(codes)
        3
    """
    if len(frequencies) == 1:
        return {list(frequencies.keys())[0]: '0'}
    
    heap = [[freq, [char, ""]] for char, freq in frequencies.items()]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    
    return {char: code for char, code in heap[0][1:]}


# ============================================================================
# SEARCHING & SELECTION
# ============================================================================

def binary_search_recursive(arr: List[int], target: int, 
                           left: int = 0, right: Optional[int] = None) -> int:
    """
    Recursive binary search.
    
    Args:
        arr: Sorted array
        target: Element to find
        left: Left bound
        right: Right bound
        
    Returns:
        Index of target, -1 if not found
        
    Example:
        >>> binary_search_recursive([1, 2, 3, 4, 5], 3)
        2
    """
    if right is None:
        right = len(arr) - 1
    
    if left > right:
        return -1
    
    mid = (left + right) // 2
    
    if arr[mid] == target:
        return mid
    elif arr[mid] > target:
        return binary_search_recursive(arr, target, left, mid - 1)
    else:
        return binary_search_recursive(arr, target, mid + 1, right)


def exponential_search(arr: List[int], target: int) -> int:
    """
    Exponential search algorithm.
    
    Args:
        arr: Sorted array
        target: Element to find
        
    Returns:
        Index of target, -1 if not found
        
    Example:
        >>> exponential_search([1, 2, 3, 4, 5, 6, 7, 8], 5)
        4
    """
    if arr[0] == target:
        return 0
    
    i = 1
    while i < len(arr) and arr[i] <= target:
        i *= 2
    
    return binary_search_recursive(arr, target, i // 2, min(i, len(arr) - 1))


def jump_search(arr: List[int], target: int) -> int:
    """
    Jump search algorithm.
    
    Args:
        arr: Sorted array
        target: Element to find
        
    Returns:
        Index of target, -1 if not found
        
    Example:
        >>> jump_search([0, 1, 2, 3, 4, 5, 6, 7, 8], 6)
        6
    """
    n = len(arr)
    step = int(n ** 0.5)
    prev = 0
    
    while arr[min(step, n) - 1] < target:
        prev = step
        step += int(n ** 0.5)
        if prev >= n:
            return -1
    
    while arr[prev] < target:
        prev += 1
        if prev == min(step, n):
            return -1
    
    if arr[prev] == target:
        return prev
    
    return -1


def interpolation_search(arr: List[int], target: int) -> int:
    """
    Interpolation search for uniformly distributed data.
    
    Args:
        arr: Sorted array
        target: Element to find
        
    Returns:
        Index of target, -1 if not found
        
    Example:
        >>> interpolation_search([10, 20, 30, 40, 50], 30)
        2
    """
    left, right = 0, len(arr) - 1
    
    while left <= right and arr[left] <= target <= arr[right]:
        if left == right:
            if arr[left] == target:
                return left
            return -1
        
        pos = left + int((target - arr[left]) / (arr[right] - arr[left]) * (right - left))
        
        if arr[pos] == target:
            return pos
        elif arr[pos] < target:
            left = pos + 1
        else:
            right = pos - 1
    
    return -1


def kth_smallest(arr: List[int], k: int) -> int:
    """
    Find kth smallest element (1-indexed).
    
    Args:
        arr: Unsorted array
        k: Position (1-indexed)
        
    Returns:
        kth smallest element
        
    Example:
        >>> kth_smallest([7, 10, 4, 3, 20, 15], 3)
        7
    """
    return sorted(arr)[k - 1]


def kth_largest(arr: List[int], k: int) -> int:
    """
    Find kth largest element (1-indexed).
    
    Args:
        arr: Unsorted array
        k: Position (1-indexed)
        
    Returns:
        kth largest element
        
    Example:
        >>> kth_largest([7, 10, 4, 3, 20, 15], 2)
        15
    """
    return sorted(arr, reverse=True)[k - 1]


# ============================================================================
# ARRAY ALGORITHMS
# ============================================================================

def kadanes_max_subarray(arr: List[int]) -> int:
    """
    Kadane's algorithm for maximum subarray sum.
    
    Args:
        arr: Input array
        
    Returns:
        Maximum subarray sum
        
    Example:
        >>> kadanes_max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4])
        6
    """
    max_sum = float('-inf')
    current_sum = 0
    
    for num in arr:
        current_sum = max(num, current_sum + num)
        max_sum = max(max_sum, current_sum)
    
    return max_sum


def sliding_window_max(arr: List[int], k: int) -> List[int]:
    """
    Maximum in each sliding window of size k.
    
    Args:
        arr: Input array
        k: Window size
        
    Returns:
        List of maximums
        
    Example:
        >>> sliding_window_max([1, 3, -1, -3, 5, 3, 6, 7], 3)
        [3, 3, 5, 5, 6, 7]
    """
    if not arr or k == 0:
        return []
    
    result = []
    for i in range(len(arr) - k + 1):
        result.append(max(arr[i:i+k]))
    
    return result


def two_pointer_sum(arr: List[int], target: int) -> Optional[Tuple[int, int]]:
    """
    Find two numbers that sum to target using two pointers.
    
    Args:
        arr: Sorted array
        target: Target sum
        
    Returns:
        Tuple of (index1, index2) or None
        
    Example:
        >>> two_pointer_sum([1, 2, 3, 4, 5], 9)
        (3, 4)
    """
    left, right = 0, len(arr) - 1
    
    while left < right:
        current_sum = arr[left] + arr[right]
        if current_sum == target:
            return (left, right)
        elif current_sum < target:
            left += 1
        else:
            right -= 1
    
    return None


def dutch_national_flag(arr: List[int], pivot: int) -> List[int]:
    """
    Dutch National Flag algorithm (3-way partitioning).
    
    Args:
        arr: Array to partition
        pivot: Pivot value
        
    Returns:
        Partitioned array
        
    Example:
        >>> dutch_national_flag([2, 0, 1, 2, 1, 0], 1)
        [0, 0, 1, 1, 2, 2]
    """
    result = arr.copy()
    low, mid, high = 0, 0, len(result) - 1
    
    while mid <= high:
        if result[mid] < pivot:
            result[low], result[mid] = result[mid], result[low]
            low += 1
            mid += 1
        elif result[mid] > pivot:
            result[mid], result[high] = result[high], result[mid]
            high -= 1
        else:
            mid += 1
    
    return result


def rotate_array(arr: List[int], k: int) -> List[int]:
    """
    Rotate array right by k positions.
    
    Args:
        arr: Array to rotate
        k: Number of positions
        
    Returns:
        Rotated array
        
    Example:
        >>> rotate_array([1, 2, 3, 4, 5], 2)
        [4, 5, 1, 2, 3]
    """
    n = len(arr)
    k = k % n
    return arr[-k:] + arr[:-k]


# ============================================================================
# BIT MANIPULATION
# ============================================================================

def count_set_bits(n: int) -> int:
    """
    Count number of set bits (1s) in binary representation.
    
    Args:
        n: Integer
        
    Returns:
        Number of set bits
        
    Example:
        >>> count_set_bits(13)  # 1101 in binary
        3
    """
    count = 0
    while n:
        count += n & 1
        n >>= 1
    return count


def power_of_two(n: int) -> bool:
    """
    Check if number is power of 2.
    
    Args:
        n: Integer
        
    Returns:
        True if power of 2
        
    Example:
        >>> power_of_two(16)
        True
    """
    return n > 0 and (n & (n - 1)) == 0


def find_missing_number(arr: List[int], n: int) -> int:
    """
    Find missing number in array [0, n] using XOR.
    
    Args:
        arr: Array with one missing number
        n: Expected range [0, n]
        
    Returns:
        Missing number
        
    Example:
        >>> find_missing_number([0, 1, 3], 3)
        2
    """
    xor_all = 0
    for i in range(n + 1):
        xor_all ^= i
    
    for num in arr:
        xor_all ^= num
    
    return xor_all


def single_number(arr: List[int]) -> int:
    """
    Find single number (all others appear twice).
    
    Args:
        arr: Array where all but one number appears twice
        
    Returns:
        The single number
        
    Example:
        >>> single_number([2, 2, 1])
        1
    """
    result = 0
    for num in arr:
        result ^= num
    return result


def reverse_bits(n: int, bit_count: int = 32) -> int:
    """
    Reverse bits of an integer.
    
    Args:
        n: Integer
        bit_count: Number of bits
        
    Returns:
        Integer with reversed bits
        
    Example:
        >>> reverse_bits(43261596, 32) & 0xFFFFFFFF
        964176192
    """
    result = 0
    for _ in range(bit_count):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result
