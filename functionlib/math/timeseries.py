"""
Time series analysis and forecasting functions.

Provides decomposition, trend analysis, seasonality detection, and forecasting methods.
Pure Python implementations of common time series techniques.
"""

import math
from typing import List, Dict, Tuple, Optional, Any
from collections import defaultdict


def moving_average(data: List[float], window: int) -> List[float]:
    """Calculate moving average."""
    if window <= 0:
        raise ValueError("Window must be positive")
    
    if window > len(data):
        return [sum(data) / len(data)] * len(data)
    
    result = []
    for i in range(len(data)):
        if i < window - 1:
            # Not enough data points yet
            window_data = data[:i+1]
        else:
            window_data = data[i-window+1:i+1]
        
        result.append(sum(window_data) / len(window_data))
    
    return result


def exponential_smoothing(data: List[float], alpha: float = 0.3) -> List[float]:
    """Exponential smoothing for time series."""
    if not 0 <= alpha <= 1:
        raise ValueError("Alpha must be between 0 and 1")
    
    if not data:
        return []
    
    smoothed = [data[0]]
    
    for i in range(1, len(data)):
        value = alpha * data[i] + (1 - alpha) * smoothed[-1]
        smoothed.append(value)
    
    return smoothed


def double_exponential_smoothing(data: List[float], alpha: float = 0.3, beta: float = 0.3) -> List[float]:
    """Double exponential smoothing (Holt's method) for trend."""
    if not data or len(data) < 2:
        return data.copy() if data else []
    
    # Initialize
    level = data[0]
    trend = data[1] - data[0]
    result = [data[0]]
    
    for i in range(1, len(data)):
        last_level = level
        level = alpha * data[i] + (1 - alpha) * (level + trend)
        trend = beta * (level - last_level) + (1 - beta) * trend
        result.append(level)
    
    return result


