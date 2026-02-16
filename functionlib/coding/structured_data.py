"""
Structured Data Manipulation (JSON/YAML)

Path-based editing, querying, and transformation of JSON and YAML files.
Supports JSONPath-like syntax, predicates, and expression evaluation.

All functions use pure Python stdlib (json, re) with optional yaml support.
"""

import json
import re
from typing import Any, Dict, List, Optional, Union, Callable
from pathlib import Path


# ============================================================================
# Path Parsing and Navigation
# ============================================================================

def parse_path(path: str) -> List[Union[str, int]]:
    """
    Parse a path string into components.
    
    Supports:
    - Dot notation: "user.name"
    - Bracket notation: "users[0].name"
    - Mixed: "data.users[0].profile.email"
    
    Args:
        path: Path string to parse
        
    Returns:
        List of path components (strings and integers)
        
    Example:
        >>> parse_path("data.users[0].name")
        ['data', 'users', 0, 'name']
    """
    if not path:
        return []
    
    components = []
    # Split by dots, but preserve bracket notation
    parts = path.split('.')
    
    for part in parts:
        # Handle bracket notation: "users[0]" -> "users", 0
        while '[' in part:
            bracket_pos = part.index('[')
            if bracket_pos > 0:
                components.append(part[:bracket_pos])
            
            # Extract index
            end_bracket = part.index(']')
            index_str = part[bracket_pos+1:end_bracket]
            
            # Try to convert to int, otherwise keep as string (for dict keys)
            try:
                components.append(int(index_str))
            except ValueError:
                # Remove quotes if present
                index_str = index_str.strip('\'"')
                components.append(index_str)
            
            part = part[end_bracket+1:]
        
        if part:
            components.append(part)
    
    return components


def get_value_by_path(data: Any, path: str, default: Any = None) -> Any:
    """
    Get value from nested structure using path syntax.
    
    Args:
        data: Dictionary, list, or nested structure
        path: Path string (e.g., "user.profile.email")
        default: Default value if path not found
        
    Returns:
        Value at path, or default if not found
        
    Example:
        >>> data = {'user': {'name': 'John', 'age': 30}}
        >>> get_value_by_path(data, 'user.name')
        'John'
    """
    if not path:
        return data
    
    components = parse_path(path)
    current = data
    
    try:
        for component in components:
            if isinstance(current, dict):
                current = current[component]
            elif isinstance(current, list):
                current = current[int(component)]
            else:
                return default
        return current
    except (KeyError, IndexError, TypeError, ValueError):
        return default


def set_value_by_path(data: Any, path: str, value: Any, create_missing: bool = True) -> bool:
    """
    Set value in nested structure using path syntax.
    
    Args:
        data: Dictionary or list to modify (modified in-place)
        path: Path string
        value: Value to set
        create_missing: Create intermediate structures if missing
        
    Returns:
        True if successful, False otherwise
        
    Example:
        >>> data = {'user': {}}
        >>> set_value_by_path(data, 'user.name', 'John')
        True
        >>> data
        {'user': {'name': 'John'}}
    """
    if not path:
        return False
    
    components = parse_path(path)
    if not components:
        return False
    
    current = data
    
    # Navigate to parent
    for component in components[:-1]:
        if isinstance(current, dict):
            if component not in current:
                if not create_missing:
                    return False
                # Guess next type based on next component
                next_idx = components.index(component) + 1
                if next_idx < len(components) and isinstance(components[next_idx], int):
                    current[component] = []
                else:
                    current[component] = {}
            current = current[component]
        elif isinstance(current, list):
            idx = int(component)
            # Extend list if needed
            while len(current) <= idx:
                if not create_missing:
                    return False
                current.append(None)
            if current[idx] is None:
                # Guess type for next level
                next_idx = components.index(component) + 1
                if next_idx < len(components) and isinstance(components[next_idx], int):
                    current[idx] = []
                else:
                    current[idx] = {}
            current = current[idx]
        else:
            return False
    
    # Set final value
    final_key = components[-1]
    try:
        if isinstance(current, dict):
            current[final_key] = value
        elif isinstance(current, list):
            idx = int(final_key)
            while len(current) <= idx:
                if not create_missing:
                    return False
                current.append(None)
            current[idx] = value
        else:
            return False
        return True
    except (TypeError, ValueError):
        return False


