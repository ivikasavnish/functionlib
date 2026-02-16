"""
Data Analysis Functions

Tabular data analysis with stdlib (CSV/dict) and optional pandas support.
Works with pure Python data structures - pandas functions gracefully degrade if not installed.
"""

from typing import List, Dict, Any, Optional, Tuple, Callable
import csv
import io
import statistics
import operator

__all__ = [
    # Data Loading (stdlib)
    'load_csv_as_dicts', 'load_csv_as_lists', 'save_dicts_to_csv',
    
    # Basic Analysis
    'describe_numeric_column', 'describe_dataset', 'count_unique', 'value_counts',
    'group_by', 'aggregate_by_group',
    
    # Filtering & Selection
    'filter_rows', 'select_columns', 'sort_by_column', 'top_n', 'sample_rows',
    
    # Transformations
    'add_calculated_column', 'rename_columns', 'drop_columns', 'fill_missing',
    'pivot_table', 'unpivot',
    
    # Statistical Analysis
    'correlation_pearson', 'covariance', 'percentile', 'quartiles',
    'detect_outliers', 'normalize_column', 'standardize_column',
    
    # Data Quality
    'count_missing', 'find_duplicates', 'drop_duplicates',
    'validate_schema', 'infer_column_types',
    
    # Pandas Helpers (optional - work if pandas installed)
    'to_pandas_dataframe', 'from_pandas_dataframe', 'has_pandas'
]

# ============================================================================
# PANDAS AVAILABILITY CHECK
# ============================================================================

def has_pandas() -> bool:
    """
    Check if pandas is available.
    
    Returns:
        True if pandas is installed
        
    Example:
        >>> available = has_pandas()
        >>> isinstance(available, bool)
        True
    """
    try:
        import pandas
        return True
    except ImportError:
        return False


# ============================================================================
# DATA LOADING (STDLIB)
# ============================================================================

def load_csv_as_dicts(csv_data: str, delimiter: str = ',') -> List[Dict[str, str]]:
    """
    Load CSV data as list of dictionaries.
    
    Args:
        csv_data: CSV string data
        delimiter: Field delimiter
        
    Returns:
        List of row dictionaries
        
    Example:
        >>> data = "name,age\\nJohn,30\\nJane,25"
        >>> rows = load_csv_as_dicts(data)
        >>> rows[0]['name']
        'John'
    """
    reader = csv.DictReader(io.StringIO(csv_data), delimiter=delimiter)
    return list(reader)


def load_csv_as_lists(csv_data: str, delimiter: str = ',',
                      has_header: bool = True) -> Tuple[Optional[List[str]], List[List[str]]]:
    """
    Load CSV data as lists.
    
    Args:
        csv_data: CSV string data
        delimiter: Field delimiter
        has_header: Whether first row is header
        
    Returns:
        Tuple of (headers, data_rows)
        
    Example:
        >>> data = "name,age\\nJohn,30\\nJane,25"
        >>> headers, rows = load_csv_as_lists(data)
        >>> headers
        ['name', 'age']
    """
    reader = csv.reader(io.StringIO(csv_data), delimiter=delimiter)
    rows = list(reader)
    
    if has_header and rows:
        return rows[0], rows[1:]
    return None, rows


def save_dicts_to_csv(data: List[Dict[str, Any]], delimiter: str = ',') -> str:
    """
    Save list of dictionaries to CSV string.
    
    Args:
        data: List of dictionaries
        delimiter: Field delimiter
        
    Returns:
        CSV string
        
    Example:
        >>> data = [{'name': 'John', 'age': 30}]
        >>> csv_str = save_dicts_to_csv(data)
        >>> 'John' in csv_str
        True
    """
    if not data:
        return ""
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys(), delimiter=delimiter)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


# ============================================================================
# BASIC ANALYSIS
# ============================================================================

