"""
Database Drivers

Universal interfaces for SQL and NoSQL databases with connection pooling.
Provides consistent API across different database systems.
"""

import sqlite3
import json
from typing import Any, Dict, List, Optional, Union, Tuple
from abc import ABC, abstractmethod
from contextlib import contextmanager
from .connection_pool import ConnectionPool, connection_retry


class DatabaseDriver(ABC):
    """Abstract base class for database drivers."""
    
    @abstractmethod
    def connect(self) -> Any:
        """Establish connection to database."""
        pass
    
    @abstractmethod
    def execute(self, query: str, params: tuple = ()) -> Any:
        """Execute a query."""
        pass
    
    @abstractmethod
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch single row."""
        pass
    
    @abstractmethod
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows."""
        pass
    
    @abstractmethod
    def close(self):
        """Close connection."""
        pass


class SQLiteDriver(DatabaseDriver):
    """
    SQLite database driver with connection pooling.
    
    Pure Python stdlib implementation.
    
    Args:
        database: Path to SQLite database file
        pool_size: Maximum connections in pool
        
    Example:
        >>> driver = SQLiteDriver('app.db')
        >>> driver.connect()
        >>> rows = driver.fetch_all("SELECT * FROM users WHERE age > ?", (25,))
        >>> driver.close()
    """
    
    def __init__(self, database: str = ':memory:', pool_size: int = 5):
        self.database = database
        self.pool_size = pool_size
        self._pool: Optional[ConnectionPool] = None
        self._connection: Optional[sqlite3.Connection] = None
    
    def connect(self) -> 'SQLiteDriver':
        """Connect to SQLite database."""
        if self.pool_size > 1:
            # Use connection pool
            self._pool = ConnectionPool(
                factory=lambda: sqlite3.connect(
                    self.database,
                    check_same_thread=False,
                    timeout=30.0
                ),
                max_size=self.pool_size,
                min_size=1
            )
        else:
            # Single connection
            self._connection = sqlite3.connect(self.database, timeout=30.0)
            self._connection.row_factory = sqlite3.Row
        
        return self
    
    @contextmanager
    def _get_connection(self):
        """Get connection from pool or use single connection."""
        if self._pool:
            with self._pool.get_connection() as conn:
                conn.row_factory = sqlite3.Row
                yield conn
        elif self._connection:
            yield self._connection
        else:
            raise RuntimeError("Not connected to database")
    
    def execute(self, query: str, params: tuple = ()) -> int:
        """
        Execute a query and return number of affected rows.
        
        Args:
            query: SQL query
            params: Query parameters
            
        Returns:
            Number of affected rows
        """
        with self._get_connection() as conn:
            cursor = conn.execute(query, params)
            conn.commit()
            return cursor.rowcount
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch single row as dictionary."""
        with self._get_connection() as conn:
            cursor = conn.execute(query, params)
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows as list of dictionaries."""
        with self._get_connection() as conn:
            cursor = conn.execute(query, params)
            return [dict(row) for row in cursor.fetchall()]
    
    def execute_many(self, query: str, params_list: List[tuple]) -> int:
        """Execute query with multiple parameter sets."""
        with self._get_connection() as conn:
            cursor = conn.executemany(query, params_list)
            conn.commit()
            return cursor.rowcount
    
    def transaction(self, queries: List[Tuple[str, tuple]]) -> bool:
        """
        Execute multiple queries in a transaction.
        
        Args:
            queries: List of (query, params) tuples
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with self._get_connection() as conn:
                for query, params in queries:
                    conn.execute(query, params)
                conn.commit()
            return True
        except Exception:
            return False
    
    def close(self):
        """Close all connections."""
        if self._pool:
            self._pool.close_all()
        elif self._connection:
            self._connection.close()


class PostgreSQLDriver(DatabaseDriver):
    """
    PostgreSQL database driver.
    
    Requires psycopg2 package. Provides fallback interface if not available.
    
    Args:
        host: Database host
        port: Database port
        database: Database name
        user: Username
        password: Password
        pool_size: Connection pool size
        
    Example:
        >>> driver = PostgreSQLDriver(
        ...     host='localhost',
        ...     database='mydb',
        ...     user='user',
        ...     password='pass'
        ... )
        >>> driver.connect()
        >>> rows = driver.fetch_all("SELECT * FROM users")
    """
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 5432,
        database: str = '',
        user: str = '',
        password: str = '',
        pool_size: int = 5
    ):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.pool_size = pool_size
        self._pool: Optional[ConnectionPool] = None
        self._connection: Optional[Any] = None
        self._has_psycopg2 = False
        
        try:
            import psycopg2
            self._psycopg2 = psycopg2
            self._has_psycopg2 = True
        except ImportError:
            pass
    
    def connect(self) -> 'PostgreSQLDriver':
        """Connect to PostgreSQL database."""
        if not self._has_psycopg2:
            raise RuntimeError("psycopg2 package not installed")
        
        def create_connection():
            return self._psycopg2.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
        
        if self.pool_size > 1:
            self._pool = ConnectionPool(
                factory=create_connection,
                max_size=self.pool_size,
                min_size=1
            )
        else:
            self._connection = create_connection()
        
        return self
    
    @contextmanager
    def _get_connection(self):
        """Get connection from pool or use single connection."""
        if self._pool:
            with self._pool.get_connection() as conn:
                yield conn
        elif self._connection:
            yield self._connection
        else:
            raise RuntimeError("Not connected to database")
    
    def execute(self, query: str, params: tuple = ()) -> int:
        """Execute query and return affected rows."""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                return cursor.rowcount
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch single row as dictionary."""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                row = cursor.fetchone()
                if row:
                    columns = [desc[0] for desc in cursor.description]
                    return dict(zip(columns, row))
                return None
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows as list of dictionaries."""
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                columns = [desc[0] for desc in cursor.description]
                return [dict(zip(columns, row)) for row in cursor.fetchall()]
    
    def close(self):
        """Close all connections."""
        if self._pool:
            self._pool.close_all()
        elif self._connection:
            self._connection.close()


class MySQLDriver(DatabaseDriver):
    """
    MySQL database driver.
    
    Requires mysql-connector-python package. Provides fallback interface.
    
    Args:
        host: Database host
        port: Database port
        database: Database name
        user: Username
        password: Password
        pool_size: Connection pool size
        
    Example:
        >>> driver = MySQLDriver(
        ...     host='localhost',
        ...     database='mydb',
        ...     user='root',
        ...     password='pass'
        ... )
        >>> driver.connect()
        >>> rows = driver.fetch_all("SELECT * FROM users")
    """
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 3306,
        database: str = '',
        user: str = '',
        password: str = '',
        pool_size: int = 5
    ):
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        self.pool_size = pool_size
        self._pool: Optional[ConnectionPool] = None
        self._connection: Optional[Any] = None
        self._has_mysql = False
        
        try:
            import mysql.connector
            self._mysql = mysql.connector
            self._has_mysql = True
        except ImportError:
            pass
    
    def connect(self) -> 'MySQLDriver':
        """Connect to MySQL database."""
        if not self._has_mysql:
            raise RuntimeError("mysql-connector-python package not installed")
        
        def create_connection():
            return self._mysql.connect(
                host=self.host,
                port=self.port,
                database=self.database,
                user=self.user,
                password=self.password
            )
        
        if self.pool_size > 1:
            self._pool = ConnectionPool(
                factory=create_connection,
                max_size=self.pool_size,
                min_size=1
            )
        else:
            self._connection = create_connection()
        
        return self
    
    @contextmanager
    def _get_connection(self):
        """Get connection from pool or use single connection."""
        if self._pool:
            with self._pool.get_connection() as conn:
                yield conn
        elif self._connection:
            yield self._connection
        else:
            raise RuntimeError("Not connected to database")
    
    def execute(self, query: str, params: tuple = ()) -> int:
        """Execute query and return affected rows."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            rowcount = cursor.rowcount
            cursor.close()
            return rowcount
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Fetch single row as dictionary."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            row = cursor.fetchone()
            if row:
                columns = [desc[0] for desc in cursor.description]
                result = dict(zip(columns, row))
                cursor.close()
                return result
            cursor.close()
            return None
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Fetch all rows as list of dictionaries."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            columns = [desc[0] for desc in cursor.description]
            rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
            cursor.close()
            return rows
    
    def close(self):
        """Close all connections."""
        if self._pool:
            self._pool.close_all()
        elif self._connection:
            self._connection.close()


