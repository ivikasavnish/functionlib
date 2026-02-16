# Structured Data Manipulation Quick Reference

**22 Functions for JSON/YAML Editing** | Path-based Operations | kubectl-style Queries

## 🎯 Path Syntax

Supports JSONPath-like syntax:
```python
"user.name"                    # Dot notation
"users[0].email"               # Array access
"config.database.settings[0]"  # Mixed
"data['key'].value"            # Bracket notation
```

## 📝 Basic Path Operations

```python
from functionlib.coding.structured_data import *

data = {
    'user': {
        'name': 'John',
        'profile': {'email': 'john@example.com', 'age': 30}
    },
    'items': [
        {'id': 1, 'name': 'Item 1'},
        {'id': 2, 'name': 'Item 2'}
    ]
}

# Parse path
parse_path("user.profile.email")
# → ['user', 'profile', 'email']

# Get value
get_value_by_path(data, 'user.profile.email')
# → 'john@example.com'

# Set value
set_value_by_path(data, 'user.profile.city', 'NYC')
# → True, data is modified

# Delete value
delete_by_path(data, 'user.profile.age')
# → True, age is removed
```

## 📄 JSON File Operations

```python
# Get from JSON file
json_get('config.json', 'database.host')
# → 'localhost'

# Set in JSON file
json_set('config.json', 'database.port', 5432)
# Creates nested structure if needed

# Delete from JSON file
json_delete('config.json', 'database.debug')

# Deep merge
json_merge('config.json', {
    'database': {'pool': 10},
    'cache': {'enabled': True}
})
```

## 🗂️ YAML Operations

```python
# Get from YAML file
yaml_get('config.yaml', 'database.host')
# → 'localhost'

# Set in YAML file
yaml_set('config.yaml', 'database.port', 5432)
# Falls back to JSON if PyYAML not installed
```

## 🔍 Query & Filter

```python
users = [
    {'name': 'John', 'age': 30, 'city': 'NYC'},
    {'name': 'Jane', 'age': 25, 'city': 'LA'},
    {'name': 'Bob', 'age': 35, 'city': 'NYC'}
]

# Filter by key-value
json_filter(users, 'city', 'NYC')
# → [{'name': 'John', ...}, {'name': 'Bob', ...}]

# Find first match
json_find(users, 'name', 'Jane')
# → {'name': 'Jane', 'age': 25, 'city': 'LA'}

# Select columns (SQL-like)
json_select(users, ['name', 'city'])
# → [{'name': 'John', 'city': 'NYC'}, ...]

# Sort by key
json_sort(users, 'age')
# → Sorted by age ascending

# Group by key
json_group_by(users, 'city')
# → {'NYC': [...], 'LA': [...]}

# Query with predicate
json_query(users, lambda x: isinstance(x, dict) and x.get('age', 0) > 26)
# → [{'name': 'John', ...}, {'name': 'Bob', ...}]
```

## 🔄 Transformations

```python
# Flatten nested structure
nested = {
    'user': {
        'name': 'John',
        'profile': {'email': 'john@example.com'}
    }
}
json_flatten(nested)
# → {'user.name': 'John', 'user.profile.email': 'john@example.com'}

# Unflatten
flat = {'user.name': 'John', 'user.age': 30}
json_unflatten(flat)
# → {'user': {'name': 'John', 'age': 30}}

# Transform all values
json_transform(data, lambda path, val: val.upper() if isinstance(val, str) else val)
# Applies function to all values

# Map values
json_map_values(data, {
    'user.name': 'John Doe',
    'user.profile.city': 'NYC'
})
# Updates specified paths
```

## 🖥️ Bash-style Operations (kubectl-like)

```python
# Extract from JSON string
json_str = '{"users": [{"name": "John"}, {"name": "Jane"}]}'
json_extract_path(json_str, 'users[0].name')
# → '"John"'

# Filter with expression (like kubectl)
json_data = '[{"name":"John","age":30}, {"name":"Jane","age":25}]'

json_pipe_filter(json_data, 'age>26')
# → '[{"name":"John","age":30}]'

json_pipe_filter(json_data, 'name=Jane')
# → '[{"name":"Jane","age":25}]'

# Supported operators: =, ==, !=, >, <, >=, <=
```

