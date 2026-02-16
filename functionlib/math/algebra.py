"""
Algebra Functions

Core algebraic operations including equation solving, polynomials, and expressions.
"""

import math
import cmath
from typing import List, Tuple, Union, Optional


def solve_linear_equation(a: float, b: float) -> float:
    """
    Solves linear equations of form ax + b = 0
    
    Args:
        a: Coefficient of x
        b: Constant term
        
    Returns:
        Solution x
        
    Example:
        >>> solve_linear_equation(2, -6)  # 2x - 6 = 0
        3.0
    """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero for a linear equation")
    return -b / a


def solve_quadratic_equation(a: float, b: float, c: float) -> Tuple[complex, complex]:
    """
    Solves quadratic equations using quadratic formula: ax² + bx + c = 0
    
    Args:
        a: Coefficient of x²
        b: Coefficient of x
        c: Constant term
        
    Returns:
        Tuple of two solutions (may be complex)
        
    Example:
        >>> solve_quadratic_equation(1, -5, 6)  # x² - 5x + 6 = 0
        ((3+0j), (2+0j))
    """
    if a == 0:
        raise ValueError("Coefficient 'a' cannot be zero for a quadratic equation")
    
    discriminant = b**2 - 4*a*c
    sqrt_discriminant = cmath.sqrt(discriminant)
    
    x1 = (-b + sqrt_discriminant) / (2*a)
    x2 = (-b - sqrt_discriminant) / (2*a)
    
    return (x1, x2)


def find_discriminant(a: float, b: float, c: float) -> float:
    """
    Calculates discriminant of quadratic equation: b² - 4ac
    
    Args:
        a: Coefficient of x²
        b: Coefficient of x
        c: Constant term
        
    Returns:
        Discriminant value
        
    Example:
        >>> find_discriminant(1, -5, 6)
        1.0
    """
    return b**2 - 4*a*c


def evaluate_polynomial(coefficients: List[float], x: float) -> float:
    """
    Evaluates polynomial at given x value using Horner's method
    
    Args:
        coefficients: List of coefficients [a_n, a_(n-1), ..., a_1, a_0]
        x: Value at which to evaluate
        
    Returns:
        Result of polynomial evaluation
        
    Example:
        >>> evaluate_polynomial([1, -5, 6], 2)  # x² - 5x + 6 at x=2
        0.0
    """
    result = 0
    for coeff in coefficients:
        result = result * x + coeff
    return result


def add_polynomials(poly1: List[float], poly2: List[float]) -> List[float]:
    """
    Adds two polynomials
    
    Args:
        poly1: First polynomial coefficients
        poly2: Second polynomial coefficients
        
    Returns:
        Sum of polynomials
        
    Example:
        >>> add_polynomials([1, 2, 3], [1, 1])  # (x² + 2x + 3) + (x + 1)
        [1, 3, 4]
    """
    # Pad shorter polynomial with zeros
    max_len = max(len(poly1), len(poly2))
    p1 = [0] * (max_len - len(poly1)) + poly1
    p2 = [0] * (max_len - len(poly2)) + poly2
    
    return [a + b for a, b in zip(p1, p2)]


def subtract_polynomials(poly1: List[float], poly2: List[float]) -> List[float]:
    """
    Subtracts second polynomial from first
    
    Args:
        poly1: First polynomial coefficients
        poly2: Second polynomial coefficients
        
    Returns:
        Difference of polynomials
        
    Example:
        >>> subtract_polynomials([1, 2, 3], [1, 1])
        [1, 1, 2]
    """
    max_len = max(len(poly1), len(poly2))
    p1 = [0] * (max_len - len(poly1)) + poly1
    p2 = [0] * (max_len - len(poly2)) + poly2
    
    return [a - b for a, b in zip(p1, p2)]


def multiply_polynomials(poly1: List[float], poly2: List[float]) -> List[float]:
    """
    Multiplies two polynomials
    
    Args:
        poly1: First polynomial coefficients
        poly2: Second polynomial coefficients
        
    Returns:
        Product of polynomials
        
    Example:
        >>> multiply_polynomials([1, 2], [1, 3])  # (x + 2)(x + 3)
        [1, 5, 6]
    """
    result = [0] * (len(poly1) + len(poly2) - 1)
    
    for i, a in enumerate(poly1):
        for j, b in enumerate(poly2):
            result[i + j] += a * b
    
    return result


