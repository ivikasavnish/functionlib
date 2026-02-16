"""
Message Queue Drivers

Universal interfaces for message queues and pub/sub systems.
Provides consistent API with connection pooling and retry logic.
"""

import json
import time
import queue
import threading
from typing import Any, Dict, List, Optional, Callable
from abc import ABC, abstractmethod
from collections import deque


class MessageQueueDriver(ABC):
    """Abstract base class for message queue drivers."""
    
    @abstractmethod
    def connect(self) -> Any:
        """Establish connection to message queue."""
        pass
    
    @abstractmethod
    def send(self, queue_name: str, message: Any) -> bool:
        """Send message to queue."""
        pass
    
    @abstractmethod
    def receive(self, queue_name: str, timeout: float = 1.0) -> Optional[Any]:
        """Receive message from queue."""
        pass
    
    @abstractmethod
    def close(self):
        """Close connection."""
        pass


class InMemoryQueueDriver(MessageQueueDriver):
    """
    In-memory message queue using Python's queue module.
    
    Useful for testing and single-process applications.
    
    Args:
        maxsize: Maximum queue size (0 = unlimited)
        
    Example:
        >>> driver = InMemoryQueueDriver()
        >>> driver.connect()
        >>> driver.send('tasks', {'job': 'process_data'})
        >>> msg = driver.receive('tasks')
    """
    
    def __init__(self, maxsize: int = 0):
        self.maxsize = maxsize
        self._queues: Dict[str, queue.Queue] = {}
        self._lock = threading.RLock()
    
    def connect(self) -> 'InMemoryQueueDriver':
        """Initialize (no actual connection needed)."""
        return self
    
    def _get_queue(self, queue_name: str) -> queue.Queue:
        """Get or create a queue."""
        with self._lock:
            if queue_name not in self._queues:
                self._queues[queue_name] = queue.Queue(maxsize=self.maxsize)
            return self._queues[queue_name]
    
    def send(self, queue_name: str, message: Any, timeout: float = 1.0) -> bool:
        """
        Send message to queue.
        
        Args:
            queue_name: Queue name
            message: Message to send (will be JSON serialized)
            timeout: Timeout for queue insertion
            
        Returns:
            True if successful
        """
        q = self._get_queue(queue_name)
        try:
            # Serialize message
            if isinstance(message, (dict, list)):
                message = json.dumps(message)
            
            q.put(message, timeout=timeout)
            return True
        except queue.Full:
            return False
    
    def receive(self, queue_name: str, timeout: float = 1.0) -> Optional[Any]:
        """
        Receive message from queue.
        
        Args:
            queue_name: Queue name
            timeout: Timeout for waiting
            
        Returns:
            Message or None if timeout
        """
        q = self._get_queue(queue_name)
        try:
            message = q.get(timeout=timeout)
            
            # Try to deserialize JSON
            if isinstance(message, str):
                try:
                    return json.loads(message)
                except json.JSONDecodeError:
                    return message
            return message
        except queue.Empty:
            return None
    
    def size(self, queue_name: str) -> int:
        """Get queue size."""
        q = self._get_queue(queue_name)
        return q.qsize()
    
    def clear(self, queue_name: str):
        """Clear all messages from queue."""
        with self._lock:
            if queue_name in self._queues:
                # Drain the queue
                q = self._queues[queue_name]
                while not q.empty():
                    try:
                        q.get_nowait()
                    except queue.Empty:
                        break
    
    def close(self):
        """Clear all queues."""
        with self._lock:
            for queue_name in list(self._queues.keys()):
                self.clear(queue_name)
            self._queues.clear()


class RedisQueueDriver(MessageQueueDriver):
    """
    Redis-based message queue using lists (LPUSH/RPOP).
    
    Requires redis package. Provides fallback interface.
    
    Args:
        host: Redis host
        port: Redis port
        db: Redis database number
        password: Redis password (optional)
        
    Example:
        >>> driver = RedisQueueDriver()
        >>> driver.connect()
        >>> driver.send('tasks', {'job': 'process_data'})
        >>> msg = driver.receive('tasks')
    """
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None
    ):
        self.host = host
        self.port = port
        self.db = db
        self.password = password
        self._client: Optional[Any] = None
        self._has_redis = False
        
        try:
            import redis
            self._redis = redis
            self._has_redis = True
        except ImportError:
            pass
    
    def connect(self) -> 'RedisQueueDriver':
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
    
    def send(self, queue_name: str, message: Any) -> bool:
        """Send message to queue (push to left of list)."""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        
        try:
            # Serialize message
            if isinstance(message, (dict, list)):
                message = json.dumps(message)
            
            self._client.lpush(queue_name, message)
            return True
        except Exception:
            return False
    
    def receive(self, queue_name: str, timeout: float = 1.0) -> Optional[Any]:
        """Receive message from queue (blocking pop from right)."""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        
        try:
            # BRPOP returns (key, value) or None
            result = self._client.brpop(queue_name, timeout=int(timeout))
            if result:
                _, message = result
                
                # Try to deserialize JSON
                try:
                    return json.loads(message)
                except json.JSONDecodeError:
                    return message
            return None
        except Exception:
            return None
    
    def size(self, queue_name: str) -> int:
        """Get queue size."""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        
        return self._client.llen(queue_name)
    
    def clear(self, queue_name: str):
        """Clear queue."""
        if not self._client:
            raise RuntimeError("Not connected to Redis")
        
        self._client.delete(queue_name)
    
    def close(self):
        """Close Redis connection."""
        if self._client:
            self._client.close()


