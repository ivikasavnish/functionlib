"""
Geometry Functions

2D and 3D geometric calculations including shapes, transformations, and measurements.
"""

import math
from typing import Tuple, List


# 2D Geometry

def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculates distance between two points in 2D
    
    Args:
        x1, y1: First point coordinates
        x2, y2: Second point coordinates
        
    Returns:
        Euclidean distance
        
    Example:
        >>> distance_2d(0, 0, 3, 4)
        5.0
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2)


def midpoint_2d(x1: float, y1: float, x2: float, y2: float) -> Tuple[float, float]:
    """
    Finds midpoint between two points in 2D
    
    Args:
        x1, y1: First point
        x2, y2: Second point
        
    Returns:
        Midpoint coordinates
        
    Example:
        >>> midpoint_2d(0, 0, 4, 6)
        (2.0, 3.0)
    """
    return ((x1 + x2) / 2, (y1 + y2) / 2)


def slope(x1: float, y1: float, x2: float, y2: float) -> float:
    """
    Calculates slope of line through two points
    
    Args:
        x1, y1: First point
        x2, y2: Second point
        
    Returns:
        Slope (m)
        
    Example:
        >>> slope(0, 0, 2, 4)
        2.0
    """
    if x2 == x1:
        raise ValueError("Vertical line - undefined slope")
    return (y2 - y1) / (x2 - x1)


def point_slope_form(x: float, y: float, m: float, x0: float) -> float:
    """
    Evaluates point-slope form: y - y1 = m(x - x1)
    
    Args:
        x: x-coordinate to evaluate
        y: y-coordinate of known point
        m: Slope
        x0: x-coordinate of known point
        
    Returns:
        y-value
        
    Example:
        >>> point_slope_form(3, 1, 2, 1)  # y - 1 = 2(x - 1) at x=3
        5.0
    """
    return m * (x - x0) + y


def circle_area(radius: float) -> float:
    """
    Calculates area of circle
    
    Args:
        radius: Circle radius
        
    Returns:
        Area (πr²)
        
    Example:
        >>> circle_area(5)
        78.53981633974483
    """
    return math.pi * radius ** 2


def circle_circumference(radius: float) -> float:
    """
    Calculates circumference of circle
    
    Args:
        radius: Circle radius
        
    Returns:
        Circumference (2πr)
        
    Example:
        >>> circle_circumference(5)
        31.41592653589793
    """
    return 2 * math.pi * radius


def rectangle_area(length: float, width: float) -> float:
    """
    Calculates area of rectangle
    
    Args:
        length: Length
        width: Width
        
    Returns:
        Area (l × w)
        
    Example:
        >>> rectangle_area(5, 3)
        15.0
    """
    return length * width


def rectangle_perimeter(length: float, width: float) -> float:
    """
    Calculates perimeter of rectangle
    
    Args:
        length: Length
        width: Width
        
    Returns:
        Perimeter (2l + 2w)
        
    Example:
        >>> rectangle_perimeter(5, 3)
        16.0
    """
    return 2 * (length + width)


def triangle_area(base: float, height: float) -> float:
    """
    Calculates area of triangle using base and height
    
    Args:
        base: Base length
        height: Height
        
    Returns:
        Area (½ × b × h)
        
    Example:
        >>> triangle_area(6, 4)
        12.0
    """
    return 0.5 * base * height


def triangle_area_heron(a: float, b: float, c: float) -> float:
    """
    Calculates triangle area using Heron's formula
    
    Args:
        a, b, c: Side lengths
        
    Returns:
        Area
        
    Example:
        >>> triangle_area_heron(3, 4, 5)
        6.0
    """
    s = (a + b + c) / 2  # Semi-perimeter
    return math.sqrt(s * (s - a) * (s - b) * (s - c))


def triangle_perimeter(a: float, b: float, c: float) -> float:
    """
    Calculates perimeter of triangle
    
    Args:
        a, b, c: Side lengths
        
    Returns:
        Perimeter
        
    Example:
        >>> triangle_perimeter(3, 4, 5)
        12.0
    """
    return a + b + c


def square_area(side: float) -> float:
    """
    Calculates area of square
    
    Args:
        side: Side length
        
    Returns:
        Area (s²)
        
    Example:
        >>> square_area(4)
        16.0
    """
    return side ** 2


