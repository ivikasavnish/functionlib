"""
Conversion Functions

Unit conversions for length, weight, temperature, volume, speed, and more.
"""

# Length Conversions

def meters_to_kilometers(meters: float) -> float:
    """Meters to kilometers"""
    return meters / 1000


def kilometers_to_meters(km: float) -> float:
    """Kilometers to meters"""
    return km * 1000


def meters_to_miles(meters: float) -> float:
    """Meters to miles"""
    return meters / 1609.34


def miles_to_meters(miles: float) -> float:
    """Miles to meters"""
    return miles * 1609.34


def meters_to_feet(meters: float) -> float:
    """Meters to feet"""
    return meters * 3.28084


def feet_to_meters(feet: float) -> float:
    """Feet to meters"""
    return feet / 3.28084


def inches_to_centimeters(inches: float) -> float:
    """Inches to centimeters"""
    return inches * 2.54


def centimeters_to_inches(cm: float) -> float:
    """Centimeters to inches"""
    return cm / 2.54


# Weight/Mass Conversions

def kilograms_to_pounds(kg: float) -> float:
    """Kilograms to pounds"""
    return kg * 2.20462


def pounds_to_kilograms(lbs: float) -> float:
    """Pounds to kilograms"""
    return lbs / 2.20462


def grams_to_ounces(grams: float) -> float:
    """Grams to ounces"""
    return grams * 0.035274


def ounces_to_grams(oz: float) -> float:
    """Ounces to grams"""
    return oz / 0.035274


def kilograms_to_tons(kg: float) -> float:
    """Kilograms to metric tons"""
    return kg / 1000


def tons_to_kilograms(tons: float) -> float:
    """Metric tons to kilograms"""
    return tons * 1000


# Temperature Conversions

def celsius_to_fahrenheit(celsius: float) -> float:
    """Celsius to Fahrenheit"""
    return (celsius * 9/5) + 32


def fahrenheit_to_celsius(fahrenheit: float) -> float:
    """Fahrenheit to Celsius"""
    return (fahrenheit - 32) * 5/9


def celsius_to_kelvin(celsius: float) -> float:
    """Celsius to Kelvin"""
    return celsius + 273.15


def kelvin_to_celsius(kelvin: float) -> float:
    """Kelvin to Celsius"""
    return kelvin - 273.15


def fahrenheit_to_kelvin(fahrenheit: float) -> float:
    """Fahrenheit to Kelvin"""
    return celsius_to_kelvin(fahrenheit_to_celsius(fahrenheit))


def kelvin_to_fahrenheit(kelvin: float) -> float:
    """Kelvin to Fahrenheit"""
    return celsius_to_fahrenheit(kelvin_to_celsius(kelvin))


# Volume Conversions

def liters_to_gallons(liters: float) -> float:
    """Liters to US gallons"""
    return liters * 0.264172


def gallons_to_liters(gallons: float) -> float:
    """US gallons to liters"""
    return gallons / 0.264172


def milliliters_to_fluid_ounces(ml: float) -> float:
    """Milliliters to fluid ounces"""
    return ml * 0.033814


def fluid_ounces_to_milliliters(oz: float) -> float:
    """Fluid ounces to milliliters"""
    return oz / 0.033814


def cubic_meters_to_cubic_feet(m3: float) -> float:
    """Cubic meters to cubic feet"""
    return m3 * 35.3147


def cubic_feet_to_cubic_meters(ft3: float) -> float:
    """Cubic feet to cubic meters"""
    return ft3 / 35.3147


# Speed Conversions

def kmh_to_mph(kmh: float) -> float:
    """Kilometers per hour to miles per hour"""
    return kmh * 0.621371


def mph_to_kmh(mph: float) -> float:
    """Miles per hour to kilometers per hour"""
    return mph / 0.621371


def ms_to_kmh(ms: float) -> float:
    """Meters per second to kilometers per hour"""
    return ms * 3.6


