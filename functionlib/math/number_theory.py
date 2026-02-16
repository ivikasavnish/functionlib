"""
Number Theory Functions

Prime numbers, divisibility, modular arithmetic, and number-theoretic functions.
"""

import math
from typing import List, Tuple, Set


def is_prime(n: int) -> bool:
    """
    Checks if number is prime
    
    Args:
        n: Number to check
        
    Returns:
        True if prime
        
    Example:
        >>> is_prime(17)
        True
        >>> is_prime(18)
        False
    """
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    
    return True


def prime_factors(n: int) -> List[int]:
    """
    Returns prime factorization
    
    Args:
        n: Number to factor
        
    Returns:
        List of prime factors
        
    Example:
        >>> prime_factors(60)
        [2, 2, 3, 5]
    """
    factors = []
    
    # Handle 2 separately
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    
    # Check odd factors
    i = 3
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 2
    
    if n > 1:
        factors.append(n)
    
    return factors


def sieve_of_eratosthenes(limit: int) -> List[int]:
    """
    Finds all primes up to limit using Sieve of Eratosthenes
    
    Args:
        limit: Upper limit
        
    Returns:
        List of primes
        
    Example:
        >>> sieve_of_eratosthenes(20)
        [2, 3, 5, 7, 11, 13, 17, 19]
    """
    if limit < 2:
        return []
    
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    
    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False
    
    return [i for i in range(limit + 1) if is_prime[i]]


def nth_prime(n: int) -> int:
    """
    Returns the nth prime number (1-indexed)
    
    Args:
        n: Prime index
        
    Returns:
        nth prime
        
    Example:
        >>> nth_prime(10)
        29
    """
    if n < 1:
        raise ValueError("n must be positive")
    
    count = 0
    candidate = 2
    
    while count < n:
        if is_prime(candidate):
            count += 1
            if count == n:
                return candidate
        candidate += 1
    
    return candidate


def prime_count(n: int) -> int:
    """
    Counts primes up to n
    
    Args:
        n: Upper limit
        
    Returns:
        Count of primes
        
    Example:
        >>> prime_count(100)
        25
    """
    return len(sieve_of_eratosthenes(n))


