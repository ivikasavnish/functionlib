"""
File Operations

File and directory utilities for reading, writing, and manipulating files.
"""

import os
import json
import csv
import hashlib
from pathlib import Path
from typing import List, Dict, Any, Optional


def read_text_file(filepath: str, encoding: str = 'utf-8') -> str:
    """
    Read text file contents
    
    Args:
        filepath: Path to file
        encoding: Text encoding (default utf-8)
        
    Returns:
        File contents as string
        
    Example:
        >>> # read_text_file('example.txt')
        'File contents...'
    """
    with open(filepath, 'r', encoding=encoding) as f:
        return f.read()


def write_text_file(filepath: str, content: str, encoding: str = 'utf-8') -> None:
    """
    Write text to file
    
    Args:
        filepath: Path to file
        content: Text content to write
        encoding: Text encoding (default utf-8)
        
    Example:
        >>> # write_text_file('output.txt', 'Hello, world!')
    """
    with open(filepath, 'w', encoding=encoding) as f:
        f.write(content)


def append_text_file(filepath: str, content: str, encoding: str = 'utf-8') -> None:
    """
    Append text to file
    
    Args:
        filepath: Path to file
        content: Text content to append
        encoding: Text encoding (default utf-8)
        
    Example:
        >>> # append_text_file('log.txt', 'New entry\\n')
    """
    with open(filepath, 'a', encoding=encoding) as f:
        f.write(content)


def read_lines(filepath: str, encoding: str = 'utf-8') -> List[str]:
    """
    Read file as list of lines
    
    Args:
        filepath: Path to file
        encoding: Text encoding
        
    Returns:
        List of lines (with newlines stripped)
        
    Example:
        >>> # read_lines('data.txt')
        ['line1', 'line2', 'line3']
    """
    with open(filepath, 'r', encoding=encoding) as f:
        return [line.rstrip('\n') for line in f]


def write_lines(filepath: str, lines: List[str], encoding: str = 'utf-8') -> None:
    """
    Write list of lines to file
    
    Args:
        filepath: Path to file
        lines: List of lines to write
        encoding: Text encoding
        
    Example:
        >>> # write_lines('output.txt', ['line1', 'line2'])
    """
    with open(filepath, 'w', encoding=encoding) as f:
        for line in lines:
            f.write(line + '\n')


def read_json(filepath: str) -> Any:
    """
    Read JSON file
    
    Args:
        filepath: Path to JSON file
        
    Returns:
        Parsed JSON data
        
    Example:
        >>> # read_json('data.json')
        {'key': 'value'}
    """
    with open(filepath, 'r') as f:
        return json.load(f)


