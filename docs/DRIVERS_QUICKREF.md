# Drivers Package Quick Reference

**17 Database & Message Queue Drivers** | Connection Pooling | Retry Logic

## 🎯 Overview

Universal driver interfaces for databases, message queues, and caches with:
- **Consistent API** across all systems
- **Connection pooling** with health checks
- **Automatic retry** with exponential backoff
- **Pure Python** implementations where possible
- **Thread-safe** operations

---

## 🗄️ Database Drivers

### SQLite (Pure Python - stdlib)

```python
from functionlib.coding.drivers import SQLiteDriver

# Connect
driver = SQLiteDriver('app.db', pool_size=5).connect()

# Execute
driver.execute("CREATE TABLE users (id INT, name TEXT)")
driver.execute("INSERT INTO users VALUES (?, ?)", (1, 'John'))

# Query
users = driver.fetch_all("SELECT * FROM users")
user = driver.fetch_one("SELECT * FROM users WHERE id = ?", (1,))

# Cleanup
driver.close()
```

### PostgreSQL (requires psycopg2)

```python
from functionlib.coding.drivers import PostgreSQLDriver

driver = PostgreSQLDriver(
    host='localhost',
    database='mydb',
    user='postgres',
    password='secret'
).connect()

users = driver.fetch_all("SELECT * FROM users")
driver.close()
```

### MySQL (requires mysql-connector-python)

```python
from functionlib.coding.drivers import MySQLDriver

driver = MySQLDriver(
    host='localhost',
    database='mydb',
    user='root',
    password='secret'
).connect()

users = driver.fetch_all("SELECT * FROM users")
driver.close()
```

### MongoDB (requires pymongo)

```python
from functionlib.coding.drivers import MongoDBDriver

driver = MongoDBDriver(database='mydb').connect()

# Find documents
docs = driver.find('users', {'age': {'$gt': 25}})

# Insert
doc_id = driver.insert_one('users', {'name': 'John', 'age': 30})

# Update
driver.update_one('users', {'name': 'John'}, {'$set': {'age': 31}})

# Delete
driver.delete_one('users', {'name': 'John'})

driver.close()
```

---

## 📨 Message Queue Drivers

### In-Memory Queue (Pure Python - stdlib)

```python
from functionlib.coding.drivers import InMemoryQueueDriver

queue = InMemoryQueueDriver().connect()

# Send message
queue.send('tasks', {'job': 'process_data', 'id': 1})

# Receive message
msg = queue.receive('tasks', timeout=1.0)

# Check size
size = queue.size('tasks')

queue.close()
```

### Redis Queue (requires redis)

```python
from functionlib.coding.drivers import RedisQueueDriver

queue = RedisQueueDriver(host='localhost').connect()

# Send to queue
queue.send('tasks', {'job': 'send_email'})

# Blocking receive
msg = queue.receive('tasks', timeout=5.0)

queue.close()
```

### RabbitMQ (requires pika)

```python
from functionlib.coding.drivers import RabbitMQDriver

queue = RabbitMQDriver(
    host='localhost',
    username='guest',
    password='guest'
).connect()

# Send message
queue.send('tasks', {'job': 'process'})

# Receive message
msg = queue.receive('tasks')

queue.close()
```

### Apache Kafka (requires kafka-python)

```python
from functionlib.coding.drivers import KafkaDriver

kafka = KafkaDriver(
    bootstrap_servers=['localhost:9092']
).connect()

# Send to topic
kafka.send('events', {'type': 'user_login', 'user_id': 123})

# Receive from topic
msg = kafka.receive('events', timeout=1.0)

kafka.close()
```

---

## 🗄️ Cache Drivers

### In-Memory Cache (Pure Python - LRU with TTL)

```python
from functionlib.coding.drivers import InMemoryCacheDriver

cache = InMemoryCacheDriver(
    max_size=1000,
    default_ttl=300  # 5 minutes
).connect()

# Set with TTL
cache.set('user:1', {'name': 'John'}, ttl=60)

# Get
user = cache.get('user:1')

# Check existence
if cache.exists('user:1'):
    print("Found in cache")

# Delete
cache.delete('user:1')

# Clear all
cache.clear()

# Stats
stats = cache.get_stats()

cache.close()
```

### Redis Cache (requires redis)

```python
from functionlib.coding.drivers import RedisCacheDriver

cache = RedisCacheDriver(
    host='localhost',
    prefix='app:'  # Namespace keys
).connect()

# Set with TTL
cache.set('user:1', {'name': 'John'}, ttl=300)

# Get
user = cache.get('user:1')

# Increment counter
cache.increment('page_views', amount=1)

cache.close()
```

### Memcached (requires pymemcache)

```python
from functionlib.coding.drivers import MemcachedDriver

cache = MemcachedDriver(
    servers=[('localhost', 11211)]
).connect()

cache.set('key', 'value', ttl=300)
value = cache.get('key')

cache.close()
```

---

## 🔄 Connection Pooling

Generic connection pool for any resource:

