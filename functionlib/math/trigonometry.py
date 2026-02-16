"""
Trigonometry Functions

Trigonometric functions, inverse functions, and identities.
"""

import math
from typing import Tuple


def sin(x: float, degrees: bool = False) -> float:
    """
    Calculates sine
    
    Args:
        x: Angle
        degrees: If True, x is in degrees; otherwise radians
        
    Returns:
        sin(x)
        
    Example:
        >>> sin(30, degrees=True)
        0.49999999999999994
    """
    if degrees:
        x = math.radians(x)
    return math.sin(x)


def cos(x: float, degrees: bool = False) -> float:
    """
    Calculates cosine
    
    Args:
        x: Angle
        degrees: If True, x is in degrees; otherwise radians
        
    Returns:
        cos(x)
        
    Example:
        >>> cos(60, degrees=True)
        0.5000000000000001
    """
    if degrees:
        x = math.radians(x)
    return math.cos(x)


def tan(x: float, degrees: bool = False) -> float:
    """
    Calculates tangent
    
    Args:
        x: Angle
        degrees: If True, x is in degrees; otherwise radians
        
    Returns:
        tan(x)
        
    Example:
        >>> tan(45, degrees=True)
        0.9999999999999999
    """
    if degrees:
        x = math.radians(x)
    return math.tan(x)


def cot(x: float, degrees: bool = False) -> float:
    """
    Calculates cotangent
    
    Args:
        x: Angle
        degrees: If True, x is in degrees; otherwise radians
        
    Returns:
        cot(x) = 1/tan(x)
        
    Example:
        >>> cot(45, degrees=True)
        1.0000000000000002
    """
    if degrees:
        x = math.radians(x)
    tan_x = math.tan(x)
    if abs(tan_x) < 1e-10:
        raise ValueError("Cotangent undefined (tangent is zero)")
    return 1 / tan_x


def sec(x: float, degrees: bool = False) -> float:
    """
    Calculates secant
    
    Args:
        x: Angle
        degrees: If True, x is in degrees; otherwise radians
        
    Returns:
        sec(x) = 1/cos(x)
        
    Example:
        >>> sec(60, degrees=True)
        1.9999999999999996
    """
    if degrees:
        x = math.radians(x)
    cos_x = math.cos(x)
    if abs(cos_x) < 1e-10:
        raise ValueError("Secant undefined (cosine is zero)")
    return 1 / cos_x


def csc(x: float, degrees: bool = False) -> float:
    """
    Calculates cosecant
    
    Args:
        x: Angle
        degrees: If True, x is in degrees; otherwise radians
        
    Returns:
        csc(x) = 1/sin(x)
        
    Example:
        >>> csc(30, degrees=True)
        2.0000000000000004
    """
    if degrees:
        x = math.radians(x)
    sin_x = math.sin(x)
    if abs(sin_x) < 1e-10:
        raise ValueError("Cosecant undefined (sine is zero)")
    return 1 / sin_x


def asin(x: float, degrees: bool = False) -> float:
    """
    Calculates arcsine (inverse sine)
    
    Args:
        x: Value between -1 and 1
        degrees: If True, returns degrees; otherwise radians
        
    Returns:
        arcsin(x)
        
    Example:
        >>> asin(0.5, degrees=True)
        30.000000000000004
    """
    result = math.asin(x)
    return math.degrees(result) if degrees else result


def acos(x: float, degrees: bool = False) -> float:
    """
    Calculates arccosine (inverse cosine)
    
    Args:
        x: Value between -1 and 1
        degrees: If True, returns degrees; otherwise radians
        
    Returns:
        arccos(x)
        
    Example:
        >>> acos(0.5, degrees=True)
        60.00000000000001
    """
    result = math.acos(x)
    return math.degrees(result) if degrees else result


def atan(x: float, degrees: bool = False) -> float:
    """
    Calculates arctangent (inverse tangent)
    
    Args:
        x: Value
        degrees: If True, returns degrees; otherwise radians
        
    Returns:
        arctan(x)
        
    Example:
        >>> atan(1, degrees=True)
        45.0
    """
    result = math.atan(x)
    return math.degrees(result) if degrees else result


def atan2(y: float, x: float, degrees: bool = False) -> float:
    """
    Calculates arctangent of y/x with correct quadrant
    
    Args:
        y: y-coordinate
        x: x-coordinate
        degrees: If True, returns degrees; otherwise radians
        
    Returns:
        arctan2(y, x)
        
    Example:
        >>> atan2(1, 1, degrees=True)
        45.0
    """
    result = math.atan2(y, x)
    return math.degrees(result) if degrees else result


def sinh(x: float) -> float:
    """
    Calculates hyperbolic sine
    
    Args:
        x: Value
        
    Returns:
        sinh(x) = (e^x - e^(-x))/2
        
    Example:
        >>> sinh(1)
        1.1752011936438014
    """
    return math.sinh(x)


def cosh(x: float) -> float:
    """
    Calculates hyperbolic cosine
    
    Args:
        x: Value
        
    Returns:
        cosh(x) = (e^x + e^(-x))/2
        
    Example:
        >>> cosh(1)
        1.5430806348152437
    """
    return math.cosh(x)


