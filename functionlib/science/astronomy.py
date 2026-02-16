"""
Astronomy Functions

Astronomical calculations including planetary orbits, celestial mechanics, and time conversions.
"""

import math
from typing import Tuple


# Constants
AU_TO_KM = 149597870.7  # Astronomical Unit in km
LIGHT_SPEED = 299792.458  # Speed of light in km/s
SOLAR_MASS = 1.989e30  # kg
EARTH_RADIUS = 6371  # km
EARTH_MASS = 5.972e24  # kg
G = 6.67430e-11  # Gravitational constant (m³ kg⁻¹ s⁻²)


def astronomical_units_to_km(au: float) -> float:
    """
    Convert astronomical units to kilometers
    
    Args:
        au: Distance in AU
        
    Returns:
        Distance in kilometers
        
    Example:
        >>> astronomical_units_to_km(1)
        149597870.7
    """
    return au * AU_TO_KM


def km_to_astronomical_units(km: float) -> float:
    """
    Convert kilometers to astronomical units
    
    Args:
        km: Distance in kilometers
        
    Returns:
        Distance in AU
        
    Example:
        >>> km_to_astronomical_units(149597870.7)
        1.0
    """
    return km / AU_TO_KM


def light_years_to_km(ly: float) -> float:
    """
    Convert light years to kilometers
    
    Args:
        ly: Distance in light years
        
    Returns:
        Distance in kilometers
        
    Example:
        >>> light_years_to_km(1) > 9e12
        True
    """
    seconds_per_year = 365.25 * 24 * 3600
    return ly * LIGHT_SPEED * seconds_per_year


def parsecs_to_light_years(parsecs: float) -> float:
    """
    Convert parsecs to light years
    
    Args:
        parsecs: Distance in parsecs
        
    Returns:
        Distance in light years
        
    Example:
        >>> parsecs_to_light_years(1)
        3.26156...
    """
    return parsecs * 3.26156


def light_travel_time(distance_km: float) -> float:
    """
    Time for light to travel a distance
    
    Args:
        distance_km: Distance in kilometers
        
    Returns:
        Time in seconds
        
    Example:
        >>> light_travel_time(299792.458)
        1.0
    """
    return distance_km / LIGHT_SPEED


def orbital_velocity(mass_kg: float, radius_m: float) -> float:
    """
    Orbital velocity for circular orbit: v = sqrt(GM/r)
    
    Args:
        mass_kg: Mass of central body (kg)
        radius_m: Orbital radius (m)
        
    Returns:
        Orbital velocity (m/s)
        
    Example:
        >>> v = orbital_velocity(5.972e24, 6.771e6)
        >>> 7500 < v < 8000
        True
    """
    return math.sqrt(G * mass_kg / radius_m)


def escape_velocity(mass_kg: float, radius_m: float) -> float:
    """
    Escape velocity: v = sqrt(2GM/r)
    
    Args:
        mass_kg: Mass of body (kg)
        radius_m: Radius of body (m)
        
    Returns:
        Escape velocity (m/s)
        
    Example:
        >>> v = escape_velocity(5.972e24, 6.371e6)
        >>> 11000 < v < 12000
        True
    """
    return math.sqrt(2 * G * mass_kg / radius_m)


def orbital_period(semi_major_axis_m: float, mass_kg: float) -> float:
    """
    Orbital period using Kepler's 3rd law: T = 2π√(a³/GM)
    
    Args:
        semi_major_axis_m: Semi-major axis (m)
        mass_kg: Mass of central body (kg)
        
    Returns:
        Period in seconds
        
    Example:
        >>> period = orbital_period(6.771e6, 5.972e24)
        >>> 5400 < period < 5500
        True
    """
    return 2 * math.pi * math.sqrt(semi_major_axis_m ** 3 / (G * mass_kg))


def schwarzschild_radius(mass_kg: float) -> float:
    """
    Schwarzschild radius (black hole event horizon): rs = 2GM/c²
    
    Args:
        mass_kg: Mass (kg)
        
    Returns:
        Schwarzschild radius (m)
        
    Example:
        >>> rs = schwarzschild_radius(1.989e30)
        >>> 2900 < rs < 3000
        True
    """
    c = LIGHT_SPEED * 1000  # m/s
    return 2 * G * mass_kg / (c ** 2)


