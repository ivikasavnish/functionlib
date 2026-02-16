"""Advanced statistical tests and methods."""

import math
from typing import List, Tuple, Optional

__all__ = [
    'z_test',
    'z_test_two_sample',
    't_test_one_sample',
    't_test_two_sample',
    't_test_paired',
    'chi_square_test',
    'chi_square_goodness_of_fit',
    'chi_square_independence',
    'anova_one_way',
    'f_statistic',
    'f_test',
    'confidence_interval_mean',
    'confidence_interval_proportion',
    'margin_of_error',
    'sample_size_mean',
    'sample_size_proportion',
    'cohens_d',
    'effect_size_r',
    'cramers_v',
    'power_analysis',
    'p_value_from_z',
    'p_value_from_t',
    'critical_value_z',
    'critical_value_t',
    'pooled_variance',
    'standard_error',
    'degrees_of_freedom',
]

def z_test(sample_mean: float, pop_mean: float, pop_std: float,
           n: int) -> Tuple[float, float]:
    """One-sample z-test.
    
    Args:
        sample_mean: Sample mean
        pop_mean: Population mean (null hypothesis)
        pop_std: Population standard deviation
        n: Sample size
        
    Returns:
        (z_score, p_value)
        
    Example:
        >>> z_score, p_value = z_test(105, 100, 15, 30)
        >>> z_score > 1.5
        True
    """
    se = pop_std / math.sqrt(n)
    z_score = (sample_mean - pop_mean) / se
    p_value = 2 * (1 - _normal_cdf(abs(z_score)))
    return z_score, p_value

def z_test_two_sample(mean1: float, mean2: float, std1: float, std2: float,
                      n1: int, n2: int) -> Tuple[float, float]:
    """Two-sample z-test.
    
    Args:
        mean1: First sample mean
        mean2: Second sample mean
        std1: First population std dev
        std2: Second population std dev
        n1: First sample size
        n2: Second sample size
        
    Returns:
        (z_score, p_value)
        
    Example:
        >>> z_score, p_value = z_test_two_sample(105, 100, 15, 15, 30, 30)
        >>> abs(z_score) > 0
        True
    """
    se = math.sqrt((std1**2 / n1) + (std2**2 / n2))
    z_score = (mean1 - mean2) / se
    p_value = 2 * (1 - _normal_cdf(abs(z_score)))
    return z_score, p_value

def t_test_one_sample(data: List[float], pop_mean: float) -> Tuple[float, float, int]:
    """One-sample t-test.
    
    Args:
        data: Sample data
        pop_mean: Population mean (null hypothesis)
        
    Returns:
        (t_statistic, p_value, degrees_of_freedom)
        
    Example:
        >>> data = [12, 14, 13, 15, 12, 14, 13]
        >>> t_stat, p_val, df = t_test_one_sample(data, 10)
        >>> t_stat > 0
        True
    """
    n = len(data)
    sample_mean = sum(data) / n
    sample_std = math.sqrt(sum((x - sample_mean)**2 for x in data) / (n - 1))
    se = sample_std / math.sqrt(n)
    t_statistic = (sample_mean - pop_mean) / se
    df = n - 1
    p_value = 2 * _t_distribution_cdf(-abs(t_statistic), df)
    return t_statistic, p_value, df

def t_test_two_sample(data1: List[float], data2: List[float],
                      equal_var: bool = True) -> Tuple[float, float, int]:
    """Two-sample t-test.
    
    Args:
        data1: First sample
        data2: Second sample
        equal_var: Assume equal variances
        
    Returns:
        (t_statistic, p_value, degrees_of_freedom)
        
    Example:
        >>> data1 = [12, 14, 13, 15, 12]
        >>> data2 = [10, 11, 9, 12, 11]
        >>> t_stat, p_val, df = t_test_two_sample(data1, data2)
        >>> t_stat > 0
        True
    """
    n1, n2 = len(data1), len(data2)
    mean1 = sum(data1) / n1
    mean2 = sum(data2) / n2
    var1 = sum((x - mean1)**2 for x in data1) / (n1 - 1)
    var2 = sum((x - mean2)**2 for x in data2) / (n2 - 1)
    
    if equal_var:
        # Pooled variance
        pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
        se = math.sqrt(pooled_var * (1/n1 + 1/n2))
        df = n1 + n2 - 2
    else:
        # Welch's t-test
        se = math.sqrt(var1/n1 + var2/n2)
        df = int((var1/n1 + var2/n2)**2 / 
                ((var1/n1)**2/(n1-1) + (var2/n2)**2/(n2-1)))
    
    t_statistic = (mean1 - mean2) / se
    p_value = 2 * _t_distribution_cdf(-abs(t_statistic), df)
    return t_statistic, p_value, df

