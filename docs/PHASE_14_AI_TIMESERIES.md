# Phase 14: AI Framework Recipes & Time Series Analysis

## Overview

Phase 14 adds **37 new components** for CrewAI-style multi-agent systems, LlamaIndex RAG patterns, and comprehensive time series analysis. Total library now contains **1,307 functions**.

## New Modules

### 1. CrewAI Patterns (`functionlib.coding.crewai_patterns`) - 8 Components

Multi-agent collaboration patterns inspired by CrewAI.

**Core Classes:**
- `Agent` - Agent with role, goal, backstory, and tools
- `CrewTask` - Task with dependencies and priority
- `Crew` - Orchestrates agents and tasks
- `AgentRole` - Enum of common roles (Researcher, Writer, Analyst, etc.)
- `TaskPriority` - Priority levels (LOW, MEDIUM, HIGH, CRITICAL)

**Collaboration Patterns:**
- `MultiAgentCollaboration` - Debate, consensus, peer review patterns

**Templates:**
- `create_research_crew()` - Research → Analysis → Writing pipeline
- `create_development_crew()` - PM → Developer → Tester workflow

#### Example: Research Crew

```python
from functionlib.coding.crewai_patterns import *

# Create agents with roles
researcher = Agent(
    role="Senior Researcher",
    goal="Research machine learning trends",
    backstory="10 years of ML experience"
)

analyst = Agent(
    role="Data Analyst",
    goal="Analyze research findings",
    backstory="Expert at finding patterns"
)

writer = Agent(
    role="Technical Writer",
    goal="Create comprehensive report",
    backstory="Published 50+ technical articles"
)

# Create tasks with dependencies
research_task = CrewTask(
    description="Research latest ML trends",
    expected_output="Research findings document",
    agent=researcher,
    priority=TaskPriority.HIGH
)

analysis_task = CrewTask(
    description="Analyze research findings",
    expected_output="Analysis report",
    agent=analyst
)
analysis_task.add_dependency(research_task)

writing_task = CrewTask(
    description="Write final report",
    expected_output="Final report",
    agent=writer
)
writing_task.add_dependency(analysis_task)

# Create crew and execute
crew = Crew(
    agents=[researcher, analyst, writer],
    tasks=[research_task, analysis_task, writing_task],
    process="sequential"  # or "hierarchical"
)

results = crew.kickoff()
status = crew.get_status()
```

#### Collaboration Patterns

```python
# Agent debate
debate_history = MultiAgentCollaboration.debate(
    topic="Best ML framework",
    agents=[agent1, agent2, agent3],
    rounds=3
)

# Consensus building
consensus = MultiAgentCollaboration.consensus(
    question="What is the priority?",
    agents=[agent1, agent2]
)

# Peer review
review_result = MultiAgentCollaboration.peer_review(
    content="Article to review",
    author=writer,
    reviewers=[reviewer1, reviewer2]
)
```

---

### 2. LlamaIndex Patterns (`functionlib.coding.llamaindex_patterns`) - 12 Components

Advanced RAG patterns compatible with LlamaIndex concepts.

**Document & Index:**
- `Document` - Document with text, metadata, embeddings
- `Node` - Chunk with relationships (prev, next, parent, child)
- `VectorStoreIndex` - Index with similarity search

**Query & Retrieval:**
- `QueryEngine` - Answer questions using index
- `Retriever` - Retrieve relevant nodes
- `SentenceWindowRetriever` - Expand to surrounding context
- `HybridRetriever` - Combine multiple retrievers
- `ContextualCompressionRetriever` - Compress to relevant parts

**Advanced:**
- `ResponseSynthesizer` - Multiple synthesis modes (compact, tree_summarize, refine)
- `SubQuestionQueryEngine` - Break complex queries into sub-questions

**Utilities:**
- `create_document_summary_index()` - Summarize documents
- `create_knowledge_graph()` - Extract entities and relationships

#### Example: Advanced RAG Pipeline

