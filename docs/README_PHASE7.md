# FunctionLib - 989 Pure Python Functions 🚀

## Nearly 1000 Functions - Zero Dependencies!

A comprehensive Python function library with **989 functions** across 39 modules, built entirely with the Python standard library (zero external dependencies).

---

## Quick Start

```python
# Vector Search
from functionlib.coding.vector_search import cosine_similarity, knn_search
similarity = cosine_similarity([1, 2, 3], [4, 5, 6])
neighbors = knn_search([0.9, 0.1], [[1, 0], [0, 1]], k=2)

# Stock Analysis
from functionlib.general_purpose.stock_analysis import relative_strength_index, sharpe_ratio
rsi = relative_strength_index([100, 102, 105, 103, 108], period=5)
sharpe = sharpe_ratio([0.01, 0.02, -0.01, 0.03], risk_free_rate=0.02)

# System Automation
from functionlib.coding.system_automation import run_command, get_system_info
result = run_command(['echo', 'Hello'])
info = get_system_info()

# Math & Science
from functionlib.math.optimization import gradient_descent
from functionlib.math.statistics_advanced import t_test_independent
from functionlib.science.physics import projectile_motion
```

---

## Latest - Phase 7 (NEW! ✨)

### Vector Search (25 functions)
- **Similarity metrics**: Cosine, Euclidean, Manhattan, Jaccard, Pearson
- **Search algorithms**: K-NN, nearest neighbors, semantic search
- **Vector database**: In-memory storage with metadata
- **Clustering**: K-means clustering
- **Text vectorization**: TF-IDF, hashing

### Stock Analysis (29 functions)
- **Technical indicators**: SMA, EMA, RSI, MACD, Bollinger Bands, ATR, Stochastic
- **Volume indicators**: OBV, A/D Line, MFI
- **Risk metrics**: Sharpe, Sortino, Calmar, VaR, Expected Shortfall
- **Performance**: Alpha, Beta, Treynor, Information Ratio
- **Portfolio**: Return, variance, Sharpe calculation

### System Automation (29 functions)
- **Commands**: Run shell commands, execute scripts
- **System info**: OS details, CPU count, disk usage
- **File operations**: Read, write, copy, move, find files
- **Process control**: List processes, manage execution
- **Environment**: Get/set environment variables

---

## Complete Module List (39 modules, 989 functions)

### Math (14 modules, 336 functions)
- algebra, calculus, combinatorics, geometry
- linear_algebra, number_theory, numerical_methods
- optimization, probability, random_sampling
- statistics, statistics_advanced, time_series, trigonometry

### Science (6 modules, 159 functions)
- astronomy, biology, chemistry
- electronics, geography, physics

### Coding (11 modules, 260 functions)
- algorithms, cryptography, data_structures
- file_operations, ml_basics, network_utils
- regex_utils, string_operations, text_analysis
- **vector_search** ✨, **system_automation** ✨

### General Purpose (8 modules, 234 functions)
- color_utils, conversion, date_time
- financial, formatting, string_utilities
- validation, **stock_analysis** ✨

---

## Growth Timeline

| Phase | Functions | Modules | Key Additions |
|-------|-----------|---------|---------------|
| 1 | 395 | 14 | Core math, science, coding, utilities |
| 2 | 623 | 24 | Number theory, astronomy, cryptography |
| 3 | 712 | 28 | Combinatorics, text analysis |
| 4 | 784 | 31 | Network utils, geography |
| 5 | 832 | 33 | ML basics, regex utilities |
| 6 | 906 | 36 | Optimization, advanced stats |
| **7** | **989** | **39** | **Vector search, stocks, automation** |

**150% growth from start!** 🎉

---

## Features

✅ **Zero Dependencies** - Pure Python standard library  
✅ **989 Functions** - Comprehensive coverage  
✅ **39 Modules** - Organized by domain  
✅ **Type Hints** - Full type annotations  
✅ **Documented** - Every function has docstrings + examples  
✅ **Tested** - All functions verified working  
✅ **Cross-platform** - Works on Windows, macOS, Linux  
✅ **Production Ready** - Real-world implementations  

---

## Installation

```bash
# Clone repository
git clone <repo-url>
cd functionlib

# Use directly (no dependencies to install!)
python3
>>> from functionlib.math.statistics import mean, standard_deviation
>>> mean([1, 2, 3, 4, 5])
3.0
```

---

## Use Cases

**Data Science & ML**
- Vector operations without NumPy
- Statistical analysis
- Machine learning basics (k-NN, linear regression, k-means)
- Time series analysis

