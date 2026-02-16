"""
Formatting Functions

Data formatting utilities for numbers, strings, dates, and more.
"""

from typing import Optional, List
import re


def format_number_with_commas(number: float, decimals: int = 0) -> str:
    """
    Format number with thousand separators
    
    Args:
        number: Number to format
        decimals: Decimal places
        
    Returns:
        Formatted string
        
    Example:
        >>> format_number_with_commas(1234567.89, 2)
        '1,234,567.89'
    """
    format_str = f"{{:,.{decimals}f}}"
    return format_str.format(number)


def format_currency(amount: float, symbol: str = '$', decimals: int = 2) -> str:
    """
    Format as currency
    
    Args:
        amount: Amount
        symbol: Currency symbol
        decimals: Decimal places
        
    Returns:
        Formatted currency string
        
    Example:
        >>> format_currency(1234.56)
        '$1,234.56'
    """
    formatted = format_number_with_commas(abs(amount), decimals)
    
    if amount < 0:
        return f"-{symbol}{formatted}"
    
    return f"{symbol}{formatted}"


def format_percentage(value: float, decimals: int = 1) -> str:
    """
    Format as percentage
    
    Args:
        value: Value (as decimal, e.g., 0.15)
        decimals: Decimal places
        
    Returns:
        Formatted percentage
        
    Example:
        >>> format_percentage(0.1567, 2)
        '15.67%'
    """
    return f"{value * 100:.{decimals}f}%"


