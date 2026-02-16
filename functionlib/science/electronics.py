"""
Electronics Functions

Circuit calculations and electronics formulas.
"""

import math
from typing import Tuple


def ohms_law_voltage(current: float, resistance: float) -> float:
    """
    Calculate voltage using Ohm's law: V = I × R
    
    Args:
        current: Current in amperes
        resistance: Resistance in ohms
        
    Returns:
        Voltage in volts
        
    Example:
        >>> ohms_law_voltage(2, 10)
        20.0
    """
    return current * resistance


def ohms_law_current(voltage: float, resistance: float) -> float:
    """
    Calculate current using Ohm's law: I = V / R
    
    Args:
        voltage: Voltage in volts
        resistance: Resistance in ohms
        
    Returns:
        Current in amperes
        
    Example:
        >>> ohms_law_current(20, 10)
        2.0
    """
    return voltage / resistance


def ohms_law_resistance(voltage: float, current: float) -> float:
    """
    Calculate resistance using Ohm's law: R = V / I
    
    Args:
        voltage: Voltage in volts
        current: Current in amperes
        
    Returns:
        Resistance in ohms
        
    Example:
        >>> ohms_law_resistance(20, 2)
        10.0
    """
    return voltage / current


def electrical_power(voltage: float, current: float) -> float:
    """
    Calculate electrical power: P = V × I
    
    Args:
        voltage: Voltage in volts
        current: Current in amperes
        
    Returns:
        Power in watts
        
    Example:
        >>> electrical_power(12, 2)
        24.0
    """
    return voltage * current


def power_from_resistance(voltage: float, resistance: float) -> float:
    """
    Calculate power: P = V² / R
    
    Args:
        voltage: Voltage in volts
        resistance: Resistance in ohms
        
    Returns:
        Power in watts
        
    Example:
        >>> power_from_resistance(10, 5)
        20.0
    """
    return voltage ** 2 / resistance


def power_from_current(current: float, resistance: float) -> float:
    """
    Calculate power: P = I² × R
    
    Args:
        current: Current in amperes
        resistance: Resistance in ohms
        
    Returns:
        Power in watts
        
    Example:
        >>> power_from_current(2, 5)
        20.0
    """
    return current ** 2 * resistance


def resistors_series(*resistances: float) -> float:
    """
    Total resistance of series resistors: R_total = R1 + R2 + ...
    
    Args:
        *resistances: Resistance values in ohms
        
    Returns:
        Total resistance in ohms
        
    Example:
        >>> resistors_series(10, 20, 30)
        60.0
    """
    return sum(resistances)


def resistors_parallel(*resistances: float) -> float:
    """
    Total resistance of parallel resistors: 1/R_total = 1/R1 + 1/R2 + ...
    
    Args:
        *resistances: Resistance values in ohms
        
    Returns:
        Total resistance in ohms
        
    Example:
        >>> resistors_parallel(10, 10)
        5.0
    """
    if any(r == 0 for r in resistances):
        raise ValueError("Resistance cannot be zero")
    
    return 1 / sum(1/r for r in resistances)


def capacitors_series(*capacitances: float) -> float:
    """
    Total capacitance of series capacitors: 1/C_total = 1/C1 + 1/C2 + ...
    
    Args:
        *capacitances: Capacitance values in farads
        
    Returns:
        Total capacitance in farads
        
    Example:
        >>> capacitors_series(10e-6, 10e-6)
        5e-06
    """
    if any(c == 0 for c in capacitances):
        raise ValueError("Capacitance cannot be zero")
    
    return 1 / sum(1/c for c in capacitances)


def capacitors_parallel(*capacitances: float) -> float:
    """
    Total capacitance of parallel capacitors: C_total = C1 + C2 + ...
    
    Args:
        *capacitances: Capacitance values in farads
        
    Returns:
        Total capacitance in farads
        
    Example:
        >>> capacitors_parallel(10e-6, 20e-6)
        3e-05
    """
    return sum(capacitances)


def inductors_series(*inductances: float) -> float:
    """
    Total inductance of series inductors: L_total = L1 + L2 + ...
    
    Args:
        *inductances: Inductance values in henries
        
    Returns:
        Total inductance in henries
        
    Example:
        >>> inductors_series(0.001, 0.002)
        0.003
    """
    return sum(inductances)


def inductors_parallel(*inductances: float) -> float:
    """
    Total inductance of parallel inductors: 1/L_total = 1/L1 + 1/L2 + ...
    
    Args:
        *inductances: Inductance values in henries
        
    Returns:
        Total inductance in henries
        
    Example:
        >>> inductors_parallel(0.002, 0.002)
        0.001
    """
    if any(l == 0 for l in inductances):
        raise ValueError("Inductance cannot be zero")
    
    return 1 / sum(1/l for l in inductances)


