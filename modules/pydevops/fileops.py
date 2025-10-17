"""
File operation utilities for DevOps tasks
"""

import os
import shutil
from pathlib import Path
from typing import List, Optional


def safe_copy(src: str, dst: str, create_dirs: bool = True) -> bool:
    """
    Safely copy file with error handling
    
    Args:
        src: Source file path
        dst: Destination file path
        create_dirs: Create destination directories if needed
    
    Returns:
        True if successful, False otherwise
    """
    try:
        src_path = Path(src)
        dst_path = Path(dst)
        
        if not src_path.exists():
            return False
        
        if create_dirs:
            dst_path.parent.mkdir(parents=True, exist_ok=True)
        
        shutil.copy2(src_path, dst_path)
        return True
    except Exception:
        return False


def safe_remove(path: str, recursive: bool = False) -> bool:
    """
    Safely remove file or directory
    
    Args:
        path: Path to remove
        recursive: Remove directories recursively
    
    Returns:
        True if successful, False otherwise
    """
    try:
        target = Path(path)
        
        if not target.exists():
            return True
        
        if target.is_file():
            target.unlink()
        elif target.is_dir() and recursive:
            shutil.rmtree(target)
        else:
            target.rmdir()
        
        return True
    except Exception:
        return False


def find_files(directory: str, pattern: str = '*', recursive: bool = True) -> List[str]:
    """
    Find files matching pattern in directory
    
    Args:
        directory: Directory to search
        pattern: File pattern (e.g., '*.py', 'test_*.txt')
        recursive: Search recursively
    
    Returns:
        List of matching file paths
    """
    path = Path(directory)
    
    if not path.exists() or not path.is_dir():
        return []
    
    if recursive:
        return [str(p) for p in path.rglob(pattern) if p.is_file()]
    else:
        return [str(p) for p in path.glob(pattern) if p.is_file()]


def get_file_size(path: str, human_readable: bool = False) -> Optional[str]:
    """
    Get file size
    
    Args:
        path: File path
        human_readable: Return human-readable format (e.g., '1.5 MB')
    
    Returns:
        File size as string or None if file doesn't exist
    """
    file_path = Path(path)
    
    if not file_path.exists() or not file_path.is_file():
        return None
    
    size = file_path.stat().st_size
    
    if not human_readable:
        return str(size)
    
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024.0:
            return f"{size:.1f} {unit}"
        size /= 1024.0
    
    return f"{size:.1f} PB"