def gravitational_force(m1_kg: float, m2_kg: float, distance_m: float) -> float:
    """
    Gravitational force: F = G(m1*m2)/r²
    
    Args:
        m1_kg: Mass 1 (kg)
        m2_kg: Mass 2 (kg)
        distance_m: Distance between centers (m)
        
    Returns:
        Force (Newtons)
        
    Example:
        >>> f = gravitational_force(5.972e24, 1, 6.371e6)
        >>> 9 < f < 10
        True
    """
    return G * m1_kg * m2_kg / (distance_m ** 2)


def surface_gravity(mass_kg: float, radius_m: float) -> float:
    """
    Surface gravity: g = GM/r²
    
    Args:
        mass_kg: Mass (kg)
        radius_m: Radius (m)
        
    Returns:
        Surface gravity (m/s²)
        
    Example:
        >>> g = surface_gravity(5.972e24, 6.371e6)
        >>> 9.8 < g < 9.82
        True
    """
    return G * mass_kg / (radius_m ** 2)


def angular_diameter(actual_diameter: float, distance: float) -> float:
    """
    Angular diameter in radians: θ = d/D (small angle approximation)
    
    Args:
        actual_diameter: Actual diameter
        distance: Distance to object
        
    Returns:
        Angular diameter (radians)
        
    Example:
        >>> theta = angular_diameter(696000, 149597870.7)
        >>> 0.0046 < theta < 0.0047
        True
    """
    return actual_diameter / distance


def apparent_magnitude_from_absolute(absolute_mag: float, distance_parsecs: float) -> float:
    """
    Apparent magnitude from absolute magnitude: m = M + 5(log₁₀(d) - 1)
    
    Args:
        absolute_mag: Absolute magnitude
        distance_parsecs: Distance in parsecs
        
    Returns:
        Apparent magnitude
        
    Example:
        >>> apparent_magnitude_from_absolute(4.83, 10)
        4.83
    """
    return absolute_mag + 5 * (math.log10(distance_parsecs) - 1)


def absolute_magnitude_from_apparent(apparent_mag: float, distance_parsecs: float) -> float:
    """
    Absolute magnitude from apparent magnitude
    
    Args:
        apparent_mag: Apparent magnitude
        distance_parsecs: Distance in parsecs
        
    Returns:
        Absolute magnitude
        
    Example:
        >>> absolute_magnitude_from_apparent(4.83, 10)
        4.83
    """
    return apparent_mag - 5 * (math.log10(distance_parsecs) - 1)


def luminosity_from_magnitude(absolute_magnitude: float) -> float:
    """
    Luminosity relative to Sun from absolute magnitude
    
    Args:
        absolute_magnitude: Absolute magnitude
        
    Returns:
        Luminosity (solar luminosities)
        
    Example:
        >>> luminosity_from_magnitude(4.83)
        1.0
    """
    solar_absolute_mag = 4.83
    return 10 ** ((solar_absolute_mag - absolute_magnitude) / 2.5)


def stellar_parallax_to_distance(parallax_arcsec: float) -> float:
    """
    Distance from parallax: d = 1/p (parsecs)
    
    Args:
        parallax_arcsec: Parallax in arcseconds
        
    Returns:
        Distance in parsecs
        
    Example:
        >>> stellar_parallax_to_distance(0.1)
        10.0
    """
    if parallax_arcsec <= 0:
        raise ValueError("Parallax must be positive")
    
    return 1 / parallax_arcsec


def redshift_to_velocity(z: float) -> float:
    """
    Velocity from redshift (non-relativistic): v = cz
    
    Args:
        z: Redshift
        
    Returns:
        Velocity (km/s)
        
    Example:
        >>> redshift_to_velocity(0.1)
        29979.2458
    """
    return LIGHT_SPEED * z


def doppler_shift_frequency(v: float, f0: float) -> float:
    """
    Doppler shift for electromagnetic radiation
    
    Args:
        v: Velocity (km/s, positive = receding)
        f0: Rest frequency
        
    Returns:
        Observed frequency
        
    Example:
        >>> doppler_shift_frequency(1000, 1e9) < 1e9
        True
    """
    return f0 * math.sqrt((LIGHT_SPEED - v) / (LIGHT_SPEED + v))


def hubble_velocity(distance_mpc: float, h0: float = 70) -> float:
    """
    Recession velocity from Hubble's law: v = H₀ × d
    
    Args:
        distance_mpc: Distance in megaparsecs
        h0: Hubble constant (km/s/Mpc), default 70
        
    Returns:
        Recession velocity (km/s)
        
    Example:
        >>> hubble_velocity(10)
        700
    """
    return h0 * distance_mpc


