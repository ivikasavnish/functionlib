.PHONY: help reindex install clean test-query

help:
	@echo "FunctionLib ChromaDB Management"
	@echo "================================"
	@echo ""
	@echo "Available commands:"
	@echo "  make install      - Install required dependencies"
	@echo "  make reindex      - Re-run vector indexing in ChromaDB"
	@echo "  make clean        - Remove ChromaDB database files"
	@echo "  make test-query   - Test ChromaDB with sample query"
	@echo ""

install:
	@echo "Installing dependencies..."
	pip install chromadb sentence-transformers

reindex:
	@echo "Starting ChromaDB re-indexing..."
	python3 reindex_chroma.py

clean:
	@echo "Removing ChromaDB database files..."
	rm -rf ./chroma_db
	@echo "ChromaDB cleaned successfully"

test-query:
	@echo "Testing ChromaDB query..."
	python3 -c "import chromadb; client = chromadb.PersistentClient(path='./chroma_db'); collection = client.get_collection('function_library'); results = collection.query(query_texts=['sorting algorithms'], n_results=3); print(f'Found {len(results[\"ids\"][0])} results'); [print(f'{i+1}. {doc[:100]}...') for i, doc in enumerate(results['documents'][0])]"
