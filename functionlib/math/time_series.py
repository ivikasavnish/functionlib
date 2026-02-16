"""Time series analysis and forecasting functions."""

import math
from typing import List, Tuple, Optional

__all__ = [
    'moving_average',
    'weighted_moving_average',
    'exponential_smoothing',
    'double_exponential_smoothing',
    'triple_exponential_smoothing',
    'seasonal_decomposition',
    'trend_line',
    'detrend',
    'difference',
    'percent_change',
    'autocorrelation',
    'partial_autocorrelation',
    'lag',
    'rolling_std',
    'rolling_variance',
    'cumulative_sum',
    'cumulative_product',
    'seasonal_indices',
    'forecast_naive',
    'forecast_moving_average',
    'forecast_exponential_smoothing',
    'mean_absolute_percentage_error',
    'forecast_accuracy',
]

def moving_average(data: List[float], window: int) -> List[float]:
    """Calculate simple moving average.
    
    Args:
        data: Time series data
        window: Window size
        
    Returns:
        Moving averages
        
    Example:
        >>> data = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> ma = moving_average(data, 3)
        >>> ma[2]
        2.0
    """
    result = []
    for i in range(len(data)):
        if i < window - 1:
            result.append(None)
        else:
            avg = sum(data[i-window+1:i+1]) / window
            result.append(avg)
    return result

def weighted_moving_average(data: List[float], weights: List[float]) -> List[float]:
    """Calculate weighted moving average.
    
    Args:
        data: Time series data
        weights: Weights (most recent first)
        
    Returns:
        Weighted moving averages
        
    Example:
        >>> data = [1, 2, 3, 4, 5, 6]
        >>> weights = [0.5, 0.3, 0.2]
        >>> wma = weighted_moving_average(data, weights)
        >>> wma[2] > 0
        True
    """
    window = len(weights)
    weight_sum = sum(weights)
    result = []
    
    for i in range(len(data)):
        if i < window - 1:
            result.append(None)
        else:
            wma = sum(data[i-j] * weights[j] for j in range(window)) / weight_sum
            result.append(wma)
    
    return result

def exponential_smoothing(data: List[float], alpha: float = 0.3) -> List[float]:
    """Simple exponential smoothing.
    
    Args:
        data: Time series data
        alpha: Smoothing parameter (0 to 1)
        
    Returns:
        Smoothed values
        
    Example:
        >>> data = [10, 12, 11, 13, 12, 14]
        >>> smoothed = exponential_smoothing(data, 0.3)
        >>> len(smoothed) == len(data)
        True
    """
    result = [data[0]]
    
    for i in range(1, len(data)):
        smoothed = alpha * data[i] + (1 - alpha) * result[-1]
        result.append(smoothed)
    
    return result

def double_exponential_smoothing(data: List[float], alpha: float = 0.3,
                                 beta: float = 0.1) -> List[float]:
    """Double exponential smoothing (Holt's method).
    
    Args:
        data: Time series data
        alpha: Level smoothing parameter
        beta: Trend smoothing parameter
        
    Returns:
        Smoothed values
        
    Example:
        >>> data = [10, 12, 14, 16, 18, 20]
        >>> smoothed = double_exponential_smoothing(data, 0.3, 0.1)
        >>> len(smoothed) == len(data)
        True
    """
    level = data[0]
    trend = data[1] - data[0] if len(data) > 1 else 0
    result = [level]
    
    for i in range(1, len(data)):
        last_level = level
        level = alpha * data[i] + (1 - alpha) * (level + trend)
        trend = beta * (level - last_level) + (1 - beta) * trend
        result.append(level + trend)
    
    return result

