"""
Database Drivers Package

Universal connection interfaces for databases, message queues, caches, and storage.
Pure Python implementations with optional external drivers.

Provides:
- Connection pooling and management
- Retry logic and error handling
- Consistent interface across different systems
- Context managers for automatic cleanup
- Query builders and helpers
"""

from .database_drivers import *
from .message_queue_drivers import *
from .cache_drivers import *
from .connection_pool import *

__all__ = [
    # Database drivers
    'SQLiteDriver',
    'PostgreSQLDriver',
    'MySQLDriver',
    'MongoDBDriver',
    
    # Message queues
    'RedisQueueDriver',
    'RabbitMQDriver',
    'KafkaDriver',
    'InMemoryQueueDriver',
    
    # Cache
    'RedisCacheDriver',
    'MemcachedDriver',
    'InMemoryCacheDriver',
    
    # Connection pooling
    'ConnectionPool',
    'PooledConnection',
    'connection_retry',
]
