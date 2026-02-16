"""
Cryptography Functions

Basic cryptographic operations including hashing, encryption, and encoding.
"""

import hashlib
import base64
import secrets
import string
from typing import Tuple, Optional


def generate_random_key(length: int = 32) -> str:
    """
    Generates cryptographically secure random key
    
    Args:
        length: Key length in bytes
        
    Returns:
        Hex-encoded key
        
    Example:
        >>> key = generate_random_key(16)
        >>> len(key)
        32
    """
    return secrets.token_hex(length)


def generate_random_bytes(length: int = 32) -> bytes:
    """
    Generates cryptographically secure random bytes
    
    Args:
        length: Number of bytes
        
    Returns:
        Random bytes
        
    Example:
        >>> data = generate_random_bytes(16)
        >>> len(data)
        16
    """
    return secrets.token_bytes(length)


def generate_password(length: int = 16, include_special: bool = True) -> str:
    """
    Generates secure random password
    
    Args:
        length: Password length
        include_special: Include special characters
        
    Returns:
        Random password
        
    Example:
        >>> pwd = generate_password(12)
        >>> len(pwd)
        12
    """
    chars = string.ascii_letters + string.digits
    
    if include_special:
        chars += string.punctuation
    
    return ''.join(secrets.choice(chars) for _ in range(length))


def hash_sha256(data: str) -> str:
    """
    Computes SHA-256 hash
    
    Args:
        data: Data to hash
        
    Returns:
        Hex digest
        
    Example:
        >>> hash_sha256("hello")
        '2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824'
    """
    return hashlib.sha256(data.encode()).hexdigest()


def hash_sha512(data: str) -> str:
    """
    Computes SHA-512 hash
    
    Args:
        data: Data to hash
        
    Returns:
        Hex digest
        
    Example:
        >>> len(hash_sha512("hello"))
        128
    """
    return hashlib.sha512(data.encode()).hexdigest()


def hash_md5(data: str) -> str:
    """
    Computes MD5 hash (not for security, legacy only)
    
    Args:
        data: Data to hash
        
    Returns:
        Hex digest
        
    Example:
        >>> hash_md5("hello")
        '5d41402abc4b2a76b9719d911017c592'
    """
    return hashlib.md5(data.encode()).hexdigest()


def hash_blake2b(data: str) -> str:
    """
    Computes BLAKE2b hash
    
    Args:
        data: Data to hash
        
    Returns:
        Hex digest
        
    Example:
        >>> len(hash_blake2b("hello"))
        128
    """
    return hashlib.blake2b(data.encode()).hexdigest()


def hmac_sha256(message: str, key: str) -> str:
    """
    Computes HMAC-SHA256
    
    Args:
        message: Message to authenticate
        key: Secret key
        
    Returns:
        HMAC hex digest
        
    Example:
        >>> hmac = hmac_sha256("message", "secret")
        >>> len(hmac)
        64
    """
    import hmac as hmac_lib
    return hmac_lib.new(key.encode(), message.encode(), hashlib.sha256).hexdigest()


def caesar_cipher_encrypt(text: str, shift: int) -> str:
    """
    Encrypts text using Caesar cipher
    
    Args:
        text: Plain text
        shift: Shift amount
        
    Returns:
        Encrypted text
        
    Example:
        >>> caesar_cipher_encrypt("HELLO", 3)
        'KHOOR'
    """
    result = []
    
    for char in text:
        if char.isalpha():
            ascii_offset = 65 if char.isupper() else 97
            shifted = (ord(char) - ascii_offset + shift) % 26 + ascii_offset
            result.append(chr(shifted))
        else:
            result.append(char)
    
    return ''.join(result)


def caesar_cipher_decrypt(text: str, shift: int) -> str:
    """
    Decrypts Caesar cipher
    
    Args:
        text: Encrypted text
        shift: Shift amount
        
    Returns:
        Decrypted text
        
    Example:
        >>> caesar_cipher_decrypt("KHOOR", 3)
        'HELLO'
    """
    return caesar_cipher_encrypt(text, -shift)


def xor_encrypt(data: str, key: str) -> str:
    """
    XOR encryption (simple, educational)
    
    Args:
        data: Data to encrypt
        key: Encryption key
        
    Returns:
        Base64-encoded ciphertext
        
    Example:
        >>> cipher = xor_encrypt("hello", "key")
        >>> isinstance(cipher, str)
        True
    """
    if not key:
        raise ValueError("Key cannot be empty")
    
    encrypted = []
    for i, char in enumerate(data):
        key_char = key[i % len(key)]
        encrypted.append(chr(ord(char) ^ ord(key_char)))
    
    return base64.b64encode(''.join(encrypted).encode()).decode()


def xor_decrypt(ciphertext: str, key: str) -> str:
    """
    XOR decryption
    
    Args:
        ciphertext: Base64-encoded ciphertext
        key: Decryption key
        
    Returns:
        Decrypted data
        
    Example:
        >>> cipher = xor_encrypt("hello", "key")
        >>> xor_decrypt(cipher, "key")
        'hello'
    """
    decoded = base64.b64decode(ciphertext).decode()
    return xor_encrypt(decoded, key)  # XOR is symmetric


def rot13(text: str) -> str:
    """
    ROT13 encoding (Caesar cipher with shift 13)
    
    Args:
        text: Text to encode/decode
        
    Returns:
        ROT13 text
        
    Example:
        >>> rot13("HELLO")
        'URYYB'
        >>> rot13(rot13("HELLO"))
        'HELLO'
    """
    return caesar_cipher_encrypt(text, 13)