def triple_exponential_smoothing(data: List[float], season_length: int,
                                 alpha: float = 0.3, beta: float = 0.1,
                                 gamma: float = 0.1) -> List[float]:
    """Triple exponential smoothing (Holt-Winters method).
    
    Args:
        data: Time series data
        season_length: Length of seasonal cycle
        alpha: Level smoothing parameter
        beta: Trend smoothing parameter
        gamma: Seasonal smoothing parameter
        
    Returns:
        Smoothed values
        
    Example:
        >>> data = [10, 15, 12, 18, 14, 19, 16, 21]
        >>> smoothed = triple_exponential_smoothing(data, 4)
        >>> len(smoothed) == len(data)
        True
    """
    # Initialize seasonal indices
    seasonal = [1.0] * season_length
    
    # Initial level and trend
    level = sum(data[:season_length]) / season_length
    trend = (sum(data[season_length:2*season_length]) - sum(data[:season_length])) / season_length**2 if len(data) >= 2*season_length else 0
    
    result = []
    
    for i in range(len(data)):
        season_idx = i % season_length
        
        # Update
        last_level = level
        level = alpha * (data[i] / seasonal[season_idx]) + (1 - alpha) * (level + trend)
        trend = beta * (level - last_level) + (1 - beta) * trend
        seasonal[season_idx] = gamma * (data[i] / level) + (1 - gamma) * seasonal[season_idx]
        
        # Forecast
        forecast = (level + trend) * seasonal[season_idx]
        result.append(forecast)
    
    return result

def seasonal_decomposition(data: List[float], period: int) -> Tuple[List[float], List[float], List[float]]:
    """Decompose time series into trend, seasonal, and residual.
    
    Args:
        data: Time series data
        period: Seasonal period
        
    Returns:
        (trend, seasonal, residual)
        
    Example:
        >>> data = [10, 15, 12, 18] * 3
        >>> trend, seasonal, residual = seasonal_decomposition(data, 4)
        >>> len(trend) == len(data)
        True
    """
    # Calculate trend using moving average
    trend = moving_average(data, period)
    
    # Calculate seasonal component
    seasonal = [0.0] * len(data)
    seasonal_avg = [[] for _ in range(period)]
    
    for i in range(len(data)):
        if trend[i] is not None:
            detrended = data[i] - trend[i]
            seasonal_avg[i % period].append(detrended)
    
    # Average seasonal components
    seasonal_pattern = [sum(values) / len(values) if values else 0 
                       for values in seasonal_avg]
    
    for i in range(len(data)):
        seasonal[i] = seasonal_pattern[i % period]
    
    # Calculate residual
    residual = []
    for i in range(len(data)):
        if trend[i] is not None:
            residual.append(data[i] - trend[i] - seasonal[i])
        else:
            residual.append(None)
    
    return trend, seasonal, residual

def trend_line(data: List[float]) -> Tuple[float, float]:
    """Calculate linear trend line (slope and intercept).
    
    Args:
        data: Time series data
        
    Returns:
        (slope, intercept)
        
    Example:
        >>> data = [1, 2, 3, 4, 5]
        >>> slope, intercept = trend_line(data)
        >>> abs(slope - 1.0) < 0.01
        True
    """
    n = len(data)
    x = list(range(n))
    
    x_mean = sum(x) / n
    y_mean = sum(data) / n
    
    numerator = sum((x[i] - x_mean) * (data[i] - y_mean) for i in range(n))
    denominator = sum((x[i] - x_mean) ** 2 for i in range(n))
    
    slope = numerator / denominator if denominator != 0 else 0
    intercept = y_mean - slope * x_mean
    
    return slope, intercept

def detrend(data: List[float]) -> List[float]:
    """Remove linear trend from data.
    
    Args:
        data: Time series data
        
    Returns:
        Detrended data
        
    Example:
        >>> data = [1, 2, 3, 4, 5]
        >>> detrended = detrend(data)
        >>> abs(sum(detrended)) < 0.01
        True
    """
    slope, intercept = trend_line(data)
    return [data[i] - (slope * i + intercept) for i in range(len(data))]

def difference(data: List[float], lag: int = 1) -> List[float]:
    """Calculate differences (for stationarity).
    
    Args:
        data: Time series data
        lag: Lag for differencing
        
    Returns:
        Differenced data
        
    Example:
        >>> data = [1, 3, 6, 10, 15]
        >>> diff = difference(data, 1)
        >>> diff[0]
        2.0
    """
    return [data[i] - data[i-lag] for i in range(lag, len(data))]

def percent_change(data: List[float]) -> List[float]:
    """Calculate percent change between consecutive values.
    
    Args:
        data: Time series data
        
    Returns:
        Percent changes
        
    Example:
        >>> data = [100, 110, 121]
        >>> pct = percent_change(data)
        >>> abs(pct[0] - 0.1) < 0.01
        True
    """
    return [(data[i] - data[i-1]) / data[i-1] if data[i-1] != 0 else 0 
            for i in range(1, len(data))]