def kmh_to_ms(kmh: float) -> float:
    """Kilometers per hour to meters per second"""
    return kmh / 3.6


def knots_to_kmh(knots: float) -> float:
    """Nautical miles per hour (knots) to kilometers per hour"""
    return knots * 1.852


def kmh_to_knots(kmh: float) -> float:
    """Kilometers per hour to knots"""
    return kmh / 1.852


# Time Conversions

def seconds_to_minutes(seconds: float) -> float:
    """Seconds to minutes"""
    return seconds / 60


def minutes_to_seconds(minutes: float) -> float:
    """Minutes to seconds"""
    return minutes * 60


def hours_to_minutes(hours: float) -> float:
    """Hours to minutes"""
    return hours * 60


def minutes_to_hours(minutes: float) -> float:
    """Minutes to hours"""
    return minutes / 60


def days_to_hours(days: float) -> float:
    """Days to hours"""
    return days * 24


def hours_to_days(hours: float) -> float:
    """Hours to days"""
    return hours / 24


def weeks_to_days(weeks: float) -> float:
    """Weeks to days"""
    return weeks * 7


def days_to_weeks(days: float) -> float:
    """Days to weeks"""
    return days / 7


# Energy Conversions

def joules_to_calories(joules: float) -> float:
    """Joules to calories"""
    return joules * 0.239006


def calories_to_joules(calories: float) -> float:
    """Calories to joules"""
    return calories / 0.239006


def kilowatt_hours_to_joules(kwh: float) -> float:
    """Kilowatt-hours to joules"""
    return kwh * 3.6e6


def joules_to_kilowatt_hours(joules: float) -> float:
    """Joules to kilowatt-hours"""
    return joules / 3.6e6


# Power Conversions

def watts_to_horsepower(watts: float) -> float:
    """Watts to horsepower"""
    return watts / 745.7


def horsepower_to_watts(hp: float) -> float:
    """Horsepower to watts"""
    return hp * 745.7


# Pressure Conversions

def pascals_to_psi(pascals: float) -> float:
    """Pascals to pounds per square inch"""
    return pascals * 0.000145038


def psi_to_pascals(psi: float) -> float:
    """Pounds per square inch to pascals"""
    return psi / 0.000145038


def pascals_to_bar(pascals: float) -> float:
    """Pascals to bar"""
    return pascals / 100000


def bar_to_pascals(bar: float) -> float:
    """Bar to pascals"""
    return bar * 100000


def atmospheres_to_pascals(atm: float) -> float:
    """Atmospheres to pascals"""
    return atm * 101325


def pascals_to_atmospheres(pascals: float) -> float:
    """Pascals to atmospheres"""
    return pascals / 101325


# Area Conversions

def square_meters_to_square_feet(m2: float) -> float:
    """Square meters to square feet"""
    return m2 * 10.7639


def square_feet_to_square_meters(ft2: float) -> float:
    """Square feet to square meters"""
    return ft2 / 10.7639


def square_meters_to_acres(m2: float) -> float:
    """Square meters to acres"""
    return m2 * 0.000247105


def acres_to_square_meters(acres: float) -> float:
    """Acres to square meters"""
    return acres / 0.000247105


def hectares_to_acres(hectares: float) -> float:
    """Hectares to acres"""
    return hectares * 2.47105


def acres_to_hectares(acres: float) -> float:
    """Acres to hectares"""
    return acres / 2.47105


# Data Size Conversions

def bytes_to_kilobytes(bytes_val: float) -> float:
    """Bytes to kilobytes"""
    return bytes_val / 1024


def kilobytes_to_bytes(kb: float) -> float:
    """Kilobytes to bytes"""
    return kb * 1024


def kilobytes_to_megabytes(kb: float) -> float:
    """Kilobytes to megabytes"""
    return kb / 1024


def megabytes_to_kilobytes(mb: float) -> float:
    """Megabytes to kilobytes"""
    return mb * 1024