def describe_numeric_column(data: List[Dict[str, Any]], column: str) -> Dict[str, float]:
    """
    Get descriptive statistics for a numeric column.
    
    Args:
        data: List of row dictionaries
        column: Column name
        
    Returns:
        Dictionary of statistics
        
    Example:
        >>> data = [{'val': 10}, {'val': 20}, {'val': 30}]
        >>> stats = describe_numeric_column(data, 'val')
        >>> stats['mean']
        20.0
    """
    values = [float(row[column]) for row in data if column in row and row[column] != '']
    
    if not values:
        return {}
    
    values.sort()
    return {
        'count': len(values),
        'mean': statistics.mean(values),
        'median': statistics.median(values),
        'std': statistics.stdev(values) if len(values) > 1 else 0.0,
        'min': min(values),
        'max': max(values),
        'q25': statistics.quantiles(values, n=4)[0] if len(values) >= 4 else values[0],
        'q75': statistics.quantiles(values, n=4)[2] if len(values) >= 4 else values[-1]
    }


def describe_dataset(data: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """
    Get descriptive statistics for all numeric columns in dataset.
    
    Args:
        data: List of row dictionaries
        
    Returns:
        Dictionary of column: statistics
        
    Example:
        >>> data = [{'a': 10, 'b': 'x'}, {'a': 20, 'b': 'y'}]
        >>> desc = describe_dataset(data)
        >>> 'a' in desc
        True
    """
    if not data:
        return {}
    
    columns = list(data[0].keys())
    result = {}
    
    for col in columns:
        try:
            stats = describe_numeric_column(data, col)
            if stats:
                result[col] = stats
        except (ValueError, TypeError):
            # Non-numeric column
            pass
    
    return result


def count_unique(data: List[Dict[str, Any]], column: str) -> int:
    """
    Count unique values in a column.
    
    Args:
        data: List of row dictionaries
        column: Column name
        
    Returns:
        Number of unique values
        
    Example:
        >>> data = [{'color': 'red'}, {'color': 'blue'}, {'color': 'red'}]
        >>> count_unique(data, 'color')
        2
    """
    values = set(row[column] for row in data if column in row)
    return len(values)


def value_counts(data: List[Dict[str, Any]], column: str) -> Dict[Any, int]:
    """
    Count occurrences of each value in a column.
    
    Args:
        data: List of row dictionaries
        column: Column name
        
    Returns:
        Dictionary of value: count
        
    Example:
        >>> data = [{'color': 'red'}, {'color': 'blue'}, {'color': 'red'}]
        >>> counts = value_counts(data, 'color')
        >>> counts['red']
        2
    """
    counts = {}
    for row in data:
        if column in row:
            value = row[column]
            counts[value] = counts.get(value, 0) + 1
    return counts


def group_by(data: List[Dict[str, Any]], column: str) -> Dict[Any, List[Dict[str, Any]]]:
    """
    Group rows by column value.
    
    Args:
        data: List of row dictionaries
        column: Column to group by
        
    Returns:
        Dictionary of value: rows
        
    Example:
        >>> data = [{'dept': 'IT', 'sal': 100}, {'dept': 'HR', 'sal': 90}]
        >>> groups = group_by(data, 'dept')
        >>> len(groups['IT'])
        1
    """
    groups = {}
    for row in data:
        if column in row:
            key = row[column]
            if key not in groups:
                groups[key] = []
            groups[key].append(row)
    return groups


def aggregate_by_group(data: List[Dict[str, Any]], group_column: str,
                       agg_column: str, func: str = 'mean') -> Dict[Any, float]:
    """
    Aggregate numeric column by groups.
    
    Args:
        data: List of row dictionaries
        group_column: Column to group by
        agg_column: Column to aggregate
        func: Aggregation function ('mean', 'sum', 'min', 'max', 'count')
        
    Returns:
        Dictionary of group_value: aggregated_value
        
    Example:
        >>> data = [{'dept': 'IT', 'sal': 100}, {'dept': 'IT', 'sal': 120}]
        >>> agg = aggregate_by_group(data, 'dept', 'sal', 'mean')
        >>> agg['IT']
        110.0
    """
    groups = group_by(data, group_column)
    result = {}
    
    for key, rows in groups.items():
        values = [float(row[agg_column]) for row in rows if agg_column in row]
        
        if not values:
            continue
        
        if func == 'mean':
            result[key] = statistics.mean(values)
        elif func == 'sum':
            result[key] = sum(values)
        elif func == 'min':
            result[key] = min(values)
        elif func == 'max':
            result[key] = max(values)
        elif func == 'count':
            result[key] = len(values)
    
    return result


# ============================================================================
# FILTERING & SELECTION
# ============================================================================

def filter_rows(data: List[Dict[str, Any]], 
                condition: Callable[[Dict[str, Any]], bool]) -> List[Dict[str, Any]]:
    """
    Filter rows based on condition function.
    
    Args:
        data: List of row dictionaries
        condition: Function that returns True for rows to keep
        
    Returns:
        Filtered list of rows
        
    Example:
        >>> data = [{'age': 25}, {'age': 35}, {'age': 45}]
        >>> filtered = filter_rows(data, lambda r: r['age'] > 30)
        >>> len(filtered)
        2
    """
    return [row for row in data if condition(row)]


def select_columns(data: List[Dict[str, Any]], columns: List[str]) -> List[Dict[str, Any]]:
    """
    Select specific columns from dataset.
    
    Args:
        data: List of row dictionaries
        columns: List of column names to keep
        
    Returns:
        List of rows with only selected columns
        
    Example:
        >>> data = [{'a': 1, 'b': 2, 'c': 3}]
        >>> selected = select_columns(data, ['a', 'c'])
        >>> list(selected[0].keys())
        ['a', 'c']
    """
    return [{col: row[col] for col in columns if col in row} for row in data]


def sort_by_column(data: List[Dict[str, Any]], column: str, 
                   reverse: bool = False) -> List[Dict[str, Any]]:
    """
    Sort rows by column value.
    
    Args:
        data: List of row dictionaries
        column: Column to sort by
        reverse: Sort in descending order
        
    Returns:
        Sorted list of rows
        
    Example:
        >>> data = [{'age': 35}, {'age': 25}, {'age': 45}]
        >>> sorted_data = sort_by_column(data, 'age')
        >>> sorted_data[0]['age']
        25
    """
    return sorted(data, key=lambda row: row.get(column, 0), reverse=reverse)


def top_n(data: List[Dict[str, Any]], column: str, n: int = 10) -> List[Dict[str, Any]]:
    """
    Get top N rows by column value.
    
    Args:
        data: List of row dictionaries
        column: Column to sort by
        n: Number of rows to return
        
    Returns:
        Top N rows
        
    Example:
        >>> data = [{'score': 85}, {'score': 95}, {'score': 75}]
        >>> top = top_n(data, 'score', 2)
        >>> top[0]['score']
        95
    """
    sorted_data = sort_by_column(data, column, reverse=True)
    return sorted_data[:n]


def sample_rows(data: List[Dict[str, Any]], n: int, seed: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Get random sample of rows.
    
    Args:
        data: List of row dictionaries
        n: Number of rows to sample
        seed: Random seed for reproducibility
        
    Returns:
        Sample of rows
        
    Example:
        >>> data = [{'id': i} for i in range(100)]
        >>> sample = sample_rows(data, 5, seed=42)
        >>> len(sample)
        5
    """
    import random
    if seed is not None:
        random.seed(seed)
    return random.sample(data, min(n, len(data)))


# ============================================================================
# TRANSFORMATIONS
# ============================================================================

def add_calculated_column(data: List[Dict[str, Any]], new_column: str,
                          func: Callable[[Dict[str, Any]], Any]) -> List[Dict[str, Any]]:
    """
    Add a new column based on calculation.
    
    Args:
        data: List of row dictionaries
        new_column: Name of new column
        func: Function that takes row dict and returns new value
        
    Returns:
        List with new column added
        
    Example:
        >>> data = [{'price': 100, 'qty': 2}]
        >>> result = add_calculated_column(data, 'total', lambda r: r['price'] * r['qty'])
        >>> result[0]['total']
        200
    """
    result = []
    for row in data:
        new_row = row.copy()
        new_row[new_column] = func(row)
        result.append(new_row)
    return result


def rename_columns(data: List[Dict[str, Any]], 
                   mapping: Dict[str, str]) -> List[Dict[str, Any]]:
    """
    Rename columns in dataset.
    
    Args:
        data: List of row dictionaries
        mapping: Dictionary of old_name: new_name
        
    Returns:
        List with renamed columns
        
    Example:
        >>> data = [{'old_name': 'value'}]
        >>> renamed = rename_columns(data, {'old_name': 'new_name'})
        >>> 'new_name' in renamed[0]
        True
    """
    result = []
    for row in data:
        new_row = {}
        for key, value in row.items():
            new_key = mapping.get(key, key)
            new_row[new_key] = value
        result.append(new_row)
    return result


def drop_columns(data: List[Dict[str, Any]], columns: List[str]) -> List[Dict[str, Any]]:
    """
    Remove columns from dataset.
    
    Args:
        data: List of row dictionaries
        columns: List of column names to remove
        
    Returns:
        List with columns removed
        
    Example:
        >>> data = [{'a': 1, 'b': 2, 'c': 3}]
        >>> result = drop_columns(data, ['b'])
        >>> 'b' not in result[0]
        True
    """
    return [{k: v for k, v in row.items() if k not in columns} for row in data]


def fill_missing(data: List[Dict[str, Any]], column: str, 
                 fill_value: Any) -> List[Dict[str, Any]]:
    """
    Fill missing values in a column.
    
    Args:
        data: List of row dictionaries
        column: Column name
        fill_value: Value to use for missing entries
        
    Returns:
        List with missing values filled
        
    Example:
        >>> data = [{'val': 10}, {'val': None}, {'val': 20}]
        >>> filled = fill_missing(data, 'val', 0)
        >>> filled[1]['val']
        0
    """
    result = []
    for row in data:
        new_row = row.copy()
        if column not in new_row or new_row[column] is None or new_row[column] == '':
            new_row[column] = fill_value
        result.append(new_row)
    return result


def pivot_table(data: List[Dict[str, Any]], index: str, columns: str,
                values: str, aggfunc: str = 'mean') -> Dict[Any, Dict[Any, float]]:
    """
    Create pivot table.
    
    Args:
        data: List of row dictionaries
        index: Column to use as row index
        columns: Column to use as columns
        values: Column to aggregate
        aggfunc: Aggregation function ('mean', 'sum', 'count')
        
    Returns:
        Nested dictionary {index_value: {column_value: aggregated_value}}
        
    Example:
        >>> data = [{'dept': 'IT', 'year': 2020, 'sal': 100}]
        >>> pivot = pivot_table(data, 'dept', 'year', 'sal', 'sum')
        >>> pivot['IT'][2020]
        100
    """
    result = {}
    
    for row in data:
        idx_val = row[index]
        col_val = row[columns]
        agg_val = float(row[values])
        
        if idx_val not in result:
            result[idx_val] = {}
        if col_val not in result[idx_val]:
            result[idx_val][col_val] = []
        
        result[idx_val][col_val].append(agg_val)
    
    # Apply aggregation
    for idx_val in result:
        for col_val in result[idx_val]:
            values_list = result[idx_val][col_val]
            if aggfunc == 'mean':
                result[idx_val][col_val] = statistics.mean(values_list)
            elif aggfunc == 'sum':
                result[idx_val][col_val] = sum(values_list)
            elif aggfunc == 'count':
                result[idx_val][col_val] = len(values_list)
    
    return result


def unpivot(data: List[Dict[str, Any]], id_vars: List[str], 
            value_vars: List[str]) -> List[Dict[str, Any]]:
    """
    Unpivot (melt) dataset from wide to long format.
    
    Args:
        data: List of row dictionaries
        id_vars: Columns to keep as identifiers
        value_vars: Columns to unpivot
        
    Returns:
        List in long format
        
    Example:
        >>> data = [{'id': 1, 'q1': 10, 'q2': 20}]
        >>> long = unpivot(data, ['id'], ['q1', 'q2'])
        >>> len(long)
        2
    """
    result = []
    for row in data:
        for var in value_vars:
            new_row = {col: row[col] for col in id_vars if col in row}
            new_row['variable'] = var
            new_row['value'] = row.get(var)
            result.append(new_row)
    return result


# ============================================================================
# STATISTICAL ANALYSIS
# ============================================================================

def correlation_pearson(data: List[Dict[str, Any]], col1: str, col2: str) -> float:
    """
    Calculate Pearson correlation between two columns.
    
    Args:
        data: List of row dictionaries
        col1: First column name
        col2: Second column name
        
    Returns:
        Correlation coefficient (-1 to 1)
        
    Example:
        >>> data = [{'x': 1, 'y': 2}, {'x': 2, 'y': 4}, {'x': 3, 'y': 6}]
        >>> corr = correlation_pearson(data, 'x', 'y')
        >>> abs(corr - 1.0) < 0.01
        True
    """
    pairs = [(float(row[col1]), float(row[col2])) 
             for row in data if col1 in row and col2 in row]
    
    if len(pairs) < 2:
        return 0.0
    
    x_vals, y_vals = zip(*pairs)
    return statistics.correlation(x_vals, y_vals)


def covariance(data: List[Dict[str, Any]], col1: str, col2: str) -> float:
    """
    Calculate covariance between two columns.
    
    Args:
        data: List of row dictionaries
        col1: First column name
        col2: Second column name
        
    Returns:
        Covariance value
        
    Example:
        >>> data = [{'x': 1, 'y': 2}, {'x': 2, 'y': 4}]
        >>> cov = covariance(data, 'x', 'y')
        >>> cov > 0
        True
    """
    pairs = [(float(row[col1]), float(row[col2])) 
             for row in data if col1 in row and col2 in row]
    
    if len(pairs) < 2:
        return 0.0
    
    x_vals, y_vals = zip(*pairs)
    return statistics.covariance(x_vals, y_vals)


def percentile(data: List[Dict[str, Any]], column: str, p: float) -> float:
    """
    Calculate percentile of a column.
    
    Args:
        data: List of row dictionaries
        column: Column name
        p: Percentile (0-100)
        
    Returns:
        Percentile value
        
    Example:
        >>> data = [{'val': i} for i in range(101)]
        >>> p50 = percentile(data, 'val', 50)
        >>> abs(p50 - 50) < 1
        True
    """
    values = sorted([float(row[column]) for row in data if column in row])
    if not values:
        return 0.0
    
    k = (len(values) - 1) * (p / 100.0)
    f = int(k)
    c = min(f + 1, len(values) - 1)
    
    if f == c:
        return values[f]
    
    return values[f] + (k - f) * (values[c] - values[f])


def quartiles(data: List[Dict[str, Any]], column: str) -> Tuple[float, float, float]:
    """
    Calculate quartiles (Q1, Q2, Q3) of a column.
    
    Args:
        data: List of row dictionaries
        column: Column name
        
    Returns:
        Tuple of (Q1, Q2, Q3)
        
    Example:
        >>> data = [{'val': i} for i in range(101)]
        >>> q1, q2, q3 = quartiles(data, 'val')
        >>> 20 < q1 < 30 and 45 < q2 < 55 and 70 < q3 < 80
        True
    """
    values = sorted([float(row[column]) for row in data if column in row])
    if len(values) < 4:
        return (values[0], values[len(values)//2], values[-1])
    
    qs = statistics.quantiles(values, n=4)
    return (qs[0], qs[1], qs[2])


def detect_outliers(data: List[Dict[str, Any]], column: str, 
                    method: str = 'iqr') -> List[Dict[str, Any]]:
    """
    Detect outliers in a column.
    
    Args:
        data: List of row dictionaries
        column: Column name
        method: Detection method ('iqr' or 'zscore')
        
    Returns:
        List of rows that are outliers
        
    Example:
        >>> data = [{'val': i} for i in range(10)] + [{'val': 1000}]
        >>> outliers = detect_outliers(data, 'val', 'iqr')
        >>> len(outliers) > 0
        True
    """
    if method == 'iqr':
        q1, q2, q3 = quartiles(data, column)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        return [row for row in data if float(row[column]) < lower or float(row[column]) > upper]
    elif method == 'zscore':
        values = [float(row[column]) for row in data if column in row]
        mean_val = statistics.mean(values)
        std_val = statistics.stdev(values) if len(values) > 1 else 1
        return [row for row in data 
                if abs(float(row[column]) - mean_val) / std_val > 3]
    return []


def normalize_column(data: List[Dict[str, Any]], column: str) -> List[Dict[str, Any]]:
    """
    Normalize column to 0-1 range (min-max scaling).
    
    Args:
        data: List of row dictionaries
        column: Column to normalize
        
    Returns:
        List with normalized column
        
    Example:
        >>> data = [{'val': 10}, {'val': 20}, {'val': 30}]
        >>> normalized = normalize_column(data, 'val')
        >>> normalized[0]['val']
        0.0
    """
    values = [float(row[column]) for row in data if column in row]
    min_val = min(values)
    max_val = max(values)
    range_val = max_val - min_val if max_val != min_val else 1
    
    result = []
    for row in data:
        new_row = row.copy()
        if column in new_row:
            new_row[column] = (float(row[column]) - min_val) / range_val
        result.append(new_row)
    return result


def standardize_column(data: List[Dict[str, Any]], column: str) -> List[Dict[str, Any]]:
    """
    Standardize column (z-score normalization).
    
    Args:
        data: List of row dictionaries
        column: Column to standardize
        
    Returns:
        List with standardized column
        
    Example:
        >>> data = [{'val': 10}, {'val': 20}, {'val': 30}]
        >>> standardized = standardize_column(data, 'val')
        >>> abs(standardized[1]['val']) < 0.1
        True
    """
    values = [float(row[column]) for row in data if column in row]
    mean_val = statistics.mean(values)
    std_val = statistics.stdev(values) if len(values) > 1 else 1
    
    result = []
    for row in data:
        new_row = row.copy()
        if column in new_row:
            new_row[column] = (float(row[column]) - mean_val) / std_val
        result.append(new_row)
    return result


# ============================================================================
# DATA QUALITY
# ============================================================================

def count_missing(data: List[Dict[str, Any]]) -> Dict[str, int]:
    """
    Count missing values per column.
    
    Args:
        data: List of row dictionaries
        
    Returns:
        Dictionary of column: missing_count
        
    Example:
        >>> data = [{'a': 1, 'b': None}, {'a': 2, 'b': 3}]
        >>> missing = count_missing(data)
        >>> missing['b']
        1
    """
    if not data:
        return {}
    
    columns = set()
    for row in data:
        columns.update(row.keys())
    
    missing = {col: 0 for col in columns}
    for row in data:
        for col in columns:
            if col not in row or row[col] is None or row[col] == '':
                missing[col] += 1
    
    return missing


def find_duplicates(data: List[Dict[str, Any]], 
                    columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Find duplicate rows.
    
    Args:
        data: List of row dictionaries
        columns: Columns to check for duplicates (None = all)
        
    Returns:
        List of duplicate rows
        
    Example:
        >>> data = [{'a': 1, 'b': 2}, {'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
        >>> dups = find_duplicates(data)
        >>> len(dups)
        1
    """
    seen = set()
    duplicates = []
    
    for row in data:
        if columns:
            key = tuple(row.get(col) for col in columns)
        else:
            key = tuple(sorted(row.items()))
        
        if key in seen:
            duplicates.append(row)
        else:
            seen.add(key)
    
    return duplicates


def drop_duplicates(data: List[Dict[str, Any]], 
                    columns: Optional[List[str]] = None) -> List[Dict[str, Any]]:
    """
    Remove duplicate rows.
    
    Args:
        data: List of row dictionaries
        columns: Columns to check for duplicates (None = all)
        
    Returns:
        List without duplicates
        
    Example:
        >>> data = [{'a': 1, 'b': 2}, {'a': 1, 'b': 2}, {'a': 3, 'b': 4}]
        >>> unique = drop_duplicates(data)
        >>> len(unique)
        2
    """
    seen = set()
    result = []
    
    for row in data:
        if columns:
            key = tuple(row.get(col) for col in columns)
        else:
            key = tuple(sorted(row.items()))
        
        if key not in seen:
            seen.add(key)
            result.append(row)
    
    return result


def validate_schema(data: List[Dict[str, Any]], 
                    expected_columns: List[str]) -> Dict[str, Any]:
    """
    Validate dataset schema.
    
    Args:
        data: List of row dictionaries
        expected_columns: List of expected column names
        
    Returns:
        Dictionary with validation results
        
    Example:
        >>> data = [{'a': 1, 'b': 2}]
        >>> result = validate_schema(data, ['a', 'b'])
        >>> result['valid']
        True
    """
    if not data:
        return {'valid': False, 'reason': 'Empty dataset'}
    
    actual_columns = set(data[0].keys())
    expected_set = set(expected_columns)
    
    missing = expected_set - actual_columns
    extra = actual_columns - expected_set
    
    return {
        'valid': len(missing) == 0,
        'missing_columns': list(missing),
        'extra_columns': list(extra)
    }


def infer_column_types(data: List[Dict[str, Any]]) -> Dict[str, str]:
    """
    Infer data types of columns.
    
    Args:
        data: List of row dictionaries
        
    Returns:
        Dictionary of column: inferred_type
        
    Example:
        >>> data = [{'a': '123', 'b': 'text', 'c': '12.5'}]
        >>> types = infer_column_types(data)
        >>> types['a']
        'integer'
    """
    if not data:
        return {}
    
    columns = list(data[0].keys())
    types = {}
    
    for col in columns:
        values = [row[col] for row in data if col in row and row[col] not in [None, '']]
        
        if not values:
            types[col] = 'empty'
            continue
        
        # Try to infer type
        is_int = all(str(v).replace('-', '').isdigit() for v in values)
        is_float = all(str(v).replace('.', '').replace('-', '').isdigit() for v in values)
        
        if is_int:
            types[col] = 'integer'
        elif is_float:
            types[col] = 'float'
        else:
            types[col] = 'string'
    
    return types


# ============================================================================
# PANDAS HELPERS (OPTIONAL)
# ============================================================================

def to_pandas_dataframe(data: List[Dict[str, Any]]) -> Any:
    """
    Convert list of dicts to pandas DataFrame (if pandas available).
    
    Args:
        data: List of row dictionaries
        
    Returns:
        pandas DataFrame or None if pandas not available
        
    Example:
        >>> data = [{'a': 1, 'b': 2}]
        >>> df = to_pandas_dataframe(data)
        >>> df is None or len(df) == 1
        True
    """
    try:
        import pandas as pd
        return pd.DataFrame(data)
    except ImportError:
        return None


def from_pandas_dataframe(df: Any) -> List[Dict[str, Any]]:
    """
    Convert pandas DataFrame to list of dicts.
    
    Args:
        df: pandas DataFrame
        
    Returns:
        List of row dictionaries
        
    Example:
        >>> # Requires pandas to be installed
        >>> data = [{'a': 1, 'b': 2}]
        >>> isinstance(data, list)
        True
    """
    try:
        return df.to_dict('records')
    except (AttributeError, TypeError):
        return []
