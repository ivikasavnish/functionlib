"""
Probability Functions

Probability distributions, combinatorics, and probabilistic calculations.
"""

import math
import random
from typing import List, Tuple


def factorial(n: int) -> int:
    """
    Computes factorial
    
    Args:
        n: Non-negative integer
        
    Returns:
        n!
        
    Example:
        >>> factorial(5)
        120
    """
    if n < 0:
        raise ValueError("Factorial undefined for negative numbers")
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


def permutations(n: int, r: int) -> int:
    """
    Number of permutations: P(n, r) = n!/(n-r)!
    
    Args:
        n: Total items
        r: Items to choose
        
    Returns:
        Number of permutations
        
    Example:
        >>> permutations(5, 3)
        60
    """
    if r > n or r < 0:
        return 0
    
    return factorial(n) // factorial(n - r)


def combinations(n: int, r: int) -> int:
    """
    Number of combinations: C(n, r) = n!/(r!(n-r)!)
    
    Args:
        n: Total items
        r: Items to choose
        
    Returns:
        Number of combinations
        
    Example:
        >>> combinations(5, 3)
        10
    """
    if r > n or r < 0:
        return 0
    
    r = min(r, n - r)  # Optimization
    
    result = 1
    for i in range(r):
        result = result * (n - i) // (i + 1)
    
    return result


def probability_union(p_a: float, p_b: float, p_both: float = 0) -> float:
    """
    Probability of A or B: P(A ∪ B) = P(A) + P(B) - P(A ∩ B)
    
    Args:
        p_a: Probability of A
        p_b: Probability of B
        p_both: Probability of both (default 0 for independent)
        
    Returns:
        P(A ∪ B)
        
    Example:
        >>> probability_union(0.3, 0.4, 0.1)
        0.6
    """
    return p_a + p_b - p_both


def probability_intersection(p_a: float, p_b: float) -> float:
    """
    Probability of both A and B for independent events: P(A ∩ B) = P(A) × P(B)
    
    Args:
        p_a: Probability of A
        p_b: Probability of B
        
    Returns:
        P(A ∩ B)
        
    Example:
        >>> probability_intersection(0.5, 0.6)
        0.3
    """
    return p_a * p_b


def conditional_probability(p_b_given_a: float, p_a: float) -> float:
    """
    Computes P(A and B) given P(B|A) and P(A)
    
    Args:
        p_b_given_a: P(B|A)
        p_a: P(A)
        
    Returns:
        P(A ∩ B)
        
    Example:
        >>> conditional_probability(0.8, 0.5)
        0.4
    """
    return p_b_given_a * p_a


def bayes_theorem(p_b_given_a: float, p_a: float, p_b: float) -> float:
    """
    Bayes' theorem: P(A|B) = P(B|A) × P(A) / P(B)
    
    Args:
        p_b_given_a: P(B|A)
        p_a: P(A)
        p_b: P(B)
        
    Returns:
        P(A|B)
        
    Example:
        >>> bayes_theorem(0.9, 0.01, 0.05)
        0.18
    """
    if p_b == 0:
        raise ValueError("P(B) cannot be zero")
    
    return (p_b_given_a * p_a) / p_b


def expected_value(values: List[float], probabilities: List[float]) -> float:
    """
    Computes expected value: E[X] = Σ(x × P(x))
    
    Args:
        values: List of values
        probabilities: Corresponding probabilities
        
    Returns:
        Expected value
        
    Example:
        >>> expected_value([1, 2, 3], [0.2, 0.5, 0.3])
        2.1
    """
    if len(values) != len(probabilities):
        raise ValueError("Values and probabilities must have same length")
    
    if abs(sum(probabilities) - 1.0) > 1e-6:
        raise ValueError("Probabilities must sum to 1")
    
    return sum(v * p for v, p in zip(values, probabilities))


def variance_discrete(values: List[float], probabilities: List[float]) -> float:
    """
    Computes variance of discrete distribution
    
    Args:
        values: List of values
        probabilities: Corresponding probabilities
        
    Returns:
        Variance
        
    Example:
        >>> variance_discrete([1, 2, 3], [0.2, 0.5, 0.3])
        0.49
    """
    ev = expected_value(values, probabilities)
    return sum(p * (v - ev) ** 2 for v, p in zip(values, probabilities))


def binomial_probability(n: int, k: int, p: float) -> float:
    """
    Binomial probability: P(X=k) = C(n,k) × p^k × (1-p)^(n-k)
    
    Args:
        n: Number of trials
        k: Number of successes
        p: Probability of success
        
    Returns:
        Probability
        
    Example:
        >>> binomial_probability(10, 3, 0.5)
        0.1171875
    """
    return combinations(n, k) * (p ** k) * ((1 - p) ** (n - k))


def binomial_expected_value(n: int, p: float) -> float:
    """
    Expected value of binomial distribution: E[X] = np
    
    Args:
        n: Number of trials
        p: Probability of success
        
    Returns:
        Expected value
        
    Example:
        >>> binomial_expected_value(10, 0.5)
        5.0
    """
    return n * p


def binomial_variance(n: int, p: float) -> float:
    """
    Variance of binomial distribution: Var(X) = np(1-p)
    
    Args:
        n: Number of trials
        p: Probability of success
        
    Returns:
        Variance
        
    Example:
        >>> binomial_variance(10, 0.5)
        2.5
    """
    return n * p * (1 - p)


