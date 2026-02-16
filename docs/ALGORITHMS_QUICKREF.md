# Advanced Algorithms Quick Reference

**53 Classical Computer Science Algorithms** | Zero Dependencies | Pure Python

## 🔍 String Search (5)

```python
from functionlib.coding.advanced_algorithms import *

# Pattern matching - O(n+m) complexity
kmp_search("text", "pattern")              # Knuth-Morris-Pratt
boyer_moore_search("text", "pattern")      # Boyer-Moore with bad char
rabin_karp_search("text", "pattern")       # Rolling hash
naive_string_search("text", "pattern")     # Brute force O(nm)
find_all_occurrences("text", "pattern")    # All positions
```

## 🧬 Pattern Matching (5)

```python
# Sequence comparison
longest_common_subsequence(s1, s2)         # LCS length - O(nm)
edit_distance(s1, s2)                      # Levenshtein distance
hamming_distance(s1, s2)                   # Bit differences
fuzzy_match(s1, s2, threshold)             # Approximate matching
pattern_match_wildcard(text, pattern)      # Wildcard support
```

## 🕸️ Graph - Shortest Path (5)

```python
# Single and all-pairs shortest paths
dijkstra_shortest_path(graph, start, end)  # O((V+E)logV)
bellman_ford(graph, start)                 # Negative weights OK
floyd_warshall(graph)                      # All pairs - O(V³)
a_star_search(graph, start, end, h)        # A* with heuristic
bfs_shortest_path(graph, start, end)       # Unweighted graphs
```

**Graph format:** `{node: [(neighbor, weight), ...]}`

## 🌲 Graph - Traversal (5)

```python
# Graph exploration
depth_first_search(graph, start)           # DFS order
breadth_first_search(graph, start)         # BFS order
topological_sort(graph)                    # Linear ordering (DAG)
strongly_connected_components(graph)       # Tarjan's algorithm
has_cycle(graph)                           # Cycle detection
```

## 🌳 Graph - Spanning Trees (3)

```python
# Minimum spanning tree
kruskal_mst(edges)                         # O(E log E) + union-find
prim_mst(graph, start)                     # O((V+E) log V)
is_connected_graph(graph)                  # Connectivity check
```

**Edges format:** `[(node1, node2, weight), ...]`

## 📊 Advanced Sorting (6)

```python
# Specialized sorting algorithms
heap_sort(arr)                             # O(n log n) in-place
counting_sort(arr)                         # O(n+k) integers
radix_sort(arr)                            # O(d(n+k)) integers
bucket_sort(arr)                           # O(n+k) floats [0,1)
shell_sort(arr)                            # Gap-based insertion
tim_sort(arr)                              # Hybrid merge-insertion
```

## 💎 Dynamic Programming (5)

```python
# Classic DP problems
knapsack_01(weights, values, capacity)     # 0/1 knapsack
knapsack_unbounded(weights, values, cap)   # Unlimited items
coin_change(coins, amount)                 # Min coins needed
longest_increasing_subsequence(arr)        # LIS length
matrix_chain_multiplication(dims)          # Optimal parenthesization
```

## 🎯 Greedy Algorithms (3)

```python
# Greedy optimization
activity_selection(activities)             # Max non-overlapping
fractional_knapsack(w, v, capacity)        # Fractional items OK
huffman_encoding(text)                     # Optimal prefix codes
```

## 🔎 Searching & Selection (6)

```python
# Advanced search techniques
binary_search_recursive(arr, target)       # Recursive O(log n)
exponential_search(arr, target)            # For unbounded arrays
jump_search(arr, target)                   # O(√n) jumps
interpolation_search(arr, target)          # For uniform distribution
kth_smallest_element(arr, k)               # Quick select O(n)
ternary_search(arr, target)                # Three-way divide
```

## 📈 Array Algorithms (5)

```python
# Essential array patterns
kadanes_max_subarray(arr)                  # Max subarray sum O(n)
sliding_window_maximum(arr, k)             # Window max values
two_pointer_sum(arr, target)               # Find pair sum
dutch_national_flag(arr)                   # 3-way partition
rotate_array(arr, k)                       # Rotate by k positions
```

## ⚡ Bit Manipulation (5)

```python
# Bitwise operations
count_set_bits(n)                          # Population count
power_of_two(n)                            # Check if 2^x
find_missing_number(arr, n)                # XOR-based
single_number(arr)                         # Find unique element
reverse_bits(n)                            # Bit reversal
```

---

## Complexity Summary

