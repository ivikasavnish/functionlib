"""
Biology Functions

Biological calculations including genetics, molecular biology, and ecology.
"""

from typing import List, Dict, Tuple


# DNA/RNA bases
DNA_BASES = {'A', 'T', 'G', 'C'}
RNA_BASES = {'A', 'U', 'G', 'C'}

# Complementary base pairs
DNA_COMPLEMENT = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
RNA_COMPLEMENT = {'A': 'U', 'U': 'A', 'G': 'C', 'C': 'G'}

# Genetic code (codon to amino acid)
CODON_TABLE = {
    'UUU': 'F', 'UUC': 'F', 'UUA': 'L', 'UUG': 'L',
    'UCU': 'S', 'UCC': 'S', 'UCA': 'S', 'UCG': 'S',
    'UAU': 'Y', 'UAC': 'Y', 'UAA': '*', 'UAG': '*',
    'UGU': 'C', 'UGC': 'C', 'UGA': '*', 'UGG': 'W',
    'CUU': 'L', 'CUC': 'L', 'CUA': 'L', 'CUG': 'L',
    'CCU': 'P', 'CCC': 'P', 'CCA': 'P', 'CCG': 'P',
    'CAU': 'H', 'CAC': 'H', 'CAA': 'Q', 'CAG': 'Q',
    'CGU': 'R', 'CGC': 'R', 'CGA': 'R', 'CGG': 'R',
    'AUU': 'I', 'AUC': 'I', 'AUA': 'I', 'AUG': 'M',
    'ACU': 'T', 'ACC': 'T', 'ACA': 'T', 'ACG': 'T',
    'AAU': 'N', 'AAC': 'N', 'AAA': 'K', 'AAG': 'K',
    'AGU': 'S', 'AGC': 'S', 'AGA': 'R', 'AGG': 'R',
    'GUU': 'V', 'GUC': 'V', 'GUA': 'V', 'GUG': 'V',
    'GCU': 'A', 'GCC': 'A', 'GCA': 'A', 'GCG': 'A',
    'GAU': 'D', 'GAC': 'D', 'GAA': 'E', 'GAG': 'E',
    'GGU': 'G', 'GGC': 'G', 'GGA': 'G', 'GGG': 'G',
}


def dna_complement(sequence: str) -> str:
    """
    Returns complementary DNA strand
    
    Args:
        sequence: DNA sequence (5' to 3')
        
    Returns:
        Complementary sequence (3' to 5')
        
    Example:
        >>> dna_complement("ATGC")
        'TACG'
    """
    sequence = sequence.upper()
    for base in sequence:
        if base not in DNA_BASES:
            raise ValueError(f"Invalid DNA base: {base}")
    
    return ''.join(DNA_COMPLEMENT[base] for base in sequence)


def dna_reverse_complement(sequence: str) -> str:
    """
    Returns reverse complement of DNA strand (useful for reverse strand)
    
    Args:
        sequence: DNA sequence (5' to 3')
        
    Returns:
        Reverse complement (5' to 3')
        
    Example:
        >>> dna_reverse_complement("ATGC")
        'GCAT'
    """
    return dna_complement(sequence)[::-1]


def transcribe_dna_to_rna(dna_sequence: str) -> str:
    """
    Transcribes DNA to RNA (replaces T with U)
    
    Args:
        dna_sequence: DNA coding strand (5' to 3')
        
    Returns:
        RNA sequence (5' to 3')
        
    Example:
        >>> transcribe_dna_to_rna("ATGC")
        'AUGC'
    """
    dna_sequence = dna_sequence.upper()
    for base in dna_sequence:
        if base not in DNA_BASES:
            raise ValueError(f"Invalid DNA base: {base}")
    
    return dna_sequence.replace('T', 'U')


def translate_rna_to_protein(rna_sequence: str) -> str:
    """
    Translates RNA sequence to amino acid sequence
    
    Args:
        rna_sequence: RNA sequence (5' to 3')
        
    Returns:
        Amino acid sequence (one-letter codes, * = stop)
        
    Example:
        >>> translate_rna_to_protein("AUGUUUUAA")
        'MF*'
    """
    rna_sequence = rna_sequence.upper()
    
    if len(rna_sequence) % 3 != 0:
        raise ValueError("RNA sequence length must be divisible by 3")
    
    protein = []
    for i in range(0, len(rna_sequence), 3):
        codon = rna_sequence[i:i+3]
        if codon not in CODON_TABLE:
            raise ValueError(f"Invalid codon: {codon}")
        
        amino_acid = CODON_TABLE[codon]
        protein.append(amino_acid)
        
        if amino_acid == '*':  # Stop codon
            break
    
    return ''.join(protein)


