"""
Random and Sampling Functions

Random number generation, sampling, and probability utilities.
"""

import random
import math
from typing import List, Any, Dict, Tuple, Callable


def random_int(min_val: int, max_val: int) -> int:
    """
    Generate random integer in range [min_val, max_val]
    
    Args:
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Random integer
        
    Example:
        >>> r = random_int(1, 10)
        >>> 1 <= r <= 10
        True
    """
    return random.randint(min_val, max_val)


def random_float(min_val: float = 0.0, max_val: float = 1.0) -> float:
    """
    Generate random float in range [min_val, max_val)
    
    Args:
        min_val: Minimum value
        max_val: Maximum value
        
    Returns:
        Random float
        
    Example:
        >>> r = random_float(0, 1)
        >>> 0 <= r < 1
        True
    """
    return random.uniform(min_val, max_val)


def random_choice(items: List[Any]) -> Any:
    """
    Choose random item from list
    
    Args:
        items: List of items
        
    Returns:
        Random item
        
    Example:
        >>> random_choice([1, 2, 3, 4, 5]) in [1, 2, 3, 4, 5]
        True
    """
    return random.choice(items)


def random_sample(items: List[Any], k: int) -> List[Any]:
    """
    Choose k random items without replacement
    
    Args:
        items: List of items
        k: Number of items to choose
        
    Returns:
        List of k random items
        
    Example:
        >>> sample = random_sample([1, 2, 3, 4, 5], 3)
        >>> len(sample) == 3
        True
    """
    return random.sample(items, k)


def shuffle_list(items: List[Any]) -> List[Any]:
    """
    Shuffle list (returns new list)
    
    Args:
        items: List to shuffle
        
    Returns:
        Shuffled list
        
    Example:
        >>> result = shuffle_list([1, 2, 3, 4, 5])
        >>> len(result) == 5
        True
    """
    shuffled = items.copy()
    random.shuffle(shuffled)
    return shuffled


def weighted_choice(items: List[Any], weights: List[float]) -> Any:
    """
    Choose random item with weights
    
    Args:
        items: List of items
        weights: List of weights
        
    Returns:
        Random item
        
    Example:
        >>> weighted_choice(['a', 'b', 'c'], [0.5, 0.3, 0.2]) in ['a', 'b', 'c']
        True
    """
    return random.choices(items, weights=weights, k=1)[0]


def weighted_sample(items: List[Any], weights: List[float], k: int) -> List[Any]:
    """
    Choose k random items with weights (with replacement)
    
    Args:
        items: List of items
        weights: List of weights
        k: Number of items
        
    Returns:
        List of k random items
        
    Example:
        >>> sample = weighted_sample(['a', 'b', 'c'], [0.5, 0.3, 0.2], 5)
        >>> len(sample) == 5
        True
    """
    return random.choices(items, weights=weights, k=k)


def random_gaussian(mu: float = 0.0, sigma: float = 1.0) -> float:
    """
    Generate random number from Gaussian distribution
    
    Args:
        mu: Mean
        sigma: Standard deviation
        
    Returns:
        Random value
        
    Example:
        >>> r = random_gaussian(0, 1)
        >>> isinstance(r, float)
        True
    """
    return random.gauss(mu, sigma)


def random_exponential(lambd: float) -> float:
    """
    Generate random number from exponential distribution
    
    Args:
        lambd: Rate parameter (1/mean)
        
    Returns:
        Random value
        
    Example:
        >>> r = random_exponential(1.0)
        >>> r >= 0
        True
    """
    return random.expovariate(lambd)


def random_poisson(lambd: float) -> int:
    """
    Generate random number from Poisson distribution (approximate)
    
    Args:
        lambd: Expected number of events
        
    Returns:
        Random integer
        
    Example:
        >>> r = random_poisson(5.0)
        >>> r >= 0
        True
    """
    # Using Knuth's algorithm
    L = math.exp(-lambd)
    k = 0
    p = 1.0
    
    while p > L:
        k += 1
        p *= random.random()
    
    return k - 1