def delete_by_path(data: Any, path: str) -> bool:
    """
    Delete value at path in nested structure.
    
    Args:
        data: Dictionary or list to modify
        path: Path to delete
        
    Returns:
        True if deleted, False if path not found
        
    Example:
        >>> data = {'user': {'name': 'John', 'age': 30}}
        >>> delete_by_path(data, 'user.age')
        True
    """
    if not path:
        return False
    
    components = parse_path(path)
    if not components:
        return False
    
    current = data
    
    # Navigate to parent
    try:
        for component in components[:-1]:
            if isinstance(current, dict):
                current = current[component]
            elif isinstance(current, list):
                current = current[int(component)]
            else:
                return False
        
        # Delete final key
        final_key = components[-1]
        if isinstance(current, dict) and final_key in current:
            del current[final_key]
            return True
        elif isinstance(current, list):
            idx = int(final_key)
            if 0 <= idx < len(current):
                current.pop(idx)
                return True
        return False
    except (KeyError, IndexError, TypeError, ValueError):
        return False


# ============================================================================
# JSON File Operations
# ============================================================================

def json_get(filepath: str, path: str = '', default: Any = None) -> Any:
    """
    Get value from JSON file using path syntax.
    
    Args:
        filepath: Path to JSON file
        path: Path to value (empty for entire file)
        default: Default if path not found
        
    Returns:
        Value at path
        
    Example:
        >>> json_get('config.json', 'database.host')
        'localhost'
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        return get_value_by_path(data, path, default) if path else data
    except (FileNotFoundError, json.JSONDecodeError):
        return default


def json_set(filepath: str, path: str, value: Any, create_missing: bool = True, 
             indent: int = 2) -> bool:
    """
    Set value in JSON file using path syntax.
    
    Args:
        filepath: Path to JSON file
        path: Path to set
        value: Value to set
        create_missing: Create intermediate structures
        indent: JSON indentation
        
    Returns:
        True if successful
        
    Example:
        >>> json_set('config.json', 'database.port', 5432)
        True
    """
    try:
        # Load existing or create new
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        
        # Set value
        if not set_value_by_path(data, path, value, create_missing):
            return False
        
        # Write back
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=indent)
        return True
    except Exception:
        return False


def json_delete(filepath: str, path: str, indent: int = 2) -> bool:
    """
    Delete value from JSON file using path syntax.
    
    Args:
        filepath: Path to JSON file
        path: Path to delete
        indent: JSON indentation
        
    Returns:
        True if deleted
        
    Example:
        >>> json_delete('config.json', 'database.debug')
        True
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        if not delete_by_path(data, path):
            return False
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=indent)
        return True
    except (FileNotFoundError, json.JSONDecodeError):
        return False


def json_merge(filepath: str, updates: Dict, indent: int = 2) -> bool:
    """
    Merge dictionary into JSON file (deep merge).
    
    Args:
        filepath: Path to JSON file
        updates: Dictionary to merge
        indent: JSON indentation
        
    Returns:
        True if successful
        
    Example:
        >>> json_merge('config.json', {'database': {'pool': 10}})
        True
    """
    def deep_merge(base: Dict, update: Dict) -> Dict:
        """Deep merge two dictionaries."""
        result = base.copy()
        for key, value in update.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    try:
        # Load existing or create new
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            data = {}
        
        # Merge
        data = deep_merge(data, updates)
        
        # Write back
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=indent)
        return True
    except Exception:
        return False


# ============================================================================
# YAML Operations (optional, falls back to JSON-like dict operations)
# ============================================================================