class MongoDBDriver(DatabaseDriver):
    """
    MongoDB database driver.
    
    Requires pymongo package. Provides fallback interface.
    
    Args:
        host: MongoDB host
        port: MongoDB port
        database: Database name
        username: Username (optional)
        password: Password (optional)
        
    Example:
        >>> driver = MongoDBDriver(database='mydb')
        >>> driver.connect()
        >>> docs = driver.find('users', {'age': {'$gt': 25}})
    """
    
    def __init__(
        self,
        host: str = 'localhost',
        port: int = 27017,
        database: str = 'test',
        username: str = '',
        password: str = ''
    ):
        self.host = host
        self.port = port
        self.database = database
        self.username = username
        self.password = password
        self._client: Optional[Any] = None
        self._db: Optional[Any] = None
        self._has_pymongo = False
        
        try:
            import pymongo
            self._pymongo = pymongo
            self._has_pymongo = True
        except ImportError:
            pass
    
    def connect(self) -> 'MongoDBDriver':
        """Connect to MongoDB."""
        if not self._has_pymongo:
            raise RuntimeError("pymongo package not installed")
        
        # Build connection string
        if self.username and self.password:
            uri = f"mongodb://{self.username}:{self.password}@{self.host}:{self.port}"
        else:
            uri = f"mongodb://{self.host}:{self.port}"
        
        self._client = self._pymongo.MongoClient(uri)
        self._db = self._client[self.database]
        return self
    
    def find(self, collection: str, query: Dict = None, limit: int = 0) -> List[Dict]:
        """
        Find documents in collection.
        
        Args:
            collection: Collection name
            query: MongoDB query
            limit: Maximum documents to return
            
        Returns:
            List of documents
        """
        if not self._db:
            raise RuntimeError("Not connected to database")
        
        cursor = self._db[collection].find(query or {})
        if limit > 0:
            cursor = cursor.limit(limit)
        
        return list(cursor)
    
    def find_one(self, collection: str, query: Dict) -> Optional[Dict]:
        """Find single document."""
        if not self._db:
            raise RuntimeError("Not connected to database")
        
        return self._db[collection].find_one(query)
    
    def insert_one(self, collection: str, document: Dict) -> str:
        """Insert single document and return ID."""
        if not self._db:
            raise RuntimeError("Not connected to database")
        
        result = self._db[collection].insert_one(document)
        return str(result.inserted_id)
    
    def insert_many(self, collection: str, documents: List[Dict]) -> List[str]:
        """Insert multiple documents and return IDs."""
        if not self._db:
            raise RuntimeError("Not connected to database")
        
        result = self._db[collection].insert_many(documents)
        return [str(id) for id in result.inserted_ids]
    
    def update_one(self, collection: str, query: Dict, update: Dict) -> int:
        """Update single document."""
        if not self._db:
            raise RuntimeError("Not connected to database")
        
        result = self._db[collection].update_one(query, update)
        return result.modified_count
    
    def delete_one(self, collection: str, query: Dict) -> int:
        """Delete single document."""
        if not self._db:
            raise RuntimeError("Not connected to database")
        
        result = self._db[collection].delete_one(query)
        return result.deleted_count
    
    # DatabaseDriver interface implementations
    def execute(self, query: str, params: tuple = ()) -> Any:
        """Not applicable for MongoDB."""
        raise NotImplementedError("Use MongoDB-specific methods")
    
    def fetch_one(self, query: str, params: tuple = ()) -> Optional[Dict]:
        """Not applicable for MongoDB."""
        raise NotImplementedError("Use find_one()")
    
    def fetch_all(self, query: str, params: tuple = ()) -> List[Dict]:
        """Not applicable for MongoDB."""
        raise NotImplementedError("Use find()")
    
    def close(self):
        """Close MongoDB connection."""
        if self._client:
            self._client.close()


__all__ = [
    'DatabaseDriver',
    'SQLiteDriver',
    'PostgreSQLDriver',
    'MySQLDriver',
    'MongoDBDriver',
]
