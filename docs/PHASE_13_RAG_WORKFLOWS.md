# Phase 13: RAG, LLM Recipes, Async Jobs & Workflow Engine

## Overview

Phase 13 adds **55 new components** for building AI applications, async task processing, and workflow orchestration. Total library now contains **1,270 functions**.

## New Modules

### 1. RAG Module (`functionlib.coding.rag`) - 14 Components

Retrieval Augmented Generation utilities for building AI search and retrieval systems.

**Vector Operations:**
- `cosine_similarity()` - Calculate similarity between vectors
- `euclidean_distance()` - Calculate distance between vectors
- `simple_embedding()` - Create deterministic embeddings from text

**Text Processing:**
- `chunk_text()` - Split text into overlapping chunks
- `chunk_by_sentences()` - Chunk by sentence boundaries
- `extract_keywords()` - TF-IDF-based keyword extraction
- `query_expansion()` - Expand queries with synonyms/related terms

**Storage & Search:**
- `InMemoryVectorStore` - Vector database with similarity search
- `DocumentStore` - Document management with metadata
- `bm25_score()` - BM25 ranking for keyword search
- `hybrid_search()` - Combine vector + keyword search
- `reciprocal_rank_fusion()` - Merge multiple ranking lists

**Utilities:**
- `rerank_results()` - Rerank search results
- `create_rag_context()` - Format results for LLM prompting

#### Example: RAG Pipeline

```python
from functionlib.coding.rag import *

# Create embeddings
docs = ["Python is great", "JavaScript is useful", "Go is fast"]
embeddings = [simple_embedding(doc) for doc in docs]

# Store in vector DB
store = InMemoryVectorStore(embedding_dim=384)
for doc, emb in zip(docs, embeddings):
    store.add_document(doc, emb, {"type": "programming"})

# Search
query = "Best programming language"
query_emb = simple_embedding(query)
results = store.search(query_emb, top_k=3)

# Create context for LLM
context = create_rag_context(query, results)
```

---

### 2. LLM Recipes Module (`functionlib.coding.llm_recipes`) - 22 Components

Common LLM patterns compatible with LlamaIndex and LangChain paradigms.

**Prompting:**
- `PromptTemplate` - Variable substitution in prompts
- `create_rag_prompt()` - RAG-style prompts
- `create_few_shot_prompt()` - Few-shot learning prompts
- `create_cot_prompt()` - Chain-of-Thought prompts
- `create_react_prompt()` - Reasoning + Acting prompts
- `create_system_message()` - System message formatting

**Memory:**
- `ConversationMemory` - Buffer conversation history
- `BufferMemory` - Alias for conversation memory
- `SummaryMemory` - Auto-summarize old conversations

**Chains:**
- `LLMChain` - Combine prompt + LLM
- `SequentialChain` - Chain multiple LLMs
- `RouterChain` - Route to different chains
- `Agent` - Agent that can use tools

**Parsing & Validation:**
- `OutputParser` - Parse LLM outputs (JSON, list, bool)
- `parse_json_response()` - Extract JSON from text
- `extract_code_blocks()` - Extract markdown code blocks
- `RetryWithFeedback` - Retry with validation

**Utilities:**
- `LLMCache` - Cache responses to avoid redundant calls
- `token_count_estimate()` - Estimate token count
- `truncate_to_tokens()` - Truncate to token limit
- `batch_prompts()` - Batch prompts for efficiency
- `format_chat_messages()` - Format for different APIs

#### Example: LLM Chain with Memory

```python
from functionlib.coding.llm_recipes import *

# Create conversation memory
memory = ConversationMemory(max_messages=10)

# Create prompt template
template = PromptTemplate(
    "Context: {context}\nQuestion: {question}\nAnswer:",
    input_variables=["context", "question"]
)

# Create chain
def mock_llm(prompt):
    return "This is a response"

chain = LLMChain(template, llm_fn=mock_llm)

# Use chain
result = chain.run(context="Python is a language", question="What is Python?")

# Save conversation
memory.add_user_message("What is Python?")
memory.add_assistant_message(result)
memory.save("conversation.json")
```

---

### 3. Async Jobs Module (`functionlib.coding.async_jobs`) - 10 Components

Thread-based async job processing with queues, workers, and schedulers.

**Core Components:**
- `Job` - Represents a task with status, retries, priority
- `JobQueue` - Thread-safe priority queue
- `Worker` - Worker thread that processes jobs
- `WorkerPool` - Pool of workers with job submission
- `JobStatus` - Enum: PENDING, RUNNING, COMPLETED, FAILED, etc.

**Scheduling:**
- `Scheduler` - Schedule jobs at intervals or specific times
- `TaskBatch` - Execute multiple tasks as a batch
- `RateLimiter` - Rate limit job submissions

**Utilities:**
- `JobProgressTracker` - Track progress of long-running jobs
- `create_job_chain()` - Chain jobs sequentially

#### Example: Worker Pool

```python
from functionlib.coding.async_jobs import *
import time

# Create worker pool
pool = WorkerPool(num_workers=4)
pool.start()

# Submit jobs
def process_data(x):
    time.sleep(0.1)
    return x * 2

job_ids = [pool.submit(process_data, i) for i in range(10)]

# Wait for completion
for job_id in job_ids:
    pool.wait_for_job(job_id, timeout=5)
    result = pool.get_job_result(job_id)
    print(f"Result: {result}")

# Get statistics
stats = pool.get_statistics()
print(f"Processed: {stats['total_processed']}")

pool.stop()
```

