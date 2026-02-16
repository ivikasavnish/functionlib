"""
Cache Drivers

Universal interfaces for caching systems.
Provides consistent API with TTL support and optional compression.
"""

import time
import json
import threading
from typing import Any, Optional, Dict
from abc import ABC, abstractmethod
from collections import OrderedDict


class CacheDriver(ABC):
    """Abstract base class for cache drivers."""
    
    @abstractmethod
    def connect(self) -> Any:
        """Establish connection to cache."""
        pass
    
    @abstractmethod
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        pass
    
    @abstractmethod
    def set(self, key: str, value: Any, ttl: int = 0) -> bool:
        """Set value in cache with optional TTL."""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        pass
    
    @abstractmethod
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        pass
    
    @abstractmethod
    def clear(self) -> bool:
        """Clear all cache entries."""
        pass
    
    @abstractmethod
    def close(self):
        """Close connection."""
        pass


class InMemoryCacheDriver(CacheDriver):
    """
    In-memory cache with LRU eviction and TTL support.
    
    Pure Python implementation using OrderedDict and threading.
    
    Args:
        max_size: Maximum cache entries (0 = unlimited)
        default_ttl: Default TTL in seconds (0 = no expiration)
        
    Example:
        >>> cache = InMemoryCacheDriver(max_size=100)
        >>> cache.connect()
        >>> cache.set('user:1', {'name': 'John'}, ttl=60)
        >>> user = cache.get('user:1')
    """
    
    def __init__(self, max_size: int = 1000, default_ttl: int = 0):
        self.max_size = max_size
        self.default_ttl = default_ttl
        self._cache: OrderedDict = OrderedDict()
        self._expiry: Dict[str, float] = {}
        self._lock = threading.RLock()
    
    def connect(self) -> 'InMemoryCacheDriver':
        """Initialize (no actual connection needed)."""
        return self
    
    def _is_expired(self, key: str) -> bool:
        """Check if key has expired."""
        if key not in self._expiry:
            return False
        return time.time() > self._expiry[key]
    
    def _evict_lru(self):
        """Evict least recently used item."""
        if self._cache:
            key, _ = self._cache.popitem(last=False)
            self._expiry.pop(key, None)
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found/expired
        """
        with self._lock:
            if key not in self._cache:
                return None
            
            # Check expiration
            if self._is_expired(key):
                del self._cache[key]
                self._expiry.pop(key, None)
                return None
            
            # Move to end (mark as recently used)
            self._cache.move_to_end(key)
            
            # Try to deserialize JSON
            value = self._cache[key]
            if isinstance(value, str):
                try:
                    return json.loads(value)
                except json.JSONDecodeError:
                    return value
            return value
    
    def set(self, key: str, value: Any, ttl: int = 0) -> bool:
        """
        Set value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds (0 = default TTL)
            
        Returns:
            True if successful
        """
        with self._lock:
            # Serialize if needed
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            # Check size limit
            if self.max_size > 0 and key not in self._cache:
                if len(self._cache) >= self.max_size:
                    self._evict_lru()
            
            # Set value
            self._cache[key] = value
            self._cache.move_to_end(key)
            
            # Set expiry
            ttl = ttl or self.default_ttl
            if ttl > 0:
                self._expiry[key] = time.time() + ttl
            elif key in self._expiry:
                del self._expiry[key]
            
            return True
    
    def delete(self, key: str) -> bool:
        """Delete key from cache."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                self._expiry.pop(key, None)
                return True
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists and is not expired."""
        with self._lock:
            if key not in self._cache:
                return False
            if self._is_expired(key):
                del self._cache[key]
                self._expiry.pop(key, None)
                return False
            return True
    
    def clear(self) -> bool:
        """Clear all cache entries."""
        with self._lock:
            self._cache.clear()
            self._expiry.clear()
            return True
    
    def size(self) -> int:
        """Get number of cached items."""
        with self._lock:
            # Clean expired items
            expired = [k for k in self._cache.keys() if self._is_expired(k)]
            for k in expired:
                del self._cache[k]
                self._expiry.pop(k, None)
            return len(self._cache)
    
    def get_stats(self) -> Dict[str, int]:
        """Get cache statistics."""
        with self._lock:
            return {
                'size': len(self._cache),
                'max_size': self.max_size,
                'expired': sum(1 for k in self._cache.keys() if self._is_expired(k))
            }
    
    def close(self):
        """Clear cache."""
        self.clear()


class RedisCacheDriver(CacheDriver):
    """
    Redis-based cache driver.
    
    Requires redis package. Provides fallback interface.
    
    Args:
        host: Redis host
        port: Redis port
        db: Redis database number
        password: Redis password (optional)
        prefix: Key prefix for namespacing
        
    Example:
        >>> cache = RedisCacheDriver(prefix='app:')
        >>> cache.connect()
        >>> cache.set('user:1', {'name': 'John'}, ttl=60)
        >>> user = cache.get('user:1')
    """
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        prefix: str = ''
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self.prefix = prefix
        self._client: Optional[Any] = None
        self._has_redis = False
        
        try:
            import redis
            self._redis = redis
            self._has_redis = True
        except ImportError:
            pass
    
    def connect(self) -> 'RedisCacheDriver':
        """Connect to Redis."""
        if not self._has_redis:
            raise RuntimeError("redis package not installed")
        
        self._client = self._redis.Redis(
            host=self.host,
            port=self.port,
            db=self.db,
            password=self.password,
            decode_responses=True
        )
        
        # Test connection
        self._client.ping()
        return self
    
    def _make_key(self, key: str) -> str:
        """Add prefix to key."""
        return f"{self.prefix}{key}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from Redis."""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        
        value = self._client.get(self._make_key(key))
        if value is None:
            return None
        
        # Try to deserialize JSON
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    def set(self, key: str, value: Any, ttl: int = 0) -> bool:
        """Set value in Redis with optional TTL."""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        
        try:
            # Serialize if needed
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            if ttl > 0:
                self._client.setex(self._make_key(key), ttl, value)
            else:
                self._client.set(self._make_key(key), value)
            return True
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from Redis."""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        
        return self._client.delete(self._make_key(key)) > 0
    
    def exists(self, key: str) -> bool:
        """Check if key exists in Redis."""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        
        return self._client.exists(self._make_key(key)) > 0
    
    def clear(self) -> bool:
        """Clear all keys with prefix."""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        
        try:
            if self.prefix:
                # Delete keys matching prefix
                pattern = f"{self.prefix}*"
                keys = self._client.keys(pattern)
                if keys:
                    self._client.delete(*keys)
            else:
                # Flush entire database
                self._client.flushdb()
            return True
        except Exception:
            return False
    
    def increment(self, key: str, amount: int = 1) -> int:
        """Increment key value."""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        
        return self._client.incrby(self._make_key(key), amount)
    
    def decrement(self, key: str, amount: int = 1) -> int:
        """Decrement key value."""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        
        return self._client.decrby(self._make_key(key), amount)
    
    def close(self):
        """Close Redis connection."""
        if self._client:
            self._client.close()


class MemcachedDriver(CacheDriver):
    """
    Memcached cache driver.
    
    Requires pymemcache package. Provides fallback interface.
    
    Args:
        servers: Memcached server addresses
        prefix: Key prefix for namespacing
        
    Example:
        >>> cache = MemcachedDriver(servers=[('localhost', 11211)])
        >>> cache.connect()
        >>> cache.set('user:1', {'name': 'John'}, ttl=60)
        >>> user = cache.get('user:1')
    """
    
    def __init__(
        self,
        servers: list = None,
        prefix: str = ''
    ):
        self.servers = servers or [('localhost', 11211)]
        self.prefix = prefix
        self._client: Optional[Any] = None
        self._has_memcache = False
        
        try:
            from pymemcache.client.base import Client
            self._memcache_client = Client
            self._has_memcache = True
        except ImportError:
            pass
    
    def connect(self) -> 'MemcachedDriver':
        """Connect to Memcached."""
        if not self._has_memcache:
            raise RuntimeError("pymemcache package not installed")
        
        # Use first server (for simplicity)
        server = self.servers[0]
        self._client = self._memcache_client(server)
        return self
    
    def _make_key(self, key: str) -> str:
        """Add prefix to key."""
        return f"{self.prefix}{key}"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from Memcached."""
        if not self._client:
            raise RuntimeError("Not connected to Memcached")
        
        value = self._client.get(self._make_key(key))
        if value is None:
            return None
        
        # Decode if bytes
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        
        # Try to deserialize JSON
        try:
            return json.loads(value)
        except json.JSONDecodeError:
            return value
    
    def set(self, key: str, value: Any, ttl: int = 0) -> bool:
        """Set value in Memcached with optional TTL."""
        if not self._client:
            raise RuntimeError("Not connected to Memcached")
        
        try:
            # Serialize if needed
            if isinstance(value, (dict, list)):
                value = json.dumps(value)
            
            # Convert to bytes
            if isinstance(value, str):
                value = value.encode('utf-8')
            
            self._client.set(self._make_key(key), value, expire=ttl)
            return True
        except Exception:
            return False
    
    def delete(self, key: str) -> bool:
        """Delete key from Memcached."""
        if not self._client:
            raise RuntimeError("Not connected to Memcached")
        
        return self._client.delete(self._make_key(key))
    
    def exists(self, key: str) -> bool:
        """Check if key exists (by trying to get it)."""
        return self.get(key) is not None
    
    def clear(self) -> bool:
        """Flush all cache (warning: affects entire server)."""
        if not self._client:
            raise RuntimeError("Not connected to Memcached")
        
        try:
            self._client.flush_all()
            return True
        except Exception:
            return False
    
    def close(self):
        """Close Memcached connection."""
        if self._client:
            self._client.close()


__all__ = [
    'CacheDriver',
    'InMemoryCacheDriver',
    'RedisCacheDriver',
    'MemcachedDriver',
]
