#!/usr/bin/env python3
"""
Backup Script - Create backups of files and directories
"""

import os
import shutil
import tarfile
import argparse
from pathlib import Path
from datetime import datetime


def create_backup(source, destination, compress=True, exclude=None):
    """
    Create a backup of source to destination
    
    Args:
        source: Source file or directory
        destination: Destination directory for backup
        compress: Whether to compress as tar.gz
        exclude: List of patterns to exclude
    """
    source_path = Path(source).resolve()
    dest_path = Path(destination).resolve()
    
    if not source_path.exists():
        raise FileNotFoundError(f"Source not found: {source}")
    
    # Create destination directory
    dest_path.mkdir(parents=True, exist_ok=True)
    
    # Generate backup filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    source_name = source_path.name
    
    if compress:
        backup_name = f"{source_name}_{timestamp}.tar.gz"
        backup_path = dest_path / backup_name
        
        print(f"Creating compressed backup: {backup_path}")
        
        with tarfile.open(backup_path, 'w:gz') as tar:
            tar.add(source_path, arcname=source_name)
        
        backup_size = backup_path.stat().st_size
        
    else:
        backup_name = f"{source_name}_{timestamp}"
        backup_path = dest_path / backup_name
        
        print(f"Creating backup: {backup_path}")
        
        if source_path.is_file():
            shutil.copy2(source_path, backup_path)
        else:
            shutil.copytree(source_path, backup_path)
        
        # Calculate total size
        if backup_path.is_file():
            backup_size = backup_path.stat().st_size
        else:
            backup_size = sum(f.stat().st_size for f in backup_path.rglob('*') if f.is_file())
    
    return backup_path, backup_size


def format_bytes(bytes_value):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def list_backups(destination):
    """List existing backups in destination"""
    dest_path = Path(destination)
    
    if not dest_path.exists():
        print("No backups found (destination doesn't exist)")
        return
    
    backups = sorted(dest_path.glob('*'), key=lambda p: p.stat().st_mtime, reverse=True)
    
    if not backups:
        print("No backups found")
        return
    
    print(f"\n{'='*70}")
    print(f"Backups in {destination}")
    print(f"{'='*70}")
    
    for backup in backups:
        size = backup.stat().st_size if backup.is_file() else sum(
            f.stat().st_size for f in backup.rglob('*') if f.is_file()
        )
        mtime = datetime.fromtimestamp(backup.stat().st_mtime)
        
        print(f"{backup.name}")
        print(f"  Size: {format_bytes(size)}")
        print(f"  Date: {mtime.strftime('%Y-%m-%d %H:%M:%S')}")
        print()


def main():
    parser = argparse.ArgumentParser(
        description='Create backups of files and directories'
    )
    parser.add_argument(
        'source',
        nargs='?',
        help='Source file or directory to backup'
    )
    parser.add_argument(
        '-d', '--destination',
        default='./backups',
        help='Destination directory for backups (default: ./backups)'
    )
    parser.add_argument(
        '-c', '--compress',
        action='store_true',
        default=True,
        help='Compress backup as tar.gz (default: True)'
    )
    parser.add_argument(
        '--no-compress',
        action='store_true',
        help='Do not compress backup'
    )
    parser.add_argument(
        '-l', '--list',
        action='store_true',
        help='List existing backups'
    )
    
    args = parser.parse_args()
    
    if args.list:
        list_backups(args.destination)
        return 0
    
    if not args.source:
        parser.error("source is required unless using --list")
    
    try:
        compress = args.compress and not args.no_compress
        backup_path, backup_size = create_backup(
            args.source,
            args.destination,
            compress=compress
        )
        
        print(f"\n{'='*60}")
        print("Backup completed successfully!")
        print(f"{'='*60}")
        print(f"Source: {args.source}")
        print(f"Backup: {backup_path}")
        print(f"Size: {format_bytes(backup_size)}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error creating backup: {e}")
        return 1


if __name__ == '__main__':
    exit(main())