def format_file_size(bytes_val: int) -> str:
    """
    Format bytes as human-readable size
    
    Args:
        bytes_val: Size in bytes
        
    Returns:
        Formatted size string
        
    Example:
        >>> format_file_size(1536)
        '1.5 KB'
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB', 'PB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    
    return f"{bytes_val:.1f} EB"


def format_phone_number(number: str, format_type: str = 'us') -> str:
    """
    Format phone number
    
    Args:
        number: Raw phone number digits
        format_type: Format ('us' or 'international')
        
    Returns:
        Formatted phone number
        
    Example:
        >>> format_phone_number('1234567890')
        '(123) 456-7890'
    """
    # Remove non-digits
    digits = re.sub(r'\D', '', number)
    
    if format_type == 'us' and len(digits) == 10:
        return f"({digits[:3]}) {digits[3:6]}-{digits[6:]}"
    elif format_type == 'us' and len(digits) == 11 and digits[0] == '1':
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    
    return number


def format_credit_card(number: str) -> str:
    """
    Format credit card number with spaces
    
    Args:
        number: Credit card number
        
    Returns:
        Formatted credit card
        
    Example:
        >>> format_credit_card('1234567890123456')
        '1234 5678 9012 3456'
    """
    digits = re.sub(r'\D', '', number)
    
    return ' '.join([digits[i:i+4] for i in range(0, len(digits), 4)])


def format_ssn(ssn: str) -> str:
    """
    Format Social Security Number
    
    Args:
        ssn: SSN digits
        
    Returns:
        Formatted SSN
        
    Example:
        >>> format_ssn('123456789')
        '123-45-6789'
    """
    digits = re.sub(r'\D', '', ssn)
    
    if len(digits) == 9:
        return f"{digits[:3]}-{digits[3:5]}-{digits[5:]}"
    
    return ssn


def truncate_string(text: str, max_length: int, suffix: str = '...') -> str:
    """
    Truncate string with ellipsis
    
    Args:
        text: Text to truncate
        max_length: Maximum length
        suffix: Suffix to add (default '...')
        
    Returns:
        Truncated string
        
    Example:
        >>> truncate_string('Hello, world!', 10)
        'Hello, ...'
    """
    if len(text) <= max_length:
        return text
    
    return text[:max_length - len(suffix)] + suffix


def pad_string(text: str, width: int, align: str = 'left', char: str = ' ') -> str:
    """
    Pad string to specified width
    
    Args:
        text: Text to pad
        width: Target width
        align: 'left', 'right', or 'center'
        char: Padding character
        
    Returns:
        Padded string
        
    Example:
        >>> pad_string('hello', 10, 'center')
        '  hello   '
    """
    if align == 'left':
        return text.ljust(width, char)
    elif align == 'right':
        return text.rjust(width, char)
    else:  # center
        return text.center(width, char)


def format_list(items: List[str], conjunction: str = 'and') -> str:
    """
    Format list as natural language
    
    Args:
        items: List of items
        conjunction: Conjunction word ('and' or 'or')
        
    Returns:
        Formatted string
        
    Example:
        >>> format_list(['apples', 'oranges', 'bananas'])
        'apples, oranges, and bananas'
    """
    if len(items) == 0:
        return ''
    elif len(items) == 1:
        return items[0]
    elif len(items) == 2:
        return f"{items[0]} {conjunction} {items[1]}"
    else:
        return f"{', '.join(items[:-1])}, {conjunction} {items[-1]}"


def format_ordinal(n: int) -> str:
    """
    Format number as ordinal
    
    Args:
        n: Number
        
    Returns:
        Ordinal string
        
    Example:
        >>> format_ordinal(1)
        '1st'
        >>> format_ordinal(22)
        '22nd'
    """
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    
    return f"{n}{suffix}"


def format_pluralize(count: int, singular: str, plural: Optional[str] = None) -> str:
    """
    Format word with pluralization
    
    Args:
        count: Count
        singular: Singular form
        plural: Plural form (auto-generates if not provided)
        
    Returns:
        Formatted string with count
        
    Example:
        >>> format_pluralize(1, 'apple')
        '1 apple'
        >>> format_pluralize(3, 'apple')
        '3 apples'
    """
    if plural is None:
        plural = singular + 's'
    
    word = singular if count == 1 else plural
    
    return f"{count} {word}"


def camel_case_to_snake_case(text: str) -> str:
    """
    Convert camelCase to snake_case
    
    Args:
        text: camelCase string
        
    Returns:
        snake_case string
        
    Example:
        >>> camel_case_to_snake_case('myVariableName')
        'my_variable_name'
    """
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()


def snake_case_to_camel_case(text: str) -> str:
    """
    Convert snake_case to camelCase
    
    Args:
        text: snake_case string
        
    Returns:
        camelCase string
        
    Example:
        >>> snake_case_to_camel_case('my_variable_name')
        'myVariableName'
    """
    components = text.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])


def title_case(text: str) -> str:
    """
    Convert to Title Case (proper capitalization)
    
    Args:
        text: Text to convert
        
    Returns:
        Title cased string
        
    Example:
        >>> title_case('the quick brown fox')
        'The Quick Brown Fox'
    """
    return text.title()


def format_table_row(values: List[str], widths: List[int], separator: str = ' | ') -> str:
    """
    Format row for ASCII table
    
    Args:
        values: Cell values
        widths: Column widths
        separator: Column separator
        
    Returns:
        Formatted row
        
    Example:
        >>> format_table_row(['Name', 'Age'], [10, 5])
        'Name       | Age  '
    """
    cells = [str(v).ljust(w) for v, w in zip(values, widths)]
    return separator.join(cells)


def format_json_pretty(obj: dict, indent: int = 2) -> str:
    """
    Format object as pretty JSON
    
    Args:
        obj: Object to format
        indent: Indentation spaces
        
    Returns:
        Formatted JSON string
        
    Example:
        >>> format_json_pretty({'key': 'value'})
        '{\\n  "key": "value"\\n}'
    """
    import json
    return json.dumps(obj, indent=indent)


def format_xml_attribute(name: str, value: str) -> str:
    """
    Format XML attribute
    
    Args:
        name: Attribute name
        value: Attribute value
        
    Returns:
        Formatted attribute
        
    Example:
        >>> format_xml_attribute('id', '123')
        'id="123"'
    """
    # Escape quotes
    value = value.replace('"', '&quot;')
    return f'{name}="{value}"'


def format_html_attributes(attrs: dict) -> str:
    """
    Format HTML attributes dict
    
    Args:
        attrs: Attribute dictionary
        
    Returns:
        Formatted attributes string
        
    Example:
        >>> format_html_attributes({'id': 'main', 'class': 'active'})
        'id="main" class="active"'
    """
    return ' '.join(f'{k}="{v}"' for k, v in attrs.items())


def format_url_params(params: dict) -> str:
    """
    Format URL query parameters
    
    Args:
        params: Parameter dictionary
        
    Returns:
        URL-encoded query string
        
    Example:
        >>> format_url_params({'q': 'hello world', 'page': '1'})
        'q=hello+world&page=1'
    """
    from urllib.parse import urlencode
    return urlencode(params)


def format_markdown_link(text: str, url: str) -> str:
    """
    Format markdown link
    
    Args:
        text: Link text
        url: URL
        
    Returns:
        Markdown link
        
    Example:
        >>> format_markdown_link('Google', 'https://google.com')
        '[Google](https://google.com)'
    """
    return f"[{text}]({url})"


def format_markdown_image(alt_text: str, url: str) -> str:
    """
    Format markdown image
    
    Args:
        alt_text: Alt text
        url: Image URL
        
    Returns:
        Markdown image
        
    Example:
        >>> format_markdown_image('Logo', 'logo.png')
        '![Logo](logo.png)'
    """
    return f"![{alt_text}]({url})"


def format_sql_values(values: List) -> str:
    """
    Format values for SQL INSERT
    
    Args:
        values: List of values
        
    Returns:
        SQL values string
        
    Example:
        >>> format_sql_values(['Alice', 30, True])
        "('Alice', 30, 1)"
    """
    def format_value(v):
        if v is None:
            return 'NULL'
        elif isinstance(v, str):
            return f"'{v.replace(chr(39), chr(39)+chr(39))}'"  # Escape quotes
        elif isinstance(v, bool):
            return '1' if v else '0'
        else:
            return str(v)
    
    formatted = ', '.join(format_value(v) for v in values)
    return f"({formatted})"


# Export all functions
__all__ = [
    'format_number_with_commas', 'format_currency', 'format_percentage',
    'format_file_size', 'format_phone_number', 'format_credit_card', 'format_ssn',
    'truncate_string', 'pad_string', 'format_list', 'format_ordinal', 'format_pluralize',
    'camel_case_to_snake_case', 'snake_case_to_camel_case', 'title_case',
    'format_table_row', 'format_json_pretty',
    'format_xml_attribute', 'format_html_attributes', 'format_url_params',
    'format_markdown_link', 'format_markdown_image',
    'format_sql_values',
]
