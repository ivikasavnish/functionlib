"""
String Utility Functions

Common string manipulation utilities.
"""

import random
import string
from typing import List, Optional
import hashlib
import base64


def capitalize_words(s: str) -> str:
    """
    Capitalizes first letter of each word
    
    Args:
        s: Input string
        
    Returns:
        Capitalized string
        
    Example:
        >>> capitalize_words("hello world")
        'Hello World'
    """
    return s.title()


def swap_case(s: str) -> str:
    """
    Swaps case of all letters
    
    Args:
        s: Input string
        
    Returns:
        Case-swapped string
        
    Example:
        >>> swap_case("Hello World")
        'hELLO wORLD'
    """
    return s.swapcase()


def random_string(length: int, chars: Optional[str] = None) -> str:
    """
    Generates random string
    
    Args:
        length: Length of string
        chars: Character set to use (default: letters + digits)
        
    Returns:
        Random string
        
    Example:
        >>> s = random_string(10)
        >>> len(s)
        10
    """
    if chars is None:
        chars = string.ascii_letters + string.digits
    
    return ''.join(random.choice(chars) for _ in range(length))


def random_lowercase(length: int) -> str:
    """
    Generates random lowercase string
    
    Args:
        length: Length of string
        
    Returns:
        Random lowercase string
        
    Example:
        >>> s = random_lowercase(10)
        >>> s.islower()
        True
    """
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(length))


def random_uppercase(length: int) -> str:
    """
    Generates random uppercase string
    
    Args:
        length: Length of string
        
    Returns:
        Random uppercase string
        
    Example:
        >>> s = random_uppercase(10)
        >>> s.isupper()
        True
    """
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(length))


def random_digits(length: int) -> str:
    """
    Generates random digit string
    
    Args:
        length: Length of string
        
    Returns:
        Random digit string
        
    Example:
        >>> s = random_digits(10)
        >>> s.isdigit()
        True
    """
    return ''.join(random.choice(string.digits) for _ in range(length))


def md5_hash(s: str) -> str:
    """
    Calculates MD5 hash
    
    Args:
        s: Input string
        
    Returns:
        MD5 hash (hex)
        
    Example:
        >>> md5_hash("hello")
        '5d41402abc4b2a76b9719d911017c592'
    """
    return hashlib.md5(s.encode()).hexdigest()


def sha256_hash(s: str) -> str:
    """
    Calculates SHA-256 hash
    
    Args:
        s: Input string
        
    Returns:
        SHA-256 hash (hex)
        
    Example:
        >>> sha256_hash("hello")
        '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    """
    return hashlib.sha256(s.encode()).hexdigest()


def base64_encode(s: str) -> str:
    """
    Encodes string in base64
    
    Args:
        s: Input string
        
    Returns:
        Base64 encoded string
        
    Example:
        >>> base64_encode("hello")
        'aGVsbG8='
    """
    return base64.b64encode(s.encode()).decode()


def base64_decode(s: str) -> str:
    """
    Decodes base64 string
    
    Args:
        s: Base64 encoded string
        
    Returns:
        Decoded string
        
    Example:
        >>> base64_decode("aGVsbG8=")
        'hello'
    """
    return base64.b64decode(s.encode()).decode()


def url_encode(s: str) -> str:
    """
    URL encodes string
    
    Args:
        s: Input string
        
    Returns:
        URL encoded string
        
    Example:
        >>> url_encode("hello world")
        'hello%20world'
    """
    import urllib.parse
    return urllib.parse.quote(s)


def url_decode(s: str) -> str:
    """
    URL decodes string
    
    Args:
        s: URL encoded string
        
    Returns:
        Decoded string
        
    Example:
        >>> url_decode("hello%20world")
        'hello world'
    """
    import urllib.parse
    return urllib.parse.unquote(s)


def escape_html(s: str) -> str:
    """
    Escapes HTML special characters
    
    Args:
        s: Input string
        
    Returns:
        HTML-safe string
        
    Example:
        >>> escape_html("<div>Hello</div>")
        '&lt;div&gt;Hello&lt;/div&gt;'
    """
    import html
    return html.escape(s)


def unescape_html(s: str) -> str:
    """
    Unescapes HTML entities
    
    Args:
        s: HTML string
        
    Returns:
        Unescaped string
        
    Example:
        >>> unescape_html("&lt;div&gt;Hello&lt;/div&gt;")
        '<div>Hello</div>'
    """
    import html
    return html.unescape(s)


def extract_numbers(s: str) -> List[float]:
    """
    Extracts all numbers from string
    
    Args:
        s: Input string
        
    Returns:
        List of numbers
        
    Example:
        >>> extract_numbers("Price is $19.99 and $29.99")
        [19.99, 29.99]
    """
    import re
    return [float(x) for x in re.findall(r'-?\d+\.?\d*', s)]


def extract_emails(s: str) -> List[str]:
    """
    Extracts email addresses from string
    
    Args:
        s: Input string
        
    Returns:
        List of email addresses
        
    Example:
        >>> extract_emails("Contact us at info@example.com or support@test.org")
        ['info@example.com', 'support@test.org']
    """
    import re
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, s)


def extract_urls(s: str) -> List[str]:
    """
    Extracts URLs from string
    
    Args:
        s: Input string
        
    Returns:
        List of URLs
        
    Example:
        >>> extract_urls("Visit https://example.com or http://test.org")
        ['https://example.com', 'http://test.org']
    """
    import re
    pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    return re.findall(pattern, s)


def levenshtein_distance(s1: str, s2: str) -> int:
    """
    Calculates Levenshtein distance (edit distance)
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Edit distance
        
    Example:
        >>> levenshtein_distance("kitten", "sitting")
        3
    """
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        
        previous_row = current_row
    
    return previous_row[-1]


def similarity_ratio(s1: str, s2: str) -> float:
    """
    Calculates similarity ratio between two strings (0-100%)
    
    Args:
        s1: First string
        s2: Second string
        
    Returns:
        Similarity percentage
        
    Example:
        >>> similarity_ratio("hello", "hallo")
        80.0
    """
    distance = levenshtein_distance(s1, s2)
    max_len = max(len(s1), len(s2))
    
    if max_len == 0:
        return 100.0
    
    return (1 - distance / max_len) * 100


# Export all functions
__all__ = [
    'capitalize_words', 'swap_case',
    'random_string', 'random_lowercase', 'random_uppercase', 'random_digits',
    'md5_hash', 'sha256_hash',
    'base64_encode', 'base64_decode',
    'url_encode', 'url_decode',
    'escape_html', 'unescape_html',
    'extract_numbers', 'extract_emails', 'extract_urls',
    'levenshtein_distance', 'similarity_ratio',
]