def square_perimeter(side: float) -> float:
    """
    Calculates perimeter of square
    
    Args:
        side: Side length
        
    Returns:
        Perimeter (4s)
        
    Example:
        >>> square_perimeter(4)
        16.0
    """
    return 4 * side


def trapezoid_area(base1: float, base2: float, height: float) -> float:
    """
    Calculates area of trapezoid
    
    Args:
        base1: First base length
        base2: Second base length
        height: Height
        
    Returns:
        Area (½(b₁ + b₂)h)
        
    Example:
        >>> trapezoid_area(5, 7, 4)
        24.0
    """
    return 0.5 * (base1 + base2) * height


def parallelogram_area(base: float, height: float) -> float:
    """
    Calculates area of parallelogram
    
    Args:
        base: Base length
        height: Height
        
    Returns:
        Area (b × h)
        
    Example:
        >>> parallelogram_area(6, 4)
        24.0
    """
    return base * height


def ellipse_area(semi_major: float, semi_minor: float) -> float:
    """
    Calculates area of ellipse
    
    Args:
        semi_major: Semi-major axis (a)
        semi_minor: Semi-minor axis (b)
        
    Returns:
        Area (πab)
        
    Example:
        >>> ellipse_area(5, 3)
        47.12388980384689
    """
    return math.pi * semi_major * semi_minor


def sector_area(radius: float, angle_degrees: float) -> float:
    """
    Calculates area of circular sector
    
    Args:
        radius: Circle radius
        angle_degrees: Central angle in degrees
        
    Returns:
        Sector area
        
    Example:
        >>> sector_area(5, 90)
        19.634954084936208
    """
    angle_radians = math.radians(angle_degrees)
    return 0.5 * radius**2 * angle_radians


def arc_length_circle(radius: float, angle_degrees: float) -> float:
    """
    Calculates arc length
    
    Args:
        radius: Circle radius
        angle_degrees: Central angle in degrees
        
    Returns:
        Arc length
        
    Example:
        >>> arc_length_circle(5, 90)
        7.853981633974483
    """
    angle_radians = math.radians(angle_degrees)
    return radius * angle_radians


# 3D Geometry

def distance_3d(x1: float, y1: float, z1: float, x2: float, y2: float, z2: float) -> float:
    """
    Calculates distance between two points in 3D
    
    Args:
        x1, y1, z1: First point coordinates
        x2, y2, z2: Second point coordinates
        
    Returns:
        Euclidean distance
        
    Example:
        >>> distance_3d(0, 0, 0, 2, 3, 6)
        7.0
    """
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)


def sphere_volume(radius: float) -> float:
    """
    Calculates volume of sphere
    
    Args:
        radius: Sphere radius
        
    Returns:
        Volume (4/3 πr³)
        
    Example:
        >>> sphere_volume(3)
        113.09733552923255
    """
    return (4/3) * math.pi * radius**3


def sphere_surface_area(radius: float) -> float:
    """
    Calculates surface area of sphere
    
    Args:
        radius: Sphere radius
        
    Returns:
        Surface area (4πr²)
        
    Example:
        >>> sphere_surface_area(3)
        113.09733552923255
    """
    return 4 * math.pi * radius**2


def cube_volume(side: float) -> float:
    """
    Calculates volume of cube
    
    Args:
        side: Side length
        
    Returns:
        Volume (s³)
        
    Example:
        >>> cube_volume(4)
        64.0
    """
    return side ** 3


def cube_surface_area(side: float) -> float:
    """
    Calculates surface area of cube
    
    Args:
        side: Side length
        
    Returns:
        Surface area (6s²)
        
    Example:
        >>> cube_surface_area(4)
        96.0
    """
    return 6 * side**2


def cylinder_volume(radius: float, height: float) -> float:
    """
    Calculates volume of cylinder
    
    Args:
        radius: Base radius
        height: Height
        
    Returns:
        Volume (πr²h)
        
    Example:
        >>> cylinder_volume(3, 5)
        141.3716694115407
    """
    return math.pi * radius**2 * height


def cylinder_surface_area(radius: float, height: float) -> float:
    """
    Calculates surface area of cylinder
    
    Args:
        radius: Base radius
        height: Height
        
    Returns:
        Surface area (2πr² + 2πrh)
        
    Example:
        >>> cylinder_surface_area(3, 5)
        150.79644737231007
    """
    return 2 * math.pi * radius**2 + 2 * math.pi * radius * height


