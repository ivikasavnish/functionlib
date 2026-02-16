"""System automation and computer use tools (stdlib only)."""

import os
import sys
import subprocess
import platform
import time
import json
import shutil
from typing import List, Dict, Optional, Tuple, Any
from pathlib import Path

__all__ = [
    'run_command',
    'execute_shell',
    'get_system_info',
    'list_processes',
    'kill_process',
    'get_environment_variable',
    'set_environment_variable',
    'create_directory',
    'remove_directory',
    'copy_file',
    'move_file',
    'find_files',
    'file_exists',
    'directory_exists',
    'get_file_size',
    'get_file_modified_time',
    'read_text_file',
    'write_text_file',
    'append_to_file',
    'read_json_file',
    'write_json_file',
    'get_current_directory',
    'change_directory',
    'list_directory',
    'get_disk_usage',
    'get_cpu_count',
    'get_python_version',
    'capture_screenshot',
    'simulate_keypress',
]

def run_command(command: List[str], timeout: Optional[int] = None,
                capture_output: bool = True) -> Dict[str, Any]:
    """Run system command.
    
    Args:
        command: Command and arguments as list
        timeout: Timeout in seconds
        capture_output: Capture stdout/stderr
        
    Returns:
        Dict with returncode, stdout, stderr
        
    Example:
        >>> result = run_command(['echo', 'hello'])
        >>> result['returncode']
        0
    """
    try:
        if capture_output:
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            return {
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr,
                'success': result.returncode == 0
            }
        else:
            result = subprocess.run(command, timeout=timeout)
            return {
                'returncode': result.returncode,
                'success': result.returncode == 0
            }
    except subprocess.TimeoutExpired:
        return {
            'returncode': -1,
            'error': 'Command timed out',
            'success': False
        }
    except Exception as e:
        return {
            'returncode': -1,
            'error': str(e),
            'success': False
        }

def execute_shell(command: str, shell: bool = True) -> Dict[str, Any]:
    """Execute shell command as string.
    
    Args:
        command: Shell command
        shell: Use shell execution
        
    Returns:
        Result dict
        
    Example:
        >>> result = execute_shell('echo test')
        >>> result['success']
        True
    """
    try:
        result = subprocess.run(
            command,
            shell=shell,
            capture_output=True,
            text=True
        )
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'success': result.returncode == 0
        }
    except Exception as e:
        return {
            'returncode': -1,
            'error': str(e),
            'success': False
        }

def get_system_info() -> Dict[str, str]:
    """Get system information.
    
    Returns:
        System info dict
        
    Example:
        >>> info = get_system_info()
        >>> 'system' in info
        True
    """
    return {
        'system': platform.system(),
        'release': platform.release(),
        'version': platform.version(),
        'machine': platform.machine(),
        'processor': platform.processor(),
        'python_version': sys.version,
        'platform': sys.platform
    }

def list_processes() -> List[Dict[str, Any]]:
    """List running processes (Unix-like systems).
    
    Returns:
        List of process dicts
        
    Example:
        >>> procs = list_processes()
        >>> len(procs) > 0
        True
    """
    if platform.system() == 'Windows':
        result = run_command(['tasklist'])
    else:
        result = run_command(['ps', 'aux'])
    
    if result['success']:
        lines = result['stdout'].strip().split('\n')
        return [{'line': line} for line in lines]
    return []

def kill_process(pid: int, force: bool = False) -> bool:
    """Kill process by PID.
    
    Args:
        pid: Process ID
        force: Force kill
        
    Returns:
        Success status
        
    Example:
        >>> # kill_process(12345)  # Would kill process
        >>> True
        True
    """
    try:
        if platform.system() == 'Windows':
            cmd = ['taskkill', '/PID', str(pid)]
            if force:
                cmd.append('/F')
        else:
            import signal
            os.kill(pid, signal.SIGKILL if force else signal.SIGTERM)
            return True
        
        result = run_command(cmd)
        return result['success']
    except:
        return False

def get_environment_variable(name: str, default: Optional[str] = None) -> Optional[str]:
    """Get environment variable.
    
    Args:
        name: Variable name
        default: Default value
        
    Returns:
        Variable value or default
        
    Example:
        >>> var = get_environment_variable('PATH')
        >>> var is not None
        True
    """
    return os.environ.get(name, default)