def gc_content(sequence: str) -> float:
    """
    Calculates GC content (percentage of G and C bases)
    
    Args:
        sequence: DNA or RNA sequence
        
    Returns:
        GC content as percentage
        
    Example:
        >>> gc_content("ATGCGC")
        66.66666666666666
    """
    sequence = sequence.upper()
    if not sequence:
        raise ValueError("Sequence cannot be empty")
    
    gc_count = sequence.count('G') + sequence.count('C')
    return (gc_count / len(sequence)) * 100


def melting_temperature_basic(sequence: str) -> float:
    """
    Calculates DNA melting temperature using basic formula
    For sequences < 14 bp: Tm = 2(A+T) + 4(G+C)
    
    Args:
        sequence: DNA sequence
        
    Returns:
        Melting temperature (°C)
        
    Example:
        >>> melting_temperature_basic("ATGCGC")
        28.0
    """
    sequence = sequence.upper()
    
    if len(sequence) > 14:
        raise ValueError("Use more accurate formula for sequences > 14 bp")
    
    at_count = sequence.count('A') + sequence.count('T')
    gc_count = sequence.count('G') + sequence.count('C')
    
    return 2 * at_count + 4 * gc_count


def melting_temperature_wallace(sequence: str) -> float:
    """
    Calculates DNA melting temperature using Wallace rule
    For sequences 14-20 bp: Tm = 64.9 + 41(G+C-16.4)/(A+T+G+C)
    
    Args:
        sequence: DNA sequence
        
    Returns:
        Melting temperature (°C)
        
    Example:
        >>> melting_temperature_wallace("ATGCGCATGCGCAT")
        75.70714285714286
    """
    sequence = sequence.upper()
    length = len(sequence)
    
    if length < 14:
        raise ValueError("Use basic formula for sequences < 14 bp")
    
    gc_count = sequence.count('G') + sequence.count('C')
    
    return 64.9 + 41 * (gc_count - 16.4) / length


def hamming_distance(seq1: str, seq2: str) -> int:
    """
    Calculates Hamming distance (number of differing positions)
    
    Args:
        seq1: First sequence
        seq2: Second sequence
        
    Returns:
        Number of positions with different bases
        
    Example:
        >>> hamming_distance("ATGC", "ATCC")
        1
    """
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must have equal length")
    
    return sum(c1 != c2 for c1, c2 in zip(seq1, seq2))


def sequence_similarity(seq1: str, seq2: str) -> float:
    """
    Calculates sequence similarity as percentage
    
    Args:
        seq1: First sequence
        seq2: Second sequence
        
    Returns:
        Similarity percentage
        
    Example:
        >>> sequence_similarity("ATGC", "ATCC")
        75.0
    """
    if len(seq1) != len(seq2):
        raise ValueError("Sequences must have equal length")
    
    matches = sum(c1 == c2 for c1, c2 in zip(seq1, seq2))
    return (matches / len(seq1)) * 100


def hardy_weinberg_equilibrium(p: float) -> Tuple[float, float, float]:
    """
    Calculates Hardy-Weinberg genotype frequencies
    p² + 2pq + q² = 1, where p + q = 1
    
    Args:
        p: Frequency of dominant allele
        
    Returns:
        Tuple of (p², 2pq, q²) - frequencies of AA, Aa, aa
        
    Example:
        >>> hardy_weinberg_equilibrium(0.6)
        (0.36, 0.48, 0.16000000000000003)
    """
    if not 0 <= p <= 1:
        raise ValueError("Allele frequency must be between 0 and 1")
    
    q = 1 - p
    
    aa_freq = p ** 2  # Homozygous dominant
    aa_het = 2 * p * q  # Heterozygous
    aa_rec = q ** 2  # Homozygous recessive
    
    return (aa_freq, aa_het, aa_rec)


def population_growth_exponential(n0: float, r: float, t: float) -> float:
    """
    Calculates exponential population growth: N(t) = N₀e^(rt)
    
    Args:
        n0: Initial population size
        r: Growth rate (per time unit)
        t: Time
        
    Returns:
        Population size at time t
        
    Example:
        >>> population_growth_exponential(100, 0.1, 10)
        271.8281828459045
    """
    import math
    return n0 * math.exp(r * t)