```python
from functionlib.coding.drivers import ConnectionPool
import sqlite3

# Create pool
pool = ConnectionPool(
    factory=lambda: sqlite3.connect('db.sqlite'),
    max_size=10,
    min_size=2,
    max_idle=300.0,  # 5 minutes
    health_check=lambda conn: conn.execute("SELECT 1")
)

# Use connection
with pool.get_connection() as conn:
    cursor = conn.execute("SELECT * FROM users")
    users = cursor.fetchall()

# Get stats
stats = pool.get_stats()
# {'size': 10, 'available': 9, 'in_use': 1, 'max_size': 10}

# Cleanup
pool.close_all()
```

---

## 🔁 Retry Logic

Automatic retry with exponential backoff:

```python
from functionlib.coding.drivers import connection_retry
import sqlite3

def connect_to_db():
    return sqlite3.connect('db.sqlite')

# Retry up to 3 times with exponential backoff
conn = connection_retry(
    func=connect_to_db,
    max_retries=3,
    retry_delay=1.0,
    backoff_multiplier=2.0,
    exceptions=(sqlite3.OperationalError,)
)
```

---

## 📋 Real-World Examples

### 1. Web Application Cache

```python
from functionlib.coding.drivers import RedisCacheDriver

cache = RedisCacheDriver(prefix='webapp:').connect()

def get_user(user_id):
    # Try cache first
    cached = cache.get(f'user:{user_id}')
    if cached:
        return cached
    
    # Load from database
    user = database.fetch_one("SELECT * FROM users WHERE id = ?", (user_id,))
    
    # Cache for 5 minutes
    cache.set(f'user:{user_id}', user, ttl=300)
    return user
```

### 2. Task Queue Worker

```python
from functionlib.coding.drivers import RedisQueueDriver

queue = RedisQueueDriver().connect()

def process_tasks():
    while True:
        task = queue.receive('tasks', timeout=5.0)
        if task:
            print(f"Processing task: {task}")
            # Process task...
            
            # Send to completed queue
            queue.send('completed', {'task_id': task['id']})
```

### 3. Multi-Database Application

```python
from functionlib.coding.drivers import (
    SQLiteDriver,
    PostgreSQLDriver,
    MongoDBDriver
)

# Local cache database
cache_db = SQLiteDriver(':memory:').connect()

# Production database
prod_db = PostgreSQLDriver(
    host='db.prod.com',
    database='app'
).connect()

# Document store
docs = MongoDBDriver(database='documents').connect()

# Query all
users = prod_db.fetch_all("SELECT * FROM users")
logs = docs.find('logs', {'level': 'ERROR'})
```

### 4. Session Store with TTL

```python
from functionlib.coding.drivers import InMemoryCacheDriver
import uuid

cache = InMemoryCacheDriver().connect()

def create_session(user_id):
    session_id = str(uuid.uuid4())
    cache.set(
        f'session:{session_id}',
        {'user_id': user_id, 'created': time.time()},
        ttl=3600  # 1 hour
    )
    return session_id

def get_session(session_id):
    return cache.get(f'session:{session_id}')
```

### 5. Event Streaming

```python
from functionlib.coding.drivers import KafkaDriver

kafka = KafkaDriver().connect()

# Producer
def log_event(event_type, data):
    kafka.send('events', {
        'type': event_type,
        'data': data,
        'timestamp': time.time()
    })

# Consumer
def process_events():
    while True:
        event = kafka.receive('events', timeout=1.0)
        if event:
            handle_event(event)
```

---

## 🎯 Driver Comparison

| Feature | Database | Message Queue | Cache |
|---------|----------|---------------|-------|
| **Purpose** | Persistent storage | Async messaging | Fast access |
| **Durability** | High | Medium-High | Low |
| **Speed** | Medium | High | Very High |
| **TTL Support** | No | No | Yes |
| **Transactions** | Yes | No | No |
| **Pooling** | Yes | Optional | Optional |

---

## 🔑 Key Features

- ✅ **Consistent Interface**: Same API across all drivers
- ✅ **Connection Pooling**: Automatic pooling with health checks
- ✅ **Retry Logic**: Exponential backoff for transient failures
- ✅ **Thread-Safe**: All drivers are thread-safe
- ✅ **Context Managers**: Automatic cleanup
- ✅ **Pure Python**: In-memory implementations use stdlib only
- ✅ **Optional Deps**: External packages only when needed
- ✅ **LRU Eviction**: Memory caches use LRU eviction
- ✅ **TTL Support**: Automatic expiration for caches

---

## 📦 Dependencies

**Pure Python (stdlib only):**
- SQLiteDriver
- InMemoryQueueDriver
- InMemoryCacheDriver
- ConnectionPool
- connection_retry

**Optional (requires external packages):**
- PostgreSQLDriver → `psycopg2`
- MySQLDriver → `mysql-connector-python`
- MongoDBDriver → `pymongo`
- RedisQueueDriver → `redis`
- RedisCacheDriver → `redis`
- RabbitMQDriver → `pika`
- KafkaDriver → `kafka-python`
- MemcachedDriver → `pymemcache`

---

**Total Drivers:** 17 (5 database + 5 queue + 4 cache + 3 utilities)  
**Pure Python Implementations:** 3 (SQLite, InMemory Queue, InMemory Cache)  
**Connection Pooling:** Built-in for all drivers  
**Thread-Safe:** Yes, all drivers
