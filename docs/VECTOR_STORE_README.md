# Vector Store Integration

This directory contains files optimized for vector store integration.

## Files Created

### Data Files
- `VECTOR_STORE_DATA.json` - Main file with all 10,094 functions ready for embedding
- `VECTOR_STORE_DATA.jsonl` - JSONL format (one JSON object per line)
- `VECTOR_STORE_PINECONE.json` - Optimized for Pinecone
- `VECTOR_STORE_WEAVIATE.json` - Optimized for Weaviate
- `VECTOR_STORE_CHROMADB.json` - Optimized for ChromaDB
- `VECTOR_STORE_QDRANT.json` - Optimized for Qdrant

### Scripts
- `vector_store_upload.py` - Script to generate embeddings and upload
- `vector_store_query.py` - Example queries for vector store

## Quick Start

### Option 1: ChromaDB (Easiest - No API keys needed)

```bash
# Install ChromaDB
pip install chromadb sentence-transformers

# Run the upload script
python3 vector_store_upload.py

# Query the vector store
python3 vector_store_query.py
```

### Option 2: Pinecone (Cloud-based)

```bash
# Install Pinecone
pip install pinecone-client sentence-transformers

# Set your API key in vector_store_upload.py
# Run the script
python3 vector_store_upload.py
```

### Option 3: Custom Implementation

Load the data and use your own embedding model:

```python
import json

# Load data
with open('VECTOR_STORE_DATA.json', 'r') as f:
    data = json.load(f)

# Each entry has:
# - id: unique identifier
# - text: rich text for embedding
# - metadata: function details

for entry in data['entries']:
    text = entry['text']  # Embed this
    metadata = entry['metadata']  # Store this
```

## Data Format

Each entry in `VECTOR_STORE_DATA.json`:

```json
{
  "id": 123,
  "text": "Function: solve_quadratic_equation\nCategory: math\n...",
  "metadata": {
    "function_name": "solve_quadratic_equation",
    "category": "math",
    "subcategory": "algebra",
    "purpose": "Solves quadratic equations",
    "path": "math/algebra/solve_quadratic_equation.md",
    "full_category_path": "math/algebra"
  }
}
```

## Embedding Models

### Free/Local Options
- **Sentence Transformers**: `all-MiniLM-L6-v2` (384 dim)
- **Sentence Transformers**: `all-mpnet-base-v2` (768 dim)
- **Sentence Transformers**: `multi-qa-mpnet-base-dot-v1` (768 dim)

### API-based Options
- **OpenAI**: `text-embedding-3-small` (1536 dim)
- **OpenAI**: `text-embedding-3-large` (3072 dim)
- **Cohere**: `embed-english-v3.0`

## Example Queries

Once uploaded, you can query for:
- "find functions to sort arrays"
- "calculate area of geometric shapes"
- "parse and format dates"
- "encrypt or hash data"
- "solve mathematical equations"
- "process images"
- "validate user input"

## Vector Store Comparison

| Store | Pros | Cons |
|-------|------|------|
| ChromaDB | Easy, local, free | Limited scale |
| Pinecone | Fast, managed, scalable | Requires API key |
| Weaviate | Feature-rich, GraphQL | More complex setup |
| Qdrant | Fast, Rust-based | Requires hosting |

## Performance

- **Total Functions**: 10,094
- **Average Text Length**: ~150 characters
- **Embedding Time** (sentence-transformers): ~2-5 minutes
- **Embedding Time** (OpenAI API): ~5-10 minutes
- **Storage Size** (with embeddings): ~50-150 MB depending on model

## Next Steps

1. Choose your vector store
2. Install dependencies
3. Run `vector_store_upload.py`
4. Test queries with `vector_store_query.py`
5. Integrate into your application

## Semantic Search Examples

After uploading, you can perform semantic searches:

```python
# Find similar functions
results = search("sort numbers in ascending order")
# Returns: quick_sort, merge_sort, bubble_sort, etc.

results = search("calculate circle measurements")
# Returns: circle_area, circle_circumference, circle_radius, etc.

results = search("check if email is valid")
# Returns: validate_email, parse_email, is_valid_email, etc.
```

## Support

- See `LLM_INTEGRATION_GUIDE.md` for general usage
- Check `INDEX_README.md` for data structure details
- Refer to vector store specific documentation
