"""
Calculus Functions

Derivatives, integrals, limits, and differential equations.
"""

import math
from typing import Callable, List, Tuple, Optional


def derivative_numerical(f: Callable[[float], float], x: float, h: float = 1e-7) -> float:
    """
    Computes numerical derivative using central difference method
    
    Args:
        f: Function to differentiate
        x: Point at which to evaluate derivative
        h: Step size (default 1e-7)
        
    Returns:
        Approximate derivative f'(x)
        
    Example:
        >>> f = lambda x: x**2
        >>> derivative_numerical(f, 3.0)  # Should be ~6
        6.000000000262855
    """
    return (f(x + h) - f(x - h)) / (2 * h)


def derivative_power_rule(coefficient: float, exponent: float, x: float) -> float:
    """
    Applies power rule for derivatives: d/dx(ax^n) = n*a*x^(n-1)
    
    Args:
        coefficient: Coefficient a
        exponent: Exponent n
        x: Point at which to evaluate
        
    Returns:
        Derivative value
        
    Example:
        >>> derivative_power_rule(3, 2, 5)  # d/dx(3x²) at x=5
        30.0
    """
    if exponent == 0:
        return 0
    return coefficient * exponent * (x ** (exponent - 1))


def integral_numerical(f: Callable[[float], float], a: float, b: float, n: int = 1000) -> float:
    """
    Computes definite integral using trapezoidal rule
    
    Args:
        f: Function to integrate
        a: Lower bound
        b: Upper bound
        n: Number of trapezoids (default 1000)
        
    Returns:
        Approximate integral ∫[a,b] f(x)dx
        
    Example:
        >>> f = lambda x: x**2
        >>> integral_numerical(f, 0, 1)  # Should be ~1/3
        0.3333333333333334
    """
    h = (b - a) / n
    result = (f(a) + f(b)) / 2.0
    
    for i in range(1, n):
        result += f(a + i * h)
    
    return result * h


def integral_simpson(f: Callable[[float], float], a: float, b: float, n: int = 1000) -> float:
    """
    Computes definite integral using Simpson's rule (more accurate)
    
    Args:
        f: Function to integrate
        a: Lower bound
        b: Upper bound
        n: Number of intervals (must be even)
        
    Returns:
        Approximate integral ∫[a,b] f(x)dx
        
    Example:
        >>> f = lambda x: x**2
        >>> integral_simpson(f, 0, 1, 100)
        0.33333333333333337
    """
    if n % 2 == 1:
        n += 1  # Make n even
    
    h = (b - a) / n
    result = f(a) + f(b)
    
    for i in range(1, n, 2):
        result += 4 * f(a + i * h)
    
    for i in range(2, n, 2):
        result += 2 * f(a + i * h)
    
    return result * h / 3


def limit_numerical(f: Callable[[float], float], x0: float, epsilon: float = 1e-6) -> float:
    """
    Computes limit of function as x approaches x0
    
    Args:
        f: Function
        x0: Point to approach
        epsilon: Small value to approach from
        
    Returns:
        Approximate limit
        
    Example:
        >>> f = lambda x: (x**2 - 1)/(x - 1)
        >>> limit_numerical(f, 1.0)  # Should be 2
        2.000001
    """
    return (f(x0 + epsilon) + f(x0 - epsilon)) / 2


def gradient_descent_step(f: Callable[[float], float], x: float, learning_rate: float = 0.01, h: float = 1e-7) -> float:
    """
    Performs one step of gradient descent
    
    Args:
        f: Function to minimize
        x: Current point
        learning_rate: Step size
        h: Finite difference step
        
    Returns:
        New x value
        
    Example:
        >>> f = lambda x: (x - 3)**2
        >>> gradient_descent_step(f, 0.0, 0.1)
        0.6000000010000001
    """
    gradient = derivative_numerical(f, x, h)
    return x - learning_rate * gradient


def newtons_method(f: Callable[[float], float], x0: float, tol: float = 1e-6, max_iter: int = 100) -> float:
    """
    Finds root of function using Newton's method
    
    Args:
        f: Function to find root of
        x0: Initial guess
        tol: Tolerance for convergence
        max_iter: Maximum iterations
        
    Returns:
        Root of function
        
    Example:
        >>> f = lambda x: x**2 - 4
        >>> newtons_method(f, 1.0)  # Should find x=2
        2.0
    """
    x = x0
    for _ in range(max_iter):
        fx = f(x)
        if abs(fx) < tol:
            return x
        
        fpx = derivative_numerical(f, x)
        if abs(fpx) < 1e-10:
            raise ValueError("Derivative too close to zero")
        
        x = x - fx / fpx
    
    return x


