#!/usr/bin/env python3
"""
System Monitor Script - Monitor system resources (CPU, Memory, Disk)
"""

import psutil
import time
import argparse
from datetime import datetime


def format_bytes(bytes_value):
    """Convert bytes to human-readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f} {unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f} PB"


def get_system_info():
    """Get current system information"""
    # CPU info
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_count = psutil.cpu_count()
    
    # Memory info
    memory = psutil.virtual_memory()
    
    # Disk info
    disk = psutil.disk_usage('/')
    
    return {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'cpu': {
            'percent': cpu_percent,
            'count': cpu_count
        },
        'memory': {
            'total': format_bytes(memory.total),
            'used': format_bytes(memory.used),
            'available': format_bytes(memory.available),
            'percent': memory.percent
        },
        'disk': {
            'total': format_bytes(disk.total),
            'used': format_bytes(disk.used),
            'free': format_bytes(disk.free),
            'percent': disk.percent
        }
    }


def monitor(interval=5, count=None):
    """Monitor system resources"""
    iterations = 0
    
    try:
        while True:
            info = get_system_info()
            
            print(f"\n{'='*60}")
            print(f"System Monitor - {info['timestamp']}")
            print(f"{'='*60}")
            
            print(f"\nCPU:")
            print(f"  Usage: {info['cpu']['percent']}%")
            print(f"  Cores: {info['cpu']['count']}")
            
            print(f"\nMemory:")
            print(f"  Total: {info['memory']['total']}")
            print(f"  Used: {info['memory']['used']} ({info['memory']['percent']}%)")
            print(f"  Available: {info['memory']['available']}")
            
            print(f"\nDisk (/):")
            print(f"  Total: {info['disk']['total']}")
            print(f"  Used: {info['disk']['used']} ({info['disk']['percent']}%)")
            print(f"  Free: {info['disk']['free']}")
            
            iterations += 1
            
            if count and iterations >= count:
                break
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\nMonitoring stopped by user.")


def main():
    parser = argparse.ArgumentParser(
        description='Monitor system resources (CPU, Memory, Disk)'
    )
    parser.add_argument(
        '-i', '--interval',
        type=int,
        default=5,
        help='Monitoring interval in seconds (default: 5)'
    )
    parser.add_argument(
        '-c', '--count',
        type=int,
        help='Number of iterations (default: infinite)'
    )
    
    args = parser.parse_args()
    
    print(f"Starting system monitor (interval: {args.interval}s)")
    if args.count:
        print(f"Will run {args.count} iterations")
    else:
        print("Press Ctrl+C to stop")
    
    monitor(interval=args.interval, count=args.count)


if __name__ == '__main__':
    main()
