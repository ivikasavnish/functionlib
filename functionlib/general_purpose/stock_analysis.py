"""Stock market analysis and technical indicators (pure Python)."""

import math
from typing import List, Tuple, Dict, Optional

__all__ = [
    'simple_moving_average',
    'exponential_moving_average',
    'moving_average_convergence_divergence',
    'relative_strength_index',
    'bollinger_bands',
    'average_true_range',
    'stochastic_oscillator',
    'on_balance_volume',
    'accumulation_distribution',
    'money_flow_index',
    'commodity_channel_index',
    'rate_of_change',
    'williams_percent_r',
    'standard_deviation',
    'beta_coefficient',
    'sharpe_ratio',
    'sortino_ratio',
    'max_drawdown',
    'calmar_ratio',
    'alpha',
    'treynor_ratio',
    'information_ratio',
    'value_at_risk',
    'expected_shortfall',
    'portfolio_return',
    'portfolio_variance',
    'portfolio_sharpe',
    'correlation_matrix',
    'covariance_matrix',
]

def simple_moving_average(prices: List[float], period: int) -> List[Optional[float]]:
    """Calculate Simple Moving Average (SMA).
    
    Args:
        prices: Price data
        period: Period for average
        
    Returns:
        SMA values
        
    Example:
        >>> prices = [10, 11, 12, 13, 14]
        >>> sma = simple_moving_average(prices, 3)
        >>> sma[2]
        11.0
    """
    result = []
    for i in range(len(prices)):
        if i < period - 1:
            result.append(None)
        else:
            result.append(sum(prices[i-period+1:i+1]) / period)
    return result

def exponential_moving_average(prices: List[float], period: int) -> List[float]:
    """Calculate Exponential Moving Average (EMA).
    
    Args:
        prices: Price data
        period: Period for average
        
    Returns:
        EMA values
        
    Example:
        >>> prices = [10, 11, 12, 13, 14]
        >>> ema = exponential_moving_average(prices, 3)
        >>> ema[-1] > 13
        True
    """
    multiplier = 2 / (period + 1)
    ema = [prices[0]]
    
    for price in prices[1:]:
        ema.append(price * multiplier + ema[-1] * (1 - multiplier))
    
    return ema

def moving_average_convergence_divergence(prices: List[float],
                                          fast: int = 12, slow: int = 26,
                                          signal: int = 9) -> Tuple[List[float], List[float]]:
    """Calculate MACD indicator.
    
    Args:
        prices: Price data
        fast: Fast EMA period
        slow: Slow EMA period
        signal: Signal line period
        
    Returns:
        (MACD line, Signal line)
        
    Example:
        >>> prices = list(range(10, 40))
        >>> macd, signal = moving_average_convergence_divergence(prices)
        >>> len(macd) == len(prices)
        True
    """
    ema_fast = exponential_moving_average(prices, fast)
    ema_slow = exponential_moving_average(prices, slow)
    
    macd_line = [f - s for f, s in zip(ema_fast, ema_slow)]
    signal_line = exponential_moving_average(macd_line, signal)
    
    return macd_line, signal_line