def synodic_period(p1: float, p2: float) -> float:
    """
    Synodic period (time between conjunctions): 1/S = |1/P1 - 1/P2|
    
    Args:
        p1: Orbital period of body 1
        p2: Orbital period of body 2
        
    Returns:
        Synodic period
        
    Example:
        >>> synodic_period(365.25, 687)
        779.94...
    """
    return 1 / abs(1/p1 - 1/p2)


def julian_date(year: int, month: int, day: int, hour: float = 0) -> float:
    """
    Calculate Julian Date
    
    Args:
        year: Year
        month: Month (1-12)
        day: Day
        hour: Hour (decimal, 0-24)
        
    Returns:
        Julian Date
        
    Example:
        >>> jd = julian_date(2000, 1, 1, 12)
        >>> 2451544 < jd < 2451546
        True
    """
    if month <= 2:
        year -= 1
        month += 12
    
    a = year // 100
    b = 2 - a + (a // 4)
    
    jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5
    jd += hour / 24
    
    return jd


def sidereal_time(jd: float, longitude: float) -> float:
    """
    Local sidereal time (simplified)
    
    Args:
        jd: Julian Date
        longitude: Observer's longitude (degrees, east positive)
        
    Returns:
        Local sidereal time (hours, 0-24)
        
    Example:
        >>> lst = sidereal_time(2451545.0, 0)
        >>> 0 <= lst < 24
        True
    """
    t = (jd - 2451545.0) / 36525
    gst = 280.46061837 + 360.98564736629 * (jd - 2451545.0) + 0.000387933 * t**2 - t**3 / 38710000
    
    # Normalize to 0-360
    gst = gst % 360
    
    # Convert to hours and add longitude
    lst = (gst + longitude) / 15
    
    return lst % 24


def hour_angle(ra_hours: float, lst_hours: float) -> float:
    """
    Hour angle: HA = LST - RA
    
    Args:
        ra_hours: Right ascension (hours)
        lst_hours: Local sidereal time (hours)
        
    Returns:
        Hour angle (hours, -12 to +12)
        
    Example:
        >>> hour_angle(12, 18)
        6.0
    """
    ha = lst_hours - ra_hours
    
    # Normalize to -12 to +12
    while ha > 12:
        ha -= 24
    while ha < -12:
        ha += 24
    
    return ha


def altitude_azimuth(dec_deg: float, lat_deg: float, ha_hours: float) -> Tuple[float, float]:
    """
    Convert equatorial to horizontal coordinates
    
    Args:
        dec_deg: Declination (degrees)
        lat_deg: Latitude (degrees)
        ha_hours: Hour angle (hours)
        
    Returns:
        (altitude, azimuth) in degrees
        
    Example:
        >>> alt, az = altitude_azimuth(0, 40, 0)
        >>> 40 < alt < 51
        True
    """
    dec = math.radians(dec_deg)
    lat = math.radians(lat_deg)
    ha = math.radians(ha_hours * 15)  # Convert hours to degrees to radians
    
    # Altitude
    sin_alt = math.sin(dec) * math.sin(lat) + math.cos(dec) * math.cos(lat) * math.cos(ha)
    alt = math.degrees(math.asin(sin_alt))
    
    # Azimuth
    cos_az = (math.sin(dec) - math.sin(lat) * math.sin(math.radians(alt))) / (math.cos(lat) * math.cos(math.radians(alt)))
    az = math.degrees(math.acos(max(-1, min(1, cos_az))))
    
    if math.sin(ha) > 0:
        az = 360 - az
    
    return alt, az


# Export all functions
__all__ = [
    'astronomical_units_to_km', 'km_to_astronomical_units',
    'light_years_to_km', 'parsecs_to_light_years',
    'light_travel_time',
    'orbital_velocity', 'escape_velocity', 'orbital_period',
    'schwarzschild_radius',
    'gravitational_force', 'surface_gravity',
    'angular_diameter',
    'apparent_magnitude_from_absolute', 'absolute_magnitude_from_apparent',
    'luminosity_from_magnitude',
    'stellar_parallax_to_distance',
    'redshift_to_velocity', 'doppler_shift_frequency',
    'hubble_velocity', 'synodic_period',
    'julian_date', 'sidereal_time', 'hour_angle', 'altitude_azimuth',
]