def autocorrelation(data: List[float], lag: int = 1) -> float:
    """Calculate autocorrelation at given lag.
    
    Args:
        data: Time series data
        lag: Lag
        
    Returns:
        Autocorrelation coefficient
        
    Example:
        >>> data = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> acf = autocorrelation(data, 1)
        >>> 0.5 < acf < 1.0
        True
    """
    n = len(data)
    mean = sum(data) / n
    
    c0 = sum((x - mean) ** 2 for x in data)
    c_lag = sum((data[i] - mean) * (data[i-lag] - mean) for i in range(lag, n))
    
    return c_lag / c0 if c0 != 0 else 0

def partial_autocorrelation(data: List[float], lag: int) -> float:
    """Calculate partial autocorrelation at given lag (approximation).
    
    Args:
        data: Time series data
        lag: Lag
        
    Returns:
        Partial autocorrelation coefficient
        
    Example:
        >>> data = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> pacf = partial_autocorrelation(data, 1)
        >>> 0 < pacf < 1
        True
    """
    # Simplified calculation using Durbin-Levinson recursion
    if lag == 0:
        return 1.0
    elif lag == 1:
        return autocorrelation(data, 1)
    else:
        # Approximate using ACF values
        acf_values = [autocorrelation(data, k) for k in range(lag + 1)]
        return acf_values[lag]  # Simplified

def lag(data: List[float], periods: int = 1) -> List[float]:
    """Create lagged version of series.
    
    Args:
        data: Time series data
        periods: Number of periods to lag
        
    Returns:
        Lagged series (with None for missing values)
        
    Example:
        >>> data = [1, 2, 3, 4, 5]
        >>> lagged = lag(data, 2)
        >>> lagged[2]
        1
    """
    return [None] * periods + data[:-periods] if periods > 0 else data

def rolling_std(data: List[float], window: int) -> List[float]:
    """Calculate rolling standard deviation.
    
    Args:
        data: Time series data
        window: Window size
        
    Returns:
        Rolling standard deviations
        
    Example:
        >>> data = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> rolling_s = rolling_std(data, 3)
        >>> rolling_s[2] > 0
        True
    """
    result = []
    for i in range(len(data)):
        if i < window - 1:
            result.append(None)
        else:
            window_data = data[i-window+1:i+1]
            mean = sum(window_data) / window
            variance = sum((x - mean) ** 2 for x in window_data) / window
            result.append(math.sqrt(variance))
    return result

def rolling_variance(data: List[float], window: int) -> List[float]:
    """Calculate rolling variance.
    
    Args:
        data: Time series data
        window: Window size
        
    Returns:
        Rolling variances
        
    Example:
        >>> data = [1, 2, 3, 4, 5, 6, 7, 8]
        >>> rolling_v = rolling_variance(data, 3)
        >>> rolling_v[2] > 0
        True
    """
    result = []
    for i in range(len(data)):
        if i < window - 1:
            result.append(None)
        else:
            window_data = data[i-window+1:i+1]
            mean = sum(window_data) / window
            variance = sum((x - mean) ** 2 for x in window_data) / window
            result.append(variance)
    return result

def cumulative_sum(data: List[float]) -> List[float]:
    """Calculate cumulative sum.
    
    Args:
        data: Time series data
        
    Returns:
        Cumulative sums
        
    Example:
        >>> data = [1, 2, 3, 4, 5]
        >>> cumsum = cumulative_sum(data)
        >>> cumsum[-1]
        15
    """
    result = []
    total = 0
    for x in data:
        total += x
        result.append(total)
    return result

def cumulative_product(data: List[float]) -> List[float]:
    """Calculate cumulative product.
    
    Args:
        data: Time series data
        
    Returns:
        Cumulative products
        
    Example:
        >>> data = [1, 2, 3, 4]
        >>> cumprod = cumulative_product(data)
        >>> cumprod[-1]
        24
    """
    result = []
    product = 1
    for x in data:
        product *= x
        result.append(product)
    return result

