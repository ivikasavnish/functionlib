"""
Validation Functions

Input validation for common data types and formats.
"""

import re
from typing import Any, List, Optional


def is_email(email: str) -> bool:
    """
    Validates email address
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid email
        
    Example:
        >>> is_email("test@example.com")
        True
        >>> is_email("invalid.email")
        False
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_url(url: str) -> bool:
    """
    Validates URL
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid URL
        
    Example:
        >>> is_url("https://example.com")
        True
        >>> is_url("not a url")
        False
    """
    pattern = r'^https?://[^\s<>"{}|\\^`\[\]]+$'
    return bool(re.match(pattern, url))


def is_phone_number(phone: str, country_code: Optional[str] = None) -> bool:
    """
    Validates phone number (basic validation)
    
    Args:
        phone: Phone number
        country_code: Optional country code filter
        
    Returns:
        True if valid phone number
        
    Example:
        >>> is_phone_number("+1-234-567-8900")
        True
        >>> is_phone_number("123")
        False
    """
    # Remove spaces, dashes, parentheses
    cleaned = re.sub(r'[\s\-\(\)]', '', phone)
    
    # Check if it contains only digits and optional + at start
    pattern = r'^\+?\d{7,15}$'
    return bool(re.match(pattern, cleaned))


def is_credit_card(card_number: str) -> bool:
    """
    Validates credit card using Luhn algorithm
    
    Args:
        card_number: Credit card number
        
    Returns:
        True if valid credit card number
        
    Example:
        >>> is_credit_card("4532015112830366")
        True
        >>> is_credit_card("1234567890123456")
        False
    """
    # Remove spaces and dashes
    cleaned = re.sub(r'[\s\-]', '', card_number)
    
    if not cleaned.isdigit() or len(cleaned) < 13 or len(cleaned) > 19:
        return False
    
    # Luhn algorithm
    digits = [int(d) for d in cleaned]
    checksum = 0
    
    for i in range(len(digits) - 1, -1, -1):
        d = digits[i]
        
        if (len(digits) - i) % 2 == 0:
            d = d * 2
            if d > 9:
                d = d - 9
        
        checksum += d
    
    return checksum % 10 == 0


def is_ipv4(ip: str) -> bool:
    """
    Validates IPv4 address
    
    Args:
        ip: IP address
        
    Returns:
        True if valid IPv4
        
    Example:
        >>> is_ipv4("192.168.1.1")
        True
        >>> is_ipv4("256.1.1.1")
        False
    """
    parts = ip.split('.')
    
    if len(parts) != 4:
        return False
    
    for part in parts:
        try:
            num = int(part)
            if num < 0 or num > 255:
                return False
        except ValueError:
            return False
    
    return True


def is_ipv6(ip: str) -> bool:
    """
    Validates IPv6 address (basic)
    
    Args:
        ip: IP address
        
    Returns:
        True if valid IPv6
        
    Example:
        >>> is_ipv6("2001:0db8:85a3:0000:0000:8a2e:0370:7334")
        True
        >>> is_ipv6("not:an:ip")
        False
    """
    pattern = r'^([0-9a-fA-F]{1,4}:){7}[0-9a-fA-F]{1,4}$'
    return bool(re.match(pattern, ip))


def is_mac_address(mac: str) -> bool:
    """
    Validates MAC address
    
    Args:
        mac: MAC address
        
    Returns:
        True if valid MAC address
        
    Example:
        >>> is_mac_address("00:1B:44:11:3A:B7")
        True
        >>> is_mac_address("invalid")
        False
    """
    pattern = r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$'
    return bool(re.match(pattern, mac))


def is_uuid(uuid_str: str) -> bool:
    """
    Validates UUID
    
    Args:
        uuid_str: UUID string
        
    Returns:
        True if valid UUID
        
    Example:
        >>> is_uuid("123e4567-e89b-12d3-a456-426614174000")
        True
        >>> is_uuid("invalid-uuid")
        False
    """
    pattern = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$'
    return bool(re.match(pattern, uuid_str.lower()))


def is_hexadecimal(s: str) -> bool:
    """
    Validates hexadecimal string
    
    Args:
        s: String to validate
        
    Returns:
        True if valid hexadecimal
        
    Example:
        >>> is_hexadecimal("1A2B3C")
        True
        >>> is_hexadecimal("GHIJKL")
        False
    """
    pattern = r'^[0-9A-Fa-f]+$'
    return bool(re.match(pattern, s))


def is_alpha(s: str) -> bool:
    """
    Checks if string contains only letters
    
    Args:
        s: String to check
        
    Returns:
        True if only letters
        
    Example:
        >>> is_alpha("Hello")
        True
        >>> is_alpha("Hello123")
        False
    """
    return s.isalpha()


def is_alphanumeric(s: str) -> bool:
    """
    Checks if string contains only letters and numbers
    
    Args:
        s: String to check
        
    Returns:
        True if only letters and numbers
        
    Example:
        >>> is_alphanumeric("Hello123")
        True
        >>> is_alphanumeric("Hello 123")
        False
    """
    return s.isalnum()


def is_numeric(s: str) -> bool:
    """
    Checks if string is numeric
    
    Args:
        s: String to check
        
    Returns:
        True if numeric
        
    Example:
        >>> is_numeric("12345")
        True
        >>> is_numeric("12.34")
        False
    """
    return s.isdigit()


def is_float(s: str) -> bool:
    """
    Checks if string can be converted to float
    
    Args:
        s: String to check
        
    Returns:
        True if valid float
        
    Example:
        >>> is_float("12.34")
        True
        >>> is_float("abc")
        False
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