def cone_volume(radius: float, height: float) -> float:
    """
    Calculates volume of cone
    
    Args:
        radius: Base radius
        height: Height
        
    Returns:
        Volume (1/3 πr²h)
        
    Example:
        >>> cone_volume(3, 5)
        47.12388980384689
    """
    return (1/3) * math.pi * radius**2 * height


def cone_surface_area(radius: float, height: float) -> float:
    """
    Calculates surface area of cone (including base)
    
    Args:
        radius: Base radius
        height: Height
        
    Returns:
        Surface area (πr² + πr√(r²+h²))
        
    Example:
        >>> cone_surface_area(3, 4)
        75.39822368615503
    """
    slant_height = math.sqrt(radius**2 + height**2)
    return math.pi * radius**2 + math.pi * radius * slant_height


def rectangular_prism_volume(length: float, width: float, height: float) -> float:
    """
    Calculates volume of rectangular prism
    
    Args:
        length: Length
        width: Width
        height: Height
        
    Returns:
        Volume (l × w × h)
        
    Example:
        >>> rectangular_prism_volume(3, 4, 5)
        60.0
    """
    return length * width * height


def rectangular_prism_surface_area(length: float, width: float, height: float) -> float:
    """
    Calculates surface area of rectangular prism
    
    Args:
        length: Length
        width: Width
        height: Height
        
    Returns:
        Surface area (2lw + 2lh + 2wh)
        
    Example:
        >>> rectangular_prism_surface_area(3, 4, 5)
        94.0
    """
    return 2 * (length * width + length * height + width * height)


def pyramid_volume(base_area: float, height: float) -> float:
    """
    Calculates volume of pyramid
    
    Args:
        base_area: Area of base
        height: Height
        
    Returns:
        Volume (1/3 × base_area × h)
        
    Example:
        >>> pyramid_volume(16, 9)
        48.0
    """
    return (1/3) * base_area * height


def torus_volume(major_radius: float, minor_radius: float) -> float:
    """
    Calculates volume of torus
    
    Args:
        major_radius: Distance from center to tube center (R)
        minor_radius: Tube radius (r)
        
    Returns:
        Volume (2π²Rr²)
        
    Example:
        >>> torus_volume(5, 2)
        394.78417604357434
    """
    return 2 * math.pi**2 * major_radius * minor_radius**2


def torus_surface_area(major_radius: float, minor_radius: float) -> float:
    """
    Calculates surface area of torus
    
    Args:
        major_radius: Distance from center to tube center (R)
        minor_radius: Tube radius (r)
        
    Returns:
        Surface area (4π²Rr)
        
    Example:
        >>> torus_surface_area(5, 2)
        394.78417604357434
    """
    return 4 * math.pi**2 * major_radius * minor_radius


def polygon_area_regular(n: int, side_length: float) -> float:
    """
    Calculates area of regular polygon
    
    Args:
        n: Number of sides
        side_length: Length of each side
        
    Returns:
        Area
        
    Example:
        >>> polygon_area_regular(6, 4)  # Regular hexagon
        41.569219381653056
    """
    return (n * side_length**2) / (4 * math.tan(math.pi / n))


def polygon_perimeter(side_lengths: List[float]) -> float:
    """
    Calculates perimeter of polygon
    
    Args:
        side_lengths: List of side lengths
        
    Returns:
        Perimeter (sum of sides)
        
    Example:
        >>> polygon_perimeter([3, 4, 5, 6])
        18.0
    """
    return sum(side_lengths)


# Export all functions
__all__ = [
    'distance_2d',
    'midpoint_2d',
    'slope',
    'point_slope_form',
    'circle_area',
    'circle_circumference',
    'rectangle_area',
    'rectangle_perimeter',
    'triangle_area',
    'triangle_area_heron',
    'triangle_perimeter',
    'square_area',
    'square_perimeter',
    'trapezoid_area',
    'parallelogram_area',
    'ellipse_area',
    'sector_area',
    'arc_length_circle',
    'distance_3d',
    'sphere_volume',
    'sphere_surface_area',
    'cube_volume',
    'cube_surface_area',
    'cylinder_volume',
    'cylinder_surface_area',
    'cone_volume',
    'cone_surface_area',
    'rectangular_prism_volume',
    'rectangular_prism_surface_area',
    'pyramid_volume',
    'torus_volume',
    'torus_surface_area',
    'polygon_area_regular',
    'polygon_perimeter',
]
