# RAG, LLM & Workflow Quick Reference

## RAG Module

```python
from functionlib.coding.rag import *

# EMBEDDINGS & SIMILARITY
emb = simple_embedding("text", dimensions=384)
sim = cosine_similarity(vec1, vec2)  # 0-1, higher = more similar
dist = euclidean_distance(vec1, vec2)

# TEXT CHUNKING
chunks = chunk_text(text, chunk_size=512, overlap=50)
chunks = chunk_by_sentences(text, max_chunk_size=512)

# VECTOR STORE
store = InMemoryVectorStore(embedding_dim=384)
store.add_document(text, embedding, metadata={"source": "..."})
results = store.search(query_embedding, top_k=5, threshold=0.7)
store.save("vectordb.json")

# SEARCH STRATEGIES
score = bm25_score(query_terms, document, corpus)
results = hybrid_search(query, query_emb, store, alpha=0.5)
results = rerank_results(query, results, strategy='keyword_boost')
fused = reciprocal_rank_fusion([results1, results2, results3])

# DOCUMENT MANAGEMENT
doc_store = DocumentStore()
doc_id = doc_store.add_document(text, metadata={})
doc = doc_store.get_document(doc_id)

# UTILITIES
context = create_rag_context(query, results, max_length=2000)
keywords = extract_keywords(text, top_k=10)
expanded = query_expansion(query, method='synonyms')
```

---

## LLM Recipes Module

```python
from functionlib.coding.llm_recipes import *

# PROMPTS
template = PromptTemplate("Hello {name}!")
prompt = template.format(name="Alice")
prompt = create_rag_prompt(query, context)
prompt = create_few_shot_prompt(examples, query)
prompt = create_cot_prompt(query)  # Chain of Thought

# MEMORY
memory = ConversationMemory(max_messages=10)
memory.add_user_message("Question")
memory.add_assistant_message("Answer")
context = memory.get_context()
memory.save("conversation.json")

# CHAINS
chain = LLMChain(prompt_template, llm_fn)
result = chain.run(input="...")

seq_chain = SequentialChain([chain1, chain2, chain3])
result = seq_chain.run(initial_input={...})

router = RouterChain(routes={"math": math_chain, "code": code_chain})
result = router.run(input="solve equation")

# AGENT
tools = [{"name": "calculator", "function": calc_fn}]
agent = Agent(tools, llm_fn)
result = agent.run("Calculate 5 + 3")

# PARSING
parser = OutputParser(expected_format="json")
data = parser.parse(llm_output)
json_data = parse_json_response(text)
code = extract_code_blocks(text, language="python")

# UTILITIES
cache = LLMCache()
cached_llm = cache.wrap(llm_fn)

tokens = token_count_estimate(text)
truncated = truncate_to_tokens(text, max_tokens=100)
batches = batch_prompts(prompts, batch_size=5)

retry = RetryWithFeedback(llm_fn, max_retries=3)
result = retry.run(prompt, validator=lambda x: len(x) > 10)
```

---

## Async Jobs Module

```python
from functionlib.coding.async_jobs import *

# WORKER POOL
pool = WorkerPool(num_workers=4)
pool.start()

# Submit jobs
job_id = pool.submit(func, arg1, arg2, kwarg=val)
job_id = pool.submit_with_priority(func, priority=10, arg1)

# Wait and get results
success = pool.wait_for_job(job_id, timeout=30)
result = pool.get_job_result(job_id)
status = pool.get_job_status(job_id)

# Statistics
stats = pool.get_statistics()
# {'num_workers': 4, 'queue_size': 2, 'total_processed': 10, ...}

pool.stop()

# SCHEDULER
scheduler = Scheduler()
scheduler.start()

# One-time job (run after 5 seconds)
job_id = scheduler.schedule_once(func, delay=5, arg1)

# Recurring job (every 60 seconds)
job_id = scheduler.schedule_interval(func, interval=60, arg1)

scheduler.cancel_scheduled(job_id)
scheduler.stop()

# BATCH EXECUTION
batch = TaskBatch()
batch.add_task(func1, arg1)
batch.add_task(func2, arg2)
job_ids = batch.execute(wait=True)
results = batch.get_results(job_ids)

# RATE LIMITING
limiter = RateLimiter(max_calls=10, time_window=60)
if limiter.acquire(timeout=5):
    # Make API call
    pass

# PROGRESS TRACKING
tracker = JobProgressTracker()
tracker.update_progress(job_id, current=50, total=100, message="Processing...")
progress = tracker.get_progress(job_id)
# {'current': 50, 'total': 100, 'percentage': 50.0, ...}

# JOB CHAINING
jobs = [(func1, args1, kwargs1), (func2, args2, kwargs2)]
job_ids = create_job_chain(jobs, worker_pool)
```