def atbash_cipher(text: str) -> str:
    """
    Atbash cipher (A↔Z, B↔Y, etc.)
    
    Args:
        text: Text to encode/decode
        
    Returns:
        Atbash text
        
    Example:
        >>> atbash_cipher("ABC")
        'ZYX'
    """
    result = []
    
    for char in text:
        if char.isalpha():
            if char.isupper():
                result.append(chr(90 - (ord(char) - 65)))
            else:
                result.append(chr(122 - (ord(char) - 97)))
        else:
            result.append(char)
    
    return ''.join(result)


def vigenere_encrypt(plaintext: str, key: str) -> str:
    """
    Vigenère cipher encryption
    
    Args:
        plaintext: Text to encrypt
        key: Encryption key
        
    Returns:
        Encrypted text
        
    Example:
        >>> vigenere_encrypt("HELLO", "KEY")
        'RIJVS'
    """
    key = key.upper()
    result = []
    key_index = 0
    
    for char in plaintext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            
            if char.isupper():
                result.append(chr((ord(char) - 65 + shift) % 26 + 65))
            else:
                result.append(chr((ord(char) - 97 + shift) % 26 + 97))
            
            key_index += 1
        else:
            result.append(char)
    
    return ''.join(result)


def vigenere_decrypt(ciphertext: str, key: str) -> str:
    """
    Vigenère cipher decryption
    
    Args:
        ciphertext: Encrypted text
        key: Decryption key
        
    Returns:
        Decrypted text
        
    Example:
        >>> vigenere_decrypt("RIJVS", "KEY")
        'HELLO'
    """
    key = key.upper()
    result = []
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - 65
            
            if char.isupper():
                result.append(chr((ord(char) - 65 - shift) % 26 + 65))
            else:
                result.append(chr((ord(char) - 97 - shift) % 26 + 97))
            
            key_index += 1
        else:
            result.append(char)
    
    return ''.join(result)


def hex_encode(data: str) -> str:
    """
    Encodes string to hexadecimal
    
    Args:
        data: Data to encode
        
    Returns:
        Hex string
        
    Example:
        >>> hex_encode("hello")
        '68656c6c6f'
    """
    return data.encode().hex()


def hex_decode(hex_string: str) -> str:
    """
    Decodes hexadecimal to string
    
    Args:
        hex_string: Hex string
        
    Returns:
        Decoded string
        
    Example:
        >>> hex_decode("68656c6c6f")
        'hello'
    """
    return bytes.fromhex(hex_string).decode()


def base32_encode(data: str) -> str:
    """
    Base32 encoding
    
    Args:
        data: Data to encode
        
    Returns:
        Base32 string
        
    Example:
        >>> base32_encode("hello")
        'NBSWY3DP'
    """
    return base64.b32encode(data.encode()).decode().rstrip('=')


def base32_decode(encoded: str) -> str:
    """
    Base32 decoding
    
    Args:
        encoded: Base32 string
        
    Returns:
        Decoded string
        
    Example:
        >>> base32_decode("NBSWY3DP")
        'hello'
    """
    # Add padding if needed
    padding = (8 - len(encoded) % 8) % 8
    encoded += '=' * padding
    
    return base64.b32decode(encoded).decode()


def generate_uuid() -> str:
    """
    Generates UUID v4
    
    Returns:
        UUID string
        
    Example:
        >>> uuid = generate_uuid()
        >>> len(uuid)
        36
    """
    import uuid
    return str(uuid.uuid4())


def checksum_simple(data: str) -> int:
    """
    Simple checksum (sum of byte values)
    
    Args:
        data: Data to checksum
        
    Returns:
        Checksum value
        
    Example:
        >>> checksum_simple("hello")
        532
    """
    return sum(ord(char) for char in data)


def luhn_checksum(number: str) -> int:
    """
    Computes Luhn checksum digit
    
    Args:
        number: Number string (without check digit)
        
    Returns:
        Check digit
        
    Example:
        >>> luhn_checksum("7992739871")
        3
    """
    digits = [int(d) for d in number]
    checksum = 0
    
    for i in range(len(digits) - 1, -1, -1):
        d = digits[i]
        
        if (len(digits) - i) % 2 == 0:
            d = d * 2
            if d > 9:
                d = d - 9
        
        checksum += d
    
    return (10 - (checksum % 10)) % 10


def verify_luhn(number: str) -> bool:
    """
    Verifies Luhn checksum
    
    Args:
        number: Number with check digit
        
    Returns:
        True if valid
        
    Example:
        >>> verify_luhn("79927398713")
        True
    """
    expected = luhn_checksum(number[:-1])
    return int(number[-1]) == expected


# Export all functions
__all__ = [
    'generate_random_key', 'generate_random_bytes', 'generate_password',
    'hash_sha256', 'hash_sha512', 'hash_md5', 'hash_blake2b',
    'hmac_sha256',
    'caesar_cipher_encrypt', 'caesar_cipher_decrypt',
    'xor_encrypt', 'xor_decrypt',
    'rot13', 'atbash_cipher',
    'vigenere_encrypt', 'vigenere_decrypt',
    'hex_encode', 'hex_decode',
    'base32_encode', 'base32_decode',
    'generate_uuid', 'checksum_simple', 'luhn_checksum', 'verify_luhn',
]