def t_test_paired(data1: List[float], data2: List[float]) -> Tuple[float, float, int]:
    """Paired t-test.
    
    Args:
        data1: First measurements
        data2: Second measurements (paired with data1)
        
    Returns:
        (t_statistic, p_value, degrees_of_freedom)
        
    Example:
        >>> before = [120, 130, 125, 135, 128]
        >>> after = [115, 125, 120, 130, 122]
        >>> t_stat, p_val, df = t_test_paired(before, after)
        >>> t_stat > 0
        True
    """
    if len(data1) != len(data2):
        raise ValueError("Paired samples must have same length")
    
    differences = [data1[i] - data2[i] for i in range(len(data1))]
    return t_test_one_sample(differences, 0)

def chi_square_test(observed: List[float], expected: List[float]) -> Tuple[float, int, float]:
    """Chi-square test.
    
    Args:
        observed: Observed frequencies
        expected: Expected frequencies
        
    Returns:
        (chi_square_statistic, degrees_of_freedom, p_value)
        
    Example:
        >>> observed = [20, 30, 25, 25]
        >>> expected = [25, 25, 25, 25]
        >>> chi2, df, p_val = chi_square_test(observed, expected)
        >>> chi2 > 0
        True
    """
    if len(observed) != len(expected):
        raise ValueError("Observed and expected must have same length")
    
    chi_square = sum((o - e)**2 / e for o, e in zip(observed, expected) if e > 0)
    df = len(observed) - 1
    p_value = _chi_square_p_value(chi_square, df)
    return chi_square, df, p_value

def chi_square_goodness_of_fit(observed: List[float], 
                                probabilities: Optional[List[float]] = None) -> Tuple[float, int, float]:
    """Chi-square goodness of fit test.
    
    Args:
        observed: Observed frequencies
        probabilities: Expected probabilities (default: uniform)
        
    Returns:
        (chi_square_statistic, degrees_of_freedom, p_value)
        
    Example:
        >>> observed = [15, 20, 25, 40]
        >>> chi2, df, p_val = chi_square_goodness_of_fit(observed)
        >>> df == 3
        True
    """
    n = sum(observed)
    
    if probabilities is None:
        probabilities = [1.0 / len(observed)] * len(observed)
    
    expected = [p * n for p in probabilities]
    return chi_square_test(observed, expected)

def chi_square_independence(contingency_table: List[List[int]]) -> Tuple[float, int, float]:
    """Chi-square test of independence.
    
    Args:
        contingency_table: 2D table of observed frequencies
        
    Returns:
        (chi_square_statistic, degrees_of_freedom, p_value)
        
    Example:
        >>> table = [[10, 20, 30], [15, 25, 10]]
        >>> chi2, df, p_val = chi_square_independence(table)
        >>> df == 2
        True
    """
    n_rows = len(contingency_table)
    n_cols = len(contingency_table[0])
    
    # Row and column totals
    row_totals = [sum(row) for row in contingency_table]
    col_totals = [sum(contingency_table[i][j] for i in range(n_rows)) for j in range(n_cols)]
    total = sum(row_totals)
    
    # Expected frequencies
    chi_square = 0
    for i in range(n_rows):
        for j in range(n_cols):
            expected = (row_totals[i] * col_totals[j]) / total
            if expected > 0:
                chi_square += (contingency_table[i][j] - expected)**2 / expected
    
    df = (n_rows - 1) * (n_cols - 1)
    p_value = _chi_square_p_value(chi_square, df)
    return chi_square, df, p_value

