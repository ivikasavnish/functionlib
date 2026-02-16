"""
Data Processing Functions

Compression, serialization, and data transformation utilities.
"""

import gzip
import zlib
import bz2
import base64
import pickle
import csv
import json
import io
from typing import Any, List, Dict, Optional, Union
import hashlib
import struct

__all__ = [
    # Compression
    'gzip_compress', 'gzip_decompress', 'zlib_compress', 'zlib_decompress',
    'bz2_compress', 'bz2_decompress', 'compress_string', 'decompress_string',
    
    # Encoding
    'base64_encode', 'base64_decode', 'hex_encode', 'hex_decode',
    'url_safe_base64_encode', 'url_safe_base64_decode',
    
    # Serialization
    'serialize_object', 'deserialize_object', 'to_json_string', 'from_json_string',
    
    # CSV Processing
    'csv_to_dict_list', 'dict_list_to_csv', 'csv_to_rows', 'rows_to_csv',
    
    # Binary Data
    'pack_integers', 'unpack_integers', 'bytes_to_hex', 'hex_to_bytes',
    'calculate_checksum', 'verify_checksum',
    
    # Data Transformation
    'flatten_dict', 'unflatten_dict', 'merge_dicts', 'deep_copy_dict'
]

# ============================================================================
# COMPRESSION FUNCTIONS
# ============================================================================

def gzip_compress(data: bytes, compression_level: int = 9) -> bytes:
    """
    Compress data using gzip compression.
    
    Args:
        data: Bytes to compress
        compression_level: Compression level (0-9, higher = better compression)
        
    Returns:
        Compressed bytes
        
    Example:
        >>> data = b"Hello, World!" * 100
        >>> compressed = gzip_compress(data)
        >>> len(compressed) < len(data)
        True
    """
    return gzip.compress(data, compresslevel=compression_level)


def gzip_decompress(data: bytes) -> bytes:
    """
    Decompress gzip-compressed data.
    
    Args:
        data: Gzip-compressed bytes
        
    Returns:
        Decompressed bytes
        
    Example:
        >>> data = b"Hello, World!"
        >>> compressed = gzip_compress(data)
        >>> gzip_decompress(compressed) == data
        True
    """
    return gzip.decompress(data)


def zlib_compress(data: bytes, level: int = 9) -> bytes:
    """
    Compress data using zlib compression.
    
    Args:
        data: Bytes to compress
        level: Compression level (0-9)
        
    Returns:
        Compressed bytes
        
    Example:
        >>> data = b"Test data" * 50
        >>> compressed = zlib_compress(data)
        >>> len(compressed) < len(data)
        True
    """
    return zlib.compress(data, level=level)


def zlib_decompress(data: bytes) -> bytes:
    """
    Decompress zlib-compressed data.
    
    Args:
        data: Zlib-compressed bytes
        
    Returns:
        Decompressed bytes
        
    Example:
        >>> data = b"Test data"
        >>> compressed = zlib_compress(data)
        >>> zlib_decompress(compressed) == data
        True
    """
    return zlib.decompress(data)


def bz2_compress(data: bytes, compression_level: int = 9) -> bytes:
    """
    Compress data using bz2 compression.
    
    Args:
        data: Bytes to compress
        compression_level: Compression level (1-9)
        
    Returns:
        Compressed bytes
        
    Example:
        >>> data = b"Sample text" * 100
        >>> compressed = bz2_compress(data)
        >>> len(compressed) < len(data)
        True
    """
    return bz2.compress(data, compresslevel=compression_level)


def bz2_decompress(data: bytes) -> bytes:
    """
    Decompress bz2-compressed data.
    
    Args:
        data: Bz2-compressed bytes
        
    Returns:
        Decompressed bytes
        
    Example:
        >>> data = b"Sample text"
        >>> compressed = bz2_compress(data)
        >>> bz2_decompress(compressed) == data
        True
    """
    return bz2.decompress(data)


def compress_string(text: str, method: str = 'gzip') -> bytes:
    """
    Compress a string using specified method.
    
    Args:
        text: String to compress
        method: Compression method ('gzip', 'zlib', or 'bz2')
        
    Returns:
        Compressed bytes
        
    Example:
        >>> text = "Hello, World!" * 100
        >>> compressed = compress_string(text)
        >>> len(compressed) < len(text.encode())
        True
    """
    data = text.encode('utf-8')
    
    if method == 'gzip':
        return gzip_compress(data)
    elif method == 'zlib':
        return zlib_compress(data)
    elif method == 'bz2':
        return bz2_compress(data)
    else:
        raise ValueError(f"Unknown compression method: {method}")


