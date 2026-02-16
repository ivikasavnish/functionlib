"""
Statistics Functions

Statistical calculations including descriptive statistics, distributions, and hypothesis testing.
"""

import math
from typing import List, Tuple, Optional


def mean(data: List[float]) -> float:
    """
    Calculates arithmetic mean (average)
    
    Args:
        data: List of numbers
        
    Returns:
        Mean value
        
    Example:
        >>> mean([1, 2, 3, 4, 5])
        3.0
    """
    if not data:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(data) / len(data)


def median(data: List[float]) -> float:
    """
    Calculates median (middle value)
    
    Args:
        data: List of numbers
        
    Returns:
        Median value
        
    Example:
        >>> median([1, 2, 3, 4, 5])
        3.0
    """
    if not data:
        raise ValueError("Cannot calculate median of empty list")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    mid = n // 2
    
    if n % 2 == 0:
        return (sorted_data[mid - 1] + sorted_data[mid]) / 2
    return sorted_data[mid]


def mode(data: List[float]) -> List[float]:
    """
    Finds mode (most frequent value(s))
    
    Args:
        data: List of numbers
        
    Returns:
        List of mode values (may be multiple if tied)
        
    Example:
        >>> mode([1, 2, 2, 3, 3, 3, 4])
        [3.0]
    """
    if not data:
        raise ValueError("Cannot calculate mode of empty list")
    
    frequency = {}
    for value in data:
        frequency[value] = frequency.get(value, 0) + 1
    
    max_freq = max(frequency.values())
    modes = [k for k, v in frequency.items() if v == max_freq]
    
    return modes


def variance(data: List[float], sample: bool = True) -> float:
    """
    Calculates variance
    
    Args:
        data: List of numbers
        sample: If True, uses sample variance (n-1); otherwise population variance (n)
        
    Returns:
        Variance
        
    Example:
        >>> variance([1, 2, 3, 4, 5])
        2.5
    """
    if not data:
        raise ValueError("Cannot calculate variance of empty list")
    if sample and len(data) < 2:
        raise ValueError("Sample variance requires at least 2 data points")
    
    mu = mean(data)
    squared_diffs = [(x - mu) ** 2 for x in data]
    divisor = len(data) - 1 if sample else len(data)
    
    return sum(squared_diffs) / divisor


def standard_deviation(data: List[float], sample: bool = True) -> float:
    """
    Calculates standard deviation
    
    Args:
        data: List of numbers
        sample: If True, uses sample std dev; otherwise population std dev
        
    Returns:
        Standard deviation
        
    Example:
        >>> standard_deviation([1, 2, 3, 4, 5])
        1.5811388300841898
    """
    return math.sqrt(variance(data, sample))


def range_stat(data: List[float]) -> float:
    """
    Calculates range (max - min)
    
    Args:
        data: List of numbers
        
    Returns:
        Range
        
    Example:
        >>> range_stat([1, 2, 3, 4, 5])
        4.0
    """
    if not data:
        raise ValueError("Cannot calculate range of empty list")
    return max(data) - min(data)


def quartiles(data: List[float]) -> Tuple[float, float, float]:
    """
    Calculates quartiles (Q1, Q2, Q3)
    
    Args:
        data: List of numbers
        
    Returns:
        Tuple of (Q1, Q2, Q3)
        
    Example:
        >>> quartiles([1, 2, 3, 4, 5, 6, 7, 8, 9])
        (2.5, 5.0, 7.5)
    """
    if not data:
        raise ValueError("Cannot calculate quartiles of empty list")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    q2 = median(sorted_data)
    
    mid = n // 2
    if n % 2 == 0:
        lower_half = sorted_data[:mid]
        upper_half = sorted_data[mid:]
    else:
        lower_half = sorted_data[:mid]
        upper_half = sorted_data[mid + 1:]
    
    q1 = median(lower_half)
    q3 = median(upper_half)
    
    return (q1, q2, q3)