**Finance & Trading**
- Technical analysis (RSI, MACD, Bollinger Bands)
- Risk management (Sharpe, Sortino, VaR)
- Portfolio optimization
- Performance metrics

**System Administration**
- Automation scripts
- File operations
- Process management
- System monitoring

**Scientific Computing**
- Physics simulations
- Chemical calculations
- Astronomical computations
- Geographic calculations

**Development Tools**
- Text processing & NLP
- Cryptography & hashing
- Network utilities
- Data structures & algorithms

---

## Documentation

- **PHASE_7_SUMMARY.md** - Latest additions and examples
- **PHASE_6_SUMMARY.md** - Optimization & advanced statistics
- **COMPREHENSIVE_SUMMARY.md** - Complete overview (Phases 1-5)
- **QUICK_API_REFERENCE.md** - Quick function lookup
- **Individual module files** - Detailed docstrings in each .py file

---

## Examples

### Vector Similarity Search
```python
from functionlib.coding.vector_search import vector_database, semantic_search

# Create database
db = vector_database(
    vectors=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
    metadata=[
        {'title': 'Doc 1', 'category': 'tech'},
        {'title': 'Doc 2', 'category': 'science'},
        {'title': 'Doc 3', 'category': 'art'}
    ]
)

# Search
results = semantic_search([0.9, 0.1, 0.0], db, k=2)
for r in results:
    print(f"{r['metadata']['title']}: {r['score']:.3f}")
```

### Stock Technical Analysis
```python
from functionlib.general_purpose.stock_analysis import (
    relative_strength_index,
    bollinger_bands,
    sharpe_ratio
)

prices = [100, 102, 101, 105, 108, 106, 110, 112]

# RSI
rsi = relative_strength_index(prices, period=5)
print(f"RSI: {rsi[-1]:.1f}")

# Bollinger Bands
upper, middle, lower = bollinger_bands(prices, period=5)
print(f"BB: {lower[-1]:.2f} - {upper[-1]:.2f}")

# Risk metrics
returns = [(prices[i] - prices[i-1])/prices[i-1] for i in range(1, len(prices))]
sharpe = sharpe_ratio(returns, 0.0)
print(f"Sharpe: {sharpe:.2f}")
```

### System Automation
```python
from functionlib.coding.system_automation import (
    find_files,
    get_system_info,
    read_json_file
)

# Find all Python files
py_files = find_files('.', pattern='*.py', recursive=True)
print(f"Found {len(py_files)} Python files")

# System info
info = get_system_info()
print(f"Running on {info['system']} ({info['platform']})")

# JSON operations
config = read_json_file('config.json')
```

---

## Architecture

```
functionlib/
├── __init__.py          # Main package
├── math/                # 336 functions, 14 modules
│   ├── algebra.py
│   ├── calculus.py
│   ├── optimization.py
│   └── ...
├── science/             # 159 functions, 6 modules
│   ├── physics.py
│   ├── chemistry.py
│   └── ...
├── coding/              # 260 functions, 11 modules
│   ├── algorithms.py
│   ├── vector_search.py ✨
│   ├── system_automation.py ✨
│   └── ...
└── general_purpose/     # 234 functions, 8 modules
    ├── date_time.py
    ├── stock_analysis.py ✨
    └── ...
```

---

## Testing

```bash
# Test Phase 7 modules
python3 -c "
from functionlib.coding.vector_search import cosine_similarity
from functionlib.general_purpose.stock_analysis import sharpe_ratio
from functionlib.coding.system_automation import get_system_info

print('✓ vector_search')
print('✓ stock_analysis')
print('✓ system_automation')
"

# Run comprehensive tests
python3 test_functions.py
```

---

## Performance Notes

- **Pure Python**: Slower than NumPy/SciPy but no dependencies
- **Suitable for**: Small to medium datasets, educational use, lightweight applications
- **Not suitable for**: Large-scale production ML (use NumPy/PyTorch instead)
- **Trade-off**: Portability & zero dependencies vs. raw performance

---

## Contributing

This is a reference implementation demonstrating:
- How to build a comprehensive function library
- Pure Python implementations of common algorithms
- Zero-dependency architecture
- Clean code organization

---

## License

[Your License Here]

---

## Stats

- **989 functions** across 39 modules
- **~40,000+ lines** of Python code
- **0 external dependencies**
- **150% growth** from Phase 1
- **11 functions away** from 1000! 🎯

---

*"Nearly 1000 functions, zero dependencies, pure Python power!"* 🚀

**Version 7.0** | Pure Python • Zero Dependencies • Production Ready
