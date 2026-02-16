#!/usr/bin/env python3
"""
Test script for functionlib
"""

def test_math():
    from functionlib.math import algebra, calculus, geometry, trigonometry, statistics
    
    print("Testing Math Functions...")
    
    # Algebra
    assert algebra.solve_linear_equation(2, -6) == 3.0
    assert algebra.factorial(5) == 120
    assert algebra.gcd(48, 18) == 6
    
    # Calculus
    result = calculus.derivative_numerical(lambda x: x**2, 3)
    assert 5.9 < result < 6.1  # Should be ~6
    
    # Geometry
    assert abs(geometry.circle_area(5) - 78.54) < 0.01
    assert geometry.distance_2d(0, 0, 3, 4) == 5.0
    
    # Trigonometry
    assert abs(trigonometry.sin(30, degrees=True) - 0.5) < 0.01
    assert trigonometry.pythagorean_theorem(3, 4) == 5.0
    
    # Statistics
    assert statistics.mean([1, 2, 3, 4, 5]) == 3.0
    assert statistics.median([1, 2, 3, 4, 5]) == 3.0
    
    print("✓ Math functions passed")


def test_science():
    from functionlib.science import physics, chemistry, biology
    
    print("Testing Science Functions...")
    
    # Physics
    assert physics.force(10, 9.8) == 98.0
    assert physics.kinetic_energy(2, 10) == 100.0
    
    # Chemistry
    assert chemistry.molecular_mass({'H': 2, 'O': 1}) == 18.015
    assert chemistry.ph_from_concentration(1e-7) == 7.0
    
    # Biology
    assert abs(biology.gc_content("ATGCGC") - 66.67) < 0.01
    assert biology.dna_complement("ATGC") == "TACG"
    
    print("✓ Science functions passed")


def test_coding():
    from functionlib.coding import data_structures, algorithms, string_operations
    
    print("Testing Coding Functions...")
    
    # Data structures
    stack = data_structures.Stack()
    stack.push(1)
    stack.push(2)
    assert stack.pop() == 2
    
    # Algorithms
    assert algorithms.bubble_sort([3, 1, 4, 1, 5]) == [1, 1, 3, 4, 5]
    assert algorithms.binary_search([1, 2, 3, 4, 5], 3) == 2
    
    # String operations
    assert string_operations.reverse_string("hello") == "olleh"
    assert string_operations.is_palindrome("racecar")
    
    print("✓ Coding functions passed")


def test_general_purpose():
    from functionlib.general_purpose import date_time, string_utilities, validation
    from datetime import datetime
    
    print("Testing General Purpose Functions...")
    
    # Date/time
    dt = datetime(2021, 1, 1)
    new_dt = date_time.add_days(dt, 5)
    assert new_dt.day == 6
    assert date_time.is_leap_year(2020)
    
    # String utilities
    assert len(string_utilities.random_string(10)) == 10
    assert string_utilities.md5_hash("hello") == "5d41402abc4b2a76b9719d911017c592"
    
    # Validation
    assert validation.is_email("test@example.com")
    assert not validation.is_email("invalid.email")
    assert validation.is_url("https://example.com")
    
    print("✓ General purpose functions passed")


if __name__ == "__main__":
    print("=" * 50)
    print("Testing FunctionLib Implementation")
    print("=" * 50)
    
    test_math()
    test_science()
    test_coding()
    test_general_purpose()
    
    print("\n" + "=" * 50)
    print("✅ ALL TESTS PASSED!")
    print("=" * 50)