## 📋 Real-World Examples

### 1. Update Kubernetes-style Config
```python
# Read config
config = json_get('k8s-config.json', 'spec.containers[0]')

# Update image
json_set('k8s-config.json', 'spec.containers[0].image', 'nginx:latest')

# Add environment variable
env_vars = json_get('k8s-config.json', 'spec.containers[0].env', [])
env_vars.append({'name': 'DEBUG', 'value': 'true'})
json_set('k8s-config.json', 'spec.containers[0].env', env_vars)
```

### 2. Query Log Files
```python
# Load logs
logs = json_get('app-logs.json', 'entries')

# Filter errors
errors = json_filter(logs, 'level', 'ERROR')

# Group by service
by_service = json_group_by(errors, 'service')

# Select important fields
summary = json_select(errors, ['timestamp', 'message', 'service'])
```

### 3. Transform API Response
```python
# Get API data
api_response = json_get('response.json')

# Extract specific fields
users = json_get('response.json', 'data.users')

# Transform to simpler format
simplified = json_select(users, ['id', 'name', 'email'])

# Group by role
by_role = json_group_by(users, 'role')
```

### 4. Configuration Management
```python
# Merge environment-specific configs
json_merge('config.json', {
    'environment': 'production',
    'database': {'replicas': 3},
    'cache': {'ttl': 3600}
})

# Flatten for environment variables
flat_config = json_flatten(json_get('config.json'))
# Export as ENV vars: DATABASE_HOST=..., CACHE_TTL=...
```

### 5. Data Pipeline
```python
# Load raw data
data = json_get('raw-data.json', 'records')

# Filter valid records
valid = json_filter(data, 'status', 'active')

# Sort by timestamp
sorted_data = json_sort(valid, 'timestamp', reverse=True)

# Select fields for output
output = json_select(sorted_data, ['id', 'timestamp', 'value'])

# Save processed data
json_set('processed-data.json', 'results', output)
```

## 🎯 Use Cases

| Use Case | Functions |
|----------|-----------|
| **Config File Editing** | json_set, yaml_set, json_merge |
| **Data Extraction** | get_value_by_path, json_extract_path |
| **Log Analysis** | json_filter, json_query, json_group_by |
| **API Response Processing** | json_select, json_transform |
| **Pipeline Filtering** | json_pipe_filter (kubectl-style) |
| **Config Flattening** | json_flatten, json_unflatten |
| **Nested Navigation** | parse_path, get_value_by_path |

## 🔑 Key Features

- ✅ **Path Syntax**: Dot notation, brackets, mixed paths
- ✅ **File Operations**: Read/write JSON and YAML files
- ✅ **SQL-like Queries**: filter, find, select, sort, group by
- ✅ **Transformations**: flatten, unflatten, transform, map
- ✅ **Bash-style**: kubectl-like predicates and filtering
- ✅ **Pure Python**: stdlib only (json, re)
- ✅ **Type Safe**: Type hints throughout

## 📦 Module

```python
from functionlib.coding.structured_data import (
    # Path operations
    parse_path, get_value_by_path, set_value_by_path, delete_by_path,
    
    # JSON file operations
    json_get, json_set, json_delete, json_merge,
    
    # YAML operations
    yaml_get, yaml_set,
    
    # Query & filter
    json_query, json_filter, json_find, json_select, 
    json_sort, json_group_by,
    
    # Transformations
    json_transform, json_map_values, json_flatten, json_unflatten,
    
    # Bash-style
    json_extract_path, json_pipe_filter
)
```

---

**Total Functions:** 22  
**Dependencies:** Pure Python stdlib (json, re)  
**Optional:** PyYAML for YAML support (falls back to JSON)