def megabytes_to_gigabytes(mb: float) -> float:
    """Megabytes to gigabytes"""
    return mb / 1024


def gigabytes_to_megabytes(gb: float) -> float:
    """Gigabytes to megabytes"""
    return gb * 1024


def gigabytes_to_terabytes(gb: float) -> float:
    """Gigabytes to terabytes"""
    return gb / 1024


def terabytes_to_gigabytes(tb: float) -> float:
    """Terabytes to gigabytes"""
    return tb * 1024


# Angle Conversions

def degrees_to_radians(degrees: float) -> float:
    """Degrees to radians"""
    import math
    return math.radians(degrees)


def radians_to_degrees(radians: float) -> float:
    """Radians to degrees"""
    import math
    return math.degrees(radians)


def degrees_to_gradians(degrees: float) -> float:
    """Degrees to gradians"""
    return degrees * 10/9


def gradians_to_degrees(gradians: float) -> float:
    """Gradians to degrees"""
    return gradians * 9/10


# Fuel Efficiency Conversions

def mpg_to_lper100km(mpg: float) -> float:
    """Miles per gallon (US) to liters per 100 km"""
    return 235.215 / mpg


def lper100km_to_mpg(lper100km: float) -> float:
    """Liters per 100 km to miles per gallon (US)"""
    return 235.215 / lper100km


# Export all functions
__all__ = [
    # Length
    'meters_to_kilometers', 'kilometers_to_meters',
    'meters_to_miles', 'miles_to_meters',
    'meters_to_feet', 'feet_to_meters',
    'inches_to_centimeters', 'centimeters_to_inches',
    # Weight
    'kilograms_to_pounds', 'pounds_to_kilograms',
    'grams_to_ounces', 'ounces_to_grams',
    'kilograms_to_tons', 'tons_to_kilograms',
    # Temperature
    'celsius_to_fahrenheit', 'fahrenheit_to_celsius',
    'celsius_to_kelvin', 'kelvin_to_celsius',
    'fahrenheit_to_kelvin', 'kelvin_to_fahrenheit',
    # Volume
    'liters_to_gallons', 'gallons_to_liters',
    'milliliters_to_fluid_ounces', 'fluid_ounces_to_milliliters',
    'cubic_meters_to_cubic_feet', 'cubic_feet_to_cubic_meters',
    # Speed
    'kmh_to_mph', 'mph_to_kmh',
    'ms_to_kmh', 'kmh_to_ms',
    'knots_to_kmh', 'kmh_to_knots',
    # Time
    'seconds_to_minutes', 'minutes_to_seconds',
    'hours_to_minutes', 'minutes_to_hours',
    'days_to_hours', 'hours_to_days',
    'weeks_to_days', 'days_to_weeks',
    # Energy
    'joules_to_calories', 'calories_to_joules',
    'kilowatt_hours_to_joules', 'joules_to_kilowatt_hours',
    # Power
    'watts_to_horsepower', 'horsepower_to_watts',
    # Pressure
    'pascals_to_psi', 'psi_to_pascals',
    'pascals_to_bar', 'bar_to_pascals',
    'atmospheres_to_pascals', 'pascals_to_atmospheres',
    # Area
    'square_meters_to_square_feet', 'square_feet_to_square_meters',
    'square_meters_to_acres', 'acres_to_square_meters',
    'hectares_to_acres', 'acres_to_hectares',
    # Data
    'bytes_to_kilobytes', 'kilobytes_to_bytes',
    'kilobytes_to_megabytes', 'megabytes_to_kilobytes',
    'megabytes_to_gigabytes', 'gigabytes_to_megabytes',
    'gigabytes_to_terabytes', 'terabytes_to_gigabytes',
    # Angle
    'degrees_to_radians', 'radians_to_degrees',
    'degrees_to_gradians', 'gradians_to_degrees',
    # Fuel
    'mpg_to_lper100km', 'lper100km_to_mpg',
]
