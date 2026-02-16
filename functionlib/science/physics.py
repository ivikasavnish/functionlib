"""
Physics Functions

Physical calculations including mechanics, thermodynamics, electromagnetism, and optics.
"""

import math
from typing import Tuple, List


# Constants
GRAVITY = 9.80665  # m/s² (standard gravity)
SPEED_OF_LIGHT = 299792458  # m/s
GRAVITATIONAL_CONSTANT = 6.67430e-11  # N⋅m²/kg²
PLANCK_CONSTANT = 6.62607015e-34  # J⋅s
BOLTZMANN_CONSTANT = 1.380649e-23  # J/K
AVOGADRO_NUMBER = 6.02214076e23  # mol⁻¹
GAS_CONSTANT = 8.314462618  # J/(mol⋅K)
ELECTRON_MASS = 9.1093837015e-31  # kg
PROTON_MASS = 1.67262192369e-27  # kg
ELECTRON_CHARGE = 1.602176634e-19  # C
VACUUM_PERMITTIVITY = 8.8541878128e-12  # F/m


# Mechanics

def velocity(displacement: float, time: float) -> float:
    """
    Calculates velocity: v = d/t
    
    Args:
        displacement: Distance traveled (m)
        time: Time elapsed (s)
        
    Returns:
        Velocity (m/s)
        
    Example:
        >>> velocity(100, 10)
        10.0
    """
    if time == 0:
        raise ValueError("Time cannot be zero")
    return displacement / time


def acceleration(initial_velocity: float, final_velocity: float, time: float) -> float:
    """
    Calculates acceleration: a = (v_f - v_i)/t
    
    Args:
        initial_velocity: Initial velocity (m/s)
        final_velocity: Final velocity (m/s)
        time: Time elapsed (s)
        
    Returns:
        Acceleration (m/s²)
        
    Example:
        >>> acceleration(0, 30, 5)
        6.0
    """
    if time == 0:
        raise ValueError("Time cannot be zero")
    return (final_velocity - initial_velocity) / time


def force(mass: float, acceleration: float) -> float:
    """
    Calculates force using Newton's second law: F = ma
    
    Args:
        mass: Mass (kg)
        acceleration: Acceleration (m/s²)
        
    Returns:
        Force (N)
        
    Example:
        >>> force(10, 9.8)
        98.0
    """
    return mass * acceleration


def kinetic_energy(mass: float, velocity: float) -> float:
    """
    Calculates kinetic energy: KE = ½mv²
    
    Args:
        mass: Mass (kg)
        velocity: Velocity (m/s)
        
    Returns:
        Kinetic energy (J)
        
    Example:
        >>> kinetic_energy(2, 10)
        100.0
    """
    return 0.5 * mass * velocity**2


def potential_energy(mass: float, height: float, g: float = GRAVITY) -> float:
    """
    Calculates gravitational potential energy: PE = mgh
    
    Args:
        mass: Mass (kg)
        height: Height (m)
        g: Gravitational acceleration (m/s², default Earth's gravity)
        
    Returns:
        Potential energy (J)
        
    Example:
        >>> potential_energy(10, 5)
        490.3325
    """
    return mass * g * height


def work(force: float, displacement: float, angle_degrees: float = 0) -> float:
    """
    Calculates work: W = F·d·cos(θ)
    
    Args:
        force: Force applied (N)
        displacement: Displacement (m)
        angle_degrees: Angle between force and displacement (degrees)
        
    Returns:
        Work done (J)
        
    Example:
        >>> work(10, 5)
        50.0
    """
    angle_radians = math.radians(angle_degrees)
    return force * displacement * math.cos(angle_radians)


def power(work: float, time: float) -> float:
    """
    Calculates power: P = W/t
    
    Args:
        work: Work done (J)
        time: Time elapsed (s)
        
    Returns:
        Power (W)
        
    Example:
        >>> power(100, 5)
        20.0
    """
    if time == 0:
        raise ValueError("Time cannot be zero")
    return work / time


def momentum(mass: float, velocity: float) -> float:
    """
    Calculates momentum: p = mv
    
    Args:
        mass: Mass (kg)
        velocity: Velocity (m/s)
        
    Returns:
        Momentum (kg⋅m/s)
        
    Example:
        >>> momentum(5, 10)
        50.0
    """
    return mass * velocity