```python
from functionlib.coding.llamaindex_patterns import *

# Create documents
documents = [
    Document("Python is a programming language...", {"source": "wiki"}),
    Document("Python is used for AI...", {"source": "tutorial"}),
    Document("Python has simple syntax...", {"source": "guide"})
]

# Build index
index = VectorStoreIndex.from_documents(
    documents,
    chunk_size=512
)

# Create query engine
query_engine = index.as_query_engine(similarity_top_k=3)

# Query
result = query_engine.query("What is Python used for?")
print(result['response'])
print(f"Sources: {len(result['source_nodes'])}")

# Use advanced retriever
window_retriever = SentenceWindowRetriever(
    index,
    similarity_top_k=3,
    window_size=2  # Expand to ±2 sentences
)

nodes = window_retriever.retrieve("Python syntax")
```

#### Response Synthesis Modes

```python
# Compact: All context in one prompt
synthesizer = ResponseSynthesizer(response_mode="compact")
answer = synthesizer.synthesize(query, nodes)

# Tree summarize: Hierarchical summarization
synthesizer = ResponseSynthesizer(response_mode="tree_summarize")
answer = synthesizer.synthesize(query, nodes)

# Refine: Iteratively refine answer
synthesizer = ResponseSynthesizer(response_mode="refine")
answer = synthesizer.synthesize(query, nodes)
```

#### Sub-Question Engine

```python
# Break complex queries into sub-questions
engines = {
    "tech": tech_query_engine,
    "business": business_query_engine
}

sub_q_engine = SubQuestionQueryEngine(engines)
result = sub_q_engine.query("How does Python impact tech and business?")

print(result['sub_questions'])  # List of generated sub-questions
print(result['sub_answers'])    # Answers to each
print(result['response'])       # Final synthesized answer
```

---

### 3. Time Series Module (`functionlib.math.timeseries`) - 17 Components

Comprehensive time series analysis and forecasting.

**Smoothing & Filtering:**
- `moving_average()` - Simple moving average
- `exponential_smoothing()` - Exponential smoothing
- `double_exponential_smoothing()` - Holt's method with trend

**Analysis:**
- `detect_trend()` - Trend detection with slope
- `detect_seasonality()` - Detect seasonal patterns
- `decompose_time_series()` - Decompose into trend/seasonal/residual
- `autocorrelation()` - Calculate ACF
- `cross_correlation()` - Correlate two series

**Forecasting:**
- `simple_forecast()` - Naive methods (last, mean, drift)
- `linear_regression_forecast()` - Linear trend forecasting
- `holt_winters_forecast()` - Seasonal forecasting
- `arima_forecast()` - Simplified ARIMA

**Utilities:**
- `calculate_forecast_accuracy()` - MAE, MSE, RMSE, MAPE
- `detect_anomalies()` - Standard deviation method
- `detect_change_points()` - Detect structural changes
- `rolling_statistics()` - Rolling mean, std, min, max
- `seasonal_decompose_strength()` - Strength of components

#### Example: Complete Time Series Analysis

```python
from functionlib.math.timeseries import *

# Sample data (monthly sales with trend and seasonality)
data = [100 + 2*i + 20*math.sin(2*math.pi*i/12) for i in range(36)]

# 1. EXPLORATORY ANALYSIS
trend_info = detect_trend(data)
print(f"Trend: {trend_info['trend']}, Slope: {trend_info['slope']:.3f}")

seasonality = detect_seasonality(data, period=12)
print(f"Has seasonality: {seasonality['has_seasonality']}")
print(f"Strength: {seasonality['strength']:.3f}")

# 2. DECOMPOSITION
decomp = decompose_time_series(data, period=12)
trend = decomp['trend']
seasonal = decomp['seasonal']
residual = decomp['residual']

# 3. SMOOTHING
smoothed = exponential_smoothing(data, alpha=0.3)
ma = moving_average(data, window=12)

# 4. FORECASTING
forecast_naive = simple_forecast(data, periods=12, method='drift')
forecast_lr = linear_regression_forecast(data, periods=12)
forecast_hw = holt_winters_forecast(data, periods=12, season_length=12)

# 5. ACCURACY
actual_test = data[-12:]  # Last 12 for testing
predicted = forecast_hw[:12]
metrics = calculate_forecast_accuracy(actual_test, predicted)
print(f"MAE: {metrics['mae']:.2f}")
print(f"RMSE: {metrics['rmse']:.2f}")
print(f"MAPE: {metrics['mape']:.2f}%")

# 6. ANOMALY DETECTION
anomalies = detect_anomalies(data, threshold=3.0)
print(f"Anomalies at indices: {anomalies}")

# 7. ROLLING STATISTICS
rolling = rolling_statistics(data, window=6)
rolling_mean = rolling['mean']
rolling_std = rolling['std']
```