def write_json(filepath: str, data: Any, indent: int = 2) -> None:
    """
    Write data to JSON file
    
    Args:
        filepath: Path to JSON file
        data: Data to serialize
        indent: Indentation spaces
        
    Example:
        >>> # write_json('output.json', {'key': 'value'})
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def read_csv(filepath: str) -> List[List[str]]:
    """
    Read CSV file as list of rows
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        List of rows (each row is a list of values)
        
    Example:
        >>> # read_csv('data.csv')
        [['col1', 'col2'], ['val1', 'val2']]
    """
    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f)
        return list(reader)


def write_csv(filepath: str, rows: List[List[Any]]) -> None:
    """
    Write rows to CSV file
    
    Args:
        filepath: Path to CSV file
        rows: List of rows to write
        
    Example:
        >>> # write_csv('output.csv', [['a', 'b'], ['1', '2']])
    """
    with open(filepath, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)


def read_csv_dict(filepath: str) -> List[Dict[str, str]]:
    """
    Read CSV file as list of dictionaries
    
    Args:
        filepath: Path to CSV file
        
    Returns:
        List of dictionaries (keys from header row)
        
    Example:
        >>> # read_csv_dict('data.csv')
        [{'name': 'Alice', 'age': '30'}]
    """
    with open(filepath, 'r', newline='') as f:
        reader = csv.DictReader(f)
        return list(reader)


def write_csv_dict(filepath: str, data: List[Dict[str, Any]], fieldnames: Optional[List[str]] = None) -> None:
    """
    Write dictionaries to CSV file
    
    Args:
        filepath: Path to CSV file
        data: List of dictionaries
        fieldnames: Optional field order (uses keys from first dict if not provided)
        
    Example:
        >>> # write_csv_dict('output.csv', [{'name': 'Alice', 'age': 30}])
    """
    if not data:
        return
    
    if fieldnames is None:
        fieldnames = list(data[0].keys())
    
    with open(filepath, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def file_exists(filepath: str) -> bool:
    """
    Check if file exists
    
    Args:
        filepath: Path to file
        
    Returns:
        True if file exists
        
    Example:
        >>> file_exists('/etc/hosts')
        True
    """
    return os.path.isfile(filepath)


def directory_exists(dirpath: str) -> bool:
    """
    Check if directory exists
    
    Args:
        dirpath: Path to directory
        
    Returns:
        True if directory exists
        
    Example:
        >>> directory_exists('/tmp')
        True
    """
    return os.path.isdir(dirpath)


def create_directory(dirpath: str, exist_ok: bool = True) -> None:
    """
    Create directory (and parents if needed)
    
    Args:
        dirpath: Path to directory
        exist_ok: Don't raise error if directory exists
        
    Example:
        >>> # create_directory('/tmp/mydir')
    """
    os.makedirs(dirpath, exist_ok=exist_ok)


def delete_file(filepath: str) -> None:
    """
    Delete file
    
    Args:
        filepath: Path to file
        
    Example:
        >>> # delete_file('/tmp/tempfile.txt')
    """
    os.remove(filepath)


def delete_directory(dirpath: str) -> None:
    """
    Delete empty directory
    
    Args:
        dirpath: Path to directory
        
    Example:
        >>> # delete_directory('/tmp/emptydir')
    """
    os.rmdir(dirpath)


def copy_file(src: str, dst: str) -> None:
    """
    Copy file
    
    Args:
        src: Source file path
        dst: Destination file path
        
    Example:
        >>> # copy_file('file.txt', 'backup.txt')
    """
    import shutil
    shutil.copy2(src, dst)


def move_file(src: str, dst: str) -> None:
    """
    Move/rename file
    
    Args:
        src: Source file path
        dst: Destination file path
        
    Example:
        >>> # move_file('old.txt', 'new.txt')
    """
    import shutil
    shutil.move(src, dst)


def get_file_size(filepath: str) -> int:
    """
    Get file size in bytes
    
    Args:
        filepath: Path to file
        
    Returns:
        File size in bytes
        
    Example:
        >>> get_file_size('/etc/hosts') > 0
        True
    """
    return os.path.getsize(filepath)


def get_file_extension(filepath: str) -> str:
    """
    Get file extension
    
    Args:
        filepath: Path to file
        
    Returns:
        File extension (with dot)
        
    Example:
        >>> get_file_extension('document.pdf')
        '.pdf'
    """
    return os.path.splitext(filepath)[1]


def get_filename(filepath: str) -> str:
    """
    Get filename without directory
    
    Args:
        filepath: Path to file
        
    Returns:
        Filename
        
    Example:
        >>> get_filename('/path/to/file.txt')
        'file.txt'
    """
    return os.path.basename(filepath)


def get_directory(filepath: str) -> str:
    """
    Get directory path from filepath
    
    Args:
        filepath: Path to file
        
    Returns:
        Directory path
        
    Example:
        >>> get_directory('/path/to/file.txt')
        '/path/to'
    """
    return os.path.dirname(filepath)


def list_files(dirpath: str, pattern: str = '*') -> List[str]:
    """
    List files in directory
    
    Args:
        dirpath: Directory path
        pattern: Glob pattern (default '*')
        
    Returns:
        List of file paths
        
    Example:
        >>> # list_files('/tmp', '*.txt')
        ['/tmp/file1.txt', '/tmp/file2.txt']
    """
    path = Path(dirpath)
    return [str(p) for p in path.glob(pattern) if p.is_file()]


def list_directories(dirpath: str) -> List[str]:
    """
    List subdirectories
    
    Args:
        dirpath: Directory path
        
    Returns:
        List of directory paths
        
    Example:
        >>> # list_directories('/tmp')
        ['/tmp/dir1', '/tmp/dir2']
    """
    path = Path(dirpath)
    return [str(p) for p in path.iterdir() if p.is_dir()]


def file_hash_md5(filepath: str) -> str:
    """
    Calculate MD5 hash of file
    
    Args:
        filepath: Path to file
        
    Returns:
        MD5 hash (hex)
        
    Example:
        >>> # file_hash_md5('file.txt')
        'abc123...'
    """
    hash_md5 = hashlib.md5()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def file_hash_sha256(filepath: str) -> str:
    """
    Calculate SHA256 hash of file
    
    Args:
        filepath: Path to file
        
    Returns:
        SHA256 hash (hex)
        
    Example:
        >>> # file_hash_sha256('file.txt')
        'def456...'
    """
    hash_sha256 = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_sha256.update(chunk)
    return hash_sha256.hexdigest()


def join_paths(*paths: str) -> str:
    """
    Join path components
    
    Args:
        *paths: Path components
        
    Returns:
        Joined path
        
    Example:
        >>> join_paths('/home', 'user', 'file.txt')
        '/home/user/file.txt'
    """
    return os.path.join(*paths)


def absolute_path(filepath: str) -> str:
    """
    Get absolute path
    
    Args:
        filepath: Relative or absolute path
        
    Returns:
        Absolute path
        
    Example:
        >>> absolute_path('file.txt').endswith('file.txt')
        True
    """
    return os.path.abspath(filepath)


def normalize_path(filepath: str) -> str:
    """
    Normalize path (resolve .. and .)
    
    Args:
        filepath: Path to normalize
        
    Returns:
        Normalized path
        
    Example:
        >>> normalize_path('/a/b/../c')
        '/a/c'
    """
    return os.path.normpath(filepath)


# Export all functions
__all__ = [
    'read_text_file', 'write_text_file', 'append_text_file',
    'read_lines', 'write_lines',
    'read_json', 'write_json',
    'read_csv', 'write_csv', 'read_csv_dict', 'write_csv_dict',
    'file_exists', 'directory_exists',
    'create_directory', 'delete_file', 'delete_directory',
    'copy_file', 'move_file',
    'get_file_size', 'get_file_extension', 'get_filename', 'get_directory',
    'list_files', 'list_directories',
    'file_hash_md5', 'file_hash_sha256',
    'join_paths', 'absolute_path', 'normalize_path',
]