def capacitor_energy(capacitance: float, voltage: float) -> float:
    """
    Energy stored in capacitor: E = ½CV²
    
    Args:
        capacitance: Capacitance in farads
        voltage: Voltage in volts
        
    Returns:
        Energy in joules
        
    Example:
        >>> capacitor_energy(0.001, 10)
        0.05
    """
    return 0.5 * capacitance * voltage ** 2


def inductor_energy(inductance: float, current: float) -> float:
    """
    Energy stored in inductor: E = ½LI²
    
    Args:
        inductance: Inductance in henries
        current: Current in amperes
        
    Returns:
        Energy in joules
        
    Example:
        >>> inductor_energy(0.1, 2)
        0.2
    """
    return 0.5 * inductance * current ** 2


def capacitive_reactance(capacitance: float, frequency: float) -> float:
    """
    Capacitive reactance: Xc = 1 / (2πfC)
    
    Args:
        capacitance: Capacitance in farads
        frequency: Frequency in hertz
        
    Returns:
        Reactance in ohms
        
    Example:
        >>> xc = capacitive_reactance(1e-6, 1000)
        >>> 150 < xc < 160
        True
    """
    return 1 / (2 * math.pi * frequency * capacitance)


def inductive_reactance(inductance: float, frequency: float) -> float:
    """
    Inductive reactance: XL = 2πfL
    
    Args:
        inductance: Inductance in henries
        frequency: Frequency in hertz
        
    Returns:
        Reactance in ohms
        
    Example:
        >>> inductive_reactance(0.01, 1000)
        62.83...
    """
    return 2 * math.pi * frequency * inductance


def impedance_rc(resistance: float, capacitance: float, frequency: float) -> float:
    """
    Impedance of RC circuit: Z = √(R² + Xc²)
    
    Args:
        resistance: Resistance in ohms
        capacitance: Capacitance in farads
        frequency: Frequency in hertz
        
    Returns:
        Impedance in ohms
        
    Example:
        >>> z = impedance_rc(100, 1e-6, 1000)
        >>> z > 100
        True
    """
    xc = capacitive_reactance(capacitance, frequency)
    return math.sqrt(resistance ** 2 + xc ** 2)


def impedance_rl(resistance: float, inductance: float, frequency: float) -> float:
    """
    Impedance of RL circuit: Z = √(R² + XL²)
    
    Args:
        resistance: Resistance in ohms
        inductance: Inductance in henries
        frequency: Frequency in hertz
        
    Returns:
        Impedance in ohms
        
    Example:
        >>> z = impedance_rl(100, 0.01, 1000)
        >>> z > 100
        True
    """
    xl = inductive_reactance(inductance, frequency)
    return math.sqrt(resistance ** 2 + xl ** 2)


def impedance_rlc(resistance: float, inductance: float, capacitance: float, frequency: float) -> float:
    """
    Impedance of RLC circuit: Z = √(R² + (XL - Xc)²)
    
    Args:
        resistance: Resistance in ohms
        inductance: Inductance in henries
        capacitance: Capacitance in farads
        frequency: Frequency in hertz
        
    Returns:
        Impedance in ohms
        
    Example:
        >>> z = impedance_rlc(100, 0.01, 1e-6, 1000)
        >>> z > 0
        True
    """
    xl = inductive_reactance(inductance, frequency)
    xc = capacitive_reactance(capacitance, frequency)
    return math.sqrt(resistance ** 2 + (xl - xc) ** 2)


def resonant_frequency(inductance: float, capacitance: float) -> float:
    """
    Resonant frequency of LC circuit: f = 1 / (2π√(LC))
    
    Args:
        inductance: Inductance in henries
        capacitance: Capacitance in farads
        
    Returns:
        Frequency in hertz
        
    Example:
        >>> f = resonant_frequency(0.001, 1e-6)
        >>> 5000 < f < 6000
        True
    """
    return 1 / (2 * math.pi * math.sqrt(inductance * capacitance))


def time_constant_rc(resistance: float, capacitance: float) -> float:
    """
    Time constant of RC circuit: τ = RC
    
    Args:
        resistance: Resistance in ohms
        capacitance: Capacitance in farads
        
    Returns:
        Time constant in seconds
        
    Example:
        >>> time_constant_rc(1000, 1e-6)
        0.001
    """
    return resistance * capacitance


def time_constant_rl(resistance: float, inductance: float) -> float:
    """
    Time constant of RL circuit: τ = L/R
    
    Args:
        resistance: Resistance in ohms
        inductance: Inductance in henries
        
    Returns:
        Time constant in seconds
        
    Example:
        >>> time_constant_rl(100, 0.1)
        0.001
    """
    return inductance / resistance


