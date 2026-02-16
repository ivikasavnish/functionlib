# Index Files for LLM Integration

This directory contains comprehensive index files for all 10,094 functions in the library, specifically designed for LLM consumption and programmatic access.

## 📋 Index Files Overview

### Primary Index Files

| File | Format | Size | Purpose |
|------|--------|------|---------|
| `MASTER_INDEX.json` | JSON | 3.1 MB | Complete index of all 10,094 functions |
| `MASTER_INDEX.csv` | CSV | 1.0 MB | Spreadsheet format for filtering/analysis |
| `MASTER_INDEX.txt` | Text | 2.1 MB | Human-readable line-by-line format |

### Detailed Specification Files

| File | Format | Functions | Purpose |
|------|--------|-----------|---------|
| `FUNCTION_INDEX.json` | JSON | ~50 | Core functions with detailed input/output specs |
| `FUNCTION_INDEX.md` | Markdown | ~50 | Same as above in readable format |
| `FUNCTION_INDEX.csv` | CSV | ~50 | Core specs in spreadsheet format |
| `ENHANCED_FUNCTION_SPECS.json` | JSON | 100 | Extended schemas with templates |

### Lookup & Summary Files

| File | Format | Purpose |
|------|--------|---------|
| `CATEGORY_LOOKUP.json` | JSON | Quick access by category/subcategory |
| `INDEX_SUMMARY.json` | JSON | Statistics and breakdown by category |
| `LLM_INTEGRATION_GUIDE.md` | Markdown | Usage guide with examples |

## 🔍 Data Structure

Each function entry contains:

```json
{
  "id": 123,
  "name": "function_name",
  "category": "math|science|coding|general_purpose",
  "subcategory": "specific_subcategory",
  "path": "category/subcategory/function_name.md",
  "purpose": "Description of what the function does",
  "input": "varies - see documentation",
  "output": "varies - see documentation"
}
```

Enhanced specs (FUNCTION_INDEX.json and ENHANCED_FUNCTION_SPECS.json) include:

```json
{
  "id": 123,
  "name": "function_name",
  "category": "math",
  "subcategory": "algebra",
  "purpose": "Detailed description",
  "input": {
    "param1": "type and description",
    "param2": "type and description"
  },
  "output": {
    "result": "type and description",
    "metadata": "object with additional info"
  }
}
```

## 💻 Usage Examples

### Python

```python
import json

# Load master index
with open('MASTER_INDEX.json') as f:
    data = json.load(f)

# Get all functions
all_functions = data['functions']
total = data['total_functions']

# Filter by category
math_functions = [f for f in all_functions if f['category'] == 'math']

# Search by name
sort_functions = [f for f in all_functions if 'sort' in f['name']]

# Get specific subcategory
algebra_functions = [f for f in all_functions if f['subcategory'] == 'algebra']

# Find by ID
function = next(f for f in all_functions if f['id'] == 42)

# Use category lookup for faster access
with open('CATEGORY_LOOKUP.json') as f:
    lookup = json.load(f)
    physics_funcs = lookup['science/physics']
```

### JavaScript

```javascript
const fs = require('fs');

// Load master index
const data = JSON.parse(fs.readFileSync('MASTER_INDEX.json', 'utf8'));

// Get all functions
const allFunctions = data.functions;

// Filter by category
const scienceFunctions = allFunctions.filter(f => f.category === 'science');

// Search by name
const sortFunctions = allFunctions.filter(f => f.name.includes('sort'));

// Find by ID
const func = allFunctions.find(f => f.id === 42);

// Use category lookup
const lookup = JSON.parse(fs.readFileSync('CATEGORY_LOOKUP.json', 'utf8'));
const codingAlgorithms = lookup['coding/algorithms'];
```

### Command Line (using jq)

```bash
# Count functions by category
jq '.functions | group_by(.category) | map({category: .[0].category, count: length})' MASTER_INDEX.json

# Get all math functions
jq '.functions[] | select(.category == "math")' MASTER_INDEX.json

# Search for specific function
jq '.functions[] | select(.name | contains("sort"))' MASTER_INDEX.json

# Get function by ID
jq '.functions[] | select(.id == 42)' MASTER_INDEX.json
```