def interquartile_range(data: List[float]) -> float:
    """
    Calculates interquartile range (IQR = Q3 - Q1)
    
    Args:
        data: List of numbers
        
    Returns:
        IQR
        
    Example:
        >>> interquartile_range([1, 2, 3, 4, 5, 6, 7, 8, 9])
        5.0
    """
    q1, _, q3 = quartiles(data)
    return q3 - q1


def percentile(data: List[float], p: float) -> float:
    """
    Calculates percentile value
    
    Args:
        data: List of numbers
        p: Percentile (0-100)
        
    Returns:
        Value at pth percentile
        
    Example:
        >>> percentile([1, 2, 3, 4, 5], 50)
        3.0
    """
    if not 0 <= p <= 100:
        raise ValueError("Percentile must be between 0 and 100")
    
    sorted_data = sorted(data)
    n = len(sorted_data)
    
    k = (n - 1) * p / 100
    f = math.floor(k)
    c = math.ceil(k)
    
    if f == c:
        return sorted_data[int(k)]
    
    d0 = sorted_data[int(f)]
    d1 = sorted_data[int(c)]
    
    return d0 + (d1 - d0) * (k - f)


def z_score(value: float, data: List[float]) -> float:
    """
    Calculates z-score (standard score)
    
    Args:
        value: Value to calculate z-score for
        data: Dataset
        
    Returns:
        Z-score: (value - mean) / std_dev
        
    Example:
        >>> z_score(5, [1, 2, 3, 4, 5])
        1.2649110640673518
    """
    mu = mean(data)
    sigma = standard_deviation(data)
    
    if sigma == 0:
        raise ValueError("Standard deviation is zero")
    
    return (value - mu) / sigma


def covariance(x: List[float], y: List[float], sample: bool = True) -> float:
    """
    Calculates covariance between two datasets
    
    Args:
        x: First dataset
        y: Second dataset
        sample: If True, uses sample covariance
        
    Returns:
        Covariance
        
    Example:
        >>> covariance([1, 2, 3], [2, 4, 6])
        2.0
    """
    if len(x) != len(y):
        raise ValueError("Datasets must have same length")
    if not x:
        raise ValueError("Datasets cannot be empty")
    
    mean_x = mean(x)
    mean_y = mean(y)
    
    cov = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    divisor = len(x) - 1 if sample else len(x)
    
    return cov / divisor


def correlation_coefficient(x: List[float], y: List[float]) -> float:
    """
    Calculates Pearson correlation coefficient
    
    Args:
        x: First dataset
        y: Second dataset
        
    Returns:
        Correlation coefficient (-1 to 1)
        
    Example:
        >>> correlation_coefficient([1, 2, 3], [2, 4, 6])
        1.0
    """
    if len(x) != len(y):
        raise ValueError("Datasets must have same length")
    
    cov = covariance(x, y, sample=True)
    std_x = standard_deviation(x, sample=True)
    std_y = standard_deviation(y, sample=True)
    
    if std_x == 0 or std_y == 0:
        raise ValueError("Standard deviation cannot be zero")
    
    return cov / (std_x * std_y)


def linear_regression(x: List[float], y: List[float]) -> Tuple[float, float]:
    """
    Performs simple linear regression: y = mx + b
    
    Args:
        x: Independent variable data
        y: Dependent variable data
        
    Returns:
        Tuple of (slope m, intercept b)
        
    Example:
        >>> linear_regression([1, 2, 3], [2, 4, 6])
        (2.0, 0.0)
    """
    if len(x) != len(y):
        raise ValueError("Datasets must have same length")
    if len(x) < 2:
        raise ValueError("Need at least 2 data points")
    
    n = len(x)
    mean_x = mean(x)
    mean_y = mean(y)
    
    numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
    denominator = sum((xi - mean_x) ** 2 for xi in x)
    
    if denominator == 0:
        raise ValueError("Cannot calculate slope (all x values are the same)")
    
    slope = numerator / denominator
    intercept = mean_y - slope * mean_x
    
    return (slope, intercept)