def voltage_divider(vin: float, r1: float, r2: float) -> float:
    """
    Output voltage of voltage divider: Vout = Vin × R2 / (R1 + R2)
    
    Args:
        vin: Input voltage
        r1: Upper resistor
        r2: Lower resistor
        
    Returns:
        Output voltage
        
    Example:
        >>> voltage_divider(10, 10, 10)
        5.0
    """
    return vin * r2 / (r1 + r2)


def current_divider(iin: float, r1: float, r2: float) -> Tuple[float, float]:
    """
    Current division in parallel resistors
    
    Args:
        iin: Input current
        r1: Resistor 1
        r2: Resistor 2
        
    Returns:
        (current through r1, current through r2)
        
    Example:
        >>> i1, i2 = current_divider(10, 10, 10)
        >>> i1
        5.0
    """
    i1 = iin * r2 / (r1 + r2)
    i2 = iin * r1 / (r1 + r2)
    return i1, i2


def led_resistor(vsupply: float, vled: float, iled: float) -> float:
    """
    Calculate current-limiting resistor for LED: R = (Vsupply - VLED) / ILED
    
    Args:
        vsupply: Supply voltage
        vled: LED forward voltage
        iled: Desired LED current
        
    Returns:
        Resistor value in ohms
        
    Example:
        >>> led_resistor(5, 2, 0.02)
        150.0
    """
    return (vsupply - vled) / iled


def wire_resistance(resistivity: float, length: float, area: float) -> float:
    """
    Wire resistance: R = ρL/A
    
    Args:
        resistivity: Resistivity (Ω·m)
        length: Length in meters
        area: Cross-sectional area in m²
        
    Returns:
        Resistance in ohms
        
    Example:
        >>> wire_resistance(1.68e-8, 10, 1e-6)
        0.168
    """
    return resistivity * length / area


def bandwidth_rc(resistance: float, capacitance: float) -> float:
    """
    3dB bandwidth of RC filter: BW = 1 / (2πRC)
    
    Args:
        resistance: Resistance in ohms
        capacitance: Capacitance in farads
        
    Returns:
        Bandwidth in hertz
        
    Example:
        >>> bw = bandwidth_rc(1000, 1e-6)
        >>> 150 < bw < 160
        True
    """
    return 1 / (2 * math.pi * resistance * capacitance)


def decibel_voltage_gain(vout: float, vin: float) -> float:
    """
    Voltage gain in decibels: dB = 20 log₁₀(Vout/Vin)
    
    Args:
        vout: Output voltage
        vin: Input voltage
        
    Returns:
        Gain in dB
        
    Example:
        >>> decibel_voltage_gain(10, 1)
        20.0
    """
    return 20 * math.log10(vout / vin)


def decibel_power_gain(pout: float, pin: float) -> float:
    """
    Power gain in decibels: dB = 10 log₁₀(Pout/Pin)
    
    Args:
        pout: Output power
        pin: Input power
        
    Returns:
        Gain in dB
        
    Example:
        >>> decibel_power_gain(100, 1)
        20.0
    """
    return 10 * math.log10(pout / pin)


def skin_depth(frequency: float, conductivity: float, permeability: float = 4e-7 * math.pi) -> float:
    """
    Skin depth in conductor: δ = √(2 / (ωσμ))
    
    Args:
        frequency: Frequency in Hz
        conductivity: Conductivity in S/m
        permeability: Magnetic permeability (default for copper)
        
    Returns:
        Skin depth in meters
        
    Example:
        >>> d = skin_depth(1e6, 5.96e7)
        >>> d > 0
        True
    """
    omega = 2 * math.pi * frequency
    return math.sqrt(2 / (omega * conductivity * permeability))


# Export all functions
__all__ = [
    'ohms_law_voltage', 'ohms_law_current', 'ohms_law_resistance',
    'electrical_power', 'power_from_resistance', 'power_from_current',
    'resistors_series', 'resistors_parallel',
    'capacitors_series', 'capacitors_parallel',
    'inductors_series', 'inductors_parallel',
    'capacitor_energy', 'inductor_energy',
    'capacitive_reactance', 'inductive_reactance',
    'impedance_rc', 'impedance_rl', 'impedance_rlc',
    'resonant_frequency',
    'time_constant_rc', 'time_constant_rl',
    'voltage_divider', 'current_divider', 'led_resistor',
    'wire_resistance', 'bandwidth_rc',
    'decibel_voltage_gain', 'decibel_power_gain',
    'skin_depth',
]
