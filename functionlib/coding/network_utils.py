"""
Network Utilities

Network operations, IP address manipulation, and HTTP utilities.
"""

import socket
import json
import re
from typing import Dict, List, Tuple, Optional
from urllib.parse import urlparse, parse_qs, urlencode, quote, unquote


def is_valid_ipv4(ip: str) -> bool:
    """
    Check if string is valid IPv4 address
    
    Args:
        ip: IP address string
        
    Returns:
        True if valid IPv4
        
    Example:
        >>> is_valid_ipv4("192.168.1.1")
        True
    """
    try:
        parts = ip.split('.')
        return len(parts) == 4 and all(0 <= int(part) <= 255 for part in parts)
    except (AttributeError, ValueError):
        return False


def is_valid_ipv6(ip: str) -> bool:
    """
    Check if string is valid IPv6 address
    
    Args:
        ip: IP address string
        
    Returns:
        True if valid IPv6
        
    Example:
        >>> is_valid_ipv6("2001:0db8:85a3::8a2e:0370:7334")
        True
    """
    try:
        socket.inet_pton(socket.AF_INET6, ip)
        return True
    except (socket.error, OSError):
        return False


def ip_to_int(ip: str) -> int:
    """
    Convert IPv4 to integer
    
    Args:
        ip: IPv4 address
        
    Returns:
        Integer representation
        
    Example:
        >>> ip_to_int("192.168.1.1")
        3232235777
    """
    parts = ip.split('.')
    return (int(parts[0]) << 24) + (int(parts[1]) << 16) + \
           (int(parts[2]) << 8) + int(parts[3])


def int_to_ip(num: int) -> str:
    """
    Convert integer to IPv4
    
    Args:
        num: Integer representation
        
    Returns:
        IPv4 address
        
    Example:
        >>> int_to_ip(3232235777)
        '192.168.1.1'
    """
    return f"{(num >> 24) & 255}.{(num >> 16) & 255}.{(num >> 8) & 255}.{num & 255}"


def is_private_ip(ip: str) -> bool:
    """
    Check if IP is private (RFC 1918)
    
    Args:
        ip: IPv4 address
        
    Returns:
        True if private
        
    Example:
        >>> is_private_ip("192.168.1.1")
        True
    """
    if not is_valid_ipv4(ip):
        return False
    
    parts = list(map(int, ip.split('.')))
    
    # 10.0.0.0/8
    if parts[0] == 10:
        return True
    
    # 172.16.0.0/12
    if parts[0] == 172 and 16 <= parts[1] <= 31:
        return True
    
    # 192.168.0.0/16
    if parts[0] == 192 and parts[1] == 168:
        return True
    
    return False


def cidr_to_netmask(cidr: int) -> str:
    """
    Convert CIDR notation to netmask
    
    Args:
        cidr: CIDR value (0-32)
        
    Returns:
        Netmask string
        
    Example:
        >>> cidr_to_netmask(24)
        '255.255.255.0'
    """
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
    return int_to_ip(mask)


def netmask_to_cidr(netmask: str) -> int:
    """
    Convert netmask to CIDR notation
    
    Args:
        netmask: Netmask string
        
    Returns:
        CIDR value
        
    Example:
        >>> netmask_to_cidr("255.255.255.0")
        24
    """
    return bin(ip_to_int(netmask)).count('1')


def ip_in_network(ip: str, network: str, cidr: int) -> bool:
    """
    Check if IP is in network
    
    Args:
        ip: IP address
        network: Network address
        cidr: CIDR notation
        
    Returns:
        True if IP in network
        
    Example:
        >>> ip_in_network("192.168.1.50", "192.168.1.0", 24)
        True
    """
    ip_int = ip_to_int(ip)
    network_int = ip_to_int(network)
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
    
    return (ip_int & mask) == (network_int & mask)


def get_network_address(ip: str, cidr: int) -> str:
    """
    Get network address from IP and CIDR
    
    Args:
        ip: IP address
        cidr: CIDR notation
        
    Returns:
        Network address
        
    Example:
        >>> get_network_address("192.168.1.50", 24)
        '192.168.1.0'
    """
    ip_int = ip_to_int(ip)
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
    return int_to_ip(ip_int & mask)


