"""
Color Utilities

Color conversions, manipulations, and calculations.
"""

import math
from typing import Tuple


def rgb_to_hex(r: int, g: int, b: int) -> str:
    """
    Convert RGB to hex color
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        
    Returns:
        Hex color string
        
    Example:
        >>> rgb_to_hex(255, 0, 0)
        '#FF0000'
    """
    return f'#{r:02X}{g:02X}{b:02X}'


def hex_to_rgb(hex_color: str) -> Tuple[int, int, int]:
    """
    Convert hex to RGB
    
    Args:
        hex_color: Hex color (with or without #)
        
    Returns:
        (r, g, b) tuple
        
    Example:
        >>> hex_to_rgb('#FF0000')
        (255, 0, 0)
    """
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def rgb_to_hsl(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Convert RGB to HSL
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        
    Returns:
        (h, s, l) where h is 0-360, s and l are 0-1
        
    Example:
        >>> h, s, l = rgb_to_hsl(255, 0, 0)
        >>> abs(h - 0) < 1 and abs(s - 1) < 0.01
        True
    """
    r, g, b = r / 255, g / 255, b / 255
    
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val
    
    # Lightness
    l = (max_val + min_val) / 2
    
    if diff == 0:
        h = s = 0
    else:
        # Saturation
        s = diff / (2 - max_val - min_val) if l > 0.5 else diff / (max_val + min_val)
        
        # Hue
        if max_val == r:
            h = ((g - b) / diff + (6 if g < b else 0)) / 6
        elif max_val == g:
            h = ((b - r) / diff + 2) / 6
        else:
            h = ((r - g) / diff + 4) / 6
        
        h *= 360
    
    return h, s, l


def hsl_to_rgb(h: float, s: float, l: float) -> Tuple[int, int, int]:
    """
    Convert HSL to RGB
    
    Args:
        h: Hue (0-360)
        s: Saturation (0-1)
        l: Lightness (0-1)
        
    Returns:
        (r, g, b) tuple (0-255)
        
    Example:
        >>> hsl_to_rgb(0, 1, 0.5)
        (255, 0, 0)
    """
    h = h / 360
    
    def hue_to_rgb(p, q, t):
        if t < 0:
            t += 1
        if t > 1:
            t -= 1
        if t < 1/6:
            return p + (q - p) * 6 * t
        if t < 1/2:
            return q
        if t < 2/3:
            return p + (q - p) * (2/3 - t) * 6
        return p
    
    if s == 0:
        r = g = b = l
    else:
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = hue_to_rgb(p, q, h + 1/3)
        g = hue_to_rgb(p, q, h)
        b = hue_to_rgb(p, q, h - 1/3)
    
    return int(r * 255), int(g * 255), int(b * 255)


def rgb_to_hsv(r: int, g: int, b: int) -> Tuple[float, float, float]:
    """
    Convert RGB to HSV
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        
    Returns:
        (h, s, v) where h is 0-360, s and v are 0-1
        
    Example:
        >>> h, s, v = rgb_to_hsv(255, 0, 0)
        >>> abs(h - 0) < 1 and abs(v - 1) < 0.01
        True
    """
    r, g, b = r / 255, g / 255, b / 255
    
    max_val = max(r, g, b)
    min_val = min(r, g, b)
    diff = max_val - min_val
    
    # Value
    v = max_val
    
    # Saturation
    s = 0 if max_val == 0 else diff / max_val
    
    # Hue
    if diff == 0:
        h = 0
    elif max_val == r:
        h = ((g - b) / diff + (6 if g < b else 0)) / 6
    elif max_val == g:
        h = ((b - r) / diff + 2) / 6
    else:
        h = ((r - g) / diff + 4) / 6
    
    h *= 360
    
    return h, s, v


def hsv_to_rgb(h: float, s: float, v: float) -> Tuple[int, int, int]:
    """
    Convert HSV to RGB
    
    Args:
        h: Hue (0-360)
        s: Saturation (0-1)
        v: Value (0-1)
        
    Returns:
        (r, g, b) tuple (0-255)
        
    Example:
        >>> hsv_to_rgb(0, 1, 1)
        (255, 0, 0)
    """
    h = h / 60
    i = int(h)
    f = h - i
    
    p = v * (1 - s)
    q = v * (1 - s * f)
    t = v * (1 - s * (1 - f))
    
    i = i % 6
    
    if i == 0:
        r, g, b = v, t, p
    elif i == 1:
        r, g, b = q, v, p
    elif i == 2:
        r, g, b = p, v, t
    elif i == 3:
        r, g, b = p, q, v
    elif i == 4:
        r, g, b = t, p, v
    else:
        r, g, b = v, p, q
    
    return int(r * 255), int(g * 255), int(b * 255)


def rgb_to_grayscale(r: int, g: int, b: int) -> int:
    """
    Convert RGB to grayscale using luminosity method
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        
    Returns:
        Grayscale value (0-255)
        
    Example:
        >>> rgb_to_grayscale(255, 0, 0)
        54
    """
    return int(0.2126 * r + 0.7152 * g + 0.0722 * b)


def color_luminance(r: int, g: int, b: int) -> float:
    """
    Calculate relative luminance (0-1)
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        
    Returns:
        Luminance value
        
    Example:
        >>> color_luminance(255, 255, 255)
        1.0
    """
    def adjust(c):
        c = c / 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    
    return 0.2126 * adjust(r) + 0.7152 * adjust(g) + 0.0722 * adjust(b)


def contrast_ratio(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """
    Calculate WCAG contrast ratio between two colors
    
    Args:
        rgb1: First color (r, g, b)
        rgb2: Second color (r, g, b)
        
    Returns:
        Contrast ratio (1-21)
        
    Example:
        >>> contrast_ratio((255, 255, 255), (0, 0, 0))
        21.0
    """
    l1 = color_luminance(*rgb1)
    l2 = color_luminance(*rgb2)
    
    lighter = max(l1, l2)
    darker = min(l1, l2)
    
    return (lighter + 0.05) / (darker + 0.05)


def complementary_color(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Get complementary color (opposite on color wheel)
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        
    Returns:
        Complementary (r, g, b)
        
    Example:
        >>> complementary_color(255, 0, 0)
        (0, 255, 255)
    """
    h, s, v = rgb_to_hsv(r, g, b)
    h = (h + 180) % 360
    return hsv_to_rgb(h, s, v)


def blend_colors(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int], 
                 alpha: float = 0.5) -> Tuple[int, int, int]:
    """
    Blend two colors with alpha
    
    Args:
        rgb1: First color
        rgb2: Second color
        alpha: Blend factor (0-1, 0=all rgb1, 1=all rgb2)
        
    Returns:
        Blended color
        
    Example:
        >>> blend_colors((255, 0, 0), (0, 0, 255), 0.5)
        (127, 0, 127)
    """
    r = int(rgb1[0] * (1 - alpha) + rgb2[0] * alpha)
    g = int(rgb1[1] * (1 - alpha) + rgb2[1] * alpha)
    b = int(rgb1[2] * (1 - alpha) + rgb2[2] * alpha)
    
    return r, g, b