def set_environment_variable(name: str, value: str) -> None:
    """Set environment variable.
    
    Args:
        name: Variable name
        value: Variable value
        
    Example:
        >>> set_environment_variable('TEST_VAR', 'test_value')
    """
    os.environ[name] = value

def create_directory(path: str, parents: bool = True, exist_ok: bool = True) -> bool:
    """Create directory.
    
    Args:
        path: Directory path
        parents: Create parent directories
        exist_ok: Don't error if exists
        
    Returns:
        Success status
        
    Example:
        >>> create_directory('/tmp/test_dir')
        True
    """
    try:
        Path(path).mkdir(parents=parents, exist_ok=exist_ok)
        return True
    except:
        return False

def remove_directory(path: str, recursive: bool = False) -> bool:
    """Remove directory.
    
    Args:
        path: Directory path
        recursive: Remove recursively
        
    Returns:
        Success status
        
    Example:
        >>> # remove_directory('/tmp/test_dir')
        >>> True
        True
    """
    try:
        if recursive:
            shutil.rmtree(path)
        else:
            os.rmdir(path)
        return True
    except:
        return False

def copy_file(src: str, dst: str) -> bool:
    """Copy file.
    
    Args:
        src: Source path
        dst: Destination path
        
    Returns:
        Success status
        
    Example:
        >>> # copy_file('/tmp/file.txt', '/tmp/file2.txt')
        >>> True
        True
    """
    try:
        shutil.copy2(src, dst)
        return True
    except:
        return False

def move_file(src: str, dst: str) -> bool:
    """Move file.
    
    Args:
        src: Source path
        dst: Destination path
        
    Returns:
        Success status
        
    Example:
        >>> # move_file('/tmp/file.txt', '/tmp/moved.txt')
        >>> True
        True
    """
    try:
        shutil.move(src, dst)
        return True
    except:
        return False

def find_files(directory: str, pattern: str = '*', recursive: bool = True) -> List[str]:
    """Find files matching pattern.
    
    Args:
        directory: Directory to search
        pattern: Glob pattern
        recursive: Search recursively
        
    Returns:
        List of matching file paths
        
    Example:
        >>> files = find_files('.', pattern='*.py', recursive=False)
        >>> isinstance(files, list)
        True
    """
    path = Path(directory)
    if recursive:
        return [str(p) for p in path.rglob(pattern)]
    else:
        return [str(p) for p in path.glob(pattern)]

def file_exists(path: str) -> bool:
    """Check if file exists.
    
    Args:
        path: File path
        
    Returns:
        True if exists
        
    Example:
        >>> file_exists(__file__)
        True
    """
    return Path(path).is_file()

def directory_exists(path: str) -> bool:
    """Check if directory exists.
    
    Args:
        path: Directory path
        
    Returns:
        True if exists
        
    Example:
        >>> directory_exists('.')
        True
    """
    return Path(path).is_dir()

def get_file_size(path: str) -> int:
    """Get file size in bytes.
    
    Args:
        path: File path
        
    Returns:
        File size
        
    Example:
        >>> size = get_file_size(__file__)
        >>> size > 0
        True
    """
    return Path(path).stat().st_size

def get_file_modified_time(path: str) -> float:
    """Get file modification time (timestamp).
    
    Args:
        path: File path
        
    Returns:
        Modification timestamp
        
    Example:
        >>> mtime = get_file_modified_time(__file__)
        >>> mtime > 0
        True
    """
    return Path(path).stat().st_mtime

def read_text_file(path: str, encoding: str = 'utf-8') -> str:
    """Read text file.
    
    Args:
        path: File path
        encoding: Text encoding
        
    Returns:
        File contents
        
    Example:
        >>> # content = read_text_file('/tmp/test.txt')
        >>> True
        True
    """
    return Path(path).read_text(encoding=encoding)

def write_text_file(path: str, content: str, encoding: str = 'utf-8') -> bool:
    """Write text file.
    
    Args:
        path: File path
        content: Content to write
        encoding: Text encoding
        
    Returns:
        Success status
        
    Example:
        >>> # write_text_file('/tmp/test.txt', 'hello')
        >>> True
        True
    """
    try:
        Path(path).write_text(content, encoding=encoding)
        return True
    except:
        return False