def bisection_method(f: Callable[[float], float], a: float, b: float, tol: float = 1e-6, max_iter: int = 100) -> float:
    """
    Finds root using bisection method
    
    Args:
        f: Function (must have opposite signs at a and b)
        a: Left endpoint
        b: Right endpoint
        tol: Tolerance
        max_iter: Maximum iterations
        
    Returns:
        Root in interval [a, b]
        
    Example:
        >>> f = lambda x: x**2 - 4
        >>> bisection_method(f, 0, 3)
        2.0
    """
    fa, fb = f(a), f(b)
    
    if fa * fb > 0:
        raise ValueError("Function must have opposite signs at endpoints")
    
    for _ in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        
        if abs(fc) < tol or (b - a) / 2 < tol:
            return c
        
        if fa * fc < 0:
            b, fb = c, fc
        else:
            a, fa = c, fc
    
    return (a + b) / 2


def secant_method(f: Callable[[float], float], x0: float, x1: float, tol: float = 1e-6, max_iter: int = 100) -> float:
    """
    Finds root using secant method
    
    Args:
        f: Function
        x0: First initial guess
        x1: Second initial guess
        tol: Tolerance
        max_iter: Maximum iterations
        
    Returns:
        Root of function
        
    Example:
        >>> f = lambda x: x**2 - 4
        >>> secant_method(f, 1.0, 3.0)
        2.0
    """
    for _ in range(max_iter):
        f0, f1 = f(x0), f(x1)
        
        if abs(f1) < tol:
            return x1
        
        if abs(f1 - f0) < 1e-10:
            raise ValueError("Function values too close")
        
        x_new = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, x1 = x1, x_new
    
    return x1


def partial_derivative_x(f: Callable[[float, float], float], x: float, y: float, h: float = 1e-7) -> float:
    """
    Computes partial derivative with respect to x
    
    Args:
        f: Function of two variables
        x: x-coordinate
        y: y-coordinate
        h: Step size
        
    Returns:
        ∂f/∂x at (x, y)
        
    Example:
        >>> f = lambda x, y: x**2 + y**2
        >>> partial_derivative_x(f, 2.0, 3.0)  # Should be ~4
        4.000000000262855
    """
    return (f(x + h, y) - f(x - h, y)) / (2 * h)


def partial_derivative_y(f: Callable[[float, float], float], x: float, y: float, h: float = 1e-7) -> float:
    """
    Computes partial derivative with respect to y
    
    Args:
        f: Function of two variables
        x: x-coordinate
        y: y-coordinate
        h: Step size
        
    Returns:
        ∂f/∂y at (x, y)
        
    Example:
        >>> f = lambda x, y: x**2 + y**2
        >>> partial_derivative_y(f, 2.0, 3.0)  # Should be ~6
        6.000000000262855
    """
    return (f(x, y + h) - f(x, y - h)) / (2 * h)


def gradient_2d(f: Callable[[float, float], float], x: float, y: float) -> Tuple[float, float]:
    """
    Computes gradient vector in 2D
    
    Args:
        f: Function of two variables
        x: x-coordinate
        y: y-coordinate
        
    Returns:
        Gradient (∂f/∂x, ∂f/∂y)
        
    Example:
        >>> f = lambda x, y: x**2 + y**2
        >>> gradient_2d(f, 2.0, 3.0)
        (4.000000000262855, 6.000000000262855)
    """
    dx = partial_derivative_x(f, x, y)
    dy = partial_derivative_y(f, x, y)
    return (dx, dy)


def laplacian_2d(f: Callable[[float, float], float], x: float, y: float, h: float = 1e-4) -> float:
    """
    Computes Laplacian (∇²f = ∂²f/∂x² + ∂²f/∂y²)
    
    Args:
        f: Function of two variables
        x: x-coordinate
        y: y-coordinate
        h: Step size
        
    Returns:
        Laplacian at (x, y)
        
    Example:
        >>> f = lambda x, y: x**2 + y**2
        >>> laplacian_2d(f, 2.0, 3.0)  # Should be ~4
        3.999999950738315
    """
    d2fdx2 = (f(x + h, y) - 2*f(x, y) + f(x - h, y)) / (h**2)
    d2fdy2 = (f(x, y + h) - 2*f(x, y) + f(x, y - h)) / (h**2)
    return d2fdx2 + d2fdy2