def polynomial_derivative(coefficients: List[float]) -> List[float]:
    """
    Computes derivative of polynomial
    
    Args:
        coefficients: Polynomial coefficients [a_n, ..., a_0]
        
    Returns:
        Derivative coefficients
        
    Example:
        >>> polynomial_derivative([3, 2, 1])  # d/dx(3x² + 2x + 1)
        [6, 2]
    """
    if len(coefficients) <= 1:
        return [0]
    
    n = len(coefficients) - 1
    return [coefficients[i] * (n - i) for i in range(n)]


def polynomial_integral(coefficients: List[float], constant: float = 0) -> List[float]:
    """
    Computes integral of polynomial
    
    Args:
        coefficients: Polynomial coefficients
        constant: Integration constant
        
    Returns:
        Integral coefficients
        
    Example:
        >>> polynomial_integral([2, 3])  # ∫(2x + 3)dx
        [1.0, 3.0, 0]
    """
    n = len(coefficients)
    result = []
    
    for i, coeff in enumerate(coefficients):
        power = n - i
        result.append(coeff / power)
    
    result.append(constant)
    return result


def arithmetic_sequence_term(a1: float, d: float, n: int) -> float:
    """
    Finds nth term of arithmetic sequence
    
    Args:
        a1: First term
        d: Common difference
        n: Term number (1-indexed)
        
    Returns:
        nth term
        
    Example:
        >>> arithmetic_sequence_term(2, 3, 5)  # 2, 5, 8, 11, 14
        14.0
    """
    return a1 + (n - 1) * d


def arithmetic_sequence_sum(a1: float, d: float, n: int) -> float:
    """
    Sums first n terms of arithmetic sequence
    
    Args:
        a1: First term
        d: Common difference
        n: Number of terms
        
    Returns:
        Sum of first n terms
        
    Example:
        >>> arithmetic_sequence_sum(2, 3, 5)
        40.0
    """
    an = arithmetic_sequence_term(a1, d, n)
    return n * (a1 + an) / 2


def geometric_sequence_term(a1: float, r: float, n: int) -> float:
    """
    Finds nth term of geometric sequence
    
    Args:
        a1: First term
        r: Common ratio
        n: Term number (1-indexed)
        
    Returns:
        nth term
        
    Example:
        >>> geometric_sequence_term(2, 3, 4)  # 2, 6, 18, 54
        54.0
    """
    return a1 * (r ** (n - 1))


def geometric_sequence_sum(a1: float, r: float, n: int) -> float:
    """
    Sums first n terms of geometric sequence
    
    Args:
        a1: First term
        r: Common ratio
        n: Number of terms
        
    Returns:
        Sum of first n terms
        
    Example:
        >>> geometric_sequence_sum(2, 3, 4)
        80.0
    """
    if r == 1:
        return a1 * n
    return a1 * (1 - r**n) / (1 - r)


def fibonacci_sequence(n: int) -> List[int]:
    """
    Generates first n Fibonacci numbers
    
    Args:
        n: Number of terms to generate
        
    Returns:
        List of Fibonacci numbers
        
    Example:
        >>> fibonacci_sequence(7)
        [0, 1, 1, 2, 3, 5, 8]
    """
    if n <= 0:
        return []
    if n == 1:
        return [0]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    
    return fib


def binomial_coefficient(n: int, k: int) -> int:
    """
    Calculates binomial coefficient C(n,k) = n! / (k!(n-k)!)
    
    Args:
        n: Total number of items
        k: Number of items to choose
        
    Returns:
        Binomial coefficient
        
    Example:
        >>> binomial_coefficient(5, 2)
        10
    """
    if k < 0 or k > n:
        return 0
    if k == 0 or k == n:
        return 1
    
    k = min(k, n - k)  # Optimization
    result = 1
    
    for i in range(k):
        result = result * (n - i) // (i + 1)
    
    return result