def tanh(x: float) -> float:
    """
    Calculates hyperbolic tangent
    
    Args:
        x: Value
        
    Returns:
        tanh(x) = sinh(x)/cosh(x)
        
    Example:
        >>> tanh(1)
        0.7615941559557649
    """
    return math.tanh(x)


def asinh(x: float) -> float:
    """
    Calculates inverse hyperbolic sine
    
    Args:
        x: Value
        
    Returns:
        arcsinh(x)
        
    Example:
        >>> asinh(1)
        0.881373587019543
    """
    return math.asinh(x)


def acosh(x: float) -> float:
    """
    Calculates inverse hyperbolic cosine
    
    Args:
        x: Value >= 1
        
    Returns:
        arccosh(x)
        
    Example:
        >>> acosh(2)
        1.3169578969248166
    """
    return math.acosh(x)


def atanh(x: float) -> float:
    """
    Calculates inverse hyperbolic tangent
    
    Args:
        x: Value between -1 and 1
        
    Returns:
        arctanh(x)
        
    Example:
        >>> atanh(0.5)
        0.5493061443340548
    """
    return math.atanh(x)


def degrees_to_radians(degrees: float) -> float:
    """
    Converts degrees to radians
    
    Args:
        degrees: Angle in degrees
        
    Returns:
        Angle in radians
        
    Example:
        >>> degrees_to_radians(180)
        3.141592653589793
    """
    return math.radians(degrees)


def radians_to_degrees(radians: float) -> float:
    """
    Converts radians to degrees
    
    Args:
        radians: Angle in radians
        
    Returns:
        Angle in degrees
        
    Example:
        >>> radians_to_degrees(math.pi)
        180.0
    """
    return math.degrees(radians)


def law_of_cosines(a: float, b: float, C_degrees: float) -> float:
    """
    Calculates third side using law of cosines: c² = a² + b² - 2ab·cos(C)
    
    Args:
        a: First side length
        b: Second side length
        C_degrees: Angle between sides a and b (in degrees)
        
    Returns:
        Length of third side c
        
    Example:
        >>> law_of_cosines(3, 4, 90)
        5.0
    """
    C_radians = math.radians(C_degrees)
    c_squared = a**2 + b**2 - 2*a*b*math.cos(C_radians)
    return math.sqrt(c_squared)


def law_of_sines_angle(a: float, A_degrees: float, b: float) -> float:
    """
    Finds angle B using law of sines: a/sin(A) = b/sin(B)
    
    Args:
        a: Side opposite to angle A
        A_degrees: Angle A in degrees
        b: Side opposite to angle B
        
    Returns:
        Angle B in degrees
        
    Example:
        >>> law_of_sines_angle(3, 30, 6)
        90.0
    """
    A_radians = math.radians(A_degrees)
    sin_B = b * math.sin(A_radians) / a
    
    if abs(sin_B) > 1:
        raise ValueError("No solution exists (invalid triangle)")
    
    B_radians = math.asin(sin_B)
    return math.degrees(B_radians)


def pythagorean_theorem(a: float, b: float) -> float:
    """
    Calculates hypotenuse using Pythagorean theorem: c = √(a² + b²)
    
    Args:
        a: First leg
        b: Second leg
        
    Returns:
        Hypotenuse c
        
    Example:
        >>> pythagorean_theorem(3, 4)
        5.0
    """
    return math.sqrt(a**2 + b**2)


def polar_to_cartesian(r: float, theta_degrees: float) -> Tuple[float, float]:
    """
    Converts polar coordinates to Cartesian
    
    Args:
        r: Radius
        theta_degrees: Angle in degrees
        
    Returns:
        (x, y) coordinates
        
    Example:
        >>> polar_to_cartesian(5, 45)
        (3.5355339059327373, 3.5355339059327378)
    """
    theta_radians = math.radians(theta_degrees)
    x = r * math.cos(theta_radians)
    y = r * math.sin(theta_radians)
    return (x, y)


def cartesian_to_polar(x: float, y: float, degrees: bool = True) -> Tuple[float, float]:
    """
    Converts Cartesian coordinates to polar
    
    Args:
        x: x-coordinate
        y: y-coordinate
        degrees: If True, returns angle in degrees
        
    Returns:
        (r, theta) where r is radius and theta is angle
        
    Example:
        >>> cartesian_to_polar(3, 4)
        (5.0, 53.13010235415598)
    """
    r = math.sqrt(x**2 + y**2)
    theta = math.atan2(y, x)
    
    if degrees:
        theta = math.degrees(theta)
    
    return (r, theta)


# Export all functions
__all__ = [
    'sin', 'cos', 'tan', 'cot', 'sec', 'csc',
    'asin', 'acos', 'atan', 'atan2',
    'sinh', 'cosh', 'tanh',
    'asinh', 'acosh', 'atanh',
    'degrees_to_radians', 'radians_to_degrees',
    'law_of_cosines', 'law_of_sines_angle',
    'pythagorean_theorem',
    'polar_to_cartesian', 'cartesian_to_polar',
]
