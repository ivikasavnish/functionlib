"""
String Operations

String manipulation, parsing, and analysis functions.
"""

import re
from typing import List, Dict, Optional


def reverse_string(s: str) -> str:
    """
    Reverses a string
    
    Args:
        s: Input string
        
    Returns:
        Reversed string
        
    Example:
        >>> reverse_string("hello")
        'olleh'
    """
    return s[::-1]


def is_palindrome(s: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
    """
    Checks if string is a palindrome
    
    Args:
        s: Input string
        ignore_case: Whether to ignore case
        ignore_spaces: Whether to ignore spaces
        
    Returns:
        True if palindrome
        
    Example:
        >>> is_palindrome("A man a plan a canal Panama")
        True
    """
    if ignore_spaces:
        s = s.replace(' ', '')
    if ignore_case:
        s = s.lower()
    
    return s == s[::-1]


def count_vowels(s: str) -> int:
    """
    Counts vowels in string
    
    Args:
        s: Input string
        
    Returns:
        Number of vowels
        
    Example:
        >>> count_vowels("hello world")
        3
    """
    vowels = 'aeiouAEIOU'
    return sum(1 for char in s if char in vowels)


def count_consonants(s: str) -> int:
    """
    Counts consonants in string
    
    Args:
        s: Input string
        
    Returns:
        Number of consonants
        
    Example:
        >>> count_consonants("hello world")
        7
    """
    consonants = 'bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ'
    return sum(1 for char in s if char in consonants)


def word_count(s: str) -> int:
    """
    Counts words in string
    
    Args:
        s: Input string
        
    Returns:
        Number of words
        
    Example:
        >>> word_count("hello world this is a test")
        6
    """
    return len(s.split())


def character_frequency(s: str) -> Dict[str, int]:
    """
    Counts frequency of each character
    
    Args:
        s: Input string
        
    Returns:
        Dict mapping characters to counts
        
    Example:
        >>> character_frequency("hello")
        {'h': 1, 'e': 1, 'l': 2, 'o': 1}
    """
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq


def remove_duplicates(s: str, preserve_order: bool = True) -> str:
    """
    Removes duplicate characters
    
    Args:
        s: Input string
        preserve_order: Whether to preserve original order
        
    Returns:
        String without duplicates
        
    Example:
        >>> remove_duplicates("hello")
        'helo'
    """
    if preserve_order:
        seen = set()
        result = []
        for char in s:
            if char not in seen:
                seen.add(char)
                result.append(char)
        return ''.join(result)
    else:
        return ''.join(set(s))


def title_case(s: str) -> str:
    """
    Converts string to title case
    
    Args:
        s: Input string
        
    Returns:
        Title-cased string
        
    Example:
        >>> title_case("hello world")
        'Hello World'
    """
    return s.title()


def snake_case(s: str) -> str:
    """
    Converts string to snake_case
    
    Args:
        s: Input string
        
    Returns:
        snake_cased string
        
    Example:
        >>> snake_case("Hello World")
        'hello_world'
    """
    s = re.sub('([A-Z]+)', r'_\1', s).lower()
    s = s.replace(' ', '_')
    s = re.sub('_+', '_', s)
    return s.strip('_')


def camel_case(s: str) -> str:
    """
    Converts string to camelCase
    
    Args:
        s: Input string
        
    Returns:
        camelCased string
        
    Example:
        >>> camel_case("hello world")
        'helloWorld'
    """
    words = s.replace('_', ' ').split()
    if not words:
        return s
    
    return words[0].lower() + ''.join(word.capitalize() for word in words[1:])


def pascal_case(s: str) -> str:
    """
    Converts string to PascalCase
    
    Args:
        s: Input string
        
    Returns:
        PascalCased string
        
    Example:
        >>> pascal_case("hello world")
        'HelloWorld'
    """
    words = s.replace('_', ' ').split()
    return ''.join(word.capitalize() for word in words)


def kebab_case(s: str) -> str:
    """
    Converts string to kebab-case
    
    Args:
        s: Input string
        
    Returns:
        kebab-cased string
        
    Example:
        >>> kebab_case("Hello World")
        'hello-world'
    """
    s = re.sub('([A-Z]+)', r'-\1', s).lower()
    s = s.replace(' ', '-').replace('_', '-')
    s = re.sub('-+', '-', s)
    return s.strip('-')


def truncate(s: str, length: int, suffix: str = '...') -> str:
    """
    Truncates string to specified length
    
    Args:
        s: Input string
        length: Maximum length
        suffix: Suffix to add if truncated
        
    Returns:
        Truncated string
        
    Example:
        >>> truncate("hello world", 8)
        'hello...'
    """
    if len(s) <= length:
        return s
    return s[:length - len(suffix)] + suffix


def pad_left(s: str, width: int, fill_char: str = ' ') -> str:
    """
    Pads string on left to specified width
    
    Args:
        s: Input string
        width: Target width
        fill_char: Character to pad with
        
    Returns:
        Padded string
        
    Example:
        >>> pad_left("hello", 10)
        '     hello'
    """
    return s.rjust(width, fill_char)


def pad_right(s: str, width: int, fill_char: str = ' ') -> str:
    """
    Pads string on right to specified width
    
    Args:
        s: Input string
        width: Target width
        fill_char: Character to pad with
        
    Returns:
        Padded string
        
    Example:
        >>> pad_right("hello", 10)
        'hello     '
    """
    return s.ljust(width, fill_char)


def pad_center(s: str, width: int, fill_char: str = ' ') -> str:
    """
    Centers string within specified width
    
    Args:
        s: Input string
        width: Target width
        fill_char: Character to pad with
        
    Returns:
        Centered string
        
    Example:
        >>> pad_center("hello", 11)
        '   hello   '
    """
    return s.center(width, fill_char)


def starts_with(s: str, prefix: str, ignore_case: bool = False) -> bool:
    """
    Checks if string starts with prefix
    
    Args:
        s: Input string
        prefix: Prefix to check
        ignore_case: Whether to ignore case
        
    Returns:
        True if starts with prefix
        
    Example:
        >>> starts_with("hello world", "hello")
        True
    """
    if ignore_case:
        return s.lower().startswith(prefix.lower())
    return s.startswith(prefix)


def ends_with(s: str, suffix: str, ignore_case: bool = False) -> bool:
    """
    Checks if string ends with suffix
    
    Args:
        s: Input string
        suffix: Suffix to check
        ignore_case: Whether to ignore case
        
    Returns:
        True if ends with suffix
        
    Example:
        >>> ends_with("hello world", "world")
        True
    """
    if ignore_case:
        return s.lower().endswith(suffix.lower())
    return s.endswith(suffix)


def contains_substring(s: str, substring: str, ignore_case: bool = False) -> bool:
    """
    Checks if string contains substring
    
    Args:
        s: Input string
        substring: Substring to find
        ignore_case: Whether to ignore case
        
    Returns:
        True if contains substring
        
    Example:
        >>> contains_substring("hello world", "lo wo")
        True
    """
    if ignore_case:
        return substring.lower() in s.lower()
    return substring in s


def repeat_string(s: str, n: int) -> str:
    """
    Repeats string n times
    
    Args:
        s: Input string
        n: Number of repetitions
        
    Returns:
        Repeated string
        
    Example:
        >>> repeat_string("ha", 3)
        'hahaha'
    """
    return s * n


def split_lines(s: str) -> List[str]:
    """
    Splits string into lines
    
    Args:
        s: Input string
        
    Returns:
        List of lines
        
    Example:
        >>> split_lines("hello\\nworld")
        ['hello', 'world']
    """
    return s.splitlines()


def join_lines(lines: List[str], separator: str = '\n') -> str:
    """
    Joins lines with separator
    
    Args:
        lines: List of lines
        separator: Separator to use
        
    Returns:
        Joined string
        
    Example:
        >>> join_lines(['hello', 'world'])
        'hello\\nworld'
    """
    return separator.join(lines)


def remove_whitespace(s: str) -> str:
    """
    Removes all whitespace from string
    
    Args:
        s: Input string
        
    Returns:
        String without whitespace
        
    Example:
        >>> remove_whitespace("hello  world  ")
        'helloworld'
    """
    return ''.join(s.split())


def normalize_whitespace(s: str) -> str:
    """
    Normalizes whitespace (single spaces, trimmed)
    
    Args:
        s: Input string
        
    Returns:
        Normalized string
        
    Example:
        >>> normalize_whitespace("  hello   world  ")
        'hello world'
    """
    return ' '.join(s.split())


def slug_ify(s: str) -> str:
    """
    Converts string to URL-friendly slug
    
    Args:
        s: Input string
        
    Returns:
        Slug string
        
    Example:
        >>> slug_ify("Hello World!")
        'hello-world'
    """
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s-]', '', s)
    s = re.sub(r'[\s-]+', '-', s)
    return s.strip('-')


# Export all functions
__all__ = [
    'reverse_string', 'is_palindrome',
    'count_vowels', 'count_consonants', 'word_count',
    'character_frequency', 'remove_duplicates',
    'title_case', 'snake_case', 'camel_case', 'pascal_case', 'kebab_case',
    'truncate', 'pad_left', 'pad_right', 'pad_center',
    'starts_with', 'ends_with', 'contains_substring',
    'repeat_string', 'split_lines', 'join_lines',
    'remove_whitespace', 'normalize_whitespace', 'slug_ify',
]
