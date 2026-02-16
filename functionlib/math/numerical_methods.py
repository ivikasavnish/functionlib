"""
Numerical Methods Functions

Root finding, optimization, interpolation, and numerical analysis.
"""

import math
from typing import Callable, Tuple, List, Optional


def bisection_root(f: Callable[[float], float], a: float, b: float, tol: float = 1e-6, max_iter: int = 100) -> Optional[float]:
    """
    Find root using bisection method
    
    Args:
        f: Function
        a: Left bound
        b: Right bound
        tol: Tolerance
        max_iter: Maximum iterations
        
    Returns:
        Root or None
        
    Example:
        >>> root = bisection_root(lambda x: x**2 - 2, 0, 2)
        >>> abs(root - math.sqrt(2)) < 1e-5
        True
    """
    if f(a) * f(b) > 0:
        return None
    
    for _ in range(max_iter):
        c = (a + b) / 2
        
        if abs(f(c)) < tol or (b - a) / 2 < tol:
            return c
        
        if f(a) * f(c) < 0:
            b = c
        else:
            a = c
    
    return (a + b) / 2


def newton_raphson(f: Callable[[float], float], df: Callable[[float], float], 
                   x0: float, tol: float = 1e-6, max_iter: int = 100) -> Optional[float]:
    """
    Newton-Raphson method for root finding
    
    Args:
        f: Function
        df: Derivative of function
        x0: Initial guess
        tol: Tolerance
        max_iter: Maximum iterations
        
    Returns:
        Root or None
        
    Example:
        >>> root = newton_raphson(lambda x: x**2 - 2, lambda x: 2*x, 1)
        >>> abs(root - math.sqrt(2)) < 1e-5
        True
    """
    x = x0
    
    for _ in range(max_iter):
        fx = f(x)
        
        if abs(fx) < tol:
            return x
        
        dfx = df(x)
        if abs(dfx) < 1e-12:
            return None
        
        x = x - fx / dfx
    
    return x


def secant_method(f: Callable[[float], float], x0: float, x1: float, 
                  tol: float = 1e-6, max_iter: int = 100) -> Optional[float]:
    """
    Secant method for root finding
    
    Args:
        f: Function
        x0: First initial guess
        x1: Second initial guess
        tol: Tolerance
        max_iter: Maximum iterations
        
    Returns:
        Root or None
        
    Example:
        >>> root = secant_method(lambda x: x**2 - 2, 1, 2)
        >>> abs(root - math.sqrt(2)) < 1e-5
        True
    """
    for _ in range(max_iter):
        f0, f1 = f(x0), f(x1)
        
        if abs(f1) < tol:
            return x1
        
        if abs(f1 - f0) < 1e-12:
            return None
        
        x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, x1 = x1, x_new
    
    return x1


def fixed_point_iteration(g: Callable[[float], float], x0: float, 
                          tol: float = 1e-6, max_iter: int = 100) -> Optional[float]:
    """
    Fixed point iteration: x = g(x)
    
    Args:
        g: Function
        x0: Initial guess
        tol: Tolerance
        max_iter: Maximum iterations
        
    Returns:
        Fixed point or None
        
    Example:
        >>> fp = fixed_point_iteration(lambda x: math.cos(x), 0)
        >>> abs(math.cos(fp) - fp) < 1e-5
        True
    """
    x = x0
    
    for _ in range(max_iter):
        x_new = g(x)
        
        if abs(x_new - x) < tol:
            return x_new
        
        x = x_new
    
    return x


def golden_section_search(f: Callable[[float], float], a: float, b: float, 
                          tol: float = 1e-6) -> float:
    """
    Golden section search for minimum
    
    Args:
        f: Function to minimize
        a: Left bound
        b: Right bound
        tol: Tolerance
        
    Returns:
        x value at minimum
        
    Example:
        >>> x_min = golden_section_search(lambda x: (x-2)**2, 0, 4)
        >>> abs(x_min - 2) < 1e-5
        True
    """
    phi = (1 + math.sqrt(5)) / 2
    resphi = 2 - phi
    
    x1 = a + resphi * (b - a)
    x2 = b - resphi * (b - a)
    f1, f2 = f(x1), f(x2)
    
    while abs(b - a) > tol:
        if f1 < f2:
            b = x2
            x2 = x1
            f2 = f1
            x1 = a + resphi * (b - a)
            f1 = f(x1)
        else:
            a = x1
            x1 = x2
            f1 = f2
            x2 = b - resphi * (b - a)
            f2 = f(x2)
    
    return (a + b) / 2


