""
File Utilities for Ollama Model Fine-Tuning UI

This module provides utility functions for file operations.
"""
import os
import shutil
import json
import logging
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, BinaryIO
import tempfile
import hashlib

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def ensure_directory_exists(directory: Union[str, Path]) -> Path:
    """Ensure that a directory exists, creating it if necessary.
    
    Args:
        directory: Path to the directory
        
    Returns:
        Path: The path to the directory
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path

def safe_write_json(data: Any, file_path: Union[str, Path], indent: int = 2) -> None:
    """Safely write data to a JSON file.
    
    Args:
        data: Data to write (must be JSON serializable)
        file_path: Path to the output file
        indent: Indentation level for the JSON file
    """
    file_path = Path(file_path)
    temp_file = file_path.with_suffix('.tmp')
    
    try:
        with open(temp_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
        
        # On Windows, we need to remove the destination file first if it exists
        if file_path.exists():
            file_path.unlink()
        
        # Rename the temp file to the target file
        temp_file.rename(file_path)
        
    except Exception as e:
        logger.error(f"Error writing to {file_path}: {str(e)}")
        if temp_file.exists():
            temp_file.unlink()
        raise

def safe_read_json(file_path: Union[str, Path], default: Any = None) -> Any:
    """Safely read data from a JSON file.
    
    Args:
        file_path: Path to the JSON file
        default: Default value to return if the file doesn't exist or is invalid
        
    Returns:
        The parsed JSON data or the default value
    """
    file_path = Path(file_path)
    if not file_path.exists():
        return default
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError) as e:
        logger.error(f"Error reading JSON from {file_path}: {str(e)}")
        return default

def get_file_hash(file_path: Union[str, Path], algorithm: str = 'sha256', chunk_size: int = 65536) -> str:
    """Calculate the hash of a file.
    
    Args:
        file_path: Path to the file
        algorithm: Hash algorithm to use (e.g., 'md5', 'sha1', 'sha256')
        chunk_size: Size of chunks to read at a time
        
    Returns:
        str: The hexadecimal digest of the file's hash
    """
    file_path = Path(file_path)
    if not file_path.is_file():
        raise FileNotFoundError(f"File not found: {file_path}")
    
    hash_func = hashlib.new(algorithm)
    
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(chunk_size), b''):
            hash_func.update(chunk)
    
    return hash_func.hexdigest()

def get_file_size(file_path: Union[str, Path]) -> int:
    """Get the size of a file in bytes.
    
    Args:
        file_path: Path to the file
        
    Returns:
        int: Size of the file in bytes
    """
    return os.path.getsize(file_path)

def format_file_size(size_in_bytes: int, precision: int = 2) -> str:
    """Format a file size in a human-readable format.
    
    Args:
        size_in_bytes: Size in bytes
        precision: Number of decimal places to include
        
    Returns:
        str: Formatted file size (e.g., "1.23 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size_in_bytes < 1024.0 or unit == 'TB':
            break
        size_in_bytes /= 1024.0
    
    return f"{size_in_bytes:.{precision}f} {unit}"

def copy_file(src: Union[str, Path], dst: Union[str, Path], overwrite: bool = False) -> bool:
    """Copy a file from source to destination.
    
    Args:
        src: Source file path
        dst: Destination file path
        overwrite: Whether to overwrite the destination file if it exists
        
    Returns:
        bool: True if the file was copied successfully, False otherwise
    """
    src_path = Path(src)
    dst_path = Path(dst)
    
    if not src_path.is_file():
        logger.error(f"Source file does not exist: {src_path}")
        return False
    
    if dst_path.exists() and not overwrite:
        logger.error(f"Destination file already exists and overwrite is False: {dst_path}")
        return False
    
    try:
        # Ensure the destination directory exists
        dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy the file
        shutil.copy2(src_path, dst_path)
        return True
    except Exception as e:
        logger.error(f"Error copying file from {src_path} to {dst_path}: {str(e)}")
        return False

def create_temp_file(suffix: str = None, prefix: str = None, dir: Union[str, Path] = None, content: str = None) -> Path:
    """Create a temporary file with optional content.
    
    Args:
        suffix: File suffix (e.g., '.txt')
        prefix: File prefix
        dir: Directory to create the file in
        content: Optional content to write to the file
        
    Returns:
        Path: Path to the created temporary file
    """
    with tempfile.NamedTemporaryFile(
        mode='w+',
        suffix=suffix or '',
        prefix=prefix or 'tmp',
        dir=dir,
        delete=False
    ) as f:
        if content is not None:
            f.write(content)
        return Path(f.name)

def cleanup_temp_files(directory: Union[str, Path], pattern: str = 'tmp*', max_age_seconds: int = 86400) -> int:
    """Clean up temporary files in a directory.
    
    Args:
        directory: Directory to clean up
        pattern: File pattern to match (supports glob format)
        max_age_seconds: Maximum age of files to keep (in seconds)
        
    Returns:
        int: Number of files deleted
    """
    import time
    from pathlib import Path
    
    directory = Path(directory)
    if not directory.is_dir():
        return 0
    
    current_time = time.time()
    deleted_count = 0
    
    for file_path in directory.glob(pattern):
        try:
            file_age = current_time - file_path.stat().st_mtime
            if file_age > max_age_seconds:
                file_path.unlink()
                deleted_count += 1
        except Exception as e:
            logger.warning(f"Error deleting temporary file {file_path}: {str(e)}")
    
    return deleted_count

def is_binary_file(file_path: Union[str, Path], chunk_size: int = 8192) -> bool:
    """Check if a file is binary.
    
    Args:
        file_path: Path to the file
        chunk_size: Number of bytes to read for the check
        
    Returns:
        bool: True if the file is binary, False otherwise
    """
    file_path = Path(file_path)
    if not file_path.is_file():
        return False
    
    try:
        with open(file_path, 'rb') as f:
            chunk = f.read(chunk_size)
            # Check for null bytes, which are common in binary files
            if b'\x00' in chunk:
                return True
            
            # Try to decode as text
            try:
                chunk.decode('utf-8')
                return False
            except UnicodeDecodeError:
                return True
    except Exception as e:
        logger.warning(f"Error checking if file is binary: {str(e)}")
        return False

def find_files(directory: Union[str, Path], patterns: List[str] = None, recursive: bool = True) -> List[Path]:
    """Find files in a directory matching the given patterns.
    
    Args:
        directory: Directory to search in
        patterns: List of file patterns to match (e.g., ['*.txt', '*.md'])
        recursive: Whether to search recursively in subdirectories
        
    Returns:
        List[Path]: List of matching file paths
    """
    directory = Path(directory)
    if not directory.is_dir():
        return []
    
    patterns = patterns or ['*']
    found_files = set()
    
    for pattern in patterns:
        if recursive:
            found_files.update(directory.rglob(pattern))
        else:
            found_files.update(directory.glob(pattern))
    
    # Filter out directories (in case a pattern matches a directory name)
    return [f for f in found_files if f.is_file()]