def decompress_string(data: bytes, method: str = 'gzip') -> str:
    """
    Decompress bytes to string.
    
    Args:
        data: Compressed bytes
        method: Compression method used ('gzip', 'zlib', or 'bz2')
        
    Returns:
        Decompressed string
        
    Example:
        >>> text = "Hello, World!"
        >>> compressed = compress_string(text)
        >>> decompress_string(compressed) == text
        True
    """
    if method == 'gzip':
        decompressed = gzip_decompress(data)
    elif method == 'zlib':
        decompressed = zlib_decompress(data)
    elif method == 'bz2':
        decompressed = bz2_decompress(data)
    else:
        raise ValueError(f"Unknown compression method: {method}")
    
    return decompressed.decode('utf-8')


# ============================================================================
# ENCODING FUNCTIONS
# ============================================================================

def base64_encode(data: bytes) -> str:
    """
    Encode bytes to base64 string.
    
    Args:
        data: Bytes to encode
        
    Returns:
        Base64-encoded string
        
    Example:
        >>> data = b"Hello, World!"
        >>> encoded = base64_encode(data)
        >>> encoded
        'SGVsbG8sIFdvcmxkIQ=='
    """
    return base64.b64encode(data).decode('ascii')


def base64_decode(encoded: str) -> bytes:
    """
    Decode base64 string to bytes.
    
    Args:
        encoded: Base64-encoded string
        
    Returns:
        Decoded bytes
        
    Example:
        >>> encoded = 'SGVsbG8sIFdvcmxkIQ=='
        >>> base64_decode(encoded)
        b'Hello, World!'
    """
    return base64.b64decode(encoded)


def hex_encode(data: bytes) -> str:
    """
    Encode bytes to hexadecimal string.
    
    Args:
        data: Bytes to encode
        
    Returns:
        Hex string
        
    Example:
        >>> data = b"Hello"
        >>> hex_encode(data)
        '48656c6c6f'
    """
    return data.hex()


def hex_decode(hex_string: str) -> bytes:
    """
    Decode hexadecimal string to bytes.
    
    Args:
        hex_string: Hex string to decode
        
    Returns:
        Decoded bytes
        
    Example:
        >>> hex_decode('48656c6c6f')
        b'Hello'
    """
    return bytes.fromhex(hex_string)


def url_safe_base64_encode(data: bytes) -> str:
    """
    Encode bytes to URL-safe base64 string.
    
    Args:
        data: Bytes to encode
        
    Returns:
        URL-safe base64 string
        
    Example:
        >>> data = b"Hello>>World"
        >>> encoded = url_safe_base64_encode(data)
        >>> '/' not in encoded and '+' not in encoded
        True
    """
    return base64.urlsafe_b64encode(data).decode('ascii')


def url_safe_base64_decode(encoded: str) -> bytes:
    """
    Decode URL-safe base64 string to bytes.
    
    Args:
        encoded: URL-safe base64 string
        
    Returns:
        Decoded bytes
        
    Example:
        >>> data = b"Test data"
        >>> encoded = url_safe_base64_encode(data)
        >>> url_safe_base64_decode(encoded) == data
        True
    """
    return base64.urlsafe_b64decode(encoded)


# ============================================================================
# SERIALIZATION FUNCTIONS
# ============================================================================

def serialize_object(obj: Any) -> bytes:
    """
    Serialize Python object to bytes using pickle.
    
    Args:
        obj: Object to serialize
        
    Returns:
        Serialized bytes
        
    Example:
        >>> data = {'key': 'value', 'numbers': [1, 2, 3]}
        >>> serialized = serialize_object(data)
        >>> isinstance(serialized, bytes)
        True
    """
    return pickle.dumps(obj)


def deserialize_object(data: bytes) -> Any:
    """
    Deserialize bytes to Python object using pickle.
    
    Args:
        data: Serialized bytes
        
    Returns:
        Deserialized object
        
    Example:
        >>> obj = {'key': 'value', 'numbers': [1, 2, 3]}
        >>> serialized = serialize_object(obj)
        >>> deserialize_object(serialized) == obj
        True
    """
    return pickle.loads(data)


def to_json_string(obj: Any, pretty: bool = False) -> str:
    """
    Convert object to JSON string.
    
    Args:
        obj: Object to serialize
        pretty: If True, format with indentation
        
    Returns:
        JSON string
        
    Example:
        >>> data = {'name': 'John', 'age': 30}
        >>> json_str = to_json_string(data)
        >>> '{"name": "John"' in json_str or '{"age": 30' in json_str
        True
    """
    if pretty:
        return json.dumps(obj, indent=2, sort_keys=True)
    return json.dumps(obj)