def detect_trend(data: List[float]) -> Dict[str, Any]:
    """Detect trend in time series."""
    if len(data) < 2:
        return {'trend': 'insufficient_data', 'slope': 0}
    
    n = len(data)
    x_mean = (n - 1) / 2
    y_mean = sum(data) / n
    
    # Calculate slope using least squares
    numerator = sum((i - x_mean) * (data[i] - y_mean) for i in range(n))
    denominator = sum((i - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        slope = 0
    else:
        slope = numerator / denominator
    
    # Classify trend
    if abs(slope) < 0.01:
        trend = 'flat'
    elif slope > 0:
        trend = 'increasing'
    else:
        trend = 'decreasing'
    
    return {
        'trend': trend,
        'slope': slope,
        'intercept': y_mean - slope * x_mean
    }


def detect_seasonality(data: List[float], period: int) -> Dict[str, Any]:
    """Detect seasonality in time series."""
    if len(data) < period * 2:
        return {'has_seasonality': False, 'strength': 0}
    
    # Calculate seasonal indices
    n_periods = len(data) // period
    seasonal_avg = [0] * period
    
    for p in range(period):
        values = [data[p + i * period] for i in range(n_periods) if p + i * period < len(data)]
        seasonal_avg[p] = sum(values) / len(values) if values else 0
    
    # Calculate overall mean
    overall_mean = sum(data) / len(data)
    
    # Calculate seasonal strength
    seasonal_variance = sum((s - overall_mean) ** 2 for s in seasonal_avg) / period
    total_variance = sum((x - overall_mean) ** 2 for x in data) / len(data)
    
    strength = seasonal_variance / total_variance if total_variance > 0 else 0
    
    return {
        'has_seasonality': strength > 0.1,
        'strength': strength,
        'seasonal_indices': seasonal_avg,
        'period': period
    }


def decompose_time_series(data: List[float], period: int) -> Dict[str, List[float]]:
    """Decompose time series into trend, seasonal, and residual components."""
    if len(data) < period:
        return {
            'trend': data.copy(),
            'seasonal': [0] * len(data),
            'residual': [0] * len(data)
        }
    
    # Calculate trend using centered moving average
    trend = moving_average(data, window=period)
    
    # Detrend the data
    detrended = [data[i] - trend[i] for i in range(len(data))]
    
    # Calculate seasonal component
    n_periods = len(data) // period
    seasonal_avg = [0] * period
    
    for p in range(period):
        values = [detrended[p + i * period] for i in range(n_periods) if p + i * period < len(data)]
        seasonal_avg[p] = sum(values) / len(values) if values else 0
    
    # Extend seasonal pattern to full length
    seasonal = [seasonal_avg[i % period] for i in range(len(data))]
    
    # Calculate residual
    residual = [data[i] - trend[i] - seasonal[i] for i in range(len(data))]
    
    return {
        'trend': trend,
        'seasonal': seasonal,
        'residual': residual,
        'original': data
    }


def autocorrelation(data: List[float], lag: int = 1) -> float:
    """Calculate autocorrelation at given lag."""
    if lag >= len(data) or lag < 0:
        return 0.0
    
    n = len(data)
    mean = sum(data) / n
    
    # Calculate variance
    variance = sum((x - mean) ** 2 for x in data) / n
    
    if variance == 0:
        return 0.0
    
    # Calculate autocorrelation
    covariance = sum((data[i] - mean) * (data[i-lag] - mean) for i in range(lag, n)) / n
    
    return covariance / variance


def simple_forecast(data: List[float], periods: int, method: str = 'last') -> List[float]:
    """Simple forecasting methods."""
    if not data:
        return []
    
    if method == 'last':
        # Naive: repeat last value
        return [data[-1]] * periods
    
    elif method == 'mean':
        # Use mean
        mean_val = sum(data) / len(data)
        return [mean_val] * periods
    
    elif method == 'drift':
        # Linear drift from first to last
        if len(data) < 2:
            return [data[-1]] * periods
        
        drift = (data[-1] - data[0]) / (len(data) - 1)
        forecast = []
        for i in range(1, periods + 1):
            forecast.append(data[-1] + drift * i)
        return forecast
    
    else:
        return [data[-1]] * periods


def linear_regression_forecast(data: List[float], periods: int) -> List[float]:
    """Forecast using linear regression."""
    if len(data) < 2:
        return simple_forecast(data, periods, method='last')
    
    n = len(data)
    
    # Fit linear model
    x_mean = (n - 1) / 2
    y_mean = sum(data) / n
    
    numerator = sum((i - x_mean) * (data[i] - y_mean) for i in range(n))
    denominator = sum((i - x_mean) ** 2 for i in range(n))
    
    if denominator == 0:
        return simple_forecast(data, periods, method='mean')
    
    slope = numerator / denominator
    intercept = y_mean - slope * x_mean
    
    # Forecast
    forecast = []
    for i in range(n, n + periods):
        forecast.append(slope * i + intercept)
    
    return forecast


def holt_winters_forecast(data: List[float], periods: int, season_length: int = 12,
                         alpha: float = 0.3, beta: float = 0.1, gamma: float = 0.1) -> List[float]:
    """Holt-Winters seasonal forecasting."""
    if len(data) < season_length * 2:
        return simple_forecast(data, periods, method='drift')
    
    n = len(data)
    
    # Initialize components
    level = sum(data[:season_length]) / season_length
    trend = (sum(data[season_length:season_length*2]) - sum(data[:season_length])) / (season_length ** 2)
    
    # Initialize seasonal components
    seasonal = [0] * season_length
    for i in range(season_length):
        seasonal[i] = data[i] / level if level != 0 else 1
    
    # Smooth the series
    for i in range(len(data)):
        last_level = level
        
        seasonal_idx = i % season_length
        level = alpha * (data[i] / seasonal[seasonal_idx]) + (1 - alpha) * (level + trend)
        trend = beta * (level - last_level) + (1 - beta) * trend
        seasonal[seasonal_idx] = gamma * (data[i] / level) + (1 - gamma) * seasonal[seasonal_idx]
    
    # Forecast
    forecast = []
    for i in range(periods):
        seasonal_idx = (n + i) % season_length
        forecast.append((level + trend * (i + 1)) * seasonal[seasonal_idx])
    
    return forecast


def arima_forecast(data: List[float], periods: int, p: int = 1, d: int = 1, q: int = 1) -> List[float]:
    """
    Simplified ARIMA forecast.
    
    p: autoregressive order
    d: differencing order
    q: moving average order
    """
    if len(data) < p + d + q:
        return simple_forecast(data, periods, method='drift')
    
    # Difference the series d times
    differenced = data.copy()
    for _ in range(d):
        differenced = [differenced[i] - differenced[i-1] for i in range(1, len(differenced))]
    
    # Simple AR(p) model on differenced data
    forecast_diff = []
    
    for _ in range(periods):
        if len(differenced) < p:
            forecast_diff.append(differenced[-1] if differenced else 0)
        else:
            # AR prediction: weighted sum of last p values
            prediction = sum(differenced[-(i+1)] * (0.5 ** i) for i in range(p))
            forecast_diff.append(prediction)
            differenced.append(prediction)
    
    # Integrate back
    forecast = []
    last_value = data[-1]
    
    for diff_val in forecast_diff:
        next_value = last_value + diff_val
        forecast.append(next_value)
        last_value = next_value
    
    return forecast


def calculate_forecast_accuracy(actual: List[float], predicted: List[float]) -> Dict[str, float]:
    """Calculate forecast accuracy metrics."""
    if len(actual) != len(predicted) or not actual:
        return {}
    
    n = len(actual)
    
    # Mean Absolute Error
    mae = sum(abs(actual[i] - predicted[i]) for i in range(n)) / n
    
    # Mean Squared Error
    mse = sum((actual[i] - predicted[i]) ** 2 for i in range(n)) / n
    
    # Root Mean Squared Error
    rmse = math.sqrt(mse)
    
    # Mean Absolute Percentage Error
    mape = 0
    valid_count = 0
    for i in range(n):
        if actual[i] != 0:
            mape += abs((actual[i] - predicted[i]) / actual[i])
            valid_count += 1
    
    mape = (mape / valid_count * 100) if valid_count > 0 else 0
    
    return {
        'mae': mae,
        'mse': mse,
        'rmse': rmse,
        'mape': mape
    }


def detect_anomalies(data: List[float], threshold: float = 3.0) -> List[int]:
    """Detect anomalies using standard deviation method."""
    if len(data) < 3:
        return []
    
    mean = sum(data) / len(data)
    variance = sum((x - mean) ** 2 for x in data) / len(data)
    std_dev = math.sqrt(variance)
    
    anomalies = []
    for i, value in enumerate(data):
        z_score = abs((value - mean) / std_dev) if std_dev > 0 else 0
        if z_score > threshold:
            anomalies.append(i)
    
    return anomalies


def detect_change_points(data: List[float], min_segment_length: int = 5) -> List[int]:
    """Detect change points in time series."""
    if len(data) < min_segment_length * 2:
        return []
    
    change_points = []
    
    for i in range(min_segment_length, len(data) - min_segment_length):
        # Compare variance/mean before and after point
        before = data[max(0, i-min_segment_length):i]
        after = data[i:min(len(data), i+min_segment_length)]
        
        mean_before = sum(before) / len(before)
        mean_after = sum(after) / len(after)
        
        # Significant change in mean
        if abs(mean_after - mean_before) > 0.5 * abs(mean_before):
            change_points.append(i)
    
    return change_points


def rolling_statistics(data: List[float], window: int) -> Dict[str, List[float]]:
    """Calculate rolling statistics."""
    if window > len(data):
        window = len(data)
    
    rolling_mean = []
    rolling_std = []
    rolling_min = []
    rolling_max = []
    
    for i in range(len(data)):
        if i < window - 1:
            window_data = data[:i+1]
        else:
            window_data = data[i-window+1:i+1]
        
        mean = sum(window_data) / len(window_data)
        variance = sum((x - mean) ** 2 for x in window_data) / len(window_data)
        std = math.sqrt(variance)
        
        rolling_mean.append(mean)
        rolling_std.append(std)
        rolling_min.append(min(window_data))
        rolling_max.append(max(window_data))
    
    return {
        'mean': rolling_mean,
        'std': rolling_std,
        'min': rolling_min,
        'max': rolling_max
    }


def seasonal_decompose_strength(data: List[float], period: int) -> Dict[str, float]:
    """Calculate strength of trend and seasonality."""
    decomposition = decompose_time_series(data, period)
    
    # Variance of components
    var_residual = sum(x ** 2 for x in decomposition['residual']) / len(data)
    var_seasonal = sum(x ** 2 for x in decomposition['seasonal']) / len(data)
    
    # Detrended data
    detrended = [data[i] - decomposition['trend'][i] for i in range(len(data))]
    var_detrended = sum(x ** 2 for x in detrended) / len(data)
    
    # Strength of seasonality
    seasonal_strength = 1 - (var_residual / var_detrended) if var_detrended > 0 else 0
    seasonal_strength = max(0, min(1, seasonal_strength))
    
    # Strength of trend (variance of trend relative to total)
    var_data = sum((x - sum(data)/len(data)) ** 2 for x in data) / len(data)
    trend_strength = 1 - (var_detrended / var_data) if var_data > 0 else 0
    trend_strength = max(0, min(1, trend_strength))
    
    return {
        'seasonal_strength': seasonal_strength,
        'trend_strength': trend_strength
    }


def cross_correlation(series1: List[float], series2: List[float], max_lag: int = 10) -> Dict[int, float]:
    """Calculate cross-correlation between two series."""
    if len(series1) != len(series2):
        raise ValueError("Series must have same length")
    
    n = len(series1)
    mean1 = sum(series1) / n
    mean2 = sum(series2) / n
    
    std1 = math.sqrt(sum((x - mean1) ** 2 for x in series1) / n)
    std2 = math.sqrt(sum((x - mean2) ** 2 for x in series2) / n)
    
    if std1 == 0 or std2 == 0:
        return {lag: 0.0 for lag in range(-max_lag, max_lag + 1)}
    
    correlations = {}
    
    for lag in range(-max_lag, max_lag + 1):
        if lag >= 0:
            # Positive lag: series2 leads series1
            overlap = [(series1[i] - mean1) * (series2[i+lag] - mean2)
                      for i in range(n - lag)]
        else:
            # Negative lag: series1 leads series2
            overlap = [(series1[i-lag] - mean1) * (series2[i] - mean2)
                      for i in range(-lag, n)]
        
        if overlap:
            correlations[lag] = sum(overlap) / (len(overlap) * std1 * std2)
        else:
            correlations[lag] = 0.0
    
    return correlations


__all__ = [
    'moving_average',
    'exponential_smoothing',
    'double_exponential_smoothing',
    'detect_trend',
    'detect_seasonality',
    'decompose_time_series',
    'autocorrelation',
    'simple_forecast',
    'linear_regression_forecast',
    'holt_winters_forecast',
    'arima_forecast',
    'calculate_forecast_accuracy',
    'detect_anomalies',
    'detect_change_points',
    'rolling_statistics',
    'seasonal_decompose_strength',
    'cross_correlation'
]