def is_integer(s: str) -> bool:
    """
    Checks if string can be converted to integer
    
    Args:
        s: String to check
        
    Returns:
        True if valid integer
        
    Example:
        >>> is_integer("123")
        True
        >>> is_integer("12.3")
        False
    """
    try:
        int(s)
        return True
    except ValueError:
        return False


def is_positive(value: float) -> bool:
    """
    Checks if number is positive
    
    Args:
        value: Number to check
        
    Returns:
        True if positive
        
    Example:
        >>> is_positive(5)
        True
        >>> is_positive(-5)
        False
    """
    return value > 0


def is_negative(value: float) -> bool:
    """
    Checks if number is negative
    
    Args:
        value: Number to check
        
    Returns:
        True if negative
        
    Example:
        >>> is_negative(-5)
        True
        >>> is_negative(5)
        False
    """
    return value < 0


def is_in_range(value: float, min_val: float, max_val: float, inclusive: bool = True) -> bool:
    """
    Checks if value is within range
    
    Args:
        value: Value to check
        min_val: Minimum value
        max_val: Maximum value
        inclusive: Whether to include boundaries
        
    Returns:
        True if in range
        
    Example:
        >>> is_in_range(5, 1, 10)
        True
        >>> is_in_range(10, 1, 10, inclusive=False)
        False
    """
    if inclusive:
        return min_val <= value <= max_val
    return min_val < value < max_val


def is_length_valid(s: str, min_length: Optional[int] = None, max_length: Optional[int] = None) -> bool:
    """
    Validates string length
    
    Args:
        s: String to check
        min_length: Minimum length (optional)
        max_length: Maximum length (optional)
        
    Returns:
        True if length is valid
        
    Example:
        >>> is_length_valid("hello", min_length=3, max_length=10)
        True
        >>> is_length_valid("hi", min_length=3)
        False
    """
    length = len(s)
    
    if min_length is not None and length < min_length:
        return False
    
    if max_length is not None and length > max_length:
        return False
    
    return True


def contains_uppercase(s: str) -> bool:
    """
    Checks if string contains at least one uppercase letter
    
    Args:
        s: String to check
        
    Returns:
        True if contains uppercase
        
    Example:
        >>> contains_uppercase("Hello")
        True
        >>> contains_uppercase("hello")
        False
    """
    return any(c.isupper() for c in s)


def contains_lowercase(s: str) -> bool:
    """
    Checks if string contains at least one lowercase letter
    
    Args:
        s: String to check
        
    Returns:
        True if contains lowercase
        
    Example:
        >>> contains_lowercase("Hello")
        True
        >>> contains_lowercase("HELLO")
        False
    """
    return any(c.islower() for c in s)


def contains_digit(s: str) -> bool:
    """
    Checks if string contains at least one digit
    
    Args:
        s: String to check
        
    Returns:
        True if contains digit
        
    Example:
        >>> contains_digit("Hello123")
        True
        >>> contains_digit("Hello")
        False
    """
    return any(c.isdigit() for c in s)


def contains_special_char(s: str) -> bool:
    """
    Checks if string contains special characters
    
    Args:
        s: String to check
        
    Returns:
        True if contains special characters
        
    Example:
        >>> contains_special_char("Hello!")
        True
        >>> contains_special_char("Hello")
        False
    """
    return bool(re.search(r'[^a-zA-Z0-9\s]', s))


def is_strong_password(password: str, min_length: int = 8) -> bool:
    """
    Validates password strength
    
    Args:
        password: Password to validate
        min_length: Minimum length
        
    Returns:
        True if strong password
        
    Example:
        >>> is_strong_password("MyP@ssw0rd")
        True
        >>> is_strong_password("weak")
        False
    """
    if len(password) < min_length:
        return False
    
    if not contains_uppercase(password):
        return False
    
    if not contains_lowercase(password):
        return False
    
    if not contains_digit(password):
        return False
    
    if not contains_special_char(password):
        return False
    
    return True


# Export all functions
__all__ = [
    'is_email', 'is_url', 'is_phone_number', 'is_credit_card',
    'is_ipv4', 'is_ipv6', 'is_mac_address', 'is_uuid', 'is_hexadecimal',
    'is_alpha', 'is_alphanumeric', 'is_numeric', 'is_float', 'is_integer',
    'is_positive', 'is_negative', 'is_in_range', 'is_length_valid',
    'contains_uppercase', 'contains_lowercase', 'contains_digit', 'contains_special_char',
    'is_strong_password',
]
