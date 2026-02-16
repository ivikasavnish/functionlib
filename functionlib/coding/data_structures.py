"""
Data Structures

Common data structure implementations and operations.
"""

from typing import List, Any, Optional, Tuple
import heapq


class Stack:
    """
    Stack (LIFO) implementation
    
    Example:
        >>> s = Stack()
        >>> s.push(1)
        >>> s.push(2)
        >>> s.pop()
        2
    """
    
    def __init__(self):
        self.items = []
    
    def push(self, item: Any) -> None:
        """Add item to top of stack"""
        self.items.append(item)
    
    def pop(self) -> Any:
        """Remove and return top item"""
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self.items.pop()
    
    def peek(self) -> Any:
        """Return top item without removing"""
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self.items[-1]
    
    def is_empty(self) -> bool:
        """Check if stack is empty"""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Return number of items"""
        return len(self.items)


class Queue:
    """
    Queue (FIFO) implementation
    
    Example:
        >>> q = Queue()
        >>> q.enqueue(1)
        >>> q.enqueue(2)
        >>> q.dequeue()
        1
    """
    
    def __init__(self):
        self.items = []
    
    def enqueue(self, item: Any) -> None:
        """Add item to rear of queue"""
        self.items.append(item)
    
    def dequeue(self) -> Any:
        """Remove and return front item"""
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self.items.pop(0)
    
    def front(self) -> Any:
        """Return front item without removing"""
        if self.is_empty():
            raise IndexError("Front from empty queue")
        return self.items[0]
    
    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self.items) == 0
    
    def size(self) -> int:
        """Return number of items"""
        return len(self.items)


class PriorityQueue:
    """
    Priority Queue implementation using heap
    
    Example:
        >>> pq = PriorityQueue()
        >>> pq.insert(3, "item3")
        >>> pq.insert(1, "item1")
        >>> pq.extract_min()
        'item1'
    """
    
    def __init__(self):
        self.heap = []
    
    def insert(self, priority: float, item: Any) -> None:
        """Insert item with priority"""
        heapq.heappush(self.heap, (priority, item))
    
    def extract_min(self) -> Any:
        """Remove and return item with lowest priority"""
        if self.is_empty():
            raise IndexError("Extract from empty priority queue")
        return heapq.heappop(self.heap)[1]
    
    def peek_min(self) -> Any:
        """Return item with lowest priority without removing"""
        if self.is_empty():
            raise IndexError("Peek from empty priority queue")
        return self.heap[0][1]
    
    def is_empty(self) -> bool:
        """Check if priority queue is empty"""
        return len(self.heap) == 0
    
    def size(self) -> int:
        """Return number of items"""
        return len(self.heap)


class LinkedListNode:
    """Node for linked list"""
    def __init__(self, data: Any):
        self.data = data
        self.next: Optional[LinkedListNode] = None


class LinkedList:
    """
    Singly linked list implementation
    
    Example:
        >>> ll = LinkedList()
        >>> ll.append(1)
        >>> ll.append(2)
        >>> ll.size()
        2
    """
    
    def __init__(self):
        self.head: Optional[LinkedListNode] = None
    
    def append(self, data: Any) -> None:
        """Add item to end of list"""
        new_node = LinkedListNode(data)
        if not self.head:
            self.head = new_node
            return
        
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node
    
    def prepend(self, data: Any) -> None:
        """Add item to beginning of list"""
        new_node = LinkedListNode(data)
        new_node.next = self.head
        self.head = new_node
    
    def delete(self, data: Any) -> bool:
        """Delete first occurrence of data"""
        if not self.head:
            return False
        
        if self.head.data == data:
            self.head = self.head.next
            return True
        
        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next
                return True
            current = current.next
        
        return False
    
    def find(self, data: Any) -> bool:
        """Check if data exists in list"""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False
    
    def size(self) -> int:
        """Return number of items"""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
    
    def to_list(self) -> List[Any]:
        """Convert to Python list"""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result


class BinaryTreeNode:
    """Node for binary tree"""
    def __init__(self, data: Any):
        self.data = data
        self.left: Optional[BinaryTreeNode] = None
        self.right: Optional[BinaryTreeNode] = None


class BinarySearchTree:
    """
    Binary Search Tree implementation
    
    Example:
        >>> bst = BinarySearchTree()
        >>> bst.insert(5)
        >>> bst.insert(3)
        >>> bst.search(3)
        True
    """
    
    def __init__(self):
        self.root: Optional[BinaryTreeNode] = None
    
    def insert(self, data: Any) -> None:
        """Insert data into BST"""
        if not self.root:
            self.root = BinaryTreeNode(data)
        else:
            self._insert_recursive(self.root, data)
    
    def _insert_recursive(self, node: BinaryTreeNode, data: Any) -> None:
        if data < node.data:
            if node.left is None:
                node.left = BinaryTreeNode(data)
            else:
                self._insert_recursive(node.left, data)
        else:
            if node.right is None:
                node.right = BinaryTreeNode(data)
            else:
                self._insert_recursive(node.right, data)
    
    def search(self, data: Any) -> bool:
        """Search for data in BST"""
        return self._search_recursive(self.root, data)
    
    def _search_recursive(self, node: Optional[BinaryTreeNode], data: Any) -> bool:
        if node is None:
            return False
        if node.data == data:
            return True
        if data < node.data:
            return self._search_recursive(node.left, data)
        return self._search_recursive(node.right, data)
    
    def inorder_traversal(self) -> List[Any]:
        """Return inorder traversal of tree"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node: Optional[BinaryTreeNode], result: List[Any]) -> None:
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.data)
            self._inorder_recursive(node.right, result)