## 📊 Category Breakdown

| Category | Functions | Subcategories |
|----------|-----------|---------------|
| Math | 2,044 | 12 |
| Science | 2,450 | 10 |
| Coding | 2,800 | 20 |
| General Purpose | 2,800 | 20 |
| **Total** | **10,094** | **62** |

### Math Subcategories (2,044 functions)
- algebra, calculus, geometry, trigonometry, statistics, probability
- number_theory, linear_algebra, discrete_math, complex_numbers
- optimization, numerical_analysis

### Science Subcategories (2,450 functions)
- physics, chemistry, biology, astronomy, earth_science
- electronics, materials_science, environmental_science
- quantum_physics, thermodynamics

### Coding Subcategories (2,800 functions)
- data_structures, algorithms, string_operations, file_operations
- database_operations, network_operations, cryptography
- image_processing, audio_processing, video_processing
- web_development, api_development, testing, debugging
- machine_learning, data_visualization, parsing, validation
- concurrency, memory_management

### General Purpose Subcategories (2,800 functions)
- date_time, string_utilities, math_utilities, array_utilities
- object_utilities, validation, formatting, conversion
- random_generation, hashing, compression, encoding
- localization, financial, geographic, color_utilities
- text_processing, business_logic, security, communication

## 🎯 LLM Use Cases

### 1. Function Discovery
```python
# Find all functions related to sorting
results = [f for f in data['functions'] if 'sort' in f['name']]
```

### 2. Code Generation
```python
# Generate function stub
def generate_stub(func_data):
    return f"""
def {func_data['name']}(*args, **kwargs):
    '''
    {func_data['purpose']}
    
    Category: {func_data['category']}/{func_data['subcategory']}
    '''
    pass
"""
```

### 3. API Documentation
```python
# Generate API docs
def generate_api_doc(func_data):
    return f"""
## {func_data['name']}

**Category:** {func_data['category']} > {func_data['subcategory']}

**Purpose:** {func_data['purpose']}

**Endpoint:** `/api/{func_data['category']}/{func_data['name']}`
"""
```

### 4. Testing Suite Generation
```python
# Generate test cases
def generate_test(func_data):
    return f"""
def test_{func_data['name']}():
    '''Test {func_data['purpose']}'''
    # TODO: Implement test
    pass
"""
```

## 📝 File Formats

### JSON Format
- **MASTER_INDEX.json**: Complete structured data
- **FUNCTION_INDEX.json**: Detailed specs for core functions
- **ENHANCED_FUNCTION_SPECS.json**: Extended schemas
- **CATEGORY_LOOKUP.json**: Fast category-based access
- **INDEX_SUMMARY.json**: Statistics and counts

### CSV Format
- **MASTER_INDEX.csv**: All functions in spreadsheet format
- **FUNCTION_INDEX.csv**: Core function specs

### Text/Markdown Format
- **MASTER_INDEX.txt**: Line-by-line listing
- **FUNCTION_INDEX.md**: Formatted documentation
- **LLM_INTEGRATION_GUIDE.md**: This guide

## 🚀 Getting Started

1. **Explore the library:**
   - Open `MASTER_INDEX.json` to see all functions
   - Check `INDEX_SUMMARY.json` for statistics

2. **Find specific functions:**
   - Use `CATEGORY_LOOKUP.json` for category-based search
   - Filter `MASTER_INDEX.json` by name or category

3. **Get detailed specs:**
   - Check `FUNCTION_INDEX.json` for core functions
   - See `ENHANCED_FUNCTION_SPECS.json` for extended info

4. **Integrate with code:**
   - Follow examples in `LLM_INTEGRATION_GUIDE.md`
   - Use provided code snippets

## 🔄 Updates

To regenerate index files after adding new functions:

```bash
python3 generate_functions.py
```

This will update all index files to include new functions.

## 📞 Support

For questions or issues with the index files:
- Check `LLM_INTEGRATION_GUIDE.md` for usage patterns
- Refer to individual function documentation in category folders
- See `README.md` in root directory for library overview

---

**Generated:** 2026-01-07  
**Version:** 1.0  
**Total Functions:** 10,094  
**Index Files:** 10