def yaml_get(filepath: str, path: str = '', default: Any = None) -> Any:
    """
    Get value from YAML file using path syntax.
    
    Falls back to JSON if PyYAML not available.
    
    Args:
        filepath: Path to YAML file
        path: Path to value
        default: Default if not found
        
    Returns:
        Value at path
        
    Example:
        >>> yaml_get('config.yaml', 'database.host')
        'localhost'
    """
    try:
        try:
            import yaml
            with open(filepath, 'r') as f:
                data = yaml.safe_load(f)
        except ImportError:
            # Fallback: try as JSON
            with open(filepath, 'r') as f:
                data = json.load(f)
        
        return get_value_by_path(data, path, default) if path else data
    except (FileNotFoundError, Exception):
        return default


def yaml_set(filepath: str, path: str, value: Any, create_missing: bool = True) -> bool:
    """
    Set value in YAML file using path syntax.
    
    Falls back to JSON if PyYAML not available.
    
    Args:
        filepath: Path to YAML file
        path: Path to set
        value: Value to set
        create_missing: Create intermediate structures
        
    Returns:
        True if successful
        
    Example:
        >>> yaml_set('config.yaml', 'database.port', 5432)
        True
    """
    try:
        try:
            import yaml
            has_yaml = True
        except ImportError:
            has_yaml = False
        
        # Load existing or create new
        try:
            with open(filepath, 'r') as f:
                if has_yaml:
                    data = yaml.safe_load(f)
                else:
                    data = json.load(f)
        except (FileNotFoundError, Exception):
            data = {}
        
        # Set value
        if not set_value_by_path(data, path, value, create_missing):
            return False
        
        # Write back
        with open(filepath, 'w') as f:
            if has_yaml:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            else:
                json.dump(data, f, indent=2)
        return True
    except Exception:
        return False


# ============================================================================
# Query and Filter Operations
# ============================================================================

def json_query(data: Any, predicate: Callable[[Any], bool]) -> List[Any]:
    """
    Query JSON structure with predicate function.
    
    Args:
        data: JSON data (dict, list, or nested)
        predicate: Function that returns True for matches
        
    Returns:
        List of matching values
        
    Example:
        >>> data = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}]
        >>> json_query(data, lambda x: isinstance(x, dict) and x.get('age', 0) > 26)
        [{'name': 'John', 'age': 30}]
    """
    results = []
    
    def recurse(obj):
        if predicate(obj):
            results.append(obj)
        
        if isinstance(obj, dict):
            for value in obj.values():
                recurse(value)
        elif isinstance(obj, list):
            for item in obj:
                recurse(item)
    
    recurse(data)
    return results


def json_filter(data: List[Dict], key: str, value: Any) -> List[Dict]:
    """
    Filter list of dictionaries by key-value match.
    
    Args:
        data: List of dictionaries
        key: Key to check (supports path syntax)
        value: Value to match
        
    Returns:
        Filtered list
        
    Example:
        >>> users = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}]
        >>> json_filter(users, 'age', 30)
        [{'name': 'John', 'age': 30}]
    """
    return [item for item in data if get_value_by_path(item, key) == value]


def json_find(data: List[Dict], key: str, value: Any) -> Optional[Dict]:
    """
    Find first dictionary matching key-value.
    
    Args:
        data: List of dictionaries
        key: Key to check (supports path syntax)
        value: Value to match
        
    Returns:
        First match or None
        
    Example:
        >>> users = [{'name': 'John'}, {'name': 'Jane'}]
        >>> json_find(users, 'name', 'Jane')
        {'name': 'Jane'}
    """
    for item in data:
        if get_value_by_path(item, key) == value:
            return item
    return None