def anova_one_way(*groups: List[float]) -> Tuple[float, float, int, int]:
    """One-way ANOVA test.
    
    Args:
        *groups: Variable number of groups
        
    Returns:
        (f_statistic, p_value, df_between, df_within)
        
    Example:
        >>> group1 = [12, 14, 13, 15]
        >>> group2 = [10, 11, 9, 12]
        >>> group3 = [8, 9, 7, 10]
        >>> f_stat, p_val, df1, df2 = anova_one_way(group1, group2, group3)
        >>> f_stat > 0
        True
    """
    k = len(groups)  # Number of groups
    n = sum(len(group) for group in groups)  # Total sample size
    
    # Grand mean
    all_data = [x for group in groups for x in group]
    grand_mean = sum(all_data) / n
    
    # Between-group sum of squares
    ss_between = sum(len(group) * (sum(group)/len(group) - grand_mean)**2 
                     for group in groups)
    
    # Within-group sum of squares
    ss_within = sum(sum((x - sum(group)/len(group))**2 for x in group) 
                    for group in groups)
    
    # Degrees of freedom
    df_between = k - 1
    df_within = n - k
    
    # Mean squares
    ms_between = ss_between / df_between
    ms_within = ss_within / df_within if df_within > 0 else 0
    
    # F-statistic
    f_statistic = ms_between / ms_within if ms_within > 0 else 0
    p_value = _f_distribution_p_value(f_statistic, df_between, df_within)
    
    return f_statistic, p_value, df_between, df_within

def f_statistic(var1: float, var2: float) -> float:
    """Calculate F-statistic from two variances.
    
    Args:
        var1: First variance
        var2: Second variance
        
    Returns:
        F-statistic (larger variance / smaller variance)
        
    Example:
        >>> f_stat(25, 16)
        1.5625
    """
    return max(var1, var2) / min(var1, var2) if min(var1, var2) > 0 else 0

def f_test(data1: List[float], data2: List[float]) -> Tuple[float, int, int, float]:
    """F-test for equality of variances.
    
    Args:
        data1: First sample
        data2: Second sample
        
    Returns:
        (f_statistic, df1, df2, p_value)
        
    Example:
        >>> data1 = [12, 14, 13, 15, 12, 14]
        >>> data2 = [10, 11, 9, 12, 11, 10]
        >>> f_stat, df1, df2, p_val = f_test(data1, data2)
        >>> f_stat > 0
        True
    """
    n1, n2 = len(data1), len(data2)
    mean1 = sum(data1) / n1
    mean2 = sum(data2) / n2
    var1 = sum((x - mean1)**2 for x in data1) / (n1 - 1)
    var2 = sum((x - mean2)**2 for x in data2) / (n2 - 1)
    
    f = var1 / var2 if var1 > var2 else var2 / var1
    df1 = n1 - 1 if var1 > var2 else n2 - 1
    df2 = n2 - 1 if var1 > var2 else n1 - 1
    
    p_value = _f_distribution_p_value(f, df1, df2)
    return f, df1, df2, p_value

def confidence_interval_mean(data: List[float], confidence: float = 0.95) -> Tuple[float, float]:
    """Confidence interval for mean.
    
    Args:
        data: Sample data
        confidence: Confidence level (default 0.95)
        
    Returns:
        (lower_bound, upper_bound)
        
    Example:
        >>> data = [10, 12, 11, 13, 12, 14, 11, 13]
        >>> lower, upper = confidence_interval_mean(data, 0.95)
        >>> lower < upper
        True
    """
    n = len(data)
    mean = sum(data) / n
    std = math.sqrt(sum((x - mean)**2 for x in data) / (n - 1))
    se = std / math.sqrt(n)
    
    # Use t-distribution
    t_crit = _t_critical_value(1 - (1 - confidence) / 2, n - 1)
    margin = t_crit * se
    
    return mean - margin, mean + margin

def confidence_interval_proportion(p: float, n: int, confidence: float = 0.95) -> Tuple[float, float]:
    """Confidence interval for proportion.
    
    Args:
        p: Sample proportion
        n: Sample size
        confidence: Confidence level (default 0.95)
        
    Returns:
        (lower_bound, upper_bound)
        
    Example:
        >>> lower, upper = confidence_interval_proportion(0.6, 100, 0.95)
        >>> 0.5 < lower < 0.6 < upper < 0.7
        True
    """
    z_crit = _z_critical_value(1 - (1 - confidence) / 2)
    se = math.sqrt(p * (1 - p) / n)
    margin = z_crit * se
    
    return max(0, p - margin), min(1, p + margin)

def margin_of_error(std: float, n: int, confidence: float = 0.95) -> float:
    """Calculate margin of error.
    
    Args:
        std: Standard deviation
        n: Sample size
        confidence: Confidence level
        
    Returns:
        Margin of error
        
    Example:
        >>> moe = margin_of_error(15, 100, 0.95)
        >>> 2.5 < moe < 3.5
        True
    """
    z_crit = _z_critical_value(1 - (1 - confidence) / 2)
    se = std / math.sqrt(n)
    return z_crit * se