def lighten_color(r: int, g: int, b: int, amount: float) -> Tuple[int, int, int]:
    """
    Lighten a color
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        amount: Amount to lighten (0-1)
        
    Returns:
        Lightened color
        
    Example:
        >>> r, g, b = lighten_color(128, 0, 0, 0.5)
        >>> r > 128
        True
    """
    h, s, l = rgb_to_hsl(r, g, b)
    l = min(1, l + amount)
    return hsl_to_rgb(h, s, l)


def darken_color(r: int, g: int, b: int, amount: float) -> Tuple[int, int, int]:
    """
    Darken a color
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        amount: Amount to darken (0-1)
        
    Returns:
        Darkened color
        
    Example:
        >>> r, g, b = darken_color(128, 0, 0, 0.5)
        >>> r < 128
        True
    """
    h, s, l = rgb_to_hsl(r, g, b)
    l = max(0, l - amount)
    return hsl_to_rgb(h, s, l)


def saturate_color(r: int, g: int, b: int, amount: float) -> Tuple[int, int, int]:
    """
    Increase saturation
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        amount: Amount to increase (0-1)
        
    Returns:
        More saturated color
        
    Example:
        >>> saturate_color(200, 100, 100, 0.5)
        (255, 50, 50)
    """
    h, s, l = rgb_to_hsl(r, g, b)
    s = min(1, s + amount)
    return hsl_to_rgb(h, s, l)


