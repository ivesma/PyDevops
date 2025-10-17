#!/usr/bin/env python3
"""
Service Health Checker - Check health of web services and APIs
"""

import requests
import argparse
import json
from datetime import datetime
from typing import Dict, List


def check_http_service(url: str, timeout: int = 5) -> Dict:
    """
    Check HTTP service health
    
    Args:
        url: Service URL
        timeout: Request timeout in seconds
    
    Returns:
        Dictionary with health check results
    """
    result = {
        'url': url,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'status': 'unknown',
        'response_time': None,
        'status_code': None,
        'error': None
    }
    
    try:
        start_time = datetime.now()
        response = requests.get(url, timeout=timeout)
        end_time = datetime.now()
        
        response_time = (end_time - start_time).total_seconds() * 1000  # ms
        
        result['response_time'] = round(response_time, 2)
        result['status_code'] = response.status_code
        
        if response.status_code == 200:
            result['status'] = 'healthy'
        elif response.status_code < 500:
            result['status'] = 'degraded'
        else:
            result['status'] = 'unhealthy'
            
    except requests.exceptions.Timeout:
        result['status'] = 'timeout'
        result['error'] = f"Request timed out after {timeout}s"
    except requests.exceptions.ConnectionError:
        result['status'] = 'unreachable'
        result['error'] = "Connection error"
    except Exception as e:
        result['status'] = 'error'
        result['error'] = str(e)
    
    return result


def print_result(result: Dict, verbose: bool = False):
    """Print health check result"""
    status_icon = {
        'healthy': '✓',
        'degraded': '⚠',
        'unhealthy': '✗',
        'timeout': '⏱',
        'unreachable': '✗',
        'error': '✗',
        'unknown': '?'
    }
    
    icon = status_icon.get(result['status'], '?')
    status = result['status'].upper()
    
    print(f"\n{icon} {result['url']}")
    print(f"  Status: {status}")
    
    if result['status_code']:
        print(f"  HTTP Code: {result['status_code']}")
    
    if result['response_time']:
        print(f"  Response Time: {result['response_time']} ms")
    
    if result['error']:
        print(f"  Error: {result['error']}")
    
    if verbose:
        print(f"  Checked at: {result['timestamp']}")


def check_services(urls: List[str], timeout: int = 5, verbose: bool = False):
    """Check multiple services"""
    results = []
    
    print(f"{'='*60}")
    print(f"Service Health Check - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    for url in urls:
        result = check_http_service(url, timeout)
        results.append(result)
        print_result(result, verbose)
    
    # Summary
    healthy_count = sum(1 for r in results if r['status'] == 'healthy')
    total_count = len(results)
    
    print(f"\n{'='*60}")
    print(f"Summary: {healthy_count}/{total_count} services healthy")
    print(f"{'='*60}")
    
    return results


def main():
    parser = argparse.ArgumentParser(
        description='Check health of web services and APIs'
    )
    parser.add_argument(
        'urls',
        nargs='*',
        help='Service URLs to check'
    )
    parser.add_argument(
        '-f', '--file',
        help='File containing URLs (one per line)'
    )
    parser.add_argument(
        '-t', '--timeout',
        type=int,
        default=5,
        help='Request timeout in seconds (default: 5)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output'
    )
    parser.add_argument(
        '-o', '--output',
        help='Save results to JSON file'
    )
    
    args = parser.parse_args()
    
    urls = list(args.urls) if args.urls else []
    
    # Load URLs from file
    if args.file:
        try:
            with open(args.file, 'r') as f:
                file_urls = [line.strip() for line in f if line.strip() and not line.startswith('#')]
                urls.extend(file_urls)
        except FileNotFoundError:
            print(f"Error: File not found: {args.file}")
            return 1
    
    if not urls:
        parser.error("No URLs provided. Use positional arguments or --file option.")
    
    # Check services
    results = check_services(urls, timeout=args.timeout, verbose=args.verbose)
    
    # Save to file if requested
    if args.output:
        with open(args.output, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to: {args.output}")
    
    # Return exit code based on health
    unhealthy_count = sum(1 for r in results if r['status'] != 'healthy')
    return 1 if unhealthy_count > 0 else 0


if __name__ == '__main__':
    exit(main())