#### Forecasting Methods Comparison

```python
# Compare multiple methods
methods = {
    'Naive (Last)': simple_forecast(data, 12, 'last'),
    'Naive (Drift)': simple_forecast(data, 12, 'drift'),
    'Linear Regression': linear_regression_forecast(data, 12),
    'Holt-Winters': holt_winters_forecast(data, 12, season_length=12),
    'ARIMA(1,1,1)': arima_forecast(data, 12, p=1, d=1, q=1)
}

for name, forecast in methods.items():
    print(f"{name}: {forecast[:3]}")  # First 3 predictions
```

---

## Integration Examples

### CrewAI + LlamaIndex RAG

```python
# Create RAG-powered research crew
from functionlib.coding.crewai_patterns import *
from functionlib.coding.llamaindex_patterns import *

# Build knowledge base
docs = [Document("Info 1"), Document("Info 2")]
index = VectorStoreIndex.from_documents(docs)
query_engine = index.as_query_engine()

# RAG-powered agent
def rag_llm(prompt):
    result = query_engine.query(prompt)
    return result['response']

researcher = Agent(
    role="RAG Researcher",
    goal="Research using knowledge base",
    backstory="Uses RAG for accurate research",
    llm_fn=rag_llm
)

# Execute task with RAG
task = CrewTask(
    description="Research topic X",
    expected_output="Findings",
    agent=researcher
)

result = researcher.execute_task(task)
```

### Time Series + Workflow Engine

```python
from functionlib.math.timeseries import *
from functionlib.coding.workflow_engine import *

# Create forecasting workflow
workflow = Workflow("time-series-pipeline")

def load_data():
    return [100 + 2*i for i in range(36)]

def analyze_data(_dependencies=None):
    data = _dependencies['load']
    return {
        'trend': detect_trend(data),
        'seasonality': detect_seasonality(data, period=12)
    }

def forecast_data(_dependencies=None):
    data = _dependencies['load']
    return holt_winters_forecast(data, 12, season_length=12)

workflow.add_task_from_func("load", load_data)
workflow.add_task_from_func("analyze", analyze_data, dependencies=["load"])
workflow.add_task_from_func("forecast", forecast_data, dependencies=["load"])

executor = WorkflowExecutor()
executor.execute_parallel(workflow)
```

---

## Key Features

✅ **Multi-agent orchestration** - CrewAI-style collaboration  
✅ **Advanced RAG** - LlamaIndex-compatible patterns  
✅ **Time series forecasting** - Multiple methods (Holt-Winters, ARIMA)  
✅ **Pure Python stdlib** - No external dependencies  
✅ **Production-ready** - Error handling, validation  
✅ **Well-tested** - All components verified  

## Performance Notes

- **CrewAI crews**: Sequential O(n), hierarchical with routing overhead
- **LlamaIndex retrieval**: O(n) vector search, O(log n) with proper indexing
- **Time series decomposition**: O(n) for STL decomposition
- **Forecasting**: Holt-Winters O(n), ARIMA O(n²) for parameter estimation

## Dependencies (Optional)

For production use, consider:
- `crewai` - Full CrewAI features
- `llama-index` - Full LlamaIndex integration
- `langchain` - Additional LangChain features
- `statsmodels` - Advanced time series (SARIMAX, VAR)
- `prophet` - Facebook Prophet forecasting
- `pmdarima` - Auto-ARIMA
- `scikit-learn` - ML-based forecasting

## Phase 14 Statistics

**New Components:** 37
- CrewAI patterns: 8
- LlamaIndex patterns: 12
- Time series: 17

**Total Functions:** 1,307 (+37 from Phase 13)
- Math: 353 (+17)
- Science: 159
- Coding: 561 (+20)
- General Purpose: 234

**Growth:** +2.9% in one phase

---

## What's Next?

Potential Phase 15:
- [ ] Distributed computing patterns
- [ ] Real-time streaming analysis
- [ ] Advanced NLP (transformers, embeddings)
- [ ] Computer vision basics
- [ ] MLOps utilities (model versioning, A/B testing)
- [ ] Data validation & quality checks

---

**Phase 14 Complete: +37 components, 1,307 total functions** 🚀