def sample_size_mean(std: float, margin: float, confidence: float = 0.95) -> int:
    """Required sample size for mean estimation.
    
    Args:
        std: Population standard deviation
        margin: Desired margin of error
        confidence: Confidence level
        
    Returns:
        Required sample size
        
    Example:
        >>> n = sample_size_mean(15, 3, 0.95)
        >>> n > 0
        True
    """
    z_crit = _z_critical_value(1 - (1 - confidence) / 2)
    n = (z_crit * std / margin)**2
    return int(math.ceil(n))

def sample_size_proportion(p: float, margin: float, confidence: float = 0.95) -> int:
    """Required sample size for proportion estimation.
    
    Args:
        p: Expected proportion
        margin: Desired margin of error
        confidence: Confidence level
        
    Returns:
        Required sample size
        
    Example:
        >>> n = sample_size_proportion(0.5, 0.05, 0.95)
        >>> n > 300
        True
    """
    z_crit = _z_critical_value(1 - (1 - confidence) / 2)
    n = (z_crit**2 * p * (1 - p)) / margin**2
    return int(math.ceil(n))

def cohens_d(data1: List[float], data2: List[float]) -> float:
    """Calculate Cohen's d effect size.
    
    Args:
        data1: First sample
        data2: Second sample
        
    Returns:
        Cohen's d
        
    Example:
        >>> data1 = [12, 14, 13, 15, 12]
        >>> data2 = [10, 11, 9, 12, 11]
        >>> d = cohens_d(data1, data2)
        >>> d > 0
        True
    """
    n1, n2 = len(data1), len(data2)
    mean1 = sum(data1) / n1
    mean2 = sum(data2) / n2
    var1 = sum((x - mean1)**2 for x in data1) / (n1 - 1)
    var2 = sum((x - mean2)**2 for x in data2) / (n2 - 1)
    
    # Pooled standard deviation
    pooled_std = math.sqrt(((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2))
    
    return (mean1 - mean2) / pooled_std if pooled_std > 0 else 0

def effect_size_r(t: float, df: int) -> float:
    """Calculate effect size r from t-statistic.
    
    Args:
        t: t-statistic
        df: Degrees of freedom
        
    Returns:
        Effect size r
        
    Example:
        >>> r = effect_size_r(2.5, 20)
        >>> 0 < r < 1
        True
    """
    return math.sqrt(t**2 / (t**2 + df))

def cramers_v(chi_square: float, n: int, min_dim: int) -> float:
    """Calculate Cramér's V effect size for chi-square.
    
    Args:
        chi_square: Chi-square statistic
        n: Total sample size
        min_dim: Minimum of (rows-1, cols-1)
        
    Returns:
        Cramér's V
        
    Example:
        >>> v = cramers_v(10.5, 100, 2)
        >>> 0 <= v <= 1
        True
    """
    return math.sqrt(chi_square / (n * min_dim))

def power_analysis(effect_size: float, alpha: float, n: int) -> float:
    """Estimate statistical power (simplified).
    
    Args:
        effect_size: Effect size (Cohen's d)
        alpha: Significance level
        n: Sample size per group
        
    Returns:
        Estimated power
        
    Example:
        >>> power = power_analysis(0.5, 0.05, 30)
        >>> 0 < power < 1
        True
    """
    # Simplified power calculation using normal approximation
    z_alpha = _z_critical_value(1 - alpha / 2)
    z_beta = effect_size * math.sqrt(n / 2) - z_alpha
    power = _normal_cdf(z_beta)
    return max(0, min(1, power))

def p_value_from_z(z: float, two_tailed: bool = True) -> float:
    """Calculate p-value from z-score.
    
    Args:
        z: Z-score
        two_tailed: Two-tailed test
        
    Returns:
        P-value
        
    Example:
        >>> p = p_value_from_z(1.96)
        >>> 0.04 < p < 0.06
        True
    """
    p = 1 - _normal_cdf(abs(z))
    return 2 * p if two_tailed else p

def p_value_from_t(t: float, df: int, two_tailed: bool = True) -> float:
    """Calculate p-value from t-statistic.
    
    Args:
        t: T-statistic
        df: Degrees of freedom
        two_tailed: Two-tailed test
        
    Returns:
        P-value
        
    Example:
        >>> p = p_value_from_t(2.0, 20)
        >>> 0 < p < 0.1
        True
    """
    p = _t_distribution_cdf(-abs(t), df)
    return 2 * p if two_tailed else p

def critical_value_z(alpha: float) -> float:
    """Calculate critical z-value.
    
    Args:
        alpha: Significance level (one-tailed)
        
    Returns:
        Critical z-value
        
    Example:
        >>> z_crit = critical_value_z(0.05)
        >>> 1.6 < z_crit < 1.7
        True
    """
    return _z_critical_value(1 - alpha)

def critical_value_t(alpha: float, df: int) -> float:
    """Calculate critical t-value.
    
    Args:
        alpha: Significance level (one-tailed)
        df: Degrees of freedom
        
    Returns:
        Critical t-value
        
    Example:
        >>> t_crit = critical_value_t(0.05, 20)
        >>> 1.7 < t_crit < 1.8
        True
    """
    return _t_critical_value(1 - alpha, df)

def pooled_variance(var1: float, var2: float, n1: int, n2: int) -> float:
    """Calculate pooled variance.
    
    Args:
        var1: First variance
        var2: Second variance
        n1: First sample size
        n2: Second sample size
        
    Returns:
        Pooled variance
        
    Example:
        >>> pooled_var = pooled_variance(25, 16, 10, 10)
        >>> 15 < pooled_var < 25
        True
    """
    return ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)

