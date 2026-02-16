"""Regular expression utilities for common pattern matching tasks."""

import re
from typing import List, Dict, Optional, Tuple

__all__ = [
    'extract_emails',
    'extract_urls',
    'extract_phone_numbers',
    'extract_hashtags',
    'extract_mentions',
    'extract_numbers',
    'extract_dates',
    'is_email_valid',
    'is_url_valid',
    'is_phone_valid',
    'sanitize_filename',
    'remove_html_tags',
    'extract_html_tags',
    'camel_to_snake',
    'snake_to_camel',
    'extract_ipv4_addresses',
    'extract_credit_cards',
    'mask_credit_card',
    'extract_code_blocks',
    'count_pattern',
    'replace_pattern',
    'split_by_pattern',
    'match_all',
    'find_between',
    'remove_whitespace',
]

def extract_emails(text: str) -> List[str]:
    """Extract all email addresses from text.
    
    Args:
        text: Input text
        
    Returns:
        List of email addresses
        
    Example:
        >>> extract_emails("Contact me at john@example.com or jane@test.org")
        ['john@example.com', 'jane@test.org']
    """
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(pattern, text)

def extract_urls(text: str, protocols: Optional[List[str]] = None) -> List[str]:
    """Extract URLs from text.
    
    Args:
        text: Input text
        protocols: List of protocols to match (default: ['http', 'https'])
        
    Returns:
        List of URLs
        
    Example:
        >>> extract_urls("Visit https://example.com or http://test.org")
        ['https://example.com', 'http://test.org']
    """
    if protocols is None:
        protocols = ['http', 'https']
    
    protocol_pattern = '|'.join(protocols)
    pattern = rf'(?:{protocol_pattern})://[A-Za-z0-9.-]+(?:/[^\s]*)?'
    return re.findall(pattern, text)

def extract_phone_numbers(text: str) -> List[str]:
    """Extract phone numbers from text (US format).
    
    Args:
        text: Input text
        
    Returns:
        List of phone numbers
        
    Example:
        >>> extract_phone_numbers("Call 123-456-7890 or (123) 456-7890")
        ['123-456-7890', '(123) 456-7890']
    """
    patterns = [
        r'\d{3}-\d{3}-\d{4}',  # 123-456-7890
        r'\(\d{3}\)\s*\d{3}-\d{4}',  # (123) 456-7890
        r'\d{10}',  # 1234567890
    ]
    
    results = []
    for pattern in patterns:
        results.extend(re.findall(pattern, text))
    return results

def extract_hashtags(text: str) -> List[str]:
    """Extract hashtags from text.
    
    Args:
        text: Input text
        
    Returns:
        List of hashtags (without #)
        
    Example:
        >>> extract_hashtags("Check out #python and #coding")
        ['python', 'coding']
    """
    return re.findall(r'#(\w+)', text)

def extract_mentions(text: str) -> List[str]:
    """Extract mentions from text (Twitter-style).
    
    Args:
        text: Input text
        
    Returns:
        List of mentions (without @)
        
    Example:
        >>> extract_mentions("Thanks @john and @jane_doe")
        ['john', 'jane_doe']
    """
    return re.findall(r'@(\w+)', text)

def extract_numbers(text: str, include_decimals: bool = True) -> List[float]:
    """Extract numbers from text.
    
    Args:
        text: Input text
        include_decimals: Include decimal numbers
        
    Returns:
        List of numbers
        
    Example:
        >>> extract_numbers("I have 5 apples and 3.5 oranges")
        [5.0, 3.5]
    """
    if include_decimals:
        pattern = r'-?\d+\.?\d*'
    else:
        pattern = r'-?\d+'
    
    matches = re.findall(pattern, text)
    return [float(m) for m in matches if m and m != '-']