def factorial(n: int) -> int:
    """
    Calculates factorial of n
    
    Args:
        n: Non-negative integer
        
    Returns:
        n! = n × (n-1) × ... × 1
        
    Example:
        >>> factorial(5)
        120
    """
    if n < 0:
        raise ValueError("Factorial not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    
    result = 1
    for i in range(2, n + 1):
        result *= i
    
    return result


def gcd(a: int, b: int) -> int:
    """
    Greatest common divisor using Euclidean algorithm
    
    Args:
        a: First integer
        b: Second integer
        
    Returns:
        Greatest common divisor
        
    Example:
        >>> gcd(48, 18)
        6
    """
    while b:
        a, b = b, a % b
    return abs(a)


def lcm(a: int, b: int) -> int:
    """
    Least common multiple
    
    Args:
        a: First integer
        b: Second integer
        
    Returns:
        Least common multiple
        
    Example:
        >>> lcm(12, 18)
        36
    """
    if a == 0 or b == 0:
        return 0
    return abs(a * b) // gcd(a, b)


def absolute_value(x: float) -> float:
    """
    Calculates absolute value
    
    Args:
        x: Number
        
    Returns:
        |x|
        
    Example:
        >>> absolute_value(-5.5)
        5.5
    """
    return abs(x)


def floor_function(x: float) -> int:
    """
    Evaluates floor function (greatest integer ≤ x)
    
    Args:
        x: Number
        
    Returns:
        Floor of x
        
    Example:
        >>> floor_function(3.7)
        3
    """
    return math.floor(x)


def ceiling_function(x: float) -> int:
    """
    Evaluates ceiling function (smallest integer ≥ x)
    
    Args:
        x: Number
        
    Returns:
        Ceiling of x
        
    Example:
        >>> ceiling_function(3.2)
        4
    """
    return math.ceil(x)


def sign_function(x: float) -> int:
    """
    Evaluates sign function
    
    Args:
        x: Number
        
    Returns:
        -1 if x < 0, 0 if x = 0, 1 if x > 0
        
    Example:
        >>> sign_function(-5)
        -1
    """
    if x > 0:
        return 1
    elif x < 0:
        return -1
    return 0


def modulo_operation(a: int, m: int) -> int:
    """
    Performs modulo operation
    
    Args:
        a: Dividend
        m: Modulus
        
    Returns:
        a mod m
        
    Example:
        >>> modulo_operation(17, 5)
        2
    """
    return a % m


def exponentiation(base: float, exponent: float) -> float:
    """
    Raises number to power
    
    Args:
        base: Base number
        exponent: Exponent
        
    Returns:
        base^exponent
        
    Example:
        >>> exponentiation(2, 10)
        1024.0
    """
    return base ** exponent


def nth_root(x: float, n: int) -> float:
    """
    Calculates nth root
    
    Args:
        x: Number
        n: Root degree
        
    Returns:
        nth root of x
        
    Example:
        >>> nth_root(27, 3)
        3.0
    """
    if n == 0:
        raise ValueError("Root degree cannot be zero")
    if x < 0 and n % 2 == 0:
        raise ValueError("Even root of negative number")
    
    if x < 0:
        return -(abs(x) ** (1/n))
    return x ** (1/n)


def logarithm(x: float, base: float = 10) -> float:
    """
    Calculates logarithm
    
    Args:
        x: Number (must be positive)
        base: Logarithm base (default 10)
        
    Returns:
        log_base(x)
        
    Example:
        >>> logarithm(100, 10)
        2.0
    """
    if x <= 0:
        raise ValueError("Logarithm undefined for non-positive numbers")
    if base <= 0 or base == 1:
        raise ValueError("Invalid logarithm base")
    
    return math.log(x, base)


def natural_logarithm(x: float) -> float:
    """
    Calculates natural logarithm (base e)
    
    Args:
        x: Number (must be positive)
        
    Returns:
        ln(x)
        
    Example:
        >>> natural_logarithm(math.e)
        1.0
    """
    if x <= 0:
        raise ValueError("Logarithm undefined for non-positive numbers")
    return math.log(x)


def common_logarithm(x: float) -> float:
    """
    Calculates common logarithm (base 10)
    
    Args:
        x: Number (must be positive)
        
    Returns:
        log₁₀(x)
        
    Example:
        >>> common_logarithm(1000)
        3.0
    """
    return math.log10(x)


def binary_logarithm(x: float) -> float:
    """
    Calculates binary logarithm (base 2)
    
    Args:
        x: Number (must be positive)
        
    Returns:
        log₂(x)
        
    Example:
        >>> binary_logarithm(8)
        3.0
    """
    return math.log2(x)


# Export all functions
__all__ = [
    'solve_linear_equation',
    'solve_quadratic_equation',
    'find_discriminant',
    'evaluate_polynomial',
    'add_polynomials',
    'subtract_polynomials',
    'multiply_polynomials',
    'polynomial_derivative',
    'polynomial_integral',
    'arithmetic_sequence_term',
    'arithmetic_sequence_sum',
    'geometric_sequence_term',
    'geometric_sequence_sum',
    'fibonacci_sequence',
    'binomial_coefficient',
    'factorial',
    'gcd',
    'lcm',
    'absolute_value',
    'floor_function',
    'ceiling_function',
    'sign_function',
    'modulo_operation',
    'exponentiation',
    'nth_root',
    'logarithm',
    'natural_logarithm',
    'common_logarithm',
    'binary_logarithm',
]