class Graph:
    """
    Graph implementation using adjacency list
    
    Example:
        >>> g = Graph()
        >>> g.add_edge(1, 2)
        >>> g.add_edge(1, 3)
        >>> g.neighbors(1)
        [2, 3]
    """
    
    def __init__(self, directed: bool = False):
        self.adjacency_list = {}
        self.directed = directed
    
    def add_vertex(self, vertex: Any) -> None:
        """Add vertex to graph"""
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
    
    def add_edge(self, v1: Any, v2: Any) -> None:
        """Add edge between vertices"""
        self.add_vertex(v1)
        self.add_vertex(v2)
        
        if v2 not in self.adjacency_list[v1]:
            self.adjacency_list[v1].append(v2)
        
        if not self.directed and v1 not in self.adjacency_list[v2]:
            self.adjacency_list[v2].append(v1)
    
    def neighbors(self, vertex: Any) -> List[Any]:
        """Return neighbors of vertex"""
        return self.adjacency_list.get(vertex, [])
    
    def vertices(self) -> List[Any]:
        """Return all vertices"""
        return list(self.adjacency_list.keys())
    
    def has_edge(self, v1: Any, v2: Any) -> bool:
        """Check if edge exists"""
        return v2 in self.adjacency_list.get(v1, [])


# Utility functions

def reverse_list(lst: List[Any]) -> List[Any]:
    """
    Reverses a list
    
    Args:
        lst: Input list
        
    Returns:
        Reversed list
        
    Example:
        >>> reverse_list([1, 2, 3])
        [3, 2, 1]
    """
    return lst[::-1]


def rotate_list(lst: List[Any], k: int) -> List[Any]:
    """
    Rotates list k positions to the right
    
    Args:
        lst: Input list
        k: Number of positions to rotate
        
    Returns:
        Rotated list
        
    Example:
        >>> rotate_list([1, 2, 3, 4, 5], 2)
        [4, 5, 1, 2, 3]
    """
    if not lst:
        return lst
    k = k % len(lst)
    return lst[-k:] + lst[:-k]


def flatten_list(nested_list: List[Any]) -> List[Any]:
    """
    Flattens a nested list
    
    Args:
        nested_list: Nested list structure
        
    Returns:
        Flattened list
        
    Example:
        >>> flatten_list([1, [2, 3], [4, [5, 6]]])
        [1, 2, 3, 4, 5, 6]
    """
    result = []
    for item in nested_list:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result


def chunk_list(lst: List[Any], chunk_size: int) -> List[List[Any]]:
    """
    Splits list into chunks
    
    Args:
        lst: Input list
        chunk_size: Size of each chunk
        
    Returns:
        List of chunks
        
    Example:
        >>> chunk_list([1, 2, 3, 4, 5], 2)
        [[1, 2], [3, 4], [5]]
    """
    return [lst[i:i + chunk_size] for i in range(0, len(lst), chunk_size)]


# Export all
__all__ = [
    'Stack', 'Queue', 'PriorityQueue',
    'LinkedList', 'LinkedListNode',
    'BinarySearchTree', 'BinaryTreeNode',
    'Graph',
    'reverse_list', 'rotate_list', 'flatten_list', 'chunk_list',
]