def relative_strength_index(prices: List[float], period: int = 14) -> List[Optional[float]]:
    """Calculate Relative Strength Index (RSI).
    
    Args:
        prices: Price data
        period: RSI period
        
    Returns:
        RSI values (0-100)
        
    Example:
        >>> prices = [44, 44.5, 44.3, 44.7, 45, 45.2]
        >>> rsi = relative_strength_index(prices, period=3)
        >>> rsi[-1] is not None
        True
    """
    if len(prices) < period + 1:
        return [None] * len(prices)
    
    # Calculate price changes
    changes = [prices[i] - prices[i-1] for i in range(1, len(prices))]
    
    gains = [max(c, 0) for c in changes]
    losses = [abs(min(c, 0)) for c in changes]
    
    result = [None]
    
    # First RSI
    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    
    if avg_loss == 0:
        result.append(100)
    else:
        rs = avg_gain / avg_loss
        result.append(100 - (100 / (1 + rs)))
    
    # Subsequent RSI values
    for i in range(period, len(changes)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        
        if avg_loss == 0:
            result.append(100)
        else:
            rs = avg_gain / avg_loss
            result.append(100 - (100 / (1 + rs)))
    
    return result

def bollinger_bands(prices: List[float], period: int = 20,
                    std_dev: int = 2) -> Tuple[List[Optional[float]], List[Optional[float]], List[Optional[float]]]:
    """Calculate Bollinger Bands.
    
    Args:
        prices: Price data
        period: Period for moving average
        std_dev: Number of standard deviations
        
    Returns:
        (Upper band, Middle band, Lower band)
        
    Example:
        >>> prices = list(range(10, 35))
        >>> upper, middle, lower = bollinger_bands(prices, period=5)
        >>> upper[4] > middle[4] > lower[4]
        True
    """
    sma = simple_moving_average(prices, period)
    
    upper = []
    lower = []
    
    for i in range(len(prices)):
        if i < period - 1:
            upper.append(None)
            lower.append(None)
        else:
            window = prices[i-period+1:i+1]
            mean = sum(window) / period
            variance = sum((x - mean) ** 2 for x in window) / period
            std = math.sqrt(variance)
            
            upper.append(sma[i] + std_dev * std)
            lower.append(sma[i] - std_dev * std)
    
    return upper, sma, lower

def average_true_range(high: List[float], low: List[float],
                       close: List[float], period: int = 14) -> List[Optional[float]]:
    """Calculate Average True Range (ATR).
    
    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: ATR period
        
    Returns:
        ATR values
        
    Example:
        >>> high = [10, 11, 12]
        >>> low = [9, 10, 11]
        >>> close = [9.5, 10.5, 11.5]
        >>> atr = average_true_range(high, low, close, period=2)
        >>> len(atr) == 3
        True
    """
    true_ranges = [high[0] - low[0]]
    
    for i in range(1, len(high)):
        tr = max(
            high[i] - low[i],
            abs(high[i] - close[i-1]),
            abs(low[i] - close[i-1])
        )
        true_ranges.append(tr)
    
    result = [None] * (period - 1)
    if len(true_ranges) >= period:
        result.append(sum(true_ranges[:period]) / period)
        
        for i in range(period, len(true_ranges)):
            atr = (result[-1] * (period - 1) + true_ranges[i]) / period
            result.append(atr)
    
    return result

def stochastic_oscillator(high: List[float], low: List[float],
                          close: List[float], period: int = 14) -> Tuple[List[Optional[float]], List[Optional[float]]]:
    """Calculate Stochastic Oscillator.
    
    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: Stochastic period
        
    Returns:
        (%K, %D)
        
    Example:
        >>> high = [10, 11, 12, 13, 14]
        >>> low = [9, 10, 11, 12, 13]
        >>> close = [9.5, 10.5, 11.5, 12.5, 13.5]
        >>> k, d = stochastic_oscillator(high, low, close, period=3)
        >>> len(k) == 5
        True
    """
    k_values = []
    
    for i in range(len(close)):
        if i < period - 1:
            k_values.append(None)
        else:
            highest = max(high[i-period+1:i+1])
            lowest = min(low[i-period+1:i+1])
            
            if highest == lowest:
                k_values.append(50)
            else:
                k = ((close[i] - lowest) / (highest - lowest)) * 100
                k_values.append(k)
    
    # %D is 3-period SMA of %K
    d_values = []
    for i in range(len(k_values)):
        if i < 2 or k_values[i] is None or k_values[i-1] is None or k_values[i-2] is None:
            d_values.append(None)
        else:
            d = (k_values[i] + k_values[i-1] + k_values[i-2]) / 3
            d_values.append(d)
    
    return k_values, d_values

def on_balance_volume(close: List[float], volume: List[int]) -> List[float]:
    """Calculate On-Balance Volume (OBV).
    
    Args:
        close: Close prices
        volume: Volume data
        
    Returns:
        OBV values
        
    Example:
        >>> close = [10, 11, 10.5, 12]
        >>> volume = [1000, 1500, 1200, 1800]
        >>> obv = on_balance_volume(close, volume)
        >>> len(obv) == 4
        True
    """
    obv = [0]
    
    for i in range(1, len(close)):
        if close[i] > close[i-1]:
            obv.append(obv[-1] + volume[i])
        elif close[i] < close[i-1]:
            obv.append(obv[-1] - volume[i])
        else:
            obv.append(obv[-1])
    
    return obv

def accumulation_distribution(high: List[float], low: List[float],
                               close: List[float], volume: List[int]) -> List[float]:
    """Calculate Accumulation/Distribution Line.
    
    Args:
        high: High prices
        low: Low prices
        close: Close prices
        volume: Volume data
        
    Returns:
        A/D line values
        
    Example:
        >>> high = [10, 11, 12]
        >>> low = [9, 10, 11]
        >>> close = [9.5, 10.5, 11.5]
        >>> volume = [1000, 1500, 1200]
        >>> ad = accumulation_distribution(high, low, close, volume)
        >>> len(ad) == 3
        True
    """
    ad_line = [0]
    
    for i in range(len(close)):
        if high[i] == low[i]:
            mfm = 0
        else:
            mfm = ((close[i] - low[i]) - (high[i] - close[i])) / (high[i] - low[i])
        
        mfv = mfm * volume[i]
        ad_line.append(ad_line[-1] + mfv)
    
    return ad_line[1:]

def money_flow_index(high: List[float], low: List[float],
                     close: List[float], volume: List[int],
                     period: int = 14) -> List[Optional[float]]:
    """Calculate Money Flow Index (MFI).
    
    Args:
        high: High prices
        low: Low prices
        close: Close prices
        volume: Volume data
        period: MFI period
        
    Returns:
        MFI values (0-100)
        
    Example:
        >>> high = [10, 11, 12, 13, 14, 15]
        >>> low = [9, 10, 11, 12, 13, 14]
        >>> close = [9.5, 10.5, 11.5, 12.5, 13.5, 14.5]
        >>> volume = [1000, 1500, 1200, 1800, 1600, 2000]
        >>> mfi = money_flow_index(high, low, close, volume, period=3)
        >>> len(mfi) == 6
        True
    """
    # Calculate typical price
    typical_price = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
    
    # Calculate money flow
    money_flow = [tp * v for tp, v in zip(typical_price, volume)]
    
    result = [None] * period
    
    for i in range(period, len(typical_price)):
        positive_flow = 0
        negative_flow = 0
        
        for j in range(i - period + 1, i + 1):
            if typical_price[j] > typical_price[j-1]:
                positive_flow += money_flow[j]
            elif typical_price[j] < typical_price[j-1]:
                negative_flow += money_flow[j]
        
        if negative_flow == 0:
            result.append(100)
        else:
            money_ratio = positive_flow / negative_flow
            mfi = 100 - (100 / (1 + money_ratio))
            result.append(mfi)
    
    return result

def commodity_channel_index(high: List[float], low: List[float],
                            close: List[float], period: int = 20) -> List[Optional[float]]:
    """Calculate Commodity Channel Index (CCI).
    
    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: CCI period
        
    Returns:
        CCI values
        
    Example:
        >>> high = list(range(10, 35))
        >>> low = list(range(9, 34))
        >>> close = [h - 0.5 for h in high]
        >>> cci = commodity_channel_index(high, low, close, period=5)
        >>> len(cci) == len(high)
        True
    """
    typical_price = [(h + l + c) / 3 for h, l, c in zip(high, low, close)]
    
    result = []
    for i in range(len(typical_price)):
        if i < period - 1:
            result.append(None)
        else:
            window = typical_price[i-period+1:i+1]
            sma = sum(window) / period
            mean_deviation = sum(abs(x - sma) for x in window) / period
            
            if mean_deviation == 0:
                result.append(0)
            else:
                cci = (typical_price[i] - sma) / (0.015 * mean_deviation)
                result.append(cci)
    
    return result

def rate_of_change(prices: List[float], period: int = 12) -> List[Optional[float]]:
    """Calculate Rate of Change (ROC).
    
    Args:
        prices: Price data
        period: ROC period
        
    Returns:
        ROC values (percentage)
        
    Example:
        >>> prices = [10, 11, 12, 13, 14]
        >>> roc = rate_of_change(prices, period=2)
        >>> roc[2] == 20.0
        True
    """
    result = [None] * period
    
    for i in range(period, len(prices)):
        if prices[i-period] == 0:
            result.append(None)
        else:
            roc = ((prices[i] - prices[i-period]) / prices[i-period]) * 100
            result.append(roc)
    
    return result

def williams_percent_r(high: List[float], low: List[float],
                       close: List[float], period: int = 14) -> List[Optional[float]]:
    """Calculate Williams %R.
    
    Args:
        high: High prices
        low: Low prices
        close: Close prices
        period: Period
        
    Returns:
        Williams %R values (-100 to 0)
        
    Example:
        >>> high = [10, 11, 12, 13, 14]
        >>> low = [9, 10, 11, 12, 13]
        >>> close = [9.5, 10.5, 11.5, 12.5, 13.5]
        >>> wr = williams_percent_r(high, low, close, period=3)
        >>> len(wr) == 5
        True
    """
    result = []
    
    for i in range(len(close)):
        if i < period - 1:
            result.append(None)
        else:
            highest = max(high[i-period+1:i+1])
            lowest = min(low[i-period+1:i+1])
            
            if highest == lowest:
                result.append(-50)
            else:
                wr = ((highest - close[i]) / (highest - lowest)) * -100
                result.append(wr)
    
    return result

def standard_deviation(prices: List[float], period: int) -> List[Optional[float]]:
    """Calculate rolling standard deviation.
    
    Args:
        prices: Price data
        period: Period
        
    Returns:
        Standard deviation values
        
    Example:
        >>> prices = [10, 11, 12, 13, 14]
        >>> std = standard_deviation(prices, 3)
        >>> std[2] > 0
        True
    """
    result = []
    
    for i in range(len(prices)):
        if i < period - 1:
            result.append(None)
        else:
            window = prices[i-period+1:i+1]
            mean = sum(window) / period
            variance = sum((x - mean) ** 2 for x in window) / period
            result.append(math.sqrt(variance))
    
    return result

def beta_coefficient(stock_returns: List[float], market_returns: List[float]) -> float:
    """Calculate beta coefficient.
    
    Args:
        stock_returns: Stock returns
        market_returns: Market returns
        
    Returns:
        Beta value
        
    Example:
        >>> stock = [0.01, 0.02, -0.01, 0.03]
        >>> market = [0.015, 0.01, -0.005, 0.02]
        >>> beta = beta_coefficient(stock, market)
        >>> beta > 0
        True
    """
    stock_mean = sum(stock_returns) / len(stock_returns)
    market_mean = sum(market_returns) / len(market_returns)
    
    covariance = sum((s - stock_mean) * (m - market_mean) 
                     for s, m in zip(stock_returns, market_returns)) / len(stock_returns)
    
    market_variance = sum((m - market_mean) ** 2 for m in market_returns) / len(market_returns)
    
    return covariance / market_variance if market_variance != 0 else 0

def sharpe_ratio(returns: List[float], risk_free_rate: float = 0.02) -> float:
    """Calculate Sharpe ratio.
    
    Args:
        returns: Return series
        risk_free_rate: Risk-free rate (annualized)
        
    Returns:
        Sharpe ratio
        
    Example:
        >>> returns = [0.01, 0.02, 0.015, 0.03]
        >>> sharpe = sharpe_ratio(returns, 0.01)
        >>> sharpe > 0
        True
    """
    mean_return = sum(returns) / len(returns)
    excess_return = mean_return - risk_free_rate / 252  # Daily risk-free rate
    
    std_dev = math.sqrt(sum((r - mean_return) ** 2 for r in returns) / len(returns))
    
    return (excess_return * math.sqrt(252)) / std_dev if std_dev != 0 else 0

def sortino_ratio(returns: List[float], risk_free_rate: float = 0.02,
                  target_return: float = 0) -> float:
    """Calculate Sortino ratio.
    
    Args:
        returns: Return series
        risk_free_rate: Risk-free rate
        target_return: Target return
        
    Returns:
        Sortino ratio
        
    Example:
        >>> returns = [0.01, 0.02, -0.01, 0.03]
        >>> sortino = sortino_ratio(returns, 0.01)
        >>> sortino != 0
        True
    """
    mean_return = sum(returns) / len(returns)
    excess_return = mean_return - risk_free_rate / 252
    
    # Downside deviation
    downside_returns = [min(r - target_return, 0) for r in returns]
    downside_std = math.sqrt(sum(r ** 2 for r in downside_returns) / len(downside_returns))
    
    return (excess_return * math.sqrt(252)) / downside_std if downside_std != 0 else 0

def max_drawdown(prices: List[float]) -> float:
    """Calculate maximum drawdown.
    
    Args:
        prices: Price series
        
    Returns:
        Max drawdown (as decimal, e.g., 0.20 = 20%)
        
    Example:
        >>> prices = [100, 110, 105, 95, 100]
        >>> mdd = max_drawdown(prices)
        >>> 0.13 < mdd < 0.14
        True
    """
    max_dd = 0
    peak = prices[0]
    
    for price in prices:
        if price > peak:
            peak = price
        
        dd = (peak - price) / peak
        if dd > max_dd:
            max_dd = dd
    
    return max_dd

def calmar_ratio(returns: List[float], prices: List[float]) -> float:
    """Calculate Calmar ratio.
    
    Args:
        returns: Return series
        prices: Price series
        
    Returns:
        Calmar ratio
        
    Example:
        >>> returns = [0.01] * 252
        >>> prices = [100 * (1.01 ** i) for i in range(252)]
        >>> calmar = calmar_ratio(returns, prices)
        >>> calmar > 0
        True
    """
    annual_return = (sum(returns) / len(returns)) * 252
    mdd = max_drawdown(prices)
    
    return annual_return / mdd if mdd != 0 else 0

def alpha(stock_returns: List[float], market_returns: List[float],
          risk_free_rate: float = 0.02) -> float:
    """Calculate Jensen's alpha.
    
    Args:
        stock_returns: Stock returns
        market_returns: Market returns
        risk_free_rate: Risk-free rate
        
    Returns:
        Alpha
        
    Example:
        >>> stock = [0.015, 0.02, 0.01]
        >>> market = [0.01, 0.015, 0.012]
        >>> a = alpha(stock, market, 0.01)
        >>> isinstance(a, float)
        True
    """
    beta = beta_coefficient(stock_returns, market_returns)
    stock_return = sum(stock_returns) / len(stock_returns)
    market_return = sum(market_returns) / len(market_returns)
    rf_daily = risk_free_rate / 252
    
    return stock_return - (rf_daily + beta * (market_return - rf_daily))

def treynor_ratio(returns: List[float], market_returns: List[float],
                  risk_free_rate: float = 0.02) -> float:
    """Calculate Treynor ratio.
    
    Args:
        returns: Return series
        market_returns: Market returns
        risk_free_rate: Risk-free rate
        
    Returns:
        Treynor ratio
        
    Example:
        >>> returns = [0.01, 0.02, 0.015]
        >>> market = [0.01, 0.015, 0.012]
        >>> treynor = treynor_ratio(returns, market, 0.01)
        >>> isinstance(treynor, float)
        True
    """
    beta = beta_coefficient(returns, market_returns)
    mean_return = sum(returns) / len(returns)
    rf_daily = risk_free_rate / 252
    
    return (mean_return - rf_daily) / beta if beta != 0 else 0

def information_ratio(returns: List[float], benchmark_returns: List[float]) -> float:
    """Calculate information ratio.
    
    Args:
        returns: Portfolio returns
        benchmark_returns: Benchmark returns
        
    Returns:
        Information ratio
        
    Example:
        >>> portfolio = [0.01, 0.02, 0.015]
        >>> benchmark = [0.01, 0.015, 0.012]
        >>> ir = information_ratio(portfolio, benchmark)
        >>> isinstance(ir, float)
        True
    """
    tracking_errors = [r - b for r, b in zip(returns, benchmark_returns)]
    mean_te = sum(tracking_errors) / len(tracking_errors)
    std_te = math.sqrt(sum((te - mean_te) ** 2 for te in tracking_errors) / len(tracking_errors))
    
    return mean_te / std_te if std_te != 0 else 0

def value_at_risk(returns: List[float], confidence: float = 0.95) -> float:
    """Calculate Value at Risk (VaR).
    
    Args:
        returns: Return series
        confidence: Confidence level
        
    Returns:
        VaR (as positive number for loss)
        
    Example:
        >>> returns = [0.01, -0.02, 0.015, -0.01, 0.02]
        >>> var = value_at_risk(returns, 0.95)
        >>> var > 0
        True
    """
    sorted_returns = sorted(returns)
    index = int((1 - confidence) * len(sorted_returns))
    return -sorted_returns[index]

def expected_shortfall(returns: List[float], confidence: float = 0.95) -> float:
    """Calculate Expected Shortfall (CVaR).
    
    Args:
        returns: Return series
        confidence: Confidence level
        
    Returns:
        Expected shortfall
        
    Example:
        >>> returns = [0.01, -0.02, 0.015, -0.01, 0.02, -0.03]
        >>> es = expected_shortfall(returns, 0.95)
        >>> es > 0
        True
    """
    sorted_returns = sorted(returns)
    index = int((1 - confidence) * len(sorted_returns))
    tail_returns = sorted_returns[:index+1]
    return -sum(tail_returns) / len(tail_returns) if tail_returns else 0

def portfolio_return(weights: List[float], returns: List[List[float]]) -> float:
    """Calculate portfolio return.
    
    Args:
        weights: Asset weights
        returns: Returns for each asset
        
    Returns:
        Portfolio return
        
    Example:
        >>> weights = [0.5, 0.5]
        >>> returns = [[0.01, 0.02], [0.015, 0.018]]
        >>> pr = portfolio_return(weights, returns)
        >>> pr > 0
        True
    """
    asset_returns = [sum(r) / len(r) for r in returns]
    return sum(w * r for w, r in zip(weights, asset_returns))

def portfolio_variance(weights: List[float], cov_matrix: List[List[float]]) -> float:
    """Calculate portfolio variance.
    
    Args:
        weights: Asset weights
        cov_matrix: Covariance matrix
        
    Returns:
        Portfolio variance
        
    Example:
        >>> weights = [0.5, 0.5]
        >>> cov = [[0.04, 0.01], [0.01, 0.09]]
        >>> pv = portfolio_variance(weights, cov)
        >>> pv > 0
        True
    """
    variance = 0
    for i in range(len(weights)):
        for j in range(len(weights)):
            variance += weights[i] * weights[j] * cov_matrix[i][j]
    return variance

def portfolio_sharpe(weights: List[float], returns: List[List[float]],
                     cov_matrix: List[List[float]], risk_free_rate: float = 0.02) -> float:
    """Calculate portfolio Sharpe ratio.
    
    Args:
        weights: Asset weights
        returns: Returns for each asset
        cov_matrix: Covariance matrix
        risk_free_rate: Risk-free rate
        
    Returns:
        Portfolio Sharpe ratio
        
    Example:
        >>> weights = [0.5, 0.5]
        >>> returns = [[0.01, 0.02], [0.015, 0.018]]
        >>> cov = [[0.0001, 0.00005], [0.00005, 0.0002]]
        >>> ps = portfolio_sharpe(weights, returns, cov, 0.01)
        >>> isinstance(ps, float)
        True
    """
    port_return = portfolio_return(weights, returns)
    port_std = math.sqrt(portfolio_variance(weights, cov_matrix))
    
    return (port_return - risk_free_rate / 252) / port_std if port_std != 0 else 0

def correlation_matrix(returns: List[List[float]]) -> List[List[float]]:
    """Calculate correlation matrix.
    
    Args:
        returns: Returns for each asset
        
    Returns:
        Correlation matrix
        
    Example:
        >>> returns = [[0.01, 0.02, 0.015], [0.012, 0.018, 0.016]]
        >>> corr = correlation_matrix(returns)
        >>> len(corr) == 2
        True
    """
    n = len(returns)
    means = [sum(r) / len(r) for r in returns]
    
    corr = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            if i == j:
                corr[i][j] = 1.0
            else:
                cov = sum((returns[i][k] - means[i]) * (returns[j][k] - means[j]) 
                         for k in range(len(returns[i]))) / len(returns[i])
                std_i = math.sqrt(sum((returns[i][k] - means[i]) ** 2 
                                     for k in range(len(returns[i]))) / len(returns[i]))
                std_j = math.sqrt(sum((returns[j][k] - means[j]) ** 2 
                                     for k in range(len(returns[j]))) / len(returns[j]))
                
                corr[i][j] = cov / (std_i * std_j) if std_i * std_j != 0 else 0
    
    return corr

def covariance_matrix(returns: List[List[float]]) -> List[List[float]]:
    """Calculate covariance matrix.
    
    Args:
        returns: Returns for each asset
        
    Returns:
        Covariance matrix
        
    Example:
        >>> returns = [[0.01, 0.02, 0.015], [0.012, 0.018, 0.016]]
        >>> cov = covariance_matrix(returns)
        >>> len(cov) == 2
        True
    """
    n = len(returns)
    means = [sum(r) / len(r) for r in returns]
    
    cov = [[0.0] * n for _ in range(n)]
    
    for i in range(n):
        for j in range(n):
            cov[i][j] = sum((returns[i][k] - means[i]) * (returns[j][k] - means[j]) 
                           for k in range(len(returns[i]))) / len(returns[i])
    
    return cov