def from_json_string(json_str: str) -> Any:
    """
    Parse JSON string to Python object.
    
    Args:
        json_str: JSON string
        
    Returns:
        Parsed object
        
    Example:
        >>> json_str = '{"name": "John", "age": 30}'
        >>> obj = from_json_string(json_str)
        >>> obj['name']
        'John'
    """
    return json.loads(json_str)


# ============================================================================
# CSV PROCESSING FUNCTIONS
# ============================================================================

def csv_to_dict_list(csv_string: str, delimiter: str = ',') -> List[Dict[str, str]]:
    """
    Parse CSV string to list of dictionaries.
    
    Args:
        csv_string: CSV data as string
        delimiter: Field delimiter
        
    Returns:
        List of dictionaries (one per row)
        
    Example:
        >>> csv = "name,age\\nJohn,30\\nJane,25"
        >>> result = csv_to_dict_list(csv)
        >>> result[0]['name']
        'John'
    """
    reader = csv.DictReader(io.StringIO(csv_string), delimiter=delimiter)
    return list(reader)


def dict_list_to_csv(data: List[Dict[str, Any]], delimiter: str = ',') -> str:
    """
    Convert list of dictionaries to CSV string.
    
    Args:
        data: List of dictionaries
        delimiter: Field delimiter
        
    Returns:
        CSV string
        
    Example:
        >>> data = [{'name': 'John', 'age': 30}, {'name': 'Jane', 'age': 25}]
        >>> csv_str = dict_list_to_csv(data)
        >>> 'name' in csv_str and 'John' in csv_str
        True
    """
    if not data:
        return ""
    
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=data[0].keys(), delimiter=delimiter)
    writer.writeheader()
    writer.writerows(data)
    return output.getvalue()


def csv_to_rows(csv_string: str, delimiter: str = ',') -> List[List[str]]:
    """
    Parse CSV string to list of rows.
    
    Args:
        csv_string: CSV data as string
        delimiter: Field delimiter
        
    Returns:
        List of rows (each row is a list)
        
    Example:
        >>> csv = "a,b,c\\n1,2,3\\n4,5,6"
        >>> rows = csv_to_rows(csv)
        >>> rows[1]
        ['1', '2', '3']
    """
    reader = csv.reader(io.StringIO(csv_string), delimiter=delimiter)
    return list(reader)


def rows_to_csv(rows: List[List[Any]], delimiter: str = ',') -> str:
    """
    Convert list of rows to CSV string.
    
    Args:
        rows: List of rows (each row is a list)
        delimiter: Field delimiter
        
    Returns:
        CSV string
        
    Example:
        >>> rows = [['a', 'b'], ['1', '2'], ['3', '4']]
        >>> csv_str = rows_to_csv(rows)
        >>> 'a,b' in csv_str
        True
    """
    output = io.StringIO()
    writer = csv.writer(output, delimiter=delimiter)
    writer.writerows(rows)
    return output.getvalue()


# ============================================================================
# BINARY DATA FUNCTIONS
# ============================================================================

def pack_integers(integers: List[int], format_char: str = 'i') -> bytes:
    """
    Pack list of integers into binary format.
    
    Args:
        integers: List of integers
        format_char: Struct format character ('i'=int, 'h'=short, 'q'=long long)
        
    Returns:
        Packed bytes
        
    Example:
        >>> nums = [1, 2, 3, 4]
        >>> packed = pack_integers(nums)
        >>> len(packed)
        16
    """
    format_string = f'{len(integers)}{format_char}'
    return struct.pack(format_string, *integers)


def unpack_integers(data: bytes, format_char: str = 'i') -> List[int]:
    """
    Unpack binary data to list of integers.
    
    Args:
        data: Packed bytes
        format_char: Struct format character
        
    Returns:
        List of integers
        
    Example:
        >>> nums = [1, 2, 3, 4]
        >>> packed = pack_integers(nums)
        >>> unpack_integers(packed) == nums
        True
    """
    item_size = struct.calcsize(format_char)
    count = len(data) // item_size
    format_string = f'{count}{format_char}'
    return list(struct.unpack(format_string, data))


def bytes_to_hex(data: bytes, separator: str = '') -> str:
    """
    Convert bytes to hex string with optional separator.
    
    Args:
        data: Bytes to convert
        separator: Optional separator between hex pairs
        
    Returns:
        Hex string
        
    Example:
        >>> data = b"\\x01\\x02\\x03"
        >>> bytes_to_hex(data)
        '010203'
        >>> bytes_to_hex(data, ':')
        '01:02:03'
    """
    hex_str = data.hex()
    if separator:
        return separator.join(hex_str[i:i+2] for i in range(0, len(hex_str), 2))
    return hex_str