def get_broadcast_address(network: str, cidr: int) -> str:
    """
    Get broadcast address
    
    Args:
        network: Network address
        cidr: CIDR notation
        
    Returns:
        Broadcast address
        
    Example:
        >>> get_broadcast_address("192.168.1.0", 24)
        '192.168.1.255'
    """
    network_int = ip_to_int(network)
    mask = (0xffffffff >> (32 - cidr)) << (32 - cidr)
    broadcast = network_int | (~mask & 0xffffffff)
    return int_to_ip(broadcast)


def parse_url(url: str) -> Dict[str, str]:
    """
    Parse URL into components
    
    Args:
        url: URL string
        
    Returns:
        Dictionary with components
        
    Example:
        >>> result = parse_url("https://example.com:8080/path?key=value")
        >>> result['scheme']
        'https'
    """
    parsed = urlparse(url)
    return {
        'scheme': parsed.scheme,
        'netloc': parsed.netloc,
        'hostname': parsed.hostname or '',
        'port': parsed.port,
        'path': parsed.path,
        'query': parsed.query,
        'fragment': parsed.fragment,
    }


def build_url(scheme: str, host: str, path: str = '', params: Dict = None, 
              port: Optional[int] = None) -> str:
    """
    Build URL from components
    
    Args:
        scheme: Protocol (http, https)
        host: Hostname
        path: Path
        params: Query parameters
        port: Port number
        
    Returns:
        Complete URL
        
    Example:
        >>> build_url("https", "example.com", "/api", {"key": "value"})
        'https://example.com/api?key=value'
    """
    url = f"{scheme}://{host}"
    
    if port:
        url += f":{port}"
    
    if path:
        if not path.startswith('/'):
            path = '/' + path
        url += path
    
    if params:
        url += '?' + urlencode(params)
    
    return url


def parse_query_string(query: str) -> Dict[str, List[str]]:
    """
    Parse query string
    
    Args:
        query: Query string
        
    Returns:
        Dictionary of parameters
        
    Example:
        >>> parse_query_string("key=value&foo=bar")
        {'key': ['value'], 'foo': ['bar']}
    """
    return parse_qs(query)


def build_query_string(params: Dict) -> str:
    """
    Build query string from dictionary
    
    Args:
        params: Dictionary of parameters
        
    Returns:
        Query string
        
    Example:
        >>> build_query_string({"key": "value", "foo": "bar"})
        'key=value&foo=bar'
    """
    return urlencode(params)


def url_encode(text: str) -> str:
    """
    URL encode text
    
    Args:
        text: Text to encode
        
    Returns:
        URL-encoded text
        
    Example:
        >>> url_encode("hello world")
        'hello%20world'
    """
    return quote(text)


def url_decode(text: str) -> str:
    """
    URL decode text
    
    Args:
        text: Encoded text
        
    Returns:
        Decoded text
        
    Example:
        >>> url_decode("hello%20world")
        'hello world'
    """
    return unquote(text)


def extract_domain(url: str) -> str:
    """
    Extract domain from URL
    
    Args:
        url: URL string
        
    Returns:
        Domain name
        
    Example:
        >>> extract_domain("https://www.example.com/path")
        'example.com'
    """
    parsed = urlparse(url)
    domain = parsed.netloc or parsed.path
    
    # Remove www. prefix
    if domain.startswith('www.'):
        domain = domain[4:]
    
    # Remove port
    if ':' in domain:
        domain = domain.split(':')[0]
    
    return domain


def is_valid_port(port: int) -> bool:
    """
    Check if port number is valid
    
    Args:
        port: Port number
        
    Returns:
        True if valid
        
    Example:
        >>> is_valid_port(8080)
        True
    """
    return 0 <= port <= 65535


def get_url_parameters(url: str) -> Dict[str, List[str]]:
    """
    Extract query parameters from URL
    
    Args:
        url: URL string
        
    Returns:
        Dictionary of parameters
        
    Example:
        >>> get_url_parameters("https://example.com?key=value")
        {'key': ['value']}
    """
    parsed = urlparse(url)
    return parse_qs(parsed.query)


def add_url_parameters(url: str, params: Dict) -> str:
    """
    Add parameters to URL
    
    Args:
        url: Base URL
        params: Parameters to add
        
    Returns:
        URL with parameters
        
    Example:
        >>> add_url_parameters("https://example.com", {"key": "value"})
        'https://example.com?key=value'
    """
    separator = '&' if '?' in url else '?'
    return url + separator + urlencode(params)