def impulse(force: float, time: float) -> float:
    """
    Calculates impulse: J = F·t
    
    Args:
        force: Average force (N)
        time: Time duration (s)
        
    Returns:
        Impulse (N⋅s)
        
    Example:
        >>> impulse(50, 2)
        100.0
    """
    return force * time


def centripetal_acceleration(velocity: float, radius: float) -> float:
    """
    Calculates centripetal acceleration: a_c = v²/r
    
    Args:
        velocity: Tangential velocity (m/s)
        radius: Radius of circular path (m)
        
    Returns:
        Centripetal acceleration (m/s²)
        
    Example:
        >>> centripetal_acceleration(10, 5)
        20.0
    """
    if radius == 0:
        raise ValueError("Radius cannot be zero")
    return velocity**2 / radius


def centripetal_force(mass: float, velocity: float, radius: float) -> float:
    """
    Calculates centripetal force: F_c = mv²/r
    
    Args:
        mass: Mass (kg)
        velocity: Tangential velocity (m/s)
        radius: Radius (m)
        
    Returns:
        Centripetal force (N)
        
    Example:
        >>> centripetal_force(2, 10, 5)
        40.0
    """
    return mass * centripetal_acceleration(velocity, radius)


def gravitational_force(m1: float, m2: float, distance: float) -> float:
    """
    Calculates gravitational force: F = G(m₁m₂)/r²
    
    Args:
        m1: First mass (kg)
        m2: Second mass (kg)
        distance: Distance between masses (m)
        
    Returns:
        Gravitational force (N)
        
    Example:
        >>> gravitational_force(1e6, 1e6, 1)
        0.0667430
    """
    if distance == 0:
        raise ValueError("Distance cannot be zero")
    return GRAVITATIONAL_CONSTANT * m1 * m2 / distance**2


def escape_velocity(mass: float, radius: float) -> float:
    """
    Calculates escape velocity: v = √(2GM/r)
    
    Args:
        mass: Mass of celestial body (kg)
        radius: Radius of celestial body (m)
        
    Returns:
        Escape velocity (m/s)
        
    Example:
        >>> escape_velocity(5.972e24, 6.371e6)  # Earth
        11179.710154859184
    """
    return math.sqrt(2 * GRAVITATIONAL_CONSTANT * mass / radius)


def free_fall_velocity(height: float, g: float = GRAVITY) -> float:
    """
    Calculates velocity after free fall: v = √(2gh)
    
    Args:
        height: Height fallen (m)
        g: Gravitational acceleration (m/s²)
        
    Returns:
        Final velocity (m/s)
        
    Example:
        >>> free_fall_velocity(10)
        14.007140952365015
    """
    return math.sqrt(2 * g * height)


def projectile_range(initial_velocity: float, angle_degrees: float, g: float = GRAVITY) -> float:
    """
    Calculates horizontal range of projectile: R = v²sin(2θ)/g
    
    Args:
        initial_velocity: Initial velocity (m/s)
        angle_degrees: Launch angle (degrees)
        g: Gravitational acceleration (m/s²)
        
    Returns:
        Horizontal range (m)
        
    Example:
        >>> projectile_range(20, 45)
        40.79683291511143
    """
    angle_radians = math.radians(angle_degrees)
    return (initial_velocity**2 * math.sin(2 * angle_radians)) / g


def projectile_max_height(initial_velocity: float, angle_degrees: float, g: float = GRAVITY) -> float:
    """
    Calculates maximum height of projectile: H = (v²sin²θ)/(2g)
    
    Args:
        initial_velocity: Initial velocity (m/s)
        angle_degrees: Launch angle (degrees)
        g: Gravitational acceleration (m/s²)
        
    Returns:
        Maximum height (m)
        
    Example:
        >>> projectile_max_height(20, 45)
        10.199208228777858
    """
    angle_radians = math.radians(angle_degrees)
    return (initial_velocity**2 * math.sin(angle_radians)**2) / (2 * g)


# Thermodynamics

def celsius_to_fahrenheit(celsius: float) -> float:
    """
    Converts Celsius to Fahrenheit: °F = (9/5)°C + 32
    
    Args:
        celsius: Temperature in Celsius
        
    Returns:
        Temperature in Fahrenheit
        
    Example:
        >>> celsius_to_fahrenheit(0)
        32.0
    """
    return (9/5) * celsius + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """
    Converts Fahrenheit to Celsius: °C = (5/9)(°F - 32)
    
    Args:
        fahrenheit: Temperature in Fahrenheit
        
    Returns:
        Temperature in Celsius
        
    Example:
        >>> fahrenheit_to_celsius(32)
        0.0
    """
    return (5/9) * (fahrenheit - 32)