def divisors(n: int) -> List[int]:
    """
    Returns all divisors of n
    
    Args:
        n: Number
        
    Returns:
        List of divisors
        
    Example:
        >>> divisors(12)
        [1, 2, 3, 4, 6, 12]
    """
    divs = []
    for i in range(1, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divs.append(i)
            if i != n // i:
                divs.append(n // i)
    
    return sorted(divs)


def proper_divisors(n: int) -> List[int]:
    """
    Returns proper divisors (excluding n itself)
    
    Args:
        n: Number
        
    Returns:
        List of proper divisors
        
    Example:
        >>> proper_divisors(12)
        [1, 2, 3, 4, 6]
    """
    divs = divisors(n)
    return divs[:-1] if divs else []


def sum_of_divisors(n: int) -> int:
    """
    Returns sum of all divisors including n
    
    Args:
        n: Number
        
    Returns:
        Sum of divisors
        
    Example:
        >>> sum_of_divisors(12)
        28
    """
    return sum(divisors(n))


def is_perfect_number(n: int) -> bool:
    """
    Checks if number is perfect (equals sum of proper divisors)
    
    Args:
        n: Number to check
        
    Returns:
        True if perfect
        
    Example:
        >>> is_perfect_number(6)
        True
        >>> is_perfect_number(28)
        True
    """
    return sum(proper_divisors(n)) == n


def totient(n: int) -> int:
    """
    Euler's totient function φ(n) - count of integers ≤ n coprime to n
    
    Args:
        n: Number
        
    Returns:
        φ(n)
        
    Example:
        >>> totient(9)
        6
    """
    result = n
    
    p = 2
    while p * p <= n:
        if n % p == 0:
            while n % p == 0:
                n //= p
            result -= result // p
        p += 1
    
    if n > 1:
        result -= result // n
    
    return result


def gcd_extended(a: int, b: int) -> Tuple[int, int, int]:
    """
    Extended Euclidean algorithm: returns (gcd, x, y) where ax + by = gcd
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        Tuple of (gcd, x, y)
        
    Example:
        >>> gcd_extended(35, 15)
        (5, 1, -2)
    """
    if b == 0:
        return (a, 1, 0)
    
    gcd, x1, y1 = gcd_extended(b, a % b)
    x = y1
    y = x1 - (a // b) * y1
    
    return (gcd, x, y)


def mod_inverse(a: int, m: int) -> int:
    """
    Modular multiplicative inverse: finds x where (a*x) % m = 1
    
    Args:
        a: Number
        m: Modulus
        
    Returns:
        Modular inverse
        
    Example:
        >>> mod_inverse(3, 11)
        4
    """
    gcd, x, _ = gcd_extended(a, m)
    
    if gcd != 1:
        raise ValueError("Modular inverse does not exist")
    
    return x % m


def mod_pow(base: int, exp: int, mod: int) -> int:
    """
    Modular exponentiation: (base^exp) % mod
    
    Args:
        base: Base
        exp: Exponent
        mod: Modulus
        
    Returns:
        Result
        
    Example:
        >>> mod_pow(2, 10, 1000)
        24
    """
    return pow(base, exp, mod)


def chinese_remainder(remainders: List[int], moduli: List[int]) -> int:
    """
    Chinese Remainder Theorem solver
    
    Args:
        remainders: List of remainders
        moduli: List of moduli
        
    Returns:
        Solution
        
    Example:
        >>> chinese_remainder([2, 3, 2], [3, 5, 7])
        23
    """
    if len(remainders) != len(moduli):
        raise ValueError("Lists must have same length")
    
    total = 0
    prod = 1
    for m in moduli:
        prod *= m
    
    for r, m in zip(remainders, moduli):
        p = prod // m
        total += r * mod_inverse(p, m) * p
    
    return total % prod


def legendre_symbol(a: int, p: int) -> int:
    """
    Legendre symbol (a/p)
    
    Args:
        a: Number
        p: Odd prime
        
    Returns:
        -1, 0, or 1
        
    Example:
        >>> legendre_symbol(2, 7)
        1
    """
    if not is_prime(p) or p == 2:
        raise ValueError("p must be odd prime")
    
    a = a % p
    
    if a == 0:
        return 0
    
    result = mod_pow(a, (p - 1) // 2, p)
    
    return -1 if result == p - 1 else result


def is_quadratic_residue(a: int, p: int) -> bool:
    """
    Checks if a is a quadratic residue modulo p
    
    Args:
        a: Number
        p: Prime
        
    Returns:
        True if quadratic residue
        
    Example:
        >>> is_quadratic_residue(4, 7)
        True
    """
    return legendre_symbol(a, p) == 1


def fibonacci_mod(n: int, m: int) -> int:
    """
    Computes nth Fibonacci number modulo m
    
    Args:
        n: Fibonacci index
        m: Modulus
        
    Returns:
        F(n) mod m
        
    Example:
        >>> fibonacci_mod(10, 100)
        55
    """
    if n <= 1:
        return n
    
    a, b = 0, 1
    for _ in range(n):
        a, b = b, (a + b) % m
    
    return a


def collatz_sequence(n: int) -> List[int]:
    """
    Generates Collatz sequence
    
    Args:
        n: Starting number
        
    Returns:
        Collatz sequence
        
    Example:
        >>> collatz_sequence(10)
        [10, 5, 16, 8, 4, 2, 1]
    """
    sequence = [n]
    
    while n != 1:
        if n % 2 == 0:
            n = n // 2
        else:
            n = 3 * n + 1
        sequence.append(n)
    
    return sequence


def collatz_length(n: int) -> int:
    """
    Returns length of Collatz sequence
    
    Args:
        n: Starting number
        
    Returns:
        Sequence length
        
    Example:
        >>> collatz_length(10)
        7
    """
    return len(collatz_sequence(n))


def carmichael_lambda(n: int) -> int:
    """
    Carmichael's lambda function
    
    Args:
        n: Number
        
    Returns:
        λ(n)
        
    Example:
        >>> carmichael_lambda(15)
        4
    """
    if n == 1:
        return 1
    
    factors = {}
    temp = n
    d = 2
    
    while d * d <= temp:
        while temp % d == 0:
            factors[d] = factors.get(d, 0) + 1
            temp //= d
        d += 1
    
    if temp > 1:
        factors[temp] = factors.get(temp, 0) + 1
    
    result = 1
    for p, k in factors.items():
        if p == 2 and k >= 3:
            lambda_pk = pow(2, k - 2)
        else:
            lambda_pk = pow(p, k - 1) * (p - 1)
        
        result = (result * lambda_pk) // math.gcd(result, lambda_pk)
    
    return result


def is_coprime(a: int, b: int) -> bool:
    """
    Checks if two numbers are coprime (gcd = 1)
    
    Args:
        a: First number
        b: Second number
        
    Returns:
        True if coprime
        
    Example:
        >>> is_coprime(15, 28)
        True
    """
    return math.gcd(a, b) == 1


def partition_count(n: int) -> int:
    """
    Counts integer partitions of n (basic implementation)
    
    Args:
        n: Number to partition
        
    Returns:
        Number of partitions
        
    Example:
        >>> partition_count(5)
        7
    """
    dp = [0] * (n + 1)
    dp[0] = 1
    
    for i in range(1, n + 1):
        for j in range(i, n + 1):
            dp[j] += dp[j - i]
    
    return dp[n]


# Export all functions
__all__ = [
    'is_prime', 'prime_factors', 'sieve_of_eratosthenes',
    'nth_prime', 'prime_count', 'divisors', 'proper_divisors',
    'sum_of_divisors', 'is_perfect_number', 'totient',
    'gcd_extended', 'mod_inverse', 'mod_pow', 'chinese_remainder',
    'legendre_symbol', 'is_quadratic_residue', 'fibonacci_mod',
    'collatz_sequence', 'collatz_length', 'carmichael_lambda',
    'is_coprime', 'partition_count',
]