def hex_to_bytes(hex_string: str) -> bytes:
    """
    Convert hex string to bytes (handles separators).
    
    Args:
        hex_string: Hex string (may contain separators)
        
    Returns:
        Bytes
        
    Example:
        >>> hex_to_bytes('010203')
        b'\\x01\\x02\\x03'
        >>> hex_to_bytes('01:02:03')
        b'\\x01\\x02\\x03'
    """
    # Remove common separators
    clean = hex_string.replace(':', '').replace('-', '').replace(' ', '')
    return bytes.fromhex(clean)


def calculate_checksum(data: bytes, algorithm: str = 'md5') -> str:
    """
    Calculate checksum of data.
    
    Args:
        data: Data to checksum
        algorithm: Hash algorithm ('md5', 'sha1', 'sha256')
        
    Returns:
        Hex digest string
        
    Example:
        >>> data = b"Hello, World!"
        >>> checksum = calculate_checksum(data, 'md5')
        >>> len(checksum)
        32
    """
    hash_obj = hashlib.new(algorithm)
    hash_obj.update(data)
    return hash_obj.hexdigest()


def verify_checksum(data: bytes, expected: str, algorithm: str = 'md5') -> bool:
    """
    Verify data checksum.
    
    Args:
        data: Data to verify
        expected: Expected checksum
        algorithm: Hash algorithm
        
    Returns:
        True if checksum matches
        
    Example:
        >>> data = b"Test data"
        >>> checksum = calculate_checksum(data)
        >>> verify_checksum(data, checksum)
        True
    """
    actual = calculate_checksum(data, algorithm)
    return actual.lower() == expected.lower()


# ============================================================================
# DATA TRANSFORMATION FUNCTIONS
# ============================================================================

def flatten_dict(nested_dict: Dict, separator: str = '.') -> Dict:
    """
    Flatten nested dictionary to single level.
    
    Args:
        nested_dict: Nested dictionary
        separator: Key separator for nested keys
        
    Returns:
        Flattened dictionary
        
    Example:
        >>> nested = {'a': {'b': {'c': 1}}}
        >>> flatten_dict(nested)
        {'a.b.c': 1}
    """
    def _flatten(d: Dict, parent_key: str = '') -> Dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{separator}{k}" if parent_key else k
            if isinstance(v, dict):
                items.extend(_flatten(v, new_key).items())
            else:
                items.append((new_key, v))
        return dict(items)
    
    return _flatten(nested_dict)


def unflatten_dict(flat_dict: Dict, separator: str = '.') -> Dict:
    """
    Unflatten dictionary to nested structure.
    
    Args:
        flat_dict: Flattened dictionary
        separator: Key separator
        
    Returns:
        Nested dictionary
        
    Example:
        >>> flat = {'a.b.c': 1, 'a.b.d': 2}
        >>> result = unflatten_dict(flat)
        >>> result['a']['b']['c']
        1
    """
    result = {}
    for key, value in flat_dict.items():
        parts = key.split(separator)
        current = result
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]
        current[parts[-1]] = value
    return result


def merge_dicts(*dicts: Dict, deep: bool = False) -> Dict:
    """
    Merge multiple dictionaries.
    
    Args:
        *dicts: Dictionaries to merge
        deep: If True, recursively merge nested dicts
        
    Returns:
        Merged dictionary
        
    Example:
        >>> d1 = {'a': 1, 'b': 2}
        >>> d2 = {'b': 3, 'c': 4}
        >>> merge_dicts(d1, d2)
        {'a': 1, 'b': 3, 'c': 4}
    """
    if not deep:
        result = {}
        for d in dicts:
            result.update(d)
        return result
    
    def _deep_merge(d1: Dict, d2: Dict) -> Dict:
        result = d1.copy()
        for key, value in d2.items():
            if key in result and isinstance(result[key], dict) and isinstance(value, dict):
                result[key] = _deep_merge(result[key], value)
            else:
                result[key] = value
        return result
    
    result = {}
    for d in dicts:
        result = _deep_merge(result, d)
    return result


def deep_copy_dict(d: Dict) -> Dict:
    """
    Create deep copy of dictionary.
    
    Args:
        d: Dictionary to copy
        
    Returns:
        Deep copy
        
    Example:
        >>> original = {'a': [1, 2, 3]}
        >>> copy = deep_copy_dict(original)
        >>> copy['a'].append(4)
        >>> len(original['a'])
        3
    """
    return pickle.loads(pickle.dumps(d))