def random_beta(alpha: float, beta: float) -> float:
    """
    Generate random number from Beta distribution
    
    Args:
        alpha: Alpha parameter
        beta: Beta parameter
        
    Returns:
        Random value in [0, 1]
        
    Example:
        >>> r = random_beta(2, 5)
        >>> 0 <= r <= 1
        True
    """
    return random.betavariate(alpha, beta)


def random_gamma(alpha: float, beta: float = 1.0) -> float:
    """
    Generate random number from Gamma distribution
    
    Args:
        alpha: Shape parameter
        beta: Scale parameter
        
    Returns:
        Random value
        
    Example:
        >>> r = random_gamma(2.0, 1.0)
        >>> r >= 0
        True
    """
    return random.gammavariate(alpha, beta)


def random_binomial(n: int, p: float) -> int:
    """
    Generate random number from binomial distribution
    
    Args:
        n: Number of trials
        p: Probability of success
        
    Returns:
        Number of successes
        
    Example:
        >>> r = random_binomial(10, 0.5)
        >>> 0 <= r <= 10
        True
    """
    return sum(1 for _ in range(n) if random.random() < p)


def random_point_in_circle(radius: float = 1.0) -> Tuple[float, float]:
    """
    Generate random point uniformly in circle
    
    Args:
        radius: Circle radius
        
    Returns:
        (x, y) coordinates
        
    Example:
        >>> x, y = random_point_in_circle(1.0)
        >>> x**2 + y**2 <= 1.0
        True
    """
    angle = random.uniform(0, 2 * math.pi)
    r = radius * math.sqrt(random.random())
    return r * math.cos(angle), r * math.sin(angle)


def random_point_on_sphere() -> Tuple[float, float, float]:
    """
    Generate random point uniformly on unit sphere
    
    Returns:
        (x, y, z) coordinates
        
    Example:
        >>> x, y, z = random_point_on_sphere()
        >>> abs(x**2 + y**2 + z**2 - 1.0) < 0.01
        True
    """
    theta = random.uniform(0, 2 * math.pi)
    u = random.uniform(-1, 1)
    c = math.sqrt(1 - u*u)
    return c * math.cos(theta), c * math.sin(theta), u


def reservoir_sampling(stream: List[Any], k: int) -> List[Any]:
    """
    Reservoir sampling: random sample from stream of unknown length
    
    Args:
        stream: Data stream (list)
        k: Sample size
        
    Returns:
        Random sample of size k
        
    Example:
        >>> sample = reservoir_sampling(range(100), 10)
        >>> len(sample) == 10
        True
    """
    reservoir = []
    
    for i, item in enumerate(stream):
        if i < k:
            reservoir.append(item)
        else:
            j = random.randint(0, i)
            if j < k:
                reservoir[j] = item
    
    return reservoir


def monte_carlo_pi(n_samples: int = 10000) -> float:
    """
    Estimate π using Monte Carlo method
    
    Args:
        n_samples: Number of random samples
        
    Returns:
        Estimate of π
        
    Example:
        >>> pi_est = monte_carlo_pi(10000)
        >>> 3.0 < pi_est < 3.3
        True
    """
    inside = 0
    
    for _ in range(n_samples):
        x, y = random.random(), random.random()
        if x*x + y*y <= 1:
            inside += 1
    
    return 4 * inside / n_samples


def bootstrap_sample(data: List[float], n_samples: int = 1000) -> List[float]:
    """
    Generate bootstrap samples (sampling with replacement)
    
    Args:
        data: Original data
        n_samples: Number of bootstrap samples
        
    Returns:
        Bootstrap sample
        
    Example:
        >>> sample = bootstrap_sample([1, 2, 3, 4, 5], 100)
        >>> len(sample) == 100
        True
    """
    return [random.choice(data) for _ in range(n_samples)]


