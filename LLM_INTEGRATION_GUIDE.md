
# Function Library for LLM Integration

## How to Use This Library

This library contains 10,094 functions across 4 main categories:
- Math (2,044 functions)
- Science (2,450 functions)
- Coding (2,800 functions)
- General Purpose (2,800 functions)

## Index Files

1. **MASTER_INDEX.json** - Complete list of all functions
2. **MASTER_INDEX.csv** - Spreadsheet format for easy filtering
3. **MASTER_INDEX.txt** - Human-readable text format
4. **FUNCTION_INDEX.json** - Detailed specs for core functions
5. **ENHANCED_FUNCTION_SPECS.json** - Extended specifications with schemas

## Query Examples

### Find all functions in a category:
```python
import json
with open('MASTER_INDEX.json') as f:
    data = json.load(f)
    math_funcs = [f for f in data['functions'] if f['category'] == 'math']
```

### Search by name:
```python
search_term = 'sort'
matches = [f for f in data['functions'] if search_term in f['name']]
```

### Get function by ID:
```python
func = next(f for f in data['functions'] if f['id'] == 42)
```

## Function Call Pattern

For any function in the library:

```python
# Standard pattern
result = function_name(
    input_params,
    options={...}
)

# Returns
{
    "result": <computed value>,
    "metadata": {
        "function": "function_name",
        "category": "category/subcategory",
        "execution_time": <milliseconds>
    }
}
```

## LLM Integration Tips

1. **Loop through functions**: Use MASTER_INDEX.json
2. **Filter by category**: Query the 'category' and 'subcategory' fields
3. **Generate code**: Use function name and purpose to create implementations
4. **Create documentation**: Use purpose and path fields
5. **Build APIs**: Use input/output schemas from ENHANCED_FUNCTION_SPECS.json

## Category Breakdown

- **Math**: Algebra, Calculus, Geometry, Statistics, and more
- **Science**: Physics, Chemistry, Biology, Engineering sciences
- **Coding**: Data structures, Algorithms, String/File operations, ML
- **General Purpose**: Date/Time, String utils, Validation, Financial, Geographic

## Access Pattern

Each function has:
- Unique ID (1-10094)
- Name (descriptive, lowercase with underscores)
- Category and Subcategory
- Purpose (what it does)
- Path (location of documentation file)
- Input/Output specifications (in enhanced specs)

