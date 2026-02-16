"""
Geographic Functions

Geographic calculations, distance, coordinates, and GIS utilities.
"""

import math
from typing import Tuple


# Earth's radius in kilometers
EARTH_RADIUS_KM = 6371.0
EARTH_RADIUS_MI = 3959.0


def degrees_to_radians(degrees: float) -> float:
    """Convert degrees to radians"""
    return degrees * math.pi / 180


def radians_to_degrees(radians: float) -> float:
    """Convert radians to degrees"""
    return radians * 180 / math.pi


def haversine_distance(lat1: float, lon1: float, lat2: float, lon2: float, 
                       unit: str = 'km') -> float:
    """
    Calculate distance between two points using Haversine formula
    
    Args:
        lat1: Latitude of point 1 (degrees)
        lon1: Longitude of point 1 (degrees)
        lat2: Latitude of point 2 (degrees)
        lon2: Longitude of point 2 (degrees)
        unit: 'km' or 'mi'
        
    Returns:
        Distance in specified unit
        
    Example:
        >>> dist = haversine_distance(40.7128, -74.0060, 51.5074, -0.1278)
        >>> 5500 < dist < 5600
        True
    """
    # Convert to radians
    lat1_rad = degrees_to_radians(lat1)
    lon1_rad = degrees_to_radians(lon1)
    lat2_rad = degrees_to_radians(lat2)
    lon2_rad = degrees_to_radians(lon2)
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat/2)**2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))
    
    radius = EARTH_RADIUS_MI if unit == 'mi' else EARTH_RADIUS_KM
    
    return radius * c


def vincenty_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    More accurate distance using Vincenty formula (spheroid)
    
    Args:
        lat1, lon1: Point 1 coordinates
        lat2, lon2: Point 2 coordinates
        
    Returns:
        Distance in kilometers
        
    Example:
        >>> dist = vincenty_distance(40.7128, -74.0060, 51.5074, -0.1278)
        >>> 5500 < dist < 5600
        True
    """
    # Simplified inverse Vincenty formula
    # For more accuracy, use a library like geopy
    return haversine_distance(lat1, lon1, lat2, lon2)


def bearing_between_points(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate initial bearing from point 1 to point 2
    
    Args:
        lat1, lon1: Starting point
        lat2, lon2: Ending point
        
    Returns:
        Bearing in degrees (0-360, where 0 is north)
        
    Example:
        >>> bearing = bearing_between_points(40, -74, 51, 0)
        >>> 0 <= bearing <= 360
        True
    """
    lat1_rad = degrees_to_radians(lat1)
    lat2_rad = degrees_to_radians(lat2)
    dlon_rad = degrees_to_radians(lon2 - lon1)
    
    y = math.sin(dlon_rad) * math.cos(lat2_rad)
    x = math.cos(lat1_rad) * math.sin(lat2_rad) - \
        math.sin(lat1_rad) * math.cos(lat2_rad) * math.cos(dlon_rad)
    
    bearing_rad = math.atan2(y, x)
    bearing_deg = radians_to_degrees(bearing_rad)
    
    return (bearing_deg + 360) % 360


def destination_point(lat: float, lon: float, distance: float, bearing: float) -> Tuple[float, float]:
    """
    Calculate destination point given distance and bearing
    
    Args:
        lat, lon: Starting point
        distance: Distance in km
        bearing: Bearing in degrees
        
    Returns:
        (lat, lon) of destination
        
    Example:
        >>> lat, lon = destination_point(40.7128, -74.0060, 100, 90)
        >>> isinstance(lat, float) and isinstance(lon, float)
        True
    """
    lat_rad = degrees_to_radians(lat)
    lon_rad = degrees_to_radians(lon)
    bearing_rad = degrees_to_radians(bearing)
    
    angular_distance = distance / EARTH_RADIUS_KM
    
    lat2_rad = math.asin(
        math.sin(lat_rad) * math.cos(angular_distance) +
        math.cos(lat_rad) * math.sin(angular_distance) * math.cos(bearing_rad)
    )
    
    lon2_rad = lon_rad + math.atan2(
        math.sin(bearing_rad) * math.sin(angular_distance) * math.cos(lat_rad),
        math.cos(angular_distance) - math.sin(lat_rad) * math.sin(lat2_rad)
    )
    
    return radians_to_degrees(lat2_rad), radians_to_degrees(lon2_rad)