def is_valid_hostname(hostname: str) -> bool:
    """
    Check if hostname is valid
    
    Args:
        hostname: Hostname
        
    Returns:
        True if valid
        
    Example:
        >>> is_valid_hostname("example.com")
        True
    """
    if len(hostname) > 255:
        return False
    
    pattern = re.compile(
        r'^(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)*'
        r'[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?$'
    )
    
    return bool(pattern.match(hostname))


def parse_user_agent(ua: str) -> Dict[str, str]:
    """
    Parse user agent string (simple)
    
    Args:
        ua: User agent string
        
    Returns:
        Dictionary with browser info
        
    Example:
        >>> result = parse_user_agent("Mozilla/5.0 (Windows NT 10.0)")
        >>> 'platform' in result
        True
    """
    result = {
        'browser': 'Unknown',
        'version': 'Unknown',
        'platform': 'Unknown'
    }
    
    # Detect browser
    if 'Firefox' in ua:
        result['browser'] = 'Firefox'
        match = re.search(r'Firefox/(\d+\.\d+)', ua)
        if match:
            result['version'] = match.group(1)
    elif 'Chrome' in ua:
        result['browser'] = 'Chrome'
        match = re.search(r'Chrome/(\d+\.\d+)', ua)
        if match:
            result['version'] = match.group(1)
    elif 'Safari' in ua and 'Chrome' not in ua:
        result['browser'] = 'Safari'
        match = re.search(r'Version/(\d+\.\d+)', ua)
        if match:
            result['version'] = match.group(1)
    
    # Detect platform
    if 'Windows' in ua:
        result['platform'] = 'Windows'
    elif 'Mac OS' in ua or 'Macintosh' in ua:
        result['platform'] = 'macOS'
    elif 'Linux' in ua:
        result['platform'] = 'Linux'
    elif 'Android' in ua:
        result['platform'] = 'Android'
    elif 'iPhone' in ua or 'iPad' in ua:
        result['platform'] = 'iOS'
    
    return result


def mac_address_format(mac: str, separator: str = ':') -> str:
    """
    Format MAC address with specified separator
    
    Args:
        mac: MAC address
        separator: Separator character
        
    Returns:
        Formatted MAC address
        
    Example:
        >>> mac_address_format("00:11:22:33:44:55", "-")
        '00-11-22-33-44-55'
    """
    # Remove existing separators
    mac_clean = re.sub(r'[:-]', '', mac)
    
    # Insert new separator every 2 characters
    return separator.join(mac_clean[i:i+2] for i in range(0, 12, 2))


def is_valid_mac(mac: str) -> bool:
    """
    Check if MAC address is valid
    
    Args:
        mac: MAC address
        
    Returns:
        True if valid
        
    Example:
        >>> is_valid_mac("00:11:22:33:44:55")
        True
    """
    pattern = re.compile(r'^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$')
    return bool(pattern.match(mac))


def calculate_subnet_size(cidr: int) -> int:
    """
    Calculate number of hosts in subnet
    
    Args:
        cidr: CIDR notation
        
    Returns:
        Number of usable hosts
        
    Example:
        >>> calculate_subnet_size(24)
        254
    """
    return (2 ** (32 - cidr)) - 2  # Subtract network and broadcast


def http_status_description(code: int) -> str:
    """
    Get HTTP status code description
    
    Args:
        code: HTTP status code
        
    Returns:
        Description
        
    Example:
        >>> http_status_description(200)
        'OK'
    """
    statuses = {
        200: 'OK',
        201: 'Created',
        204: 'No Content',
        301: 'Moved Permanently',
        302: 'Found',
        304: 'Not Modified',
        400: 'Bad Request',
        401: 'Unauthorized',
        403: 'Forbidden',
        404: 'Not Found',
        500: 'Internal Server Error',
        502: 'Bad Gateway',
        503: 'Service Unavailable',
    }
    
    return statuses.get(code, 'Unknown')


# Export all functions
__all__ = [
    'is_valid_ipv4', 'is_valid_ipv6', 'ip_to_int', 'int_to_ip',
    'is_private_ip', 'cidr_to_netmask', 'netmask_to_cidr',
    'ip_in_network', 'get_network_address', 'get_broadcast_address',
    'parse_url', 'build_url', 'parse_query_string', 'build_query_string',
    'url_encode', 'url_decode', 'extract_domain',
    'is_valid_port', 'get_url_parameters', 'add_url_parameters',
    'is_valid_hostname', 'parse_user_agent',
    'mac_address_format', 'is_valid_mac',
    'calculate_subnet_size', 'http_status_description',
]