| Algorithm Category | Time | Space | Use Case |
|-------------------|------|-------|----------|
| **String Search** |
| KMP | O(n+m) | O(m) | General pattern matching |
| Boyer-Moore | O(n/m) best | O(m) | Long patterns |
| Rabin-Karp | O(n+m) avg | O(1) | Multiple patterns |
| **Graph - Shortest Path** |
| Dijkstra | O((V+E)logV) | O(V) | Positive weights |
| Bellman-Ford | O(VE) | O(V) | Negative weights |
| Floyd-Warshall | O(V³) | O(V²) | All pairs |
| A* | Heuristic-dep | O(V) | With good heuristic |
| **Graph - Traversal** |
| DFS/BFS | O(V+E) | O(V) | Graph exploration |
| Topological Sort | O(V+E) | O(V) | Task ordering |
| Tarjan's SCC | O(V+E) | O(V) | Strongly connected |
| **Graph - MST** |
| Kruskal | O(E log E) | O(V) | Sparse graphs |
| Prim | O((V+E)logV) | O(V) | Dense graphs |
| **Sorting** |
| Heap Sort | O(n log n) | O(1) | In-place guaranteed |
| Counting Sort | O(n+k) | O(k) | Small integer range |
| Radix Sort | O(d(n+k)) | O(n+k) | Fixed-width integers |
| **Dynamic Programming** |
| Knapsack 0/1 | O(nW) | O(nW) | Binary choice |
| Coin Change | O(nA) | O(A) | Min/count solutions |
| LCS | O(nm) | O(nm) | Sequence comparison |
| LIS | O(n²) or O(nlogn) | O(n) | Increasing subsequence |
| **Array** |
| Kadane's | O(n) | O(1) | Max subarray |
| Two Pointer | O(n) | O(1) | Sorted array search |
| Sliding Window | O(n) | O(k) | Window operations |

## Common Patterns

### Graph Algorithms
```python
# Adjacency list format
graph = {
    'A': [('B', 1), ('C', 4)],  # Weighted
    'B': ['C', 'D'],            # Unweighted
}

# Edge list format
edges = [('A', 'B', 1), ('B', 'C', 2)]
```

### Dynamic Programming Table
```python
# 2D DP table initialization
dp = [[0] * (cols + 1) for _ in range(rows + 1)]

# Fill table bottom-up
for i in range(1, rows + 1):
    for j in range(1, cols + 1):
        dp[i][j] = # recurrence relation
```

### String Search Preprocessing
```python
# KMP failure function
def compute_lps(pattern):
    lps = [0] * len(pattern)
    # Build longest proper prefix-suffix array
    return lps
```

### Union-Find (for graph algorithms)
```python
parent = {v: v for v in vertices}

def find(x):
    if parent[x] != x:
        parent[x] = find(parent[x])  # Path compression
    return parent[x]

def union(x, y):
    parent[find(x)] = find(y)
```

## Real-World Applications

| Algorithm | Application |
|-----------|-------------|
| **KMP/Boyer-Moore** | Text editors, search engines, DNA sequencing |
| **Rabin-Karp** | Plagiarism detection, pattern matching in large texts |
| **Dijkstra** | GPS navigation, network routing, game pathfinding |
| **A*** | Game AI, robotics, route planning |
| **Topological Sort** | Build systems, task scheduling, course prerequisites |
| **MST** | Network design, clustering, image segmentation |
| **Counting/Radix Sort** | Integer sorting, database indexing |
| **Knapsack** | Resource allocation, portfolio optimization |
| **Huffman Encoding** | Data compression (ZIP, JPEG, MP3) |
| **LCS/Edit Distance** | Diff tools, spell checkers, bioinformatics |
| **Kadane's** | Stock trading (max profit), data stream analysis |
| **Bit Manipulation** | Low-level optimization, cryptography, compression |

## Testing Examples

```python
# Import all at once
from functionlib.coding.advanced_algorithms import *

# String search
text = "ABABDABACDABABCABAB"
assert kmp_search(text, "ABABCABAB") == 10

# Graph shortest path
graph = {'A': [('B', 1), ('C', 4)], 'B': [('C', 2), ('D', 5)], 
         'C': [('D', 1)], 'D': []}
path, dist = dijkstra_shortest_path(graph, 'A', 'D')
assert dist == 4

# Dynamic programming
assert knapsack_01([2, 3, 4], [3, 4, 5], 5) == 7
assert coin_change([1, 2, 5], 11) == 3

# Array algorithms
assert kadanes_max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == 6

# Bit manipulation
assert count_set_bits(13) == 3  # 1101 binary
assert power_of_two(16) == True
```

## Performance Tips

1. **String Search**
   - Use KMP for general cases
   - Use Boyer-Moore for long patterns
   - Use Rabin-Karp for multiple patterns

2. **Graph Algorithms**
   - Dijkstra for sparse graphs with positive weights
   - Bellman-Ford only when negative weights exist
   - Floyd-Warshall for dense graphs or all-pairs

3. **Sorting**
   - Use counting sort for small integer ranges
   - Use radix sort for fixed-width integers
   - Use heap sort when stable sorting not needed

4. **Dynamic Programming**
   - Use tabulation (bottom-up) for better performance
   - Consider space optimization (1D array)
   - Memoization for recursive solutions

5. **Array Operations**
   - Two pointer for sorted arrays
   - Sliding window for subarray problems
   - Kadane's for maximum subarray

---

**Library:** functionlib v1.0  
**Module:** `functionlib.coding.advanced_algorithms`  
**Functions:** 53  
**Dependencies:** Pure Python stdlib (heapq, deque, defaultdict)  
**License:** Open source

📚 See PHASE_10_SUMMARY.md for detailed documentation and examples.