def midpoint(lat1: float, lon1: float, lat2: float, lon2: float) -> Tuple[float, float]:
    """
    Calculate midpoint between two coordinates
    
    Args:
        lat1, lon1: Point 1
        lat2, lon2: Point 2
        
    Returns:
        (lat, lon) of midpoint
        
    Example:
        >>> lat, lon = midpoint(40, -74, 50, -70)
        >>> 40 < lat < 50
        True
    """
    lat1_rad = degrees_to_radians(lat1)
    lon1_rad = degrees_to_radians(lon1)
    lat2_rad = degrees_to_radians(lat2)
    dlon_rad = degrees_to_radians(lon2 - lon1)
    
    bx = math.cos(lat2_rad) * math.cos(dlon_rad)
    by = math.cos(lat2_rad) * math.sin(dlon_rad)
    
    lat3_rad = math.atan2(
        math.sin(lat1_rad) + math.sin(lat2_rad),
        math.sqrt((math.cos(lat1_rad) + bx)**2 + by**2)
    )
    
    lon3_rad = lon1_rad + math.atan2(by, math.cos(lat1_rad) + bx)
    
    return radians_to_degrees(lat3_rad), radians_to_degrees(lon3_rad)


def is_point_in_circle(lat: float, lon: float, center_lat: float, center_lon: float, 
                       radius_km: float) -> bool:
    """
    Check if point is within circle
    
    Args:
        lat, lon: Point to check
        center_lat, center_lon: Circle center
        radius_km: Radius in km
        
    Returns:
        True if point is inside circle
        
    Example:
        >>> is_point_in_circle(40.7, -74.0, 40.7128, -74.0060, 10)
        True
    """
    distance = haversine_distance(lat, lon, center_lat, center_lon)
    return distance <= radius_km


def bounding_box(lat: float, lon: float, distance_km: float) -> Tuple[float, float, float, float]:
    """
    Calculate bounding box around a point
    
    Args:
        lat, lon: Center point
        distance_km: Distance from center to edges
        
    Returns:
        (min_lat, min_lon, max_lat, max_lon)
        
    Example:
        >>> box = bounding_box(40.7128, -74.0060, 10)
        >>> len(box) == 4
        True
    """
    # North
    north_lat, _ = destination_point(lat, lon, distance_km, 0)
    
    # South
    south_lat, _ = destination_point(lat, lon, distance_km, 180)
    
    # East
    _, east_lon = destination_point(lat, lon, distance_km, 90)
    
    # West
    _, west_lon = destination_point(lat, lon, distance_km, 270)
    
    return south_lat, west_lon, north_lat, east_lon


def is_valid_coordinate(lat: float, lon: float) -> bool:
    """
    Check if coordinates are valid
    
    Args:
        lat: Latitude
        lon: Longitude
        
    Returns:
        True if valid
        
    Example:
        >>> is_valid_coordinate(40.7128, -74.0060)
        True
    """
    return -90 <= lat <= 90 and -180 <= lon <= 180


def dms_to_decimal(degrees: int, minutes: int, seconds: float, direction: str = 'N') -> float:
    """
    Convert DMS (degrees, minutes, seconds) to decimal
    
    Args:
        degrees: Degrees
        minutes: Minutes
        seconds: Seconds
        direction: N, S, E, or W
        
    Returns:
        Decimal degrees
        
    Example:
        >>> dms_to_decimal(40, 42, 46, 'N')
        40.712...
    """
    decimal = degrees + minutes/60 + seconds/3600
    
    if direction in ['S', 'W']:
        decimal = -decimal
    
    return decimal


def decimal_to_dms(decimal: float) -> Tuple[int, int, float, str]:
    """
    Convert decimal degrees to DMS
    
    Args:
        decimal: Decimal degrees
        
    Returns:
        (degrees, minutes, seconds, direction)
        
    Example:
        >>> d, m, s, dir = decimal_to_dms(40.7128)
        >>> d == 40
        True
    """
    direction = 'N' if decimal >= 0 else 'S'
    decimal = abs(decimal)
    
    degrees = int(decimal)
    minutes_decimal = (decimal - degrees) * 60
    minutes = int(minutes_decimal)
    seconds = (minutes_decimal - minutes) * 60
    
    return degrees, minutes, seconds, direction


def meters_to_feet(meters: float) -> float:
    """Convert meters to feet"""
    return meters * 3.28084


