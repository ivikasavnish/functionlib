"""
Database Utilities

Database operations, SQL helpers, and database reflection using sqlite3 (stdlib).
"""

import sqlite3
from typing import List, Dict, Any, Optional, Tuple
import json

__all__ = [
    # Connection Management
    'create_connection', 'close_connection', 'execute_query', 'execute_many',
    
    # Table Operations
    'create_table', 'drop_table', 'table_exists', 'get_table_names',
    'get_table_info', 'get_table_schema', 'get_column_names', 'get_primary_keys',
    
    # Data Operations
    'insert_row', 'insert_many', 'select_all', 'select_where',
    'update_rows', 'delete_rows', 'count_rows',
    
    # Query Helpers
    'build_insert_query', 'build_select_query', 'build_update_query',
    'build_where_clause', 'escape_value',
    
    # Data Export/Import
    'export_to_dict', 'export_to_json', 'import_from_dict', 'import_from_json',
    
    # Database Reflection
    'get_database_info', 'get_indexes', 'get_foreign_keys',
    'analyze_table', 'get_row_count_all_tables'
]

# ============================================================================
# CONNECTION MANAGEMENT
# ============================================================================

def create_connection(database: str = ":memory:") -> sqlite3.Connection:
    """
    Create SQLite database connection.
    
    Args:
        database: Database file path or ":memory:" for in-memory database
        
    Returns:
        Database connection
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> conn is not None
        True
    """
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row  # Enable column access by name
    return conn


def close_connection(conn: sqlite3.Connection) -> None:
    """
    Close database connection.
    
    Args:
        conn: Database connection
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> close_connection(conn)
    """
    conn.close()


def execute_query(conn: sqlite3.Connection, query: str, params: tuple = ()) -> sqlite3.Cursor:
    """
    Execute a SQL query.
    
    Args:
        conn: Database connection
        query: SQL query string
        params: Query parameters
        
    Returns:
        Cursor object
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> cursor = execute_query(conn, "SELECT 1")
        >>> cursor is not None
        True
    """
    cursor = conn.cursor()
    cursor.execute(query, params)
    conn.commit()
    return cursor


def execute_many(conn: sqlite3.Connection, query: str, params_list: List[tuple]) -> None:
    """
    Execute query with multiple parameter sets.
    
    Args:
        conn: Database connection
        query: SQL query string
        params_list: List of parameter tuples
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> execute_query(conn, "CREATE TABLE test (id INTEGER, name TEXT)")
        <sqlite3.Cursor object at ...>
        >>> execute_many(conn, "INSERT INTO test VALUES (?, ?)", [(1, 'a'), (2, 'b')])
    """
    cursor = conn.cursor()
    cursor.executemany(query, params_list)
    conn.commit()


# ============================================================================
# TABLE OPERATIONS
# ============================================================================

def create_table(conn: sqlite3.Connection, table_name: str, 
                 columns: Dict[str, str]) -> None:
    """
    Create a table with specified columns.
    
    Args:
        conn: Database connection
        table_name: Name of table
        columns: Dictionary of column_name: type_definition
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "users", {"id": "INTEGER PRIMARY KEY", "name": "TEXT"})
        >>> table_exists(conn, "users")
        True
    """
    column_defs = ", ".join([f"{name} {dtype}" for name, dtype in columns.items()])
    query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_defs})"
    execute_query(conn, query)


def drop_table(conn: sqlite3.Connection, table_name: str) -> None:
    """
    Drop a table.
    
    Args:
        conn: Database connection
        table_name: Name of table to drop
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "temp", {"id": "INTEGER"})
        >>> drop_table(conn, "temp")
    """
    execute_query(conn, f"DROP TABLE IF EXISTS {table_name}")