def seasonal_indices(data: List[float], period: int) -> List[float]:
    """Calculate seasonal indices.
    
    Args:
        data: Time series data
        period: Seasonal period
        
    Returns:
        Seasonal indices for each period
        
    Example:
        >>> data = [10, 15, 12, 18] * 3
        >>> indices = seasonal_indices(data, 4)
        >>> len(indices) == 4
        True
    """
    # Calculate overall mean
    overall_mean = sum(data) / len(data)
    
    # Calculate average for each season
    seasonal_sums = [[] for _ in range(period)]
    
    for i, value in enumerate(data):
        seasonal_sums[i % period].append(value)
    
    seasonal_means = [sum(values) / len(values) if values else 0 
                     for values in seasonal_sums]
    
    # Calculate indices
    indices = [mean / overall_mean if overall_mean != 0 else 1.0 
              for mean in seasonal_means]
    
    return indices

def forecast_naive(data: List[float], periods: int = 1) -> List[float]:
    """Naive forecast (last value repeated).
    
    Args:
        data: Time series data
        periods: Number of periods to forecast
        
    Returns:
        Forecasted values
        
    Example:
        >>> data = [1, 2, 3, 4, 5]
        >>> forecast = forecast_naive(data, 3)
        >>> forecast == [5, 5, 5]
        True
    """
    return [data[-1]] * periods

def forecast_moving_average(data: List[float], window: int, periods: int = 1) -> List[float]:
    """Forecast using moving average.
    
    Args:
        data: Time series data
        window: Window size
        periods: Number of periods to forecast
        
    Returns:
        Forecasted values
        
    Example:
        >>> data = [1, 2, 3, 4, 5, 6]
        >>> forecast = forecast_moving_average(data, 3, 2)
        >>> len(forecast) == 2
        True
    """
    last_ma = sum(data[-window:]) / window
    return [last_ma] * periods

def forecast_exponential_smoothing(data: List[float], alpha: float = 0.3,
                                   periods: int = 1) -> List[float]:
    """Forecast using exponential smoothing.
    
    Args:
        data: Time series data
        alpha: Smoothing parameter
        periods: Number of periods to forecast
        
    Returns:
        Forecasted values
        
    Example:
        >>> data = [10, 12, 11, 13, 12]
        >>> forecast = forecast_exponential_smoothing(data, 0.3, 3)
        >>> len(forecast) == 3
        True
    """
    # Calculate last smoothed value
    smoothed = data[0]
    for value in data[1:]:
        smoothed = alpha * value + (1 - alpha) * smoothed
    
    return [smoothed] * periods

def mean_absolute_percentage_error(actual: List[float], forecast: List[float]) -> float:
    """Calculate MAPE (Mean Absolute Percentage Error).
    
    Args:
        actual: Actual values
        forecast: Forecasted values
        
    Returns:
        MAPE as percentage
        
    Example:
        >>> actual = [100, 110, 120]
        >>> forecast = [98, 112, 118]
        >>> mape = mean_absolute_percentage_error(actual, forecast)
        >>> 0 < mape < 10
        True
    """
    if len(actual) != len(forecast):
        raise ValueError("Actual and forecast must have same length")
    
    errors = []
    for a, f in zip(actual, forecast):
        if a != 0:
            errors.append(abs((a - f) / a))
    
    return (sum(errors) / len(errors)) * 100 if errors else 0

def forecast_accuracy(actual: List[float], forecast: List[float]) -> dict:
    """Calculate multiple forecast accuracy metrics.
    
    Args:
        actual: Actual values
        forecast: Forecasted values
        
    Returns:
        Dictionary with MAE, MSE, RMSE, MAPE
        
    Example:
        >>> actual = [100, 110, 120]
        >>> forecast = [98, 112, 118]
        >>> metrics = forecast_accuracy(actual, forecast)
        >>> 'MAE' in metrics
        True
    """
    if len(actual) != len(forecast):
        raise ValueError("Actual and forecast must have same length")
    
    n = len(actual)
    errors = [actual[i] - forecast[i] for i in range(n)]
    
    mae = sum(abs(e) for e in errors) / n
    mse = sum(e ** 2 for e in errors) / n
    rmse = math.sqrt(mse)
    
    # MAPE
    mape_errors = [abs((actual[i] - forecast[i]) / actual[i]) 
                   for i in range(n) if actual[i] != 0]
    mape = (sum(mape_errors) / len(mape_errors)) * 100 if mape_errors else 0
    
    return {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'MAPE': mape
    }