def geometric_probability(k: int, p: float) -> float:
    """
    Geometric probability: P(X=k) = (1-p)^(k-1) × p
    
    Args:
        k: Trial number of first success
        p: Probability of success
        
    Returns:
        Probability
        
    Example:
        >>> geometric_probability(3, 0.5)
        0.125
    """
    return ((1 - p) ** (k - 1)) * p


def poisson_probability(k: int, lambda_: float) -> float:
    """
    Poisson probability: P(X=k) = (λ^k × e^(-λ)) / k!
    
    Args:
        k: Number of events
        lambda_: Average rate (λ)
        
    Returns:
        Probability
        
    Example:
        >>> poisson_probability(3, 2.5)
        0.21376...
    """
    return (lambda_ ** k * math.exp(-lambda_)) / factorial(k)


def normal_pdf(x: float, mu: float = 0, sigma: float = 1) -> float:
    """
    Normal (Gaussian) probability density function
    
    Args:
        x: Value
        mu: Mean
        sigma: Standard deviation
        
    Returns:
        Probability density
        
    Example:
        >>> normal_pdf(0, 0, 1)
        0.3989422804014327
    """
    return (1 / (sigma * math.sqrt(2 * math.pi))) * math.exp(-0.5 * ((x - mu) / sigma) ** 2)


def standard_normal_cdf(z: float) -> float:
    """
    Cumulative distribution function for standard normal (approximation)
    
    Args:
        z: Z-score
        
    Returns:
        P(Z ≤ z)
        
    Example:
        >>> standard_normal_cdf(0)
        0.5
    """
    # Using approximation formula
    return 0.5 * (1 + math.erf(z / math.sqrt(2)))


def z_score_probability(z: float) -> float:
    """
    Probability that Z ≤ z for standard normal distribution
    
    Args:
        z: Z-score
        
    Returns:
        Probability
        
    Example:
        >>> z_score_probability(1.96)
        0.975...
    """
    return standard_normal_cdf(z)


def confidence_interval_mean(mean: float, std_error: float, confidence: float = 0.95) -> Tuple[float, float]:
    """
    Confidence interval for mean (using z-score)
    
    Args:
        mean: Sample mean
        std_error: Standard error
        confidence: Confidence level (default 0.95)
        
    Returns:
        Tuple of (lower bound, upper bound)
        
    Example:
        >>> confidence_interval_mean(100, 5, 0.95)
        (90.2, 109.8)
    """
    # Z-scores for common confidence levels
    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    
    if confidence not in z_scores:
        raise ValueError("Confidence level must be 0.90, 0.95, or 0.99")
    
    z = z_scores[confidence]
    margin = z * std_error
    
    return (mean - margin, mean + margin)


def sample_size_proportion(margin: float, confidence: float = 0.95, p: float = 0.5) -> int:
    """
    Required sample size for proportion
    
    Args:
        margin: Margin of error
        confidence: Confidence level
        p: Estimated proportion
        
    Returns:
        Required sample size
        
    Example:
        >>> sample_size_proportion(0.05, 0.95)
        384
    """
    z_scores = {0.90: 1.645, 0.95: 1.96, 0.99: 2.576}
    
    if confidence not in z_scores:
        raise ValueError("Confidence level must be 0.90, 0.95, or 0.99")
    
    z = z_scores[confidence]
    n = (z ** 2 * p * (1 - p)) / (margin ** 2)
    
    return math.ceil(n)


def odds_to_probability(odds: float) -> float:
    """
    Converts odds to probability: P = odds / (1 + odds)
    
    Args:
        odds: Odds value
        
    Returns:
        Probability
        
    Example:
        >>> odds_to_probability(3)
        0.75
    """
    return odds / (1 + odds)


def probability_to_odds(probability: float) -> float:
    """
    Converts probability to odds: odds = P / (1 - P)
    
    Args:
        probability: Probability value
        
    Returns:
        Odds
        
    Example:
        >>> probability_to_odds(0.75)
        3.0
    """
    if probability >= 1:
        raise ValueError("Probability must be less than 1")
    
    return probability / (1 - probability)


def monte_carlo_pi(samples: int = 10000) -> float:
    """
    Estimates π using Monte Carlo method
    
    Args:
        samples: Number of random samples
        
    Returns:
        Estimate of π
        
    Example:
        >>> pi_estimate = monte_carlo_pi(100000)
        >>> 3.0 < pi_estimate < 3.3
        True
    """
    inside_circle = 0
    
    for _ in range(samples):
        x = random.uniform(-1, 1)
        y = random.uniform(-1, 1)
        
        if x**2 + y**2 <= 1:
            inside_circle += 1
    
    return 4 * inside_circle / samples


def birthday_paradox(n: int) -> float:
    """
    Probability that at least 2 people share a birthday in group of n
    
    Args:
        n: Number of people
        
    Returns:
        Probability
        
    Example:
        >>> birthday_paradox(23)
        0.507...
    """
    if n > 365:
        return 1.0
    
    # Probability that all have different birthdays
    prob_all_different = 1.0
    
    for i in range(n):
        prob_all_different *= (365 - i) / 365
    
    return 1 - prob_all_different


# Export all functions
__all__ = [
    'factorial', 'permutations', 'combinations',
    'probability_union', 'probability_intersection', 'conditional_probability',
    'bayes_theorem', 'expected_value', 'variance_discrete',
    'binomial_probability', 'binomial_expected_value', 'binomial_variance',
    'geometric_probability', 'poisson_probability',
    'normal_pdf', 'standard_normal_cdf', 'z_score_probability',
    'confidence_interval_mean', 'sample_size_proportion',
    'odds_to_probability', 'probability_to_odds',
    'monte_carlo_pi', 'birthday_paradox',
]