def json_select(data: List[Dict], keys: List[str]) -> List[Dict]:
    """
    Select specific keys from list of dictionaries (like SQL SELECT).
    
    Args:
        data: List of dictionaries
        keys: Keys to select (supports path syntax)
        
    Returns:
        List with only selected keys
        
    Example:
        >>> users = [{'name': 'John', 'age': 30, 'city': 'NYC'}]
        >>> json_select(users, ['name', 'age'])
        [{'name': 'John', 'age': 30}]
    """
    result = []
    for item in data:
        selected = {}
        for key in keys:
            value = get_value_by_path(item, key)
            if value is not None:
                selected[key] = value
        if selected:
            result.append(selected)
    return result


def json_sort(data: List[Dict], key: str, reverse: bool = False) -> List[Dict]:
    """
    Sort list of dictionaries by key.
    
    Args:
        data: List of dictionaries
        key: Key to sort by (supports path syntax)
        reverse: Sort in descending order
        
    Returns:
        Sorted list
        
    Example:
        >>> users = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}]
        >>> json_sort(users, 'age')
        [{'name': 'Jane', 'age': 25}, {'name': 'John', 'age': 30}]
    """
    return sorted(data, key=lambda x: get_value_by_path(x, key, ''), reverse=reverse)


def json_group_by(data: List[Dict], key: str) -> Dict[Any, List[Dict]]:
    """
    Group list of dictionaries by key value.
    
    Args:
        data: List of dictionaries
        key: Key to group by (supports path syntax)
        
    Returns:
        Dictionary mapping key values to lists of items
        
    Example:
        >>> users = [{'name': 'John', 'city': 'NYC'}, {'name': 'Jane', 'city': 'NYC'}]
        >>> json_group_by(users, 'city')
        {'NYC': [{'name': 'John', 'city': 'NYC'}, {'name': 'Jane', 'city': 'NYC'}]}
    """
    groups = {}
    for item in data:
        group_key = get_value_by_path(item, key)
        if group_key not in groups:
            groups[group_key] = []
        groups[group_key].append(item)
    return groups


# ============================================================================
# Transformation Operations
# ============================================================================

def json_transform(data: Any, transform_fn: Callable[[str, Any], Any], path: str = '') -> Any:
    """
    Transform JSON structure by applying function to all values.
    
    Args:
        data: JSON data
        transform_fn: Function(path, value) -> transformed_value
        path: Current path (used internally for recursion)
        
    Returns:
        Transformed data
        
    Example:
        >>> data = {'a': 1, 'b': 2}
        >>> json_transform(data, lambda k, v: v * 2 if isinstance(v, int) else v)
        {'a': 2, 'b': 4}
    """
    if isinstance(data, dict):
        return {k: json_transform(v, transform_fn, f"{path}.{k}" if path else k) 
                for k, v in data.items()}
    elif isinstance(data, list):
        return [json_transform(item, transform_fn, f"{path}[{i}]") 
                for i, item in enumerate(data)]
    else:
        return transform_fn(path, data)


def json_map_values(data: Dict, mapping: Dict[str, Any]) -> Dict:
    """
    Map values in dictionary using mapping dictionary.
    
    Args:
        data: Source dictionary
        mapping: Path -> value mapping
        
    Returns:
        Dictionary with mapped values
        
    Example:
        >>> data = {'user': {'name': 'john'}}
        >>> json_map_values(data, {'user.name': 'John Smith'})
        {'user': {'name': 'John Smith'}}
    """
    result = data.copy() if isinstance(data, dict) else {}
    for path, value in mapping.items():
        set_value_by_path(result, path, value, create_missing=True)
    return result


def json_flatten(data: Dict, separator: str = '.', prefix: str = '') -> Dict[str, Any]:
    """
    Flatten nested dictionary to single level with dotted keys.
    
    Args:
        data: Nested dictionary
        separator: Key separator
        prefix: Key prefix (for recursion)
        
    Returns:
        Flattened dictionary
        
    Example:
        >>> json_flatten({'a': {'b': 1, 'c': 2}})
        {'a.b': 1, 'a.c': 2}
    """
    result = {}
    
    for key, value in data.items():
        new_key = f"{prefix}{separator}{key}" if prefix else key
        
        if isinstance(value, dict):
            result.update(json_flatten(value, separator, new_key))
        elif isinstance(value, list):
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    result.update(json_flatten(item, separator, f"{new_key}[{i}]"))
                else:
                    result[f"{new_key}[{i}]"] = item
        else:
            result[new_key] = value
    
    return result