def celsius_to_kelvin(celsius: float) -> float:
    """
    Converts Celsius to Kelvin: K = °C + 273.15
    
    Args:
        celsius: Temperature in Celsius
        
    Returns:
        Temperature in Kelvin
        
    Example:
        >>> celsius_to_kelvin(0)
        273.15
    """
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """
    Converts Kelvin to Celsius: °C = K - 273.15
    
    Args:
        kelvin: Temperature in Kelvin
        
    Returns:
        Temperature in Celsius
        
    Example:
        >>> kelvin_to_celsius(273.15)
        0.0
    """
    return kelvin - 273.15


def ideal_gas_law(pressure: float = None, volume: float = None, n: float = None, 
                  temperature: float = None) -> float:
    """
    Ideal gas law: PV = nRT. Solves for the missing variable.
    
    Args:
        pressure: Pressure (Pa)
        volume: Volume (m³)
        n: Amount of substance (mol)
        temperature: Temperature (K)
        
    Returns:
        The missing variable
        
    Example:
        >>> ideal_gas_law(pressure=101325, volume=0.0224, n=1, temperature=None)
        273.3217925092251
    """
    count_none = sum(x is None for x in [pressure, volume, n, temperature])
    
    if count_none != 1:
        raise ValueError("Exactly one parameter must be None")
    
    if pressure is None:
        return (n * GAS_CONSTANT * temperature) / volume
    elif volume is None:
        return (n * GAS_CONSTANT * temperature) / pressure
    elif n is None:
        return (pressure * volume) / (GAS_CONSTANT * temperature)
    else:  # temperature is None
        return (pressure * volume) / (n * GAS_CONSTANT)


def heat_transfer(mass: float, specific_heat: float, temperature_change: float) -> float:
    """
    Calculates heat transfer: Q = mcΔT
    
    Args:
        mass: Mass (kg)
        specific_heat: Specific heat capacity (J/(kg⋅K))
        temperature_change: Change in temperature (K or °C)
        
    Returns:
        Heat transferred (J)
        
    Example:
        >>> heat_transfer(1, 4186, 10)  # Water
        41860.0
    """
    return mass * specific_heat * temperature_change


def thermal_expansion_linear(original_length: float, coefficient: float, temperature_change: float) -> float:
    """
    Calculates linear thermal expansion: ΔL = αL₀ΔT
    
    Args:
        original_length: Original length (m)
        coefficient: Linear expansion coefficient (1/K)
        temperature_change: Temperature change (K)
        
    Returns:
        Change in length (m)
        
    Example:
        >>> thermal_expansion_linear(1, 1.2e-5, 50)  # Steel
        0.0006
    """
    return coefficient * original_length * temperature_change


# Electromagnetism

def coulomb_law(q1: float, q2: float, distance: float) -> float:
    """
    Calculates electric force: F = k(q₁q₂)/r²
    
    Args:
        q1: First charge (C)
        q2: Second charge (C)
        distance: Distance between charges (m)
        
    Returns:
        Electric force (N)
        
    Example:
        >>> coulomb_law(1e-6, 1e-6, 1)
        0.008988
    """
    if distance == 0:
        raise ValueError("Distance cannot be zero")
    k = 1 / (4 * math.pi * VACUUM_PERMITTIVITY)
    return k * q1 * q2 / distance**2


def ohms_law(voltage: float = None, current: float = None, resistance: float = None) -> float:
    """
    Ohm's law: V = IR. Solves for the missing variable.
    
    Args:
        voltage: Voltage (V)
        current: Current (A)
        resistance: Resistance (Ω)
        
    Returns:
        The missing variable
        
    Example:
        >>> ohms_law(voltage=12, current=2, resistance=None)
        6.0
    """
    count_none = sum(x is None for x in [voltage, current, resistance])
    
    if count_none != 1:
        raise ValueError("Exactly one parameter must be None")
    
    if voltage is None:
        return current * resistance
    elif current is None:
        if resistance == 0:
            raise ValueError("Resistance cannot be zero")
        return voltage / resistance
    else:  # resistance is None
        if current == 0:
            raise ValueError("Current cannot be zero")
        return voltage / current