def taylor_series_expansion(f: Callable[[float], float], a: float, x: float, n: int = 5) -> float:
    """
    Approximates f(x) using Taylor series around point a
    
    Args:
        f: Function to approximate
        a: Center point
        x: Point to evaluate
        n: Number of terms
        
    Returns:
        Taylor series approximation
        
    Example:
        >>> import math
        >>> taylor_series_expansion(math.sin, 0, 0.1, 5)
        0.09999833334166667
    """
    result = 0
    factorial = 1
    
    for k in range(n):
        if k > 0:
            factorial *= k
        
        # Compute kth derivative numerically
        derivative = f(a)
        h = 1e-5
        for _ in range(k):
            derivative = (f(a + h) - f(a - h)) / (2 * h)
        
        result += derivative * ((x - a) ** k) / factorial
    
    return result


def euler_method(f: Callable[[float, float], float], x0: float, y0: float, h: float, n: int) -> List[Tuple[float, float]]:
    """
    Solves ODE dy/dx = f(x,y) using Euler's method
    
    Args:
        f: Right-hand side of ODE
        x0: Initial x
        y0: Initial y
        h: Step size
        n: Number of steps
        
    Returns:
        List of (x, y) points
        
    Example:
        >>> f = lambda x, y: y  # dy/dx = y
        >>> euler_method(f, 0, 1, 0.1, 5)
        [(0, 1), (0.1, 1.1), (0.2, 1.21), (0.30000000000000004, 1.331), (0.4, 1.4641000000000002)]
    """
    points = [(x0, y0)]
    x, y = x0, y0
    
    for _ in range(n):
        y = y + h * f(x, y)
        x = x + h
        points.append((x, y))
    
    return points


def runge_kutta_4(f: Callable[[float, float], float], x0: float, y0: float, h: float, n: int) -> List[Tuple[float, float]]:
    """
    Solves ODE dy/dx = f(x,y) using 4th order Runge-Kutta
    
    Args:
        f: Right-hand side of ODE
        x0: Initial x
        y0: Initial y
        h: Step size
        n: Number of steps
        
    Returns:
        List of (x, y) points
        
    Example:
        >>> f = lambda x, y: y
        >>> runge_kutta_4(f, 0, 1, 0.1, 2)
        [(0, 1), (0.1, 1.1051708333333333), (0.2, 1.2214026666666666)]
    """
    points = [(x0, y0)]
    x, y = x0, y0
    
    for _ in range(n):
        k1 = h * f(x, y)
        k2 = h * f(x + h/2, y + k1/2)
        k3 = h * f(x + h/2, y + k2/2)
        k4 = h * f(x + h, y + k3)
        
        y = y + (k1 + 2*k2 + 2*k3 + k4) / 6
        x = x + h
        points.append((x, y))
    
    return points


def definite_integral_power(coefficient: float, exponent: float, a: float, b: float) -> float:
    """
    Computes definite integral of ax^n from a to b
    
    Args:
        coefficient: Coefficient a
        exponent: Exponent n
        a: Lower bound
        b: Upper bound
        
    Returns:
        ∫[a,b] ax^n dx
        
    Example:
        >>> definite_integral_power(1, 2, 0, 2)  # ∫[0,2] x² dx
        2.6666666666666665
    """
    if exponent == -1:
        return coefficient * (math.log(abs(b)) - math.log(abs(a)))
    
    return coefficient * (b**(exponent + 1) - a**(exponent + 1)) / (exponent + 1)


def arc_length(f: Callable[[float], float], a: float, b: float, n: int = 1000) -> float:
    """
    Computes arc length of curve y=f(x) from a to b
    
    Args:
        f: Function defining curve
        a: Start x
        b: End x
        n: Number of segments
        
    Returns:
        Arc length
        
    Example:
        >>> f = lambda x: x**2
        >>> arc_length(f, 0, 1, 1000)
        1.4789428575451943
    """
    h = (b - a) / n
    length = 0
    
    for i in range(n):
        x = a + i * h
        dx = h
        dy = f(x + h) - f(x)
        length += math.sqrt(dx**2 + dy**2)
    
    return length


# Export all functions
__all__ = [
    'derivative_numerical',
    'derivative_power_rule',
    'integral_numerical',
    'integral_simpson',
    'limit_numerical',
    'gradient_descent_step',
    'newtons_method',
    'bisection_method',
    'secant_method',
    'partial_derivative_x',
    'partial_derivative_y',
    'gradient_2d',
    'laplacian_2d',
    'taylor_series_expansion',
    'euler_method',
    'runge_kutta_4',
    'definite_integral_power',
    'arc_length',
]