def gradient_descent(f: Callable[[List[float]], float], 
                     grad: Callable[[List[float]], List[float]],
                     x0: List[float], learning_rate: float = 0.01, 
                     tol: float = 1e-6, max_iter: int = 1000) -> List[float]:
    """
    Gradient descent optimization
    
    Args:
        f: Function to minimize
        grad: Gradient function
        x0: Initial point
        learning_rate: Step size
        tol: Tolerance
        max_iter: Maximum iterations
        
    Returns:
        Optimal point
        
    Example:
        >>> x = gradient_descent(
        ...     lambda x: x[0]**2 + x[1]**2,
        ...     lambda x: [2*x[0], 2*x[1]],
        ...     [1.0, 1.0], 0.1
        ... )
        >>> abs(x[0]) < 0.01 and abs(x[1]) < 0.01
        True
    """
    x = x0[:]
    
    for _ in range(max_iter):
        g = grad(x)
        norm = math.sqrt(sum(gi**2 for gi in g))
        
        if norm < tol:
            break
        
        x = [xi - learning_rate * gi for xi, gi in zip(x, g)]
    
    return x


def linear_interpolation(x: float, x0: float, y0: float, x1: float, y1: float) -> float:
    """
    Linear interpolation between two points
    
    Args:
        x: Point to interpolate at
        x0, y0: First point
        x1, y1: Second point
        
    Returns:
        Interpolated value
        
    Example:
        >>> linear_interpolation(0.5, 0, 0, 1, 10)
        5.0
    """
    return y0 + (y1 - y0) * (x - x0) / (x1 - x0)


def lagrange_interpolation(x: float, points: List[Tuple[float, float]]) -> float:
    """
    Lagrange polynomial interpolation
    
    Args:
        x: Point to interpolate at
        points: List of (x, y) tuples
        
    Returns:
        Interpolated value
        
    Example:
        >>> lagrange_interpolation(0.5, [(0, 0), (1, 1), (2, 4)])
        0.25
    """
    n = len(points)
    result = 0
    
    for i in range(n):
        xi, yi = points[i]
        term = yi
        
        for j in range(n):
            if i != j:
                xj = points[j][0]
                term *= (x - xj) / (xi - xj)
        
        result += term
    
    return result


def newton_forward_difference(x: float, x0: float, h: float, y: List[float]) -> float:
    """
    Newton forward difference interpolation
    
    Args:
        x: Point to interpolate at
        x0: First x value
        h: Step size
        y: Function values at x0, x0+h, x0+2h, ...
        
    Returns:
        Interpolated value
        
    Example:
        >>> newton_forward_difference(0.5, 0, 1, [0, 1, 4, 9])
        0.25
    """
    n = len(y)
    u = (x - x0) / h
    
    # Calculate forward differences
    diff = [y[:]]
    for i in range(1, n):
        diff.append([diff[i-1][j+1] - diff[i-1][j] for j in range(n-i)])
    
    # Apply Newton formula
    result = y[0]
    u_term = 1
    
    for i in range(1, n):
        u_term *= (u - i + 1) / i
        result += u_term * diff[i][0]
    
    return result