def bootstrap_confidence_interval(data: List[float], statistic: Callable, 
                                  n_bootstrap: int = 1000, confidence: float = 0.95) -> Tuple[float, float]:
    """
    Bootstrap confidence interval for a statistic
    
    Args:
        data: Original data
        statistic: Function to compute statistic (e.g., mean, median)
        n_bootstrap: Number of bootstrap iterations
        confidence: Confidence level
        
    Returns:
        (lower, upper) confidence bounds
        
    Example:
        >>> data = [1, 2, 3, 4, 5]
        >>> lower, upper = bootstrap_confidence_interval(data, lambda x: sum(x)/len(x))
        >>> lower < upper
        True
    """
    stats = []
    
    for _ in range(n_bootstrap):
        sample = bootstrap_sample(data, len(data))
        stats.append(statistic(sample))
    
    stats.sort()
    
    alpha = 1 - confidence
    lower_idx = int(alpha/2 * n_bootstrap)
    upper_idx = int((1 - alpha/2) * n_bootstrap)
    
    return stats[lower_idx], stats[upper_idx]


def random_permutation(n: int) -> List[int]:
    """
    Generate random permutation of 0 to n-1
    
    Args:
        n: Size
        
    Returns:
        Random permutation
        
    Example:
        >>> perm = random_permutation(5)
        >>> set(perm) == {0, 1, 2, 3, 4}
        True
    """
    return random.sample(range(n), n)


def random_partition(n: int, k: int) -> List[int]:
    """
    Randomly partition n into k positive integers
    
    Args:
        n: Total to partition
        k: Number of parts
        
    Returns:
        List of k integers that sum to n
        
    Example:
        >>> parts = random_partition(10, 3)
        >>> sum(parts) == 10 and len(parts) == 3
        True
    """
    # Place k-1 dividers randomly
    dividers = sorted(random.sample(range(1, n), k-1))
    dividers = [0] + dividers + [n]
    
    return [dividers[i+1] - dividers[i] for i in range(k)]


def random_walk_1d(n_steps: int, step_size: float = 1.0) -> List[float]:
    """
    Simulate 1D random walk
    
    Args:
        n_steps: Number of steps
        step_size: Size of each step
        
    Returns:
        List of positions
        
    Example:
        >>> walk = random_walk_1d(100)
        >>> len(walk) == 101
        True
    """
    position = 0
    positions = [position]
    
    for _ in range(n_steps):
        position += step_size * random.choice([-1, 1])
        positions.append(position)
    
    return positions


def random_walk_2d(n_steps: int, step_size: float = 1.0) -> List[Tuple[float, float]]:
    """
    Simulate 2D random walk
    
    Args:
        n_steps: Number of steps
        step_size: Size of each step
        
    Returns:
        List of (x, y) positions
        
    Example:
        >>> walk = random_walk_2d(100)
        >>> len(walk) == 101
        True
    """
    x, y = 0.0, 0.0
    positions = [(x, y)]
    
    for _ in range(n_steps):
        angle = random.uniform(0, 2 * math.pi)
        x += step_size * math.cos(angle)
        y += step_size * math.sin(angle)
        positions.append((x, y))
    
    return positions


def set_random_seed(seed: int) -> None:
    """
    Set random seed for reproducibility
    
    Args:
        seed: Random seed
        
    Example:
        >>> set_random_seed(42)
        >>> random_int(1, 100)
        82
    """
    random.seed(seed)


def random_string(length: int, chars: str = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789') -> str:
    """
    Generate random string
    
    Args:
        length: String length
        chars: Characters to choose from
        
    Returns:
        Random string
        
    Example:
        >>> s = random_string(10)
        >>> len(s) == 10
        True
    """
    return ''.join(random.choice(chars) for _ in range(length))


def random_hex(length: int) -> str:
    """
    Generate random hexadecimal string
    
    Args:
        length: String length
        
    Returns:
        Random hex string
        
    Example:
        >>> h = random_hex(16)
        >>> len(h) == 16
        True
    """
    return ''.join(random.choice('0123456789abcdef') for _ in range(length))


# Export all functions
__all__ = [
    'random_int', 'random_float', 'random_choice', 'random_sample', 'shuffle_list',
    'weighted_choice', 'weighted_sample',
    'random_gaussian', 'random_exponential', 'random_poisson',
    'random_beta', 'random_gamma', 'random_binomial',
    'random_point_in_circle', 'random_point_on_sphere',
    'reservoir_sampling', 'monte_carlo_pi',
    'bootstrap_sample', 'bootstrap_confidence_interval',
    'random_permutation', 'random_partition',
    'random_walk_1d', 'random_walk_2d',
    'set_random_seed', 'random_string', 'random_hex',
]
