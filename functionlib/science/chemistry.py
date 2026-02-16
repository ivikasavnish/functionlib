"""
Chemistry Functions

Chemical calculations including molecular mass, stoichiometry, and equilibrium.
"""

import math
from typing import Dict, List, Tuple


# Atomic masses (amu)
ATOMIC_MASSES = {
    'H': 1.008, 'He': 4.003, 'Li': 6.941, 'Be': 9.012, 'B': 10.811,
    'C': 12.011, 'N': 14.007, 'O': 15.999, 'F': 18.998, 'Ne': 20.180,
    'Na': 22.990, 'Mg': 24.305, 'Al': 26.982, 'Si': 28.086, 'P': 30.974,
    'S': 32.065, 'Cl': 35.453, 'Ar': 39.948, 'K': 39.098, 'Ca': 40.078,
    'Fe': 55.845, 'Cu': 63.546, 'Zn': 65.38, 'Ag': 107.868, 'Au': 196.967,
    'Hg': 200.592, 'Pb': 207.2, 'U': 238.029
}

# Constants
AVOGADRO_NUMBER = 6.02214076e23  # mol⁻¹
GAS_CONSTANT = 8.314462618  # J/(mol⋅K)
FARADAY_CONSTANT = 96485.33212  # C/mol


def molecular_mass(formula: Dict[str, int]) -> float:
    """
    Calculates molecular mass
    
    Args:
        formula: Dict mapping element symbols to counts
        
    Returns:
        Molecular mass (amu or g/mol)
        
    Example:
        >>> molecular_mass({'H': 2, 'O': 1})  # H₂O
        18.015
    """
    total_mass = 0
    for element, count in formula.items():
        if element not in ATOMIC_MASSES:
            raise ValueError(f"Unknown element: {element}")
        total_mass += ATOMIC_MASSES[element] * count
    
    return total_mass


def moles_to_grams(moles: float, molar_mass: float) -> float:
    """
    Converts moles to grams: mass = moles × molar_mass
    
    Args:
        moles: Amount in moles
        molar_mass: Molar mass (g/mol)
        
    Returns:
        Mass in grams
        
    Example:
        >>> moles_to_grams(2, 18.015)  # 2 moles of H₂O
        36.03
    """
    return moles * molar_mass


def grams_to_moles(grams: float, molar_mass: float) -> float:
    """
    Converts grams to moles: moles = mass / molar_mass
    
    Args:
        grams: Mass in grams
        molar_mass: Molar mass (g/mol)
        
    Returns:
        Amount in moles
        
    Example:
        >>> grams_to_moles(36.03, 18.015)
        1.9991671387103524
    """
    if molar_mass == 0:
        raise ValueError("Molar mass cannot be zero")
    return grams / molar_mass


def moles_to_molecules(moles: float) -> float:
    """
    Converts moles to number of molecules
    
    Args:
        moles: Amount in moles
        
    Returns:
        Number of molecules
        
    Example:
        >>> moles_to_molecules(1)
        6.02214076e+23
    """
    return moles * AVOGADRO_NUMBER


def molecules_to_moles(molecules: float) -> float:
    """
    Converts number of molecules to moles
    
    Args:
        molecules: Number of molecules
        
    Returns:
        Amount in moles
        
    Example:
        >>> molecules_to_moles(6.02214076e23)
        1.0
    """
    return molecules / AVOGADRO_NUMBER


def molarity(moles_solute: float, volume_liters: float) -> float:
    """
    Calculates molarity: M = moles/volume
    
    Args:
        moles_solute: Moles of solute
        volume_liters: Volume of solution in liters
        
    Returns:
        Molarity (mol/L or M)
        
    Example:
        >>> molarity(0.5, 2)
        0.25
    """
    if volume_liters == 0:
        raise ValueError("Volume cannot be zero")
    return moles_solute / volume_liters


def dilution(initial_molarity: float, initial_volume: float, final_volume: float) -> float:
    """
    Calculates final molarity after dilution: M₁V₁ = M₂V₂
    
    Args:
        initial_molarity: Initial molarity (M)
        initial_volume: Initial volume
        final_volume: Final volume (same units as initial)
        
    Returns:
        Final molarity (M)
        
    Example:
        >>> dilution(1.0, 10, 100)
        0.1
    """
    if final_volume == 0:
        raise ValueError("Final volume cannot be zero")
    return (initial_molarity * initial_volume) / final_volume