def standard_error(std: float, n: int) -> float:
    """Calculate standard error of the mean.
    
    Args:
        std: Standard deviation
        n: Sample size
        
    Returns:
        Standard error
        
    Example:
        >>> se = standard_error(15, 100)
        >>> 1.4 < se < 1.6
        True
    """
    return std / math.sqrt(n)

def degrees_of_freedom(*sample_sizes: int) -> int:
    """Calculate degrees of freedom for multiple samples.
    
    Args:
        *sample_sizes: Sample sizes
        
    Returns:
        Degrees of freedom
        
    Example:
        >>> df = degrees_of_freedom(10, 12, 15)
        >>> df == 34
        True
    """
    return sum(sample_sizes) - len(sample_sizes)

# Helper functions for distributions
def _normal_cdf(x: float) -> float:
    """Cumulative distribution function for standard normal."""
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def _z_critical_value(probability: float) -> float:
    """Inverse normal CDF (approximate)."""
    # Approximation for common values
    if probability >= 0.975:
        return 1.96
    elif probability >= 0.95:
        return 1.645
    elif probability >= 0.90:
        return 1.28
    else:
        # Simple approximation
        return math.sqrt(2) * _inverse_erf(2 * probability - 1)

def _t_critical_value(probability: float, df: int) -> float:
    """Approximate t critical value."""
    z = _z_critical_value(probability)
    # Approximation: t ≈ z for large df
    if df > 30:
        return z
    # Simple correction for small df
    return z * (1 + 1/(4*df))

def _t_distribution_cdf(t: float, df: int) -> float:
    """Approximate t-distribution CDF."""
    # For large df, approximate with normal
    if df > 30:
        return _normal_cdf(t)
    # Simple approximation for small df
    return _normal_cdf(t / (1 + 1/(4*df)))

def _chi_square_p_value(chi_square: float, df: int) -> float:
    """Approximate chi-square p-value."""
    # Simple approximation using normal distribution
    if df > 30:
        z = (chi_square - df) / math.sqrt(2 * df)
        return 1 - _normal_cdf(z)
    # For small df, use rough approximation
    return max(0, min(1, 1 - chi_square / (2 * df)))

def _f_distribution_p_value(f: float, df1: int, df2: int) -> float:
    """Approximate F-distribution p-value."""
    # Very rough approximation
    if f > 10:
        return 0.001
    elif f > 5:
        return 0.01
    elif f > 3:
        return 0.05
    elif f > 2:
        return 0.10
    else:
        return 0.20

def _inverse_erf(y: float) -> float:
    """Approximate inverse error function."""
    a = 0.147
    b = 2 / (math.pi * a) + math.log(1 - y**2) / 2
    sign = 1 if y >= 0 else -1
    return sign * math.sqrt(math.sqrt(b**2 - math.log(1 - y**2) / a) - b)