---

## Workflow Engine Module

```python
from functionlib.coding.workflow_engine import *

# BASIC WORKFLOW
workflow = Workflow("my-workflow")

def task1():
    return "result1"

def task2(_dependencies=None):
    prev = _dependencies.get('task1')
    return f"processed {prev}"

# Add tasks with dependencies
workflow.add_task_from_func("task1", task1)
workflow.add_task_from_func("task2", task2, dependencies=["task1"])
workflow.add_task_from_func("task3", task3, dependencies=["task1"])

# Validate (checks for cycles)
valid, error = workflow.validate()

# Execute
executor = WorkflowExecutor(max_parallel=4)
success = executor.execute_sequential(workflow)
success = executor.execute_parallel(workflow)

# With callbacks
def on_complete(task):
    print(f"Task {task.task_id} done")

executor.execute_with_callback(workflow, on_task_complete=on_complete)

# Get results
task = workflow.get_task("task1")
print(task.result, task.status, task.error)

# CONDITIONAL TASKS
condition = lambda deps: deps.get('task1') > 10

conditional = ConditionalTask("cond", func, condition)
workflow.add_task(conditional)

# PARALLEL GROUPS
group = ParallelTaskGroup("group1")
group.add_task(task1)
group.add_task(task2)
success = group.execute()

# WORKFLOW TEMPLATES

# Map-Reduce
workflow = WorkflowTemplate.create_map_reduce(
    map_func=lambda x: x ** 2,
    reduce_func=lambda **kw: sum(kw['_dependencies'].values()),
    inputs=[1, 2, 3, 4, 5]
)

# Pipeline (linear)
workflow = WorkflowTemplate.create_pipeline([
    ("fetch", fetch_func),
    ("transform", transform_func),
    ("save", save_func)
])

# Fan-out / Fan-in
workflow = WorkflowTemplate.create_fan_out_fan_in(
    prepare_func=prepare,
    parallel_funcs=[("task1", func1), ("task2", func2)],
    aggregate_func=aggregate
)

# MONITORING
monitor = WorkflowMonitor()
monitor.register_workflow(workflow)

status = monitor.get_workflow_status(workflow_id)
all_status = monitor.get_all_workflows()
monitor.cleanup_completed()

# VISUALIZATION
viz = visualize_workflow(workflow)
print(viz)
# Workflow: my-workflow
# ==================================================
# ✓ task1
#   ✓ task2 <- [task1]
#   ✓ task3 <- [task1]

# SAVE/LOAD
workflow.save("workflow.json")
stats = workflow.get_statistics()
```

---

## Common Patterns

### Pattern 1: RAG Pipeline
```python
# Build vector store
store = InMemoryVectorStore()
for doc in documents:
    emb = simple_embedding(doc)
    store.add_document(doc, emb, metadata)

# Query
query_emb = simple_embedding(query)
results = hybrid_search(query, query_emb, store, alpha=0.7)
context = create_rag_context(query, results)

# Generate answer (with your LLM)
prompt = create_rag_prompt(query, context)
answer = llm(prompt)
```

### Pattern 2: Async Batch Processing
```python
pool = WorkerPool(num_workers=8)
pool.start()

# Submit many jobs
job_ids = [pool.submit(process_item, item) for item in items]

# Wait for all
for job_id in job_ids:
    pool.wait_for_job(job_id)

# Collect results
results = [pool.get_job_result(jid) for jid in job_ids]
pool.stop()
```

### Pattern 3: ETL Workflow
```python
workflow = Workflow("etl")

workflow.add_task_from_func("extract", extract_data)
workflow.add_task_from_func("transform", transform_data, dependencies=["extract"])
workflow.add_task_from_func("load", load_data, dependencies=["transform"])

executor = WorkflowExecutor()
executor.execute_sequential(workflow)
```

### Pattern 4: Scheduled Jobs
```python
scheduler = Scheduler()
scheduler.start()

# Run every hour
scheduler.schedule_interval(backup_database, interval=3600)

# Run at specific time (after delay)
scheduler.schedule_once(send_report, delay=calculate_delay())
```

---

## Status Enums

**JobStatus**: PENDING, RUNNING, COMPLETED, FAILED, CANCELLED, RETRYING

**TaskStatus**: PENDING, READY, RUNNING, COMPLETED, FAILED, SKIPPED, CANCELLED

---

## Best Practices

1. **RAG**: Use hybrid search (alpha=0.5-0.7) for best results
2. **Jobs**: Always call `pool.stop()` when done
3. **Workflows**: Validate before executing
4. **Memory**: Use SummaryMemory for long conversations
5. **Rate Limiting**: Apply to external API calls
6. **Monitoring**: Register workflows for debugging

---

**Quick Reference Complete**