def percent_composition(element_mass: float, total_mass: float) -> float:
    """
    Calculates percent composition by mass
    
    Args:
        element_mass: Mass of element in compound
        total_mass: Total molecular mass
        
    Returns:
        Percent composition
        
    Example:
        >>> percent_composition(2.016, 18.015)  # H in H₂O
        11.190819458845548
    """
    if total_mass == 0:
        raise ValueError("Total mass cannot be zero")
    return (element_mass / total_mass) * 100


def empirical_formula_from_percent(percent_comp: Dict[str, float]) -> Dict[str, int]:
    """
    Determines empirical formula from percent composition
    
    Args:
        percent_comp: Dict mapping element symbols to percent composition
        
    Returns:
        Dict representing empirical formula
        
    Example:
        >>> empirical_formula_from_percent({'C': 40.0, 'H': 6.7, 'O': 53.3})
        {'C': 1, 'H': 2, 'O': 1}
    """
    # Convert percentages to moles
    moles = {}
    for element, percent in percent_comp.items():
        if element not in ATOMIC_MASSES:
            raise ValueError(f"Unknown element: {element}")
        moles[element] = percent / ATOMIC_MASSES[element]
    
    # Find smallest mole value
    min_moles = min(moles.values())
    
    # Divide all by smallest
    ratios = {elem: moles[elem] / min_moles for elem in moles}
    
    # Round to nearest integer
    formula = {elem: round(ratio) for elem, ratio in ratios.items()}
    
    return formula


def ph_from_concentration(h_concentration: float) -> float:
    """
    Calculates pH from H⁺ concentration: pH = -log[H⁺]
    
    Args:
        h_concentration: Hydrogen ion concentration (mol/L)
        
    Returns:
        pH value
        
    Example:
        >>> ph_from_concentration(1e-7)
        7.0
    """
    if h_concentration <= 0:
        raise ValueError("Concentration must be positive")
    return -math.log10(h_concentration)


def concentration_from_ph(ph: float) -> float:
    """
    Calculates H⁺ concentration from pH: [H⁺] = 10^(-pH)
    
    Args:
        ph: pH value
        
    Returns:
        Hydrogen ion concentration (mol/L)
        
    Example:
        >>> concentration_from_ph(7.0)
        1e-07
    """
    return 10 ** (-ph)


def poh_from_concentration(oh_concentration: float) -> float:
    """
    Calculates pOH from OH⁻ concentration: pOH = -log[OH⁻]
    
    Args:
        oh_concentration: Hydroxide ion concentration (mol/L)
        
    Returns:
        pOH value
        
    Example:
        >>> poh_from_concentration(1e-7)
        7.0
    """
    if oh_concentration <= 0:
        raise ValueError("Concentration must be positive")
    return -math.log10(oh_concentration)


def ph_to_poh(ph: float) -> float:
    """
    Converts pH to pOH: pH + pOH = 14 (at 25°C)
    
    Args:
        ph: pH value
        
    Returns:
        pOH value
        
    Example:
        >>> ph_to_poh(7.0)
        7.0
    """
    return 14 - ph


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


def combined_gas_law(p1: float = None, v1: float = None, t1: float = None,
                     p2: float = None, v2: float = None, t2: float = None) -> float:
    """
    Combined gas law: (P₁V₁)/T₁ = (P₂V₂)/T₂
    
    Args:
        p1: Initial pressure
        v1: Initial volume
        t1: Initial temperature (K)
        p2: Final pressure
        v2: Final volume
        t2: Final temperature (K)
        
    Returns:
        The missing variable
        
    Example:
        >>> combined_gas_law(p1=1, v1=2, t1=300, p2=2, v2=None, t2=300)
        1.0
    """
    count_none = sum(x is None for x in [p1, v1, t1, p2, v2, t2])
    
    if count_none != 1:
        raise ValueError("Exactly one parameter must be None")
    
    if p1 is None:
        return (p2 * v2 * t1) / (v1 * t2)
    elif v1 is None:
        return (p2 * v2 * t1) / (p1 * t2)
    elif t1 is None:
        return (p1 * v1 * t2) / (p2 * v2)
    elif p2 is None:
        return (p1 * v1 * t2) / (v2 * t1)
    elif v2 is None:
        return (p1 * v1 * t2) / (p2 * t1)
    else:  # t2 is None
        return (p2 * v2 * t1) / (p1 * v1)