#### Example: Scheduler

```python
from functionlib.coding.async_jobs import *

def send_report():
    print("Sending daily report...")

# Create scheduler
scheduler = Scheduler()
scheduler.start()

# Schedule recurring task (every 60 seconds)
job_id = scheduler.schedule_interval(send_report, interval=60)

# Schedule one-time task (after 5 seconds)
scheduler.schedule_once(lambda: print("One-time task"), delay=5)
```

---

### 4. Workflow Engine Module (`functionlib.coding.workflow_engine`) - 9 Components

DAG-based workflow orchestration for complex task pipelines.

**Core Components:**
- `Task` - Workflow task with dependencies
- `Workflow` - DAG of tasks
- `TaskStatus` - Enum: PENDING, READY, RUNNING, COMPLETED, FAILED, etc.
- `WorkflowExecutor` - Execute workflows (sequential/parallel)

**Advanced Features:**
- `ConditionalTask` - Task that runs conditionally
- `ParallelTaskGroup` - Group of tasks running in parallel
- `WorkflowTemplate` - Create common patterns (map-reduce, pipeline, fan-out)
- `WorkflowMonitor` - Monitor multiple workflows

**Utilities:**
- `visualize_workflow()` - Text visualization of DAG

#### Example: Workflow with Dependencies

```python
from functionlib.coding.workflow_engine import *

# Create workflow
workflow = Workflow("data-pipeline")

# Add tasks with dependencies
def fetch_data():
    return [1, 2, 3, 4, 5]

def transform_data(_dependencies=None):
    data = _dependencies['fetch']
    return [x * 2 for x in data]

def save_data(_dependencies=None):
    data = _dependencies['transform']
    print(f"Saving: {data}")
    return True

workflow.add_task_from_func("fetch", fetch_data)
workflow.add_task_from_func("transform", transform_data, dependencies=["fetch"])
workflow.add_task_from_func("save", save_data, dependencies=["transform"])

# Validate and execute
valid, error = workflow.validate()
if valid:
    executor = WorkflowExecutor(max_parallel=2)
    success = executor.execute_parallel(workflow)
    print(f"Workflow completed: {success}")

# Visualize
print(visualize_workflow(workflow))
```

#### Example: Map-Reduce Pattern

```python
from functionlib.coding.workflow_engine import *

# Create map-reduce workflow
def map_func(item):
    return item ** 2

def reduce_func(**kwargs):
    results = kwargs.get('_dependencies', {}).values()
    return sum(results)

workflow = WorkflowTemplate.create_map_reduce(
    map_func,
    reduce_func,
    inputs=[1, 2, 3, 4, 5]
)

# Execute
executor = WorkflowExecutor()
executor.execute_parallel(workflow)

# Get result
reduce_task = workflow.get_task("reduce")
print(f"Sum of squares: {reduce_task.result}")
```

---

## Integration Examples

### RAG + LLM Recipes

```python
from functionlib.coding.rag import *
from functionlib.coding.llm_recipes import *

# Build RAG system
store = InMemoryVectorStore()
documents = ["Doc 1 content", "Doc 2 content", "Doc 3 content"]

for doc in documents:
    emb = simple_embedding(doc)
    store.add_document(doc, emb)

# Create RAG chain
def rag_chain(query):
    # Retrieve
    query_emb = simple_embedding(query)
    results = store.search(query_emb, top_k=3)
    context = create_rag_context(query, results)
    
    # Create prompt
    prompt = create_rag_prompt(query, context)
    
    # Call LLM (mock)
    return f"Answer based on: {context[:100]}..."

result = rag_chain("What is Python?")
```

### Async Jobs + Workflow

```python
from functionlib.coding.async_jobs import *
from functionlib.coding.workflow_engine import *

# Create worker pool
pool = WorkerPool(num_workers=4)
pool.start()

# Create workflow that submits async jobs
workflow = Workflow("async-pipeline")

def async_task():
    job_id = pool.submit(lambda: "processed")
    pool.wait_for_job(job_id)
    return pool.get_job_result(job_id)

workflow.add_task_from_func("task1", async_task)

executor = WorkflowExecutor()
executor.execute_sequential(workflow)
```

---

## Key Features

✅ **Pure Python stdlib** - No external dependencies required  
✅ **Thread-safe** - All components use proper locking  
✅ **Production-ready** - Error handling, retries, monitoring  
✅ **Extensible** - Easy to integrate with real LLM APIs  
✅ **Well-tested** - All components verified working  

## Performance Notes

- **RAG searches**: O(n) linear scan (use Faiss/Pinecone for production)
- **Worker pools**: Supports high concurrency with priority queues
- **Workflows**: DAG validation O(V+E), execution parallel where possible
- **Embeddings**: Deterministic hash-based (use sentence-transformers for production)

## Dependencies (Optional)

For production use, consider adding:
- `sentence-transformers` - Better embeddings
- `langchain` - Full LangChain integration
- `llama-index` - Full LlamaIndex integration
- `chromadb` / `pinecone` - Production vector databases
- `redis` - Distributed job queues

## Next Steps

Consider adding:
- [ ] Streaming support for LLM responses
- [ ] Distributed workflow execution
- [ ] Graph database for complex RAG
- [ ] Vector DB integrations (Chroma, Pinecone, Weaviate)
- [ ] Async/await support (asyncio module)

---

**Phase 13 Complete: +55 components, 1,270 total functions**