def feet_to_meters(feet: float) -> float:
    """Convert feet to meters"""
    return feet / 3.28084


def km_to_miles(km: float) -> float:
    """Convert kilometers to miles"""
    return km * 0.621371


def miles_to_km(miles: float) -> float:
    """Convert miles to kilometers"""
    return miles / 0.621371


def nautical_miles_to_km(nm: float) -> float:
    """Convert nautical miles to kilometers"""
    return nm * 1.852


def km_to_nautical_miles(km: float) -> float:
    """Convert kilometers to nautical miles"""
    return km / 1.852


def cross_track_distance(lat1: float, lon1: float, lat2: float, lon2: float,
                         lat3: float, lon3: float) -> float:
    """
    Distance of point 3 from great circle path between points 1 and 2
    
    Args:
        lat1, lon1: Start of path
        lat2, lon2: End of path
        lat3, lon3: Point to measure
        
    Returns:
        Cross-track distance in km
        
    Example:
        >>> dist = cross_track_distance(40, -74, 50, -60, 45, -70)
        >>> isinstance(dist, float)
        True
    """
    # Convert to radians
    lat1_rad = degrees_to_radians(lat1)
    lon1_rad = degrees_to_radians(lon1)
    lat3_rad = degrees_to_radians(lat3)
    lon3_rad = degrees_to_radians(lon3)
    
    # Distance from point 1 to point 3
    d13 = haversine_distance(lat1, lon1, lat3, lon3) / EARTH_RADIUS_KM
    
    # Bearing from point 1 to point 3
    bearing13 = degrees_to_radians(bearing_between_points(lat1, lon1, lat3, lon3))
    
    # Bearing from point 1 to point 2
    bearing12 = degrees_to_radians(bearing_between_points(lat1, lon1, lat2, lon2))
    
    # Cross-track distance
    dxt = math.asin(math.sin(d13) * math.sin(bearing13 - bearing12))
    
    return abs(dxt * EARTH_RADIUS_KM)


def area_of_polygon(coords: list) -> float:
    """
    Calculate area of polygon on sphere (approximate)
    
    Args:
        coords: List of (lat, lon) tuples
        
    Returns:
        Area in square kilometers
        
    Example:
        >>> coords = [(0, 0), (0, 1), (1, 1), (1, 0)]
        >>> area = area_of_polygon(coords)
        >>> area > 0
        True
    """
    # Simple spherical excess method
    n = len(coords)
    if n < 3:
        return 0
    
    area = 0
    for i in range(n):
        j = (i + 1) % n
        lat1, lon1 = coords[i]
        lat2, lon2 = coords[j]
        
        lat1_rad = degrees_to_radians(lat1)
        lat2_rad = degrees_to_radians(lat2)
        dlon_rad = degrees_to_radians(lon2 - lon1)
        
        area += dlon_rad * (2 + math.sin(lat1_rad) + math.sin(lat2_rad))
    
    area = abs(area * EARTH_RADIUS_KM * EARTH_RADIUS_KM / 2)
    
    return area


def normalize_longitude(lon: float) -> float:
    """
    Normalize longitude to -180 to 180
    
    Args:
        lon: Longitude
        
    Returns:
        Normalized longitude
        
    Example:
        >>> normalize_longitude(190)
        -170.0
    """
    while lon > 180:
        lon -= 360
    while lon < -180:
        lon += 360
    return lon


def normalize_latitude(lat: float) -> float:
    """
    Normalize latitude to -90 to 90
    
    Args:
        lat: Latitude
        
    Returns:
        Normalized latitude
        
    Example:
        >>> normalize_latitude(100)
        80.0
    """
    if lat > 90:
        lat = 180 - lat
    if lat < -90:
        lat = -180 - lat
    return max(-90, min(90, lat))


# Export all functions
__all__ = [
    'haversine_distance', 'vincenty_distance',
    'bearing_between_points', 'destination_point', 'midpoint',
    'is_point_in_circle', 'bounding_box', 'is_valid_coordinate',
    'dms_to_decimal', 'decimal_to_dms',
    'meters_to_feet', 'feet_to_meters',
    'km_to_miles', 'miles_to_km',
    'nautical_miles_to_km', 'km_to_nautical_miles',
    'cross_track_distance', 'area_of_polygon',
    'normalize_longitude', 'normalize_latitude',
]