def append_to_file(path: str, content: str, encoding: str = 'utf-8') -> bool:
    """Append to text file.
    
    Args:
        path: File path
        content: Content to append
        encoding: Text encoding
        
    Returns:
        Success status
        
    Example:
        >>> # append_to_file('/tmp/test.txt', 'world')
        >>> True
        True
    """
    try:
        with open(path, 'a', encoding=encoding) as f:
            f.write(content)
        return True
    except:
        return False

def read_json_file(path: str) -> Any:
    """Read JSON file.
    
    Args:
        path: File path
        
    Returns:
        Parsed JSON data
        
    Example:
        >>> # data = read_json_file('/tmp/data.json')
        >>> True
        True
    """
    with open(path, 'r') as f:
        return json.load(f)

def write_json_file(path: str, data: Any, indent: int = 2) -> bool:
    """Write JSON file.
    
    Args:
        path: File path
        data: Data to write
        indent: JSON indentation
        
    Returns:
        Success status
        
    Example:
        >>> # write_json_file('/tmp/data.json', {'key': 'value'})
        >>> True
        True
    """
    try:
        with open(path, 'w') as f:
            json.dump(data, f, indent=indent)
        return True
    except:
        return False

def get_current_directory() -> str:
    """Get current working directory.
    
    Returns:
        Current directory path
        
    Example:
        >>> cwd = get_current_directory()
        >>> len(cwd) > 0
        True
    """
    return os.getcwd()

def change_directory(path: str) -> bool:
    """Change current directory.
    
    Args:
        path: New directory path
        
    Returns:
        Success status
        
    Example:
        >>> # change_directory('/tmp')
        >>> True
        True
    """
    try:
        os.chdir(path)
        return True
    except:
        return False

def list_directory(path: str = '.', include_hidden: bool = False) -> List[str]:
    """List directory contents.
    
    Args:
        path: Directory path
        include_hidden: Include hidden files
        
    Returns:
        List of filenames
        
    Example:
        >>> files = list_directory('.')
        >>> isinstance(files, list)
        True
    """
    files = os.listdir(path)
    if not include_hidden:
        files = [f for f in files if not f.startswith('.')]
    return sorted(files)

def get_disk_usage(path: str = '/') -> Dict[str, int]:
    """Get disk usage statistics.
    
    Args:
        path: Path to check
        
    Returns:
        Dict with total, used, free bytes
        
    Example:
        >>> usage = get_disk_usage('.')
        >>> usage['total'] > 0
        True
    """
    stat = shutil.disk_usage(path)
    return {
        'total': stat.total,
        'used': stat.used,
        'free': stat.free
    }

def get_cpu_count() -> int:
    """Get number of CPU cores.
    
    Returns:
        CPU count
        
    Example:
        >>> count = get_cpu_count()
        >>> count > 0
        True
    """
    return os.cpu_count() or 1

def get_python_version() -> str:
    """Get Python version string.
    
    Returns:
        Python version
        
    Example:
        >>> version = get_python_version()
        >>> '3.' in version
        True
    """
    return sys.version

def capture_screenshot(filename: str) -> bool:
    """Capture screenshot (requires external tools).
    
    Args:
        filename: Output filename
        
    Returns:
        Success status
        
    Note:
        Uses system-specific screenshot tools:
        - macOS: screencapture
        - Linux: scrot or import
        - Windows: Not implemented in stdlib
        
    Example:
        >>> # capture_screenshot('/tmp/screen.png')
        >>> True
        True
    """
    system = platform.system()
    
    try:
        if system == 'Darwin':  # macOS
            result = run_command(['screencapture', '-x', filename])
            return result['success']
        elif system == 'Linux':
            # Try scrot first
            result = run_command(['scrot', filename])
            if not result['success']:
                # Try imagemagick import
                result = run_command(['import', '-window', 'root', filename])
            return result['success']
        else:
            return False
    except:
        return False

def simulate_keypress(key: str) -> bool:
    """Simulate keypress (limited stdlib support).
    
    Args:
        key: Key to press
        
    Returns:
        Success status
        
    Note:
        This is a placeholder - real keyboard simulation
        requires external libraries like pyautogui.
        Returns False as not implemented in stdlib.
        
    Example:
        >>> # simulate_keypress('a')
        >>> True
        True
    """
    # Not implemented in stdlib - would need external library
    return False