def desaturate_color(r: int, g: int, b: int, amount: float) -> Tuple[int, int, int]:
    """
    Decrease saturation
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        amount: Amount to decrease (0-1)
        
    Returns:
        Less saturated color
        
    Example:
        >>> desaturate_color(255, 0, 0, 1.0)
        (127, 127, 127)
    """
    h, s, l = rgb_to_hsl(r, g, b)
    s = max(0, s - amount)
    return hsl_to_rgb(h, s, l)


def color_temperature(kelvin: int) -> Tuple[int, int, int]:
    """
    Convert color temperature (Kelvin) to RGB
    
    Args:
        kelvin: Temperature (1000-40000)
        
    Returns:
        Approximate RGB color
        
    Example:
        >>> color_temperature(6500)  # Daylight
        (255, 249, 253)
    """
    temp = kelvin / 100
    
    # Red
    if temp <= 66:
        r = 255
    else:
        r = temp - 60
        r = 329.698727446 * (r ** -0.1332047592)
        r = max(0, min(255, int(r)))
    
    # Green
    if temp <= 66:
        g = temp
        g = 99.4708025861 * math.log(g) - 161.1195681661
    else:
        g = temp - 60
        g = 288.1221695283 * (g ** -0.0755148492)
    g = max(0, min(255, int(g)))
    
    # Blue
    if temp >= 66:
        b = 255
    elif temp <= 19:
        b = 0
    else:
        b = temp - 10
        b = 138.5177312231 * math.log(b) - 305.0447927307
        b = max(0, min(255, int(b)))
    
    return r, g, b


def invert_color(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Invert color
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        
    Returns:
        Inverted color
        
    Example:
        >>> invert_color(255, 0, 0)
        (0, 255, 255)
    """
    return 255 - r, 255 - g, 255 - b


def sepia_tone(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Apply sepia tone effect
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        
    Returns:
        Sepia-toned color
        
    Example:
        >>> sepia_tone(255, 255, 255)
        (255, 255, 239)
    """
    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
    
    return min(255, tr), min(255, tg), min(255, tb)


def color_distance(rgb1: Tuple[int, int, int], rgb2: Tuple[int, int, int]) -> float:
    """
    Calculate Euclidean distance between two colors
    
    Args:
        rgb1: First color
        rgb2: Second color
        
    Returns:
        Distance
        
    Example:
        >>> color_distance((255, 0, 0), (0, 0, 0))
        255.0
    """
    return math.sqrt(
        (rgb1[0] - rgb2[0])**2 + 
        (rgb1[1] - rgb2[1])**2 + 
        (rgb1[2] - rgb2[2])**2
    )


def nearest_web_safe_color(r: int, g: int, b: int) -> Tuple[int, int, int]:
    """
    Find nearest web-safe color (00, 33, 66, 99, CC, FF)
    
    Args:
        r: Red (0-255)
        g: Green (0-255)
        b: Blue (0-255)
        
    Returns:
        Nearest web-safe color
        
    Example:
        >>> nearest_web_safe_color(100, 100, 100)
        (102, 102, 102)
    """
    web_safe_values = [0, 51, 102, 153, 204, 255]
    
    def nearest(val):
        return min(web_safe_values, key=lambda x: abs(x - val))
    
    return nearest(r), nearest(g), nearest(b)


def rgba_to_rgb(r: int, g: int, b: int, a: float, bg_r: int = 255, bg_g: int = 255, bg_b: int = 255) -> Tuple[int, int, int]:
    """
    Convert RGBA to RGB by compositing over background
    
    Args:
        r, g, b: Foreground color (0-255)
        a: Alpha (0-1)
        bg_r, bg_g, bg_b: Background color (default white)
        
    Returns:
        Composited RGB color
        
    Example:
        >>> rgba_to_rgb(255, 0, 0, 0.5)
        (255, 127, 127)
    """
    r_out = int(r * a + bg_r * (1 - a))
    g_out = int(g * a + bg_g * (1 - a))
    b_out = int(b * a + bg_b * (1 - a))
    
    return r_out, g_out, b_out


# Export all functions
__all__ = [
    'rgb_to_hex', 'hex_to_rgb',
    'rgb_to_hsl', 'hsl_to_rgb',
    'rgb_to_hsv', 'hsv_to_rgb',
    'rgb_to_grayscale', 'color_luminance', 'contrast_ratio',
    'complementary_color', 'blend_colors',
    'lighten_color', 'darken_color', 'saturate_color', 'desaturate_color',
    'color_temperature', 'invert_color', 'sepia_tone',
    'color_distance', 'nearest_web_safe_color', 'rgba_to_rgb',
]