def skewness(data: List[float]) -> float:
    """
    Calculates skewness (measure of asymmetry)
    
    Args:
        data: List of numbers
        
    Returns:
        Skewness value
        
    Example:
        >>> skewness([1, 2, 3, 4, 5])
        0.0
    """
    if len(data) < 3:
        raise ValueError("Skewness requires at least 3 data points")
    
    mu = mean(data)
    sigma = standard_deviation(data, sample=False)
    n = len(data)
    
    if sigma == 0:
        raise ValueError("Standard deviation is zero")
    
    sum_cubed_deviations = sum(((x - mu) / sigma) ** 3 for x in data)
    
    return sum_cubed_deviations / n


def kurtosis(data: List[float]) -> float:
    """
    Calculates kurtosis (measure of "tailedness")
    
    Args:
        data: List of numbers
        
    Returns:
        Kurtosis value (excess kurtosis)
        
    Example:
        >>> kurtosis([1, 2, 3, 4, 5])
        -1.3
    """
    if len(data) < 4:
        raise ValueError("Kurtosis requires at least 4 data points")
    
    mu = mean(data)
    sigma = standard_deviation(data, sample=False)
    n = len(data)
    
    if sigma == 0:
        raise ValueError("Standard deviation is zero")
    
    sum_fourth_deviations = sum(((x - mu) / sigma) ** 4 for x in data)
    
    return (sum_fourth_deviations / n) - 3  # Excess kurtosis


def geometric_mean(data: List[float]) -> float:
    """
    Calculates geometric mean
    
    Args:
        data: List of positive numbers
        
    Returns:
        Geometric mean
        
    Example:
        >>> geometric_mean([1, 2, 4, 8])
        2.8284271247461903
    """
    if not data:
        raise ValueError("Cannot calculate geometric mean of empty list")
    if any(x <= 0 for x in data):
        raise ValueError("All values must be positive")
    
    product = 1
    for x in data:
        product *= x
    
    return product ** (1 / len(data))


def harmonic_mean(data: List[float]) -> float:
    """
    Calculates harmonic mean
    
    Args:
        data: List of non-zero numbers
        
    Returns:
        Harmonic mean
        
    Example:
        >>> harmonic_mean([1, 2, 4])
        1.7142857142857142
    """
    if not data:
        raise ValueError("Cannot calculate harmonic mean of empty list")
    if any(x == 0 for x in data):
        raise ValueError("Values cannot be zero")
    
    reciprocal_sum = sum(1 / x for x in data)
    
    return len(data) / reciprocal_sum


def coefficient_of_variation(data: List[float]) -> float:
    """
    Calculates coefficient of variation (CV = std_dev / mean)
    
    Args:
        data: List of numbers
        
    Returns:
        Coefficient of variation (as percentage)
        
    Example:
        >>> coefficient_of_variation([2, 4, 6, 8])
        44.72135954999579
    """
    mu = mean(data)
    if mu == 0:
        raise ValueError("Mean is zero, CV undefined")
    
    sigma = standard_deviation(data)
    
    return (sigma / abs(mu)) * 100


def moving_average(data: List[float], window: int) -> List[float]:
    """
    Calculates moving average
    
    Args:
        data: List of numbers
        window: Window size
        
    Returns:
        List of moving averages
        
    Example:
        >>> moving_average([1, 2, 3, 4, 5], 3)
        [2.0, 3.0, 4.0]
    """
    if window > len(data):
        raise ValueError("Window size cannot exceed data length")
    if window < 1:
        raise ValueError("Window size must be at least 1")
    
    result = []
    for i in range(len(data) - window + 1):
        window_data = data[i:i + window]
        result.append(mean(window_data))
    
    return result


# Export all functions
__all__ = [
    'mean', 'median', 'mode',
    'variance', 'standard_deviation', 'range_stat',
    'quartiles', 'interquartile_range', 'percentile',
    'z_score', 'covariance', 'correlation_coefficient',
    'linear_regression', 'skewness', 'kurtosis',
    'geometric_mean', 'harmonic_mean',
    'coefficient_of_variation', 'moving_average',
]