def trapezoidal_rule(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
    """
    Trapezoidal rule for numerical integration
    
    Args:
        f: Function to integrate
        a: Lower bound
        b: Upper bound
        n: Number of intervals
        
    Returns:
        Approximate integral
        
    Example:
        >>> result = trapezoidal_rule(lambda x: x**2, 0, 1, 100)
        >>> abs(result - 1/3) < 0.01
        True
    """
    h = (b - a) / n
    result = (f(a) + f(b)) / 2
    
    for i in range(1, n):
        result += f(a + i * h)
    
    return result * h


def simpsons_rule(f: Callable[[float], float], a: float, b: float, n: int = 100) -> float:
    """
    Simpson's rule for numerical integration (n must be even)
    
    Args:
        f: Function to integrate
        a: Lower bound
        b: Upper bound
        n: Number of intervals (must be even)
        
    Returns:
        Approximate integral
        
    Example:
        >>> result = simpsons_rule(lambda x: x**2, 0, 1, 100)
        >>> abs(result - 1/3) < 0.0001
        True
    """
    if n % 2 != 0:
        n += 1
    
    h = (b - a) / n
    result = f(a) + f(b)
    
    for i in range(1, n):
        x = a + i * h
        if i % 2 == 0:
            result += 2 * f(x)
        else:
            result += 4 * f(x)
    
    return result * h / 3


def romberg_integration(f: Callable[[float], float], a: float, b: float, 
                        max_steps: int = 10, tol: float = 1e-8) -> float:
    """
    Romberg integration (Richardson extrapolation)
    
    Args:
        f: Function to integrate
        a: Lower bound
        b: Upper bound
        max_steps: Maximum refinement steps
        tol: Tolerance
        
    Returns:
        Approximate integral
        
    Example:
        >>> result = romberg_integration(lambda x: x**2, 0, 1)
        >>> abs(result - 1/3) < 1e-8
        True
    """
    r = [[0] * (max_steps + 1) for _ in range(max_steps + 1)]
    
    h = b - a
    r[0][0] = h * (f(a) + f(b)) / 2
    
    for i in range(1, max_steps + 1):
        h /= 2
        
        # Trapezoidal approximation
        sum_val = 0
        for k in range(1, 2**i, 2):
            sum_val += f(a + k * h)
        
        r[i][0] = r[i-1][0] / 2 + h * sum_val
        
        # Richardson extrapolation
        for j in range(1, i + 1):
            r[i][j] = r[i][j-1] + (r[i][j-1] - r[i-1][j-1]) / (4**j - 1)
        
        if i > 0 and abs(r[i][i] - r[i-1][i-1]) < tol:
            return r[i][i]
    
    return r[max_steps][max_steps]


def monte_carlo_integration(f: Callable[[List[float]], float], 
                            bounds: List[Tuple[float, float]], 
                            n_samples: int = 10000) -> float:
    """
    Monte Carlo integration for multi-dimensional functions
    
    Args:
        f: Function to integrate
        bounds: List of (min, max) for each dimension
        n_samples: Number of random samples
        
    Returns:
        Approximate integral
        
    Example:
        >>> result = monte_carlo_integration(
        ...     lambda x: x[0]**2, [(0, 1)], 10000
        ... )
        >>> abs(result - 1/3) < 0.05
        True
    """
    import random
    
    volume = 1
    for low, high in bounds:
        volume *= (high - low)
    
    total = 0
    for _ in range(n_samples):
        point = [random.uniform(low, high) for low, high in bounds]
        total += f(point)
    
    return volume * total / n_samples


def euler_ode(f: Callable[[float, float], float], y0: float, t0: float, 
              t_end: float, h: float) -> List[Tuple[float, float]]:
    """
    Euler method for solving ODE: dy/dt = f(t, y)
    
    Args:
        f: Function f(t, y)
        y0: Initial value
        t0: Initial time
        t_end: End time
        h: Step size
        
    Returns:
        List of (t, y) points
        
    Example:
        >>> result = euler_ode(lambda t, y: y, 1, 0, 1, 0.1)
        >>> len(result)
        11
    """
    t = t0
    y = y0
    points = [(t, y)]
    
    while t < t_end:
        y = y + h * f(t, y)
        t = t + h
        points.append((t, y))
    
    return points


def runge_kutta_4(f: Callable[[float, float], float], y0: float, t0: float, 
                  t_end: float, h: float) -> List[Tuple[float, float]]:
    """
    4th order Runge-Kutta method for ODE
    
    Args:
        f: Function f(t, y)
        y0: Initial value
        t0: Initial time
        t_end: End time
        h: Step size
        
    Returns:
        List of (t, y) points
        
    Example:
        >>> result = runge_kutta_4(lambda t, y: y, 1, 0, 1, 0.1)
        >>> len(result)
        11
    """
    t = t0
    y = y0
    points = [(t, y)]
    
    while t < t_end:
        k1 = h * f(t, y)
        k2 = h * f(t + h/2, y + k1/2)
        k3 = h * f(t + h/2, y + k2/2)
        k4 = h * f(t + h, y + k3)
        
        y = y + (k1 + 2*k2 + 2*k3 + k4) / 6
        t = t + h
        points.append((t, y))
    
    return points


def finite_difference_derivative(f: Callable[[float], float], x: float, h: float = 1e-5) -> float:
    """
    Finite difference approximation of derivative
    
    Args:
        f: Function
        x: Point
        h: Step size
        
    Returns:
        Approximate derivative
        
    Example:
        >>> df = finite_difference_derivative(lambda x: x**2, 3)
        >>> abs(df - 6) < 0.001
        True
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def richardson_extrapolation(f: Callable[[float], float], x: float, 
                             h: float = 0.1, n: int = 4) -> float:
    """
    Richardson extrapolation for derivative
    
    Args:
        f: Function
        x: Point
        h: Initial step size
        n: Number of refinements
        
    Returns:
        Improved derivative approximation
        
    Example:
        >>> df = richardson_extrapolation(lambda x: x**3, 2)
        >>> abs(df - 12) < 1e-6
        True
    """
    d = [[0] * n for _ in range(n)]
    
    for i in range(n):
        hi = h / (2 ** i)
        d[i][0] = (f(x + hi) - f(x - hi)) / (2 * hi)
    
    for j in range(1, n):
        for i in range(n - j):
            d[i][j] = d[i+1][j-1] + (d[i+1][j-1] - d[i][j-1]) / (4**j - 1)
    
    return d[0][n-1]


def least_squares_fit(x: List[float], y: List[float], degree: int = 1) -> List[float]:
    """
    Polynomial least squares fit
    
    Args:
        x: x values
        y: y values
        degree: Polynomial degree
        
    Returns:
        Coefficients [a0, a1, ..., an]
        
    Example:
        >>> coef = least_squares_fit([0, 1, 2], [1, 2, 3], 1)
        >>> abs(coef[0] - 1) < 0.01 and abs(coef[1] - 1) < 0.01
        True
    """
    n = len(x)
    m = degree + 1
    
    # Build matrices
    A = [[sum(x[i]**(j+k) for i in range(n)) for k in range(m)] for j in range(m)]
    b = [sum(y[i] * x[i]**j for i in range(n)) for j in range(m)]
    
    # Gaussian elimination (simplified)
    for i in range(m):
        # Partial pivoting
        max_row = i
        for k in range(i+1, m):
            if abs(A[k][i]) > abs(A[max_row][i]):
                max_row = k
        A[i], A[max_row] = A[max_row], A[i]
        b[i], b[max_row] = b[max_row], b[i]
        
        # Forward elimination
        for k in range(i+1, m):
            c = A[k][i] / A[i][i]
            for j in range(i, m):
                A[k][j] -= c * A[i][j]
            b[k] -= c * b[i]
    
    # Back substitution
    coeffs = [0] * m
    for i in range(m-1, -1, -1):
        coeffs[i] = b[i]
        for j in range(i+1, m):
            coeffs[i] -= A[i][j] * coeffs[j]
        coeffs[i] /= A[i][i]
    
    return coeffs


# Export all functions
__all__ = [
    'bisection_root', 'newton_raphson', 'secant_method', 'fixed_point_iteration',
    'golden_section_search', 'gradient_descent',
    'linear_interpolation', 'lagrange_interpolation', 'newton_forward_difference',
    'trapezoidal_rule', 'simpsons_rule', 'romberg_integration', 'monte_carlo_integration',
    'euler_ode', 'runge_kutta_4',
    'finite_difference_derivative', 'richardson_extrapolation',
    'least_squares_fit',
]