def extract_dates(text: str) -> List[str]:
    """Extract dates in common formats (MM/DD/YYYY, DD-MM-YYYY, YYYY-MM-DD).
    
    Args:
        text: Input text
        
    Returns:
        List of date strings
        
    Example:
        >>> extract_dates("Meeting on 12/25/2023 or 2023-12-25")
        ['12/25/2023', '2023-12-25']
    """
    patterns = [
        r'\d{2}/\d{2}/\d{4}',  # MM/DD/YYYY
        r'\d{2}-\d{2}-\d{4}',  # DD-MM-YYYY
        r'\d{4}-\d{2}-\d{2}',  # YYYY-MM-DD
    ]
    
    results = []
    for pattern in patterns:
        results.extend(re.findall(pattern, text))
    return results

def is_email_valid(email: str) -> bool:
    """Validate email address format.
    
    Args:
        email: Email address to validate
        
    Returns:
        True if valid format
        
    Example:
        >>> is_email_valid("john@example.com")
        True
        >>> is_email_valid("invalid.email")
        False
    """
    pattern = r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}$'
    return bool(re.match(pattern, email))

def is_url_valid(url: str) -> bool:
    """Validate URL format.
    
    Args:
        url: URL to validate
        
    Returns:
        True if valid format
        
    Example:
        >>> is_url_valid("https://example.com")
        True
    """
    pattern = r'^https?://[A-Za-z0-9.-]+(?:/[^\s]*)?$'
    return bool(re.match(pattern, url))

def is_phone_valid(phone: str) -> bool:
    """Validate US phone number format.
    
    Args:
        phone: Phone number to validate
        
    Returns:
        True if valid format
        
    Example:
        >>> is_phone_valid("123-456-7890")
        True
    """
    patterns = [
        r'^\d{3}-\d{3}-\d{4}$',
        r'^\(\d{3}\)\s*\d{3}-\d{4}$',
        r'^\d{10}$',
    ]
    return any(re.match(p, phone) for p in patterns)

def sanitize_filename(filename: str, replacement: str = '_') -> str:
    """Remove invalid characters from filename.
    
    Args:
        filename: Original filename
        replacement: Character to replace invalid chars with
        
    Returns:
        Sanitized filename
        
    Example:
        >>> sanitize_filename("my*file?.txt")
        'my_file_.txt'
    """
    # Remove invalid filename characters
    pattern = r'[<>:"/\\|?*]'
    return re.sub(pattern, replacement, filename)

def remove_html_tags(html: str) -> str:
    """Remove HTML tags from text.
    
    Args:
        html: HTML text
        
    Returns:
        Text without HTML tags
        
    Example:
        >>> remove_html_tags("<p>Hello <b>world</b></p>")
        'Hello world'
    """
    clean = re.sub(r'<[^>]+>', '', html)
    return re.sub(r'\s+', ' ', clean).strip()

def extract_html_tags(html: str) -> List[Tuple[str, str]]:
    """Extract HTML tags and their content.
    
    Args:
        html: HTML text
        
    Returns:
        List of (tag_name, content) tuples
        
    Example:
        >>> extract_html_tags("<p>Hello</p><b>world</b>")
        [('p', 'Hello'), ('b', 'world')]
    """
    pattern = r'<(\w+)[^>]*>(.*?)</\1>'
    return re.findall(pattern, html)

def camel_to_snake(text: str) -> str:
    """Convert camelCase to snake_case.
    
    Args:
        text: camelCase string
        
    Returns:
        snake_case string
        
    Example:
        >>> camel_to_snake("myVariableName")
        'my_variable_name'
    """
    # Insert underscore before uppercase letters
    result = re.sub(r'(?<!^)(?=[A-Z])', '_', text)
    return result.lower()

def snake_to_camel(text: str) -> str:
    """Convert snake_case to camelCase.
    
    Args:
        text: snake_case string
        
    Returns:
        camelCase string
        
    Example:
        >>> snake_to_camel("my_variable_name")
        'myVariableName'
    """
    components = text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def extract_ipv4_addresses(text: str) -> List[str]:
    """Extract IPv4 addresses from text.
    
    Args:
        text: Input text
        
    Returns:
        List of IPv4 addresses
        
    Example:
        >>> extract_ipv4_addresses("Server at 192.168.1.1 or 10.0.0.1")
        ['192.168.1.1', '10.0.0.1']
    """
    pattern = r'\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b'
    return re.findall(pattern, text)

