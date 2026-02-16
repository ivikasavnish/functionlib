"""
Connection Pool Management

Generic connection pooling for any resource with retry logic and health checks.
"""

import time
import threading
from typing import Any, Callable, Optional, List, Dict
from collections import deque
from contextlib import contextmanager


class PooledConnection:
    """Wrapper for a pooled connection with metadata."""
    
    def __init__(self, connection: Any, pool: 'ConnectionPool'):
        self.connection = connection
        self.pool = pool
        self.created_at = time.time()
        self.last_used = time.time()
        self.use_count = 0
        self.is_healthy = True
    
    def __enter__(self):
        return self.connection
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.return_connection(self)
        return False


class ConnectionPool:
    """
    Generic connection pool with configurable limits and health checks.
    
    Args:
        factory: Function to create new connections
        max_size: Maximum pool size
        min_size: Minimum pool size
        max_idle: Maximum idle time before closing (seconds)
        health_check: Function to check connection health
        
    Example:
        >>> def create_conn():
        ...     return sqlite3.connect('db.sqlite')
        >>> pool = ConnectionPool(create_conn, max_size=10)
        >>> with pool.get_connection() as conn:
        ...     conn.execute("SELECT 1")
    """
    
    def __init__(
        self,
        factory: Callable[[], Any],
        max_size: int = 10,
        min_size: int = 2,
        max_idle: float = 300.0,
        health_check: Optional[Callable[[Any], bool]] = None
    ):
        self.factory = factory
        self.max_size = max_size
        self.min_size = min_size
        self.max_idle = max_idle
        self.health_check = health_check or (lambda x: True)
        
        self._pool: deque = deque()
        self._lock = threading.RLock()
        self._size = 0
        self._closed = False
        
        # Pre-create minimum connections
        for _ in range(min_size):
            try:
                conn = self._create_connection()
                self._pool.append(conn)
            except Exception:
                pass
    
    def _create_connection(self) -> PooledConnection:
        """Create a new pooled connection."""
        with self._lock:
            if self._size >= self.max_size:
                raise RuntimeError(f"Connection pool full (max={self.max_size})")
            
            conn = self.factory()
            self._size += 1
            return PooledConnection(conn, self)
    
    @contextmanager
    def get_connection(self, timeout: float = 30.0):
        """
        Get a connection from the pool.
        
        Args:
            timeout: Maximum time to wait for a connection
            
        Yields:
            Connection from pool
            
        Example:
            >>> with pool.get_connection() as conn:
            ...     conn.execute("SELECT 1")
        """
        if self._closed:
            raise RuntimeError("Connection pool is closed")
        
        start_time = time.time()
        pooled = None
        
        while True:
            with self._lock:
                # Try to get existing connection
                while self._pool:
                    pooled = self._pool.popleft()
                    
                    # Check if connection is still healthy
                    if self._is_connection_valid(pooled):
                        pooled.use_count += 1
                        pooled.last_used = time.time()
                        break
                    else:
                        # Connection is stale, close it
                        self._close_connection(pooled)
                        pooled = None
                
                if pooled:
                    break
                
                # Try to create new connection if under limit
                if self._size < self.max_size:
                    try:
                        pooled = self._create_connection()
                        pooled.use_count += 1
                        pooled.last_used = time.time()
                        break
                    except Exception as e:
                        raise RuntimeError(f"Failed to create connection: {e}")
            
            # Wait for a connection to be returned
            if time.time() - start_time > timeout:
                raise TimeoutError("Timeout waiting for connection from pool")
            
            time.sleep(0.1)
        
        try:
            yield pooled.connection
        finally:
            self.return_connection(pooled)
    
    def return_connection(self, pooled: PooledConnection):
        """Return a connection to the pool."""
        with self._lock:
            if self._closed:
                self._close_connection(pooled)
                return
            
            # Check if connection is still healthy
            if self._is_connection_valid(pooled):
                self._pool.append(pooled)
            else:
                self._close_connection(pooled)
    
    def _is_connection_valid(self, pooled: PooledConnection) -> bool:
        """Check if connection is still valid."""
        # Check idle time
        idle_time = time.time() - pooled.last_used
        if idle_time > self.max_idle:
            return False
        
        # Run health check
        try:
            return self.health_check(pooled.connection)
        except Exception:
            return False
    
    def _close_connection(self, pooled: PooledConnection):
        """Close a connection and update pool size."""
        try:
            if hasattr(pooled.connection, 'close'):
                pooled.connection.close()
        except Exception:
            pass
        finally:
            with self._lock:
                self._size -= 1
    
    def close_all(self):
        """Close all connections in the pool."""
        with self._lock:
            self._closed = True
            while self._pool:
                pooled = self._pool.popleft()
                self._close_connection(pooled)
    
    def get_stats(self) -> Dict[str, int]:
        """Get pool statistics."""
        with self._lock:
            return {
                'size': self._size,
                'available': len(self._pool),
                'in_use': self._size - len(self._pool),
                'max_size': self.max_size,
            }
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close_all()
        return False


def connection_retry(
    func: Callable,
    max_retries: int = 3,
    retry_delay: float = 1.0,
    backoff_multiplier: float = 2.0,
    exceptions: tuple = (Exception,)
) -> Any:
    """
    Retry a function call with exponential backoff.
    
    Args:
        func: Function to retry
        max_retries: Maximum number of retries
        retry_delay: Initial delay between retries
        backoff_multiplier: Multiplier for exponential backoff
        exceptions: Tuple of exceptions to catch and retry
        
    Returns:
        Result of successful function call
        
    Raises:
        Last exception if all retries fail
        
    Example:
        >>> def connect():
        ...     return sqlite3.connect('db.sqlite')
        >>> conn = connection_retry(connect, max_retries=3)
    """
    last_exception = None
    delay = retry_delay
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        except exceptions as e:
            last_exception = e
            if attempt < max_retries:
                time.sleep(delay)
                delay *= backoff_multiplier
            else:
                raise last_exception
    
    # Should not reach here, but just in case
    raise last_exception


__all__ = [
    'ConnectionPool',
    'PooledConnection',
    'connection_retry',
]