def enthalpy_change(bonds_broken: float, bonds_formed: float) -> float:
    """
    Calculates enthalpy change: ΔH = Σ(bonds broken) - Σ(bonds formed)
    
    Args:
        bonds_broken: Sum of bond energies broken (kJ/mol)
        bonds_formed: Sum of bond energies formed (kJ/mol)
        
    Returns:
        Enthalpy change (kJ/mol)
        
    Example:
        >>> enthalpy_change(500, 700)
        -200.0
    """
    return bonds_broken - bonds_formed


def gibbs_free_energy(enthalpy: float, temperature: float, entropy: float) -> float:
    """
    Calculates Gibbs free energy: ΔG = ΔH - TΔS
    
    Args:
        enthalpy: Enthalpy change (J/mol)
        temperature: Temperature (K)
        entropy: Entropy change (J/(mol⋅K))
        
    Returns:
        Gibbs free energy change (J/mol)
        
    Example:
        >>> gibbs_free_energy(-100000, 298, -100)
        -70200.0
    """
    return enthalpy - temperature * entropy


def equilibrium_constant(concentrations_products: List[float], 
                         concentrations_reactants: List[float],
                         coefficients_products: List[int],
                         coefficients_reactants: List[int]) -> float:
    """
    Calculates equilibrium constant K
    
    Args:
        concentrations_products: Concentrations of products
        concentrations_reactants: Concentrations of reactants
        coefficients_products: Stoichiometric coefficients of products
        coefficients_reactants: Stoichiometric coefficients of reactants
        
    Returns:
        Equilibrium constant K
        
    Example:
        >>> equilibrium_constant([2.0], [0.5, 0.5], [1], [1, 1])
        8.0
    """
    numerator = 1
    for conc, coeff in zip(concentrations_products, coefficients_products):
        numerator *= conc ** coeff
    
    denominator = 1
    for conc, coeff in zip(concentrations_reactants, coefficients_reactants):
        denominator *= conc ** coeff
    
    if denominator == 0:
        raise ValueError("Denominator cannot be zero")
    
    return numerator / denominator


def half_life(initial_amount: float, decay_constant: float) -> float:
    """
    Calculates half-life: t₁/₂ = ln(2)/λ
    
    Args:
        initial_amount: Not used (for consistency)
        decay_constant: Decay constant (1/time)
        
    Returns:
        Half-life (in time units matching decay_constant)
        
    Example:
        >>> half_life(100, 0.1)
        6.931471805599453
    """
    if decay_constant <= 0:
        raise ValueError("Decay constant must be positive")
    return math.log(2) / decay_constant


def radioactive_decay(initial_amount: float, time: float, half_life: float) -> float:
    """
    Calculates remaining amount after radioactive decay: N = N₀(1/2)^(t/t₁/₂)
    
    Args:
        initial_amount: Initial amount
        time: Time elapsed
        half_life: Half-life (same units as time)
        
    Returns:
        Remaining amount
        
    Example:
        >>> radioactive_decay(100, 6.93, 6.93)
        50.06
    """
    if half_life <= 0:
        raise ValueError("Half-life must be positive")
    return initial_amount * (0.5 ** (time / half_life))


def arrhenius_equation(activation_energy: float, temperature: float, 
                       frequency_factor: float) -> float:
    """
    Calculates rate constant: k = Ae^(-Ea/RT)
    
    Args:
        activation_energy: Activation energy (J/mol)
        temperature: Temperature (K)
        frequency_factor: Pre-exponential factor (same units as rate)
        
    Returns:
        Rate constant
        
    Example:
        >>> arrhenius_equation(50000, 298, 1e10)
        59315.48165588093
    """
    exponent = -activation_energy / (GAS_CONSTANT * temperature)
    return frequency_factor * math.exp(exponent)


# Export all functions
__all__ = [
    'ATOMIC_MASSES', 'AVOGADRO_NUMBER', 'GAS_CONSTANT', 'FARADAY_CONSTANT',
    'molecular_mass', 'moles_to_grams', 'grams_to_moles',
    'moles_to_molecules', 'molecules_to_moles',
    'molarity', 'dilution', 'percent_composition',
    'empirical_formula_from_percent',
    'ph_from_concentration', 'concentration_from_ph',
    'poh_from_concentration', 'ph_to_poh',
    'ideal_gas_law', 'combined_gas_law',
    'enthalpy_change', 'gibbs_free_energy',
    'equilibrium_constant', 'half_life', 'radioactive_decay',
    'arrhenius_equation',
]