def electrical_power(voltage: float = None, current: float = None, resistance: float = None) -> float:
    """
    Calculates electrical power: P = VI = I²R = V²/R
    
    Args:
        voltage: Voltage (V)
        current: Current (A)
        resistance: Resistance (Ω)
        
    Returns:
        Power (W)
        
    Example:
        >>> electrical_power(voltage=12, current=2)
        24.0
    """
    count_none = sum(x is None for x in [voltage, current, resistance])
    
    if count_none > 1:
        raise ValueError("At least two parameters must be provided")
    
    if voltage is not None and current is not None:
        return voltage * current
    elif current is not None and resistance is not None:
        return current**2 * resistance
    else:  # voltage and resistance
        return voltage**2 / resistance


def magnetic_force_on_charge(charge: float, velocity: float, magnetic_field: float, angle_degrees: float = 90) -> float:
    """
    Calculates magnetic force on moving charge: F = qvBsin(θ)
    
    Args:
        charge: Charge (C)
        velocity: Velocity (m/s)
        magnetic_field: Magnetic field strength (T)
        angle_degrees: Angle between velocity and field (degrees)
        
    Returns:
        Magnetic force (N)
        
    Example:
        >>> magnetic_force_on_charge(1.6e-19, 1e6, 0.5)
        8e-14
    """
    angle_radians = math.radians(angle_degrees)
    return abs(charge) * velocity * magnetic_field * math.sin(angle_radians)


# Optics

def snells_law(n1: float, theta1_degrees: float, n2: float) -> float:
    """
    Calculates refraction angle using Snell's law: n₁sin(θ₁) = n₂sin(θ₂)
    
    Args:
        n1: Refractive index of first medium
        theta1_degrees: Incident angle (degrees)
        n2: Refractive index of second medium
        
    Returns:
        Refracted angle (degrees)
        
    Example:
        >>> snells_law(1.0, 30, 1.5)  # Air to glass
        19.471220634490694
    """
    theta1_radians = math.radians(theta1_degrees)
    sin_theta2 = (n1 * math.sin(theta1_radians)) / n2
    
    if abs(sin_theta2) > 1:
        raise ValueError("Total internal reflection occurs")
    
    theta2_radians = math.asin(sin_theta2)
    return math.degrees(theta2_radians)


def lens_equation(focal_length: float = None, object_distance: float = None, 
                  image_distance: float = None) -> float:
    """
    Thin lens equation: 1/f = 1/d_o + 1/d_i
    
    Args:
        focal_length: Focal length (m)
        object_distance: Object distance (m)
        image_distance: Image distance (m)
        
    Returns:
        The missing variable
        
    Example:
        >>> lens_equation(focal_length=0.1, object_distance=0.3, image_distance=None)
        0.15000000000000002
    """
    count_none = sum(x is None for x in [focal_length, object_distance, image_distance])
    
    if count_none != 1:
        raise ValueError("Exactly one parameter must be None")
    
    if focal_length is None:
        return 1 / (1/object_distance + 1/image_distance)
    elif object_distance is None:
        return 1 / (1/focal_length - 1/image_distance)
    else:  # image_distance is None
        return 1 / (1/focal_length - 1/object_distance)


def magnification(image_distance: float, object_distance: float) -> float:
    """
    Calculates magnification: m = -d_i/d_o
    
    Args:
        image_distance: Image distance (m)
        object_distance: Object distance (m)
        
    Returns:
        Magnification (negative = inverted)
        
    Example:
        >>> magnification(0.15, 0.3)
        -0.5
    """
    if object_distance == 0:
        raise ValueError("Object distance cannot be zero")
    return -image_distance / object_distance


# Export all functions
__all__ = [
    'GRAVITY', 'SPEED_OF_LIGHT', 'GRAVITATIONAL_CONSTANT', 'PLANCK_CONSTANT',
    'BOLTZMANN_CONSTANT', 'AVOGADRO_NUMBER', 'GAS_CONSTANT',
    'velocity', 'acceleration', 'force', 'kinetic_energy', 'potential_energy',
    'work', 'power', 'momentum', 'impulse',
    'centripetal_acceleration', 'centripetal_force',
    'gravitational_force', 'escape_velocity', 'free_fall_velocity',
    'projectile_range', 'projectile_max_height',
    'celsius_to_fahrenheit', 'fahrenheit_to_celsius',
    'celsius_to_kelvin', 'kelvin_to_celsius',
    'ideal_gas_law', 'heat_transfer', 'thermal_expansion_linear',
    'coulomb_law', 'ohms_law', 'electrical_power', 'magnetic_force_on_charge',
    'snells_law', 'lens_equation', 'magnification',
]