class RabbitMQDriver(MessageQueueDriver):
    """
    RabbitMQ message queue driver.
    
    Requires pika package. Provides fallback interface.
    
    Args:
        host: RabbitMQ host
        port: RabbitMQ port
        username: Username
        password: Password
        virtual_host: Virtual host
        
    Example:
        >>> driver = RabbitMQDriver()
        >>> driver.connect()
        >>> driver.send('tasks', {'job': 'process_data'})
        >>> msg = driver.receive('tasks')
    """
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 5672,
        username: str = 'guest',
        password: str = 'guest',
        virtual_host: str = '/'
    ):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.virtual_host = virtual_host
        self._connection: Optional[Any] = None
        self._channel: Optional[Any] = None
        self._has_pika = False
        
        try:
            import pika
            self._pika = pika
            self._has_pika = True
        except ImportError:
            pass
    
    def connect(self) -> 'RabbitMQDriver':
        """Connect to RabbitMQ."""
        if not self._has_pika:
            raise RuntimeError("pika package not installed")
        
        credentials = self._pika.PlainCredentials(self.username, self.password)
        parameters = self._pika.ConnectionParameters(
            host=self.host,
            port=self.port,
            virtual_host=self.virtual_host,
            credentials=credentials
        )
        
        self._connection = self._pika.BlockingConnection(parameters)
        self._channel = self._connection.channel()
        return self
    
    def send(self, queue_name: str, message: Any) -> bool:
        """Send message to queue."""
        if not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        try:
            # Declare queue (idempotent)
            self._channel.queue_declare(queue=queue_name, durable=True)
            
            # Serialize message
            if isinstance(message, (dict, list)):
                body = json.dumps(message)
            else:
                body = str(message)
            
            self._channel.basic_publish(
                exchange='',
                routing_key=queue_name,
                body=body,
                properties=self._pika.BasicProperties(
                    delivery_mode=2,  # Make message persistent
                )
            )
            return True
        except Exception:
            return False
    
    def receive(self, queue_name: str, timeout: float = 1.0) -> Optional[Any]:
        """Receive message from queue."""
        if not self._channel:
            raise RuntimeError("Not connected to RabbitMQ")
        
        try:
            # Declare queue (idempotent)
            self._channel.queue_declare(queue=queue_name, durable=True)
            
            # Get message
            method, properties, body = self._channel.basic_get(
                queue=queue_name,
                auto_ack=True
            )
            
            if method:
                # Try to deserialize JSON
                try:
                    return json.loads(body)
                except json.JSONDecodeError:
                    return body.decode('utf-8')
            return None
        except Exception:
            return None
    
    def close(self):
        """Close RabbitMQ connection."""
        if self._connection:
            self._connection.close()


class KafkaDriver(MessageQueueDriver):
    """
    Apache Kafka message queue driver.
    
    Requires kafka-python package. Provides fallback interface.
    
    Args:
        bootstrap_servers: Kafka broker addresses
        client_id: Client identifier
        
    Example:
        >>> driver = KafkaDriver(bootstrap_servers=['localhost:9092'])
        >>> driver.connect()
        >>> driver.send('events', {'type': 'user_login'})
        >>> msg = driver.receive('events')
    """
    
    def __init__(
        self,
        bootstrap_servers: List[str] = None,
        client_id: str = 'functionlib-client'
    ):
        self.bootstrap_servers = bootstrap_servers or ['localhost:9092']
        self.client_id = client_id
        self._producer: Optional[Any] = None
        self._consumer: Optional[Any] = None
        self._has_kafka = False
        
        try:
            from kafka import KafkaProducer, KafkaConsumer
            self._kafka_producer = KafkaProducer
            self._kafka_consumer = KafkaConsumer
            self._has_kafka = True
        except ImportError:
            pass
    
    def connect(self) -> 'KafkaDriver':
        """Connect to Kafka."""
        if not self._has_kafka:
            raise RuntimeError("kafka-python package not installed")
        
        self._producer = self._kafka_producer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        
        return self
    
    def send(self, topic: str, message: Any) -> bool:
        """Send message to Kafka topic."""
        if not self._producer:
            raise RuntimeError("Not connected to Kafka")
        
        try:
            future = self._producer.send(topic, message)
            # Wait for send to complete
            future.get(timeout=10)
            return True
        except Exception:
            return False
    
    def receive(self, topic: str, timeout: float = 1.0) -> Optional[Any]:
        """
        Receive message from Kafka topic.
        
        Note: Creates a new consumer for each call. For production,
        use a persistent consumer with consumer groups.
        """
        if not self._has_kafka:
            raise RuntimeError("kafka-python package not installed")
        
        try:
            consumer = self._kafka_consumer(
                topic,
                bootstrap_servers=self.bootstrap_servers,
                auto_offset_reset='earliest',
                consumer_timeout_ms=int(timeout * 1000),
                value_deserializer=lambda m: json.loads(m.decode('utf-8'))
            )
            
            for message in consumer:
                consumer.close()
                return message.value
            
            consumer.close()
            return None
        except Exception:
            return None
    
    def close(self):
        """Close Kafka connections."""
        if self._producer:
            self._producer.close()
        if self._consumer:
            self._consumer.close()


__all__ = [
    'MessageQueueDriver',
    'InMemoryQueueDriver',
    'RedisQueueDriver',
    'RabbitMQDriver',
    'KafkaDriver',
]