def extract_credit_cards(text: str) -> List[str]:
    """Extract credit card numbers (simple pattern, not validated).
    
    Args:
        text: Input text
        
    Returns:
        List of potential credit card numbers
        
    Example:
        >>> extract_credit_cards("Card: 1234-5678-9012-3456")
        ['1234-5678-9012-3456']
    """
    patterns = [
        r'\b\d{4}-\d{4}-\d{4}-\d{4}\b',  # 1234-5678-9012-3456
        r'\b\d{16}\b',  # 1234567890123456
    ]
    
    results = []
    for pattern in patterns:
        results.extend(re.findall(pattern, text))
    return results

def mask_credit_card(card_number: str, mask_char: str = '*') -> str:
    """Mask credit card number, showing only last 4 digits.
    
    Args:
        card_number: Credit card number
        mask_char: Character to use for masking
        
    Returns:
        Masked credit card number
        
    Example:
        >>> mask_credit_card("1234567890123456")
        '************3456'
    """
    digits = re.sub(r'\D', '', card_number)
    if len(digits) < 4:
        return mask_char * len(digits)
    return mask_char * (len(digits) - 4) + digits[-4:]

def extract_code_blocks(text: str, language: Optional[str] = None) -> List[str]:
    """Extract code blocks from markdown text.
    
    Args:
        text: Markdown text
        language: Specific language to extract (or None for all)
        
    Returns:
        List of code blocks
        
    Example:
        >>> extract_code_blocks("```python\\nprint('hello')\\n```")
        ["print('hello')"]
    """
    if language:
        pattern = rf'```{language}\n(.*?)```'
    else:
        pattern = r'```(?:\w+)?\n(.*?)```'
    
    return re.findall(pattern, text, re.DOTALL)

def count_pattern(text: str, pattern: str) -> int:
    """Count occurrences of a regex pattern.
    
    Args:
        text: Input text
        pattern: Regex pattern
        
    Returns:
        Number of matches
        
    Example:
        >>> count_pattern("hello hello world", r'\bhello\b')
        2
    """
    return len(re.findall(pattern, text))

def replace_pattern(text: str, pattern: str, replacement: str) -> str:
    """Replace all occurrences of a pattern.
    
    Args:
        text: Input text
        pattern: Regex pattern
        replacement: Replacement string
        
    Returns:
        Text with replacements
        
    Example:
        >>> replace_pattern("hello world", r'\bhello\b', "hi")
        'hi world'
    """
    return re.sub(pattern, replacement, text)

def split_by_pattern(text: str, pattern: str) -> List[str]:
    """Split text by regex pattern.
    
    Args:
        text: Input text
        pattern: Regex pattern
        
    Returns:
        List of text segments
        
    Example:
        >>> split_by_pattern("a,b;c:d", r'[,;:]')
        ['a', 'b', 'c', 'd']
    """
    return re.split(pattern, text)

def match_all(text: str, pattern: str) -> List[str]:
    """Find all matches of a pattern.
    
    Args:
        text: Input text
        pattern: Regex pattern
        
    Returns:
        List of all matches
        
    Example:
        >>> match_all("test123abc456", r'\d+')
        ['123', '456']
    """
    return re.findall(pattern, text)

def find_between(text: str, start: str, end: str) -> List[str]:
    """Find text between two patterns.
    
    Args:
        text: Input text
        start: Starting pattern
        end: Ending pattern
        
    Returns:
        List of text segments between patterns
        
    Example:
        >>> find_between("(hello) (world)", r'\(', r'\)')
        ['hello', 'world']
    """
    pattern = f'{start}(.*?){end}'
    return re.findall(pattern, text)

def remove_whitespace(text: str, keep_single_space: bool = True) -> str:
    """Remove extra whitespace from text.
    
    Args:
        text: Input text
        keep_single_space: Keep single spaces between words
        
    Returns:
        Text with normalized whitespace
        
    Example:
        >>> remove_whitespace("hello    world\\n\\n  test")
        'hello world test'
    """
    if keep_single_space:
        return re.sub(r'\s+', ' ', text).strip()
    else:
        return re.sub(r'\s+', '', text)