def table_exists(conn: sqlite3.Connection, table_name: str) -> bool:
    """
    Check if table exists.
    
    Args:
        conn: Database connection
        table_name: Name of table
        
    Returns:
        True if table exists
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> table_exists(conn, "nonexistent")
        False
    """
    cursor = execute_query(conn, 
        "SELECT name FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,))
    return cursor.fetchone() is not None


def get_table_names(conn: sqlite3.Connection) -> List[str]:
    """
    Get all table names in database.
    
    Args:
        conn: Database connection
        
    Returns:
        List of table names
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test1", {"id": "INTEGER"})
        >>> create_table(conn, "test2", {"id": "INTEGER"})
        >>> tables = get_table_names(conn)
        >>> len(tables) >= 2
        True
    """
    cursor = execute_query(conn, 
        "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    return [row['name'] for row in cursor.fetchall()]


def get_table_info(conn: sqlite3.Connection, table_name: str) -> List[Dict[str, Any]]:
    """
    Get table column information.
    
    Args:
        conn: Database connection
        table_name: Name of table
        
    Returns:
        List of column info dictionaries
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> info = get_table_info(conn, "test")
        >>> len(info) == 2
        True
    """
    cursor = execute_query(conn, f"PRAGMA table_info({table_name})")
    return [dict(row) for row in cursor.fetchall()]


def get_table_schema(conn: sqlite3.Connection, table_name: str) -> str:
    """
    Get CREATE TABLE statement for a table.
    
    Args:
        conn: Database connection
        table_name: Name of table
        
    Returns:
        CREATE TABLE SQL statement
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER PRIMARY KEY"})
        >>> schema = get_table_schema(conn, "test")
        >>> "CREATE TABLE" in schema
        True
    """
    cursor = execute_query(conn,
        "SELECT sql FROM sqlite_master WHERE type='table' AND name=?",
        (table_name,))
    row = cursor.fetchone()
    return row['sql'] if row else ""


def get_column_names(conn: sqlite3.Connection, table_name: str) -> List[str]:
    """
    Get column names for a table.
    
    Args:
        conn: Database connection
        table_name: Name of table
        
    Returns:
        List of column names
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> cols = get_column_names(conn, "test")
        >>> 'name' in cols
        True
    """
    info = get_table_info(conn, table_name)
    return [col['name'] for col in info]


def get_primary_keys(conn: sqlite3.Connection, table_name: str) -> List[str]:
    """
    Get primary key columns for a table.
    
    Args:
        conn: Database connection
        table_name: Name of table
        
    Returns:
        List of primary key column names
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER PRIMARY KEY", "val": "TEXT"})
        >>> pks = get_primary_keys(conn, "test")
        >>> 'id' in pks
        True
    """
    info = get_table_info(conn, table_name)
    return [col['name'] for col in info if col['pk'] > 0]


# ============================================================================
# DATA OPERATIONS
# ============================================================================

def insert_row(conn: sqlite3.Connection, table_name: str, 
               data: Dict[str, Any]) -> int:
    """
    Insert a row into table.
    
    Args:
        conn: Database connection
        table_name: Name of table
        data: Dictionary of column: value
        
    Returns:
        Row ID of inserted row
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> rowid = insert_row(conn, "test", {"id": 1, "name": "John"})
        >>> rowid > 0
        True
    """
    columns = ", ".join(data.keys())
    placeholders = ", ".join(["?" for _ in data])
    query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
    cursor = execute_query(conn, query, tuple(data.values()))
    return cursor.lastrowid


def insert_many(conn: sqlite3.Connection, table_name: str, 
                data_list: List[Dict[str, Any]]) -> None:
    """
    Insert multiple rows into table.
    
    Args:
        conn: Database connection
        table_name: Name of table
        data_list: List of dictionaries (column: value)
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> insert_many(conn, "test", [{"id": 1, "name": "A"}, {"id": 2, "name": "B"}])
        >>> count_rows(conn, "test")
        2
    """
    if not data_list:
        return
    
    columns = list(data_list[0].keys())
    column_str = ", ".join(columns)
    placeholders = ", ".join(["?" for _ in columns])
    query = f"INSERT INTO {table_name} ({column_str}) VALUES ({placeholders})"
    
    params_list = [tuple(row[col] for col in columns) for row in data_list]
    execute_many(conn, query, params_list)


def select_all(conn: sqlite3.Connection, table_name: str, 
               limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Select all rows from table.
    
    Args:
        conn: Database connection
        table_name: Name of table
        limit: Optional limit on number of rows
        
    Returns:
        List of row dictionaries
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> insert_row(conn, "test", {"id": 1, "name": "John"})
        1
        >>> rows = select_all(conn, "test")
        >>> len(rows)
        1
    """
    query = f"SELECT * FROM {table_name}"
    if limit:
        query += f" LIMIT {limit}"
    cursor = execute_query(conn, query)
    return [dict(row) for row in cursor.fetchall()]


def select_where(conn: sqlite3.Connection, table_name: str,
                 conditions: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Select rows matching conditions.
    
    Args:
        conn: Database connection
        table_name: Name of table
        conditions: Dictionary of column: value conditions
        
    Returns:
        List of matching row dictionaries
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> insert_row(conn, "test", {"id": 1, "name": "John"})
        1
        >>> rows = select_where(conn, "test", {"name": "John"})
        >>> len(rows)
        1
    """
    where_clause, params = build_where_clause(conditions)
    query = f"SELECT * FROM {table_name} WHERE {where_clause}"
    cursor = execute_query(conn, query, params)
    return [dict(row) for row in cursor.fetchall()]


def update_rows(conn: sqlite3.Connection, table_name: str,
                data: Dict[str, Any], conditions: Dict[str, Any]) -> int:
    """
    Update rows matching conditions.
    
    Args:
        conn: Database connection
        table_name: Name of table
        data: Dictionary of column: new_value
        conditions: Dictionary of column: value conditions
        
    Returns:
        Number of rows updated
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> insert_row(conn, "test", {"id": 1, "name": "John"})
        1
        >>> update_rows(conn, "test", {"name": "Jane"}, {"id": 1})
        1
    """
    set_clause = ", ".join([f"{col}=?" for col in data.keys()])
    where_clause, where_params = build_where_clause(conditions)
    query = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"
    params = tuple(data.values()) + where_params
    cursor = execute_query(conn, query, params)
    return cursor.rowcount


def delete_rows(conn: sqlite3.Connection, table_name: str,
                conditions: Dict[str, Any]) -> int:
    """
    Delete rows matching conditions.
    
    Args:
        conn: Database connection
        table_name: Name of table
        conditions: Dictionary of column: value conditions
        
    Returns:
        Number of rows deleted
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER"})
        >>> insert_row(conn, "test", {"id": 1})
        1
        >>> delete_rows(conn, "test", {"id": 1})
        1
    """
    where_clause, params = build_where_clause(conditions)
    query = f"DELETE FROM {table_name} WHERE {where_clause}"
    cursor = execute_query(conn, query, params)
    return cursor.rowcount


def count_rows(conn: sqlite3.Connection, table_name: str,
               conditions: Optional[Dict[str, Any]] = None) -> int:
    """
    Count rows in table.
    
    Args:
        conn: Database connection
        table_name: Name of table
        conditions: Optional conditions dictionary
        
    Returns:
        Number of rows
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER"})
        >>> insert_row(conn, "test", {"id": 1})
        1
        >>> count_rows(conn, "test")
        1
    """
    query = f"SELECT COUNT(*) as count FROM {table_name}"
    if conditions:
        where_clause, params = build_where_clause(conditions)
        query += f" WHERE {where_clause}"
        cursor = execute_query(conn, query, params)
    else:
        cursor = execute_query(conn, query)
    return cursor.fetchone()['count']


# ============================================================================
# QUERY HELPERS
# ============================================================================

def build_insert_query(table_name: str, columns: List[str]) -> str:
    """
    Build INSERT query template.
    
    Args:
        table_name: Name of table
        columns: List of column names
        
    Returns:
        INSERT query string
        
    Example:
        >>> build_insert_query("users", ["id", "name"])
        'INSERT INTO users (id, name) VALUES (?, ?)'
    """
    column_str = ", ".join(columns)
    placeholders = ", ".join(["?" for _ in columns])
    return f"INSERT INTO {table_name} ({column_str}) VALUES ({placeholders})"


def build_select_query(table_name: str, columns: Optional[List[str]] = None,
                       where: Optional[str] = None) -> str:
    """
    Build SELECT query.
    
    Args:
        table_name: Name of table
        columns: List of columns to select (None = all)
        where: Optional WHERE clause
        
    Returns:
        SELECT query string
        
    Example:
        >>> build_select_query("users", ["name", "email"], "id > 10")
        'SELECT name, email FROM users WHERE id > 10'
    """
    column_str = ", ".join(columns) if columns else "*"
    query = f"SELECT {column_str} FROM {table_name}"
    if where:
        query += f" WHERE {where}"
    return query


def build_update_query(table_name: str, columns: List[str], where: str) -> str:
    """
    Build UPDATE query template.
    
    Args:
        table_name: Name of table
        columns: List of columns to update
        where: WHERE clause
        
    Returns:
        UPDATE query string
        
    Example:
        >>> build_update_query("users", ["name", "email"], "id=?")
        'UPDATE users SET name=?, email=? WHERE id=?'
    """
    set_clause = ", ".join([f"{col}=?" for col in columns])
    return f"UPDATE {table_name} SET {set_clause} WHERE {where}"


def build_where_clause(conditions: Dict[str, Any]) -> Tuple[str, tuple]:
    """
    Build WHERE clause from conditions dictionary.
    
    Args:
        conditions: Dictionary of column: value
        
    Returns:
        Tuple of (where_clause, params)
        
    Example:
        >>> clause, params = build_where_clause({"id": 1, "active": True})
        >>> "id=?" in clause
        True
    """
    clauses = [f"{col}=?" for col in conditions.keys()]
    where_clause = " AND ".join(clauses)
    params = tuple(conditions.values())
    return where_clause, params


def escape_value(value: Any) -> str:
    """
    Escape value for SQL (basic escaping).
    
    Args:
        value: Value to escape
        
    Returns:
        Escaped string
        
    Example:
        >>> escape_value("O'Brien")
        "O''Brien"
    """
    if isinstance(value, str):
        return value.replace("'", "''")
    return str(value)


# ============================================================================
# DATA EXPORT/IMPORT
# ============================================================================

def export_to_dict(conn: sqlite3.Connection, table_name: str) -> List[Dict[str, Any]]:
    """
    Export table data to list of dictionaries.
    
    Args:
        conn: Database connection
        table_name: Name of table
        
    Returns:
        List of row dictionaries
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> insert_row(conn, "test", {"id": 1, "name": "John"})
        1
        >>> data = export_to_dict(conn, "test")
        >>> len(data)
        1
    """
    return select_all(conn, table_name)


def export_to_json(conn: sqlite3.Connection, table_name: str) -> str:
    """
    Export table data to JSON string.
    
    Args:
        conn: Database connection
        table_name: Name of table
        
    Returns:
        JSON string
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> insert_row(conn, "test", {"id": 1, "name": "John"})
        1
        >>> json_str = export_to_json(conn, "test")
        >>> "John" in json_str
        True
    """
    data = export_to_dict(conn, table_name)
    return json.dumps(data, indent=2)


def import_from_dict(conn: sqlite3.Connection, table_name: str,
                     data: List[Dict[str, Any]]) -> None:
    """
    Import data from list of dictionaries.
    
    Args:
        conn: Database connection
        table_name: Name of table
        data: List of row dictionaries
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> import_from_dict(conn, "test", [{"id": 1, "name": "John"}])
        >>> count_rows(conn, "test")
        1
    """
    insert_many(conn, table_name, data)


def import_from_json(conn: sqlite3.Connection, table_name: str,
                     json_str: str) -> None:
    """
    Import data from JSON string.
    
    Args:
        conn: Database connection
        table_name: Name of table
        json_str: JSON string
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> import_from_json(conn, "test", '[{"id": 1, "name": "John"}]')
        >>> count_rows(conn, "test")
        1
    """
    data = json.loads(json_str)
    import_from_dict(conn, table_name, data)


# ============================================================================
# DATABASE REFLECTION
# ============================================================================

def get_database_info(conn: sqlite3.Connection) -> Dict[str, Any]:
    """
    Get comprehensive database information.
    
    Args:
        conn: Database connection
        
    Returns:
        Dictionary with database info
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER"})
        >>> info = get_database_info(conn)
        >>> 'tables' in info
        True
    """
    tables = get_table_names(conn)
    info = {
        'tables': tables,
        'table_count': len(tables),
        'table_details': {}
    }
    
    for table in tables:
        info['table_details'][table] = {
            'columns': get_column_names(conn, table),
            'primary_keys': get_primary_keys(conn, table),
            'row_count': count_rows(conn, table)
        }
    
    return info


def get_indexes(conn: sqlite3.Connection, table_name: str) -> List[Dict[str, Any]]:
    """
    Get indexes for a table.
    
    Args:
        conn: Database connection
        table_name: Name of table
        
    Returns:
        List of index information dictionaries
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER PRIMARY KEY"})
        >>> indexes = get_indexes(conn, "test")
        >>> isinstance(indexes, list)
        True
    """
    cursor = execute_query(conn, f"PRAGMA index_list({table_name})")
    return [dict(row) for row in cursor.fetchall()]


def get_foreign_keys(conn: sqlite3.Connection, table_name: str) -> List[Dict[str, Any]]:
    """
    Get foreign keys for a table.
    
    Args:
        conn: Database connection
        table_name: Name of table
        
    Returns:
        List of foreign key information dictionaries
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER"})
        >>> fks = get_foreign_keys(conn, "test")
        >>> isinstance(fks, list)
        True
    """
    cursor = execute_query(conn, f"PRAGMA foreign_key_list({table_name})")
    return [dict(row) for row in cursor.fetchall()]


def analyze_table(conn: sqlite3.Connection, table_name: str) -> Dict[str, Any]:
    """
    Analyze table and return statistics.
    
    Args:
        conn: Database connection
        table_name: Name of table
        
    Returns:
        Dictionary with table analysis
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test", {"id": "INTEGER", "name": "TEXT"})
        >>> insert_row(conn, "test", {"id": 1, "name": "John"})
        1
        >>> analysis = analyze_table(conn, "test")
        >>> analysis['row_count']
        1
    """
    return {
        'table_name': table_name,
        'row_count': count_rows(conn, table_name),
        'columns': get_column_names(conn, table_name),
        'primary_keys': get_primary_keys(conn, table_name),
        'schema': get_table_schema(conn, table_name),
        'indexes': get_indexes(conn, table_name),
        'foreign_keys': get_foreign_keys(conn, table_name)
    }


def get_row_count_all_tables(conn: sqlite3.Connection) -> Dict[str, int]:
    """
    Get row count for all tables.
    
    Args:
        conn: Database connection
        
    Returns:
        Dictionary of table_name: row_count
        
    Example:
        >>> conn = create_connection(":memory:")
        >>> create_table(conn, "test1", {"id": "INTEGER"})
        >>> create_table(conn, "test2", {"id": "INTEGER"})
        >>> counts = get_row_count_all_tables(conn)
        >>> isinstance(counts, dict)
        True
    """
    tables = get_table_names(conn)
    return {table: count_rows(conn, table) for table in tables}