def json_unflatten(data: Dict[str, Any], separator: str = '.') -> Dict:
    """
    Unflatten dictionary with dotted keys to nested structure.
    
    Args:
        data: Flattened dictionary
        separator: Key separator
        
    Returns:
        Nested dictionary
        
    Example:
        >>> json_unflatten({'a.b': 1, 'a.c': 2})
        {'a': {'b': 1, 'c': 2}}
    """
    result = {}
    
    for key, value in data.items():
        set_value_by_path(result, key.replace(separator, '.'), value)
    
    return result


# ============================================================================
# Bash-style Operations (kubectl -o json like)
# ============================================================================

def json_extract_path(json_str: str, path: str) -> Optional[str]:
    """
    Extract value from JSON string using path (like kubectl -o jsonpath).
    
    Args:
        json_str: JSON string
        path: Path to extract
        
    Returns:
        JSON string of extracted value
        
    Example:
        >>> json_extract_path('{"user": {"name": "John"}}', 'user.name')
        '"John"'
    """
    try:
        data = json.loads(json_str)
        value = get_value_by_path(data, path)
        return json.dumps(value) if value is not None else None
    except json.JSONDecodeError:
        return None


def json_pipe_filter(json_str: str, filter_expr: str) -> Optional[str]:
    """
    Filter JSON using simple expression (key=value).
    
    Args:
        json_str: JSON string (should be array)
        filter_expr: Filter like "name=John" or "age>25"
        
    Returns:
        Filtered JSON string
        
    Example:
        >>> data = '[{"name":"John","age":30},{"name":"Jane","age":25}]'
        >>> json_pipe_filter(data, 'age>26')
        '[{"name":"John","age":30}]'
    """
    try:
        data = json.loads(json_str)
        if not isinstance(data, list):
            return json_str
        
        # Parse filter expression
        match = re.match(r'(\w+(?:\.\w+)*)\s*([=<>!]+)\s*(.+)', filter_expr)
        if not match:
            return json_str
        
        key, op, value = match.groups()
        
        # Try to convert value to appropriate type
        try:
            value = int(value)
        except ValueError:
            try:
                value = float(value)
            except ValueError:
                value = value.strip('\'"')
        
        # Filter based on operator
        filtered = []
        for item in data:
            item_value = get_value_by_path(item, key)
            if item_value is None:
                continue
            
            if op == '=' or op == '==':
                if item_value == value:
                    filtered.append(item)
            elif op == '!=':
                if item_value != value:
                    filtered.append(item)
            elif op == '>':
                if item_value > value:
                    filtered.append(item)
            elif op == '<':
                if item_value < value:
                    filtered.append(item)
            elif op == '>=':
                if item_value >= value:
                    filtered.append(item)
            elif op == '<=':
                if item_value <= value:
                    filtered.append(item)
        
        return json.dumps(filtered)
    except (json.JSONDecodeError, Exception):
        return None


# ============================================================================
# Module exports
# ============================================================================

__all__ = [
    # Path operations
    'parse_path',
    'get_value_by_path',
    'set_value_by_path',
    'delete_by_path',
    
    # JSON file operations
    'json_get',
    'json_set',
    'json_delete',
    'json_merge',
    
    # YAML operations
    'yaml_get',
    'yaml_set',
    
    # Query and filter
    'json_query',
    'json_filter',
    'json_find',
    'json_select',
    'json_sort',
    'json_group_by',
    
    # Transformation
    'json_transform',
    'json_map_values',
    'json_flatten',
    'json_unflatten',
    
    # Bash-style operations
    'json_extract_path',
    'json_pipe_filter',
]