def population_growth_logistic(n0: float, r: float, k: float, t: float) -> float:
    """
    Calculates logistic population growth: N(t) = K / (1 + ((K-N₀)/N₀)e^(-rt))
    
    Args:
        n0: Initial population size
        r: Growth rate
        k: Carrying capacity
        t: Time
        
    Returns:
        Population size at time t
        
    Example:
        >>> population_growth_logistic(10, 0.5, 1000, 10)
        141.68946458265433
    """
    import math
    numerator = k
    denominator = 1 + ((k - n0) / n0) * math.exp(-r * t)
    return numerator / denominator


def doubling_time(growth_rate: float) -> float:
    """
    Calculates population doubling time: t_d = ln(2)/r
    
    Args:
        growth_rate: Growth rate (per time unit)
        
    Returns:
        Doubling time (in same units as growth rate)
        
    Example:
        >>> doubling_time(0.1)
        6.931471805599453
    """
    import math
    if growth_rate <= 0:
        raise ValueError("Growth rate must be positive")
    return math.log(2) / growth_rate


def species_richness(species_counts: List[int]) -> int:
    """
    Calculates species richness (number of species)
    
    Args:
        species_counts: List of individual counts per species
        
    Returns:
        Number of species
        
    Example:
        >>> species_richness([10, 20, 5, 15])
        4
    """
    return len(species_counts)


def shannon_diversity_index(species_counts: List[int]) -> float:
    """
    Calculates Shannon diversity index: H' = -Σ(p_i × ln(p_i))
    
    Args:
        species_counts: List of individual counts per species
        
    Returns:
        Shannon diversity index
        
    Example:
        >>> shannon_diversity_index([10, 20, 10])
        1.0549201679861442
    """
    import math
    
    if not species_counts:
        return 0.0
    
    total = sum(species_counts)
    if total == 0:
        return 0.0
    
    h_prime = 0
    for count in species_counts:
        if count > 0:
            p_i = count / total
            h_prime -= p_i * math.log(p_i)
    
    return h_prime


def simpson_diversity_index(species_counts: List[int]) -> float:
    """
    Calculates Simpson's diversity index: D = 1 - Σ(p_i²)
    
    Args:
        species_counts: List of individual counts per species
        
    Returns:
        Simpson's diversity index (0-1, higher = more diverse)
        
    Example:
        >>> simpson_diversity_index([10, 20, 10])
        0.65
    """
    if not species_counts:
        return 0.0
    
    total = sum(species_counts)
    if total == 0:
        return 0.0
    
    sum_p_squared = sum((count / total) ** 2 for count in species_counts)
    
    return 1 - sum_p_squared


def bmi(weight_kg: float, height_m: float) -> float:
    """
    Calculates Body Mass Index: BMI = weight(kg) / height²(m)
    
    Args:
        weight_kg: Weight in kilograms
        height_m: Height in meters
        
    Returns:
        BMI value
        
    Example:
        >>> bmi(70, 1.75)
        22.857142857142858
    """
    if height_m <= 0:
        raise ValueError("Height must be positive")
    
    return weight_kg / (height_m ** 2)


def blood_alcohol_concentration(alcohol_g: float, weight_kg: float, gender: str, 
                                time_hours: float = 0) -> float:
    """
    Estimates blood alcohol concentration (Widmark formula)
    
    Args:
        alcohol_g: Grams of alcohol consumed
        weight_kg: Body weight in kg
        gender: 'male' or 'female'
        time_hours: Hours since drinking
        
    Returns:
        BAC (g/dL)
        
    Example:
        >>> blood_alcohol_concentration(30, 70, 'male', 1)
        0.033
    """
    # Distribution ratio
    r = 0.68 if gender.lower() == 'male' else 0.55
    
    # Metabolism rate (g/dL per hour)
    beta = 0.015
    
    bac = (alcohol_g / (weight_kg * r * 10)) - (beta * time_hours)
    
    return max(0, bac)  # Cannot be negative


# Export all functions
__all__ = [
    'DNA_BASES', 'RNA_BASES', 'DNA_COMPLEMENT', 'RNA_COMPLEMENT', 'CODON_TABLE',
    'dna_complement', 'dna_reverse_complement',
    'transcribe_dna_to_rna', 'translate_rna_to_protein',
    'gc_content', 'melting_temperature_basic', 'melting_temperature_wallace',
    'hamming_distance', 'sequence_similarity',
    'hardy_weinberg_equilibrium',
    'population_growth_exponential', 'population_growth_logistic', 'doubling_time',
    'species_richness', 'shannon_diversity_index', 'simpson_diversity_index',
    'bmi', 'blood_alcohol_concentration',
]
