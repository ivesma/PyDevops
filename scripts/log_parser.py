#!/usr/bin/env python3
"""
Log Parser Script - Parse and analyze log files
"""

import re
import argparse
from collections import Counter, defaultdict
from pathlib import Path
from datetime import datetime


class LogParser:
    """Parse and analyze log files"""
    
    def __init__(self, log_file):
        self.log_file = Path(log_file)
        self.lines = []
        self.errors = []
        self.warnings = []
        self.stats = defaultdict(int)
        
    def load(self):
        """Load log file"""
        if not self.log_file.exists():
            raise FileNotFoundError(f"Log file not found: {self.log_file}")
        
        with open(self.log_file, 'r', encoding='utf-8', errors='ignore') as f:
            self.lines = f.readlines()
        
        return len(self.lines)
    
    def parse(self):
        """Parse log entries"""
        for line in self.lines:
            line = line.strip()
            
            if not line:
                continue
            
            # Count log levels
            if 'ERROR' in line.upper():
                self.errors.append(line)
                self.stats['errors'] += 1
            elif 'WARN' in line.upper():
                self.warnings.append(line)
                self.stats['warnings'] += 1
            elif 'INFO' in line.upper():
                self.stats['info'] += 1
            elif 'DEBUG' in line.upper():
                self.stats['debug'] += 1
            
            self.stats['total'] += 1
    
    def find_pattern(self, pattern):
        """Find lines matching regex pattern"""
        regex = re.compile(pattern, re.IGNORECASE)
        matches = []
        
        for line in self.lines:
            if regex.search(line):
                matches.append(line.strip())
        
        return matches
    
    def get_top_errors(self, n=10):
        """Get most common error messages"""
        if not self.errors:
            return []
        
        # Simple deduplication by removing timestamps
        cleaned = []
        for error in self.errors:
            # Remove common timestamp patterns
            cleaned_error = re.sub(r'\d{4}-\d{2}-\d{2}', '', error)
            cleaned_error = re.sub(r'\d{2}:\d{2}:\d{2}', '', cleaned_error)
            cleaned.append(cleaned_error.strip())
        
        counter = Counter(cleaned)
        return counter.most_common(n)
    
    def print_summary(self):
        """Print summary statistics"""
        print(f"\n{'='*60}")
        print(f"Log Analysis Summary - {self.log_file.name}")
        print(f"{'='*60}")
        
        print(f"\nTotal lines: {self.stats['total']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"Warnings: {self.stats['warnings']}")
        print(f"Info: {self.stats['info']}")
        print(f"Debug: {self.stats['debug']}")
        
        if self.errors:
            print(f"\n{'='*60}")
            print("Top Error Messages:")
            print(f"{'='*60}")
            for i, (error, count) in enumerate(self.get_top_errors(5), 1):
                print(f"\n{i}. Count: {count}")
                print(f"   {error[:100]}...")
        
        if self.warnings:
            print(f"\n{'='*60}")
            print(f"Recent Warnings (last 5):")
            print(f"{'='*60}")
            for warning in self.warnings[-5:]:
                print(f"  {warning[:100]}...")


def main():
    parser = argparse.ArgumentParser(
        description='Parse and analyze log files'
    )
    parser.add_argument(
        'log_file',
        help='Path to log file'
    )
    parser.add_argument(
        '-p', '--pattern',
        help='Search for specific pattern (regex)'
    )
    parser.add_argument(
        '-e', '--errors-only',
        action='store_true',
        help='Show only errors'
    )
    parser.add_argument(
        '-w', '--warnings-only',
        action='store_true',
        help='Show only warnings'
    )
    
    args = parser.parse_args()
    
    try:
        parser_obj = LogParser(args.log_file)
        lines_loaded = parser_obj.load()
        print(f"Loaded {lines_loaded} lines from {args.log_file}")
        
        parser_obj.parse()
        
        if args.pattern:
            matches = parser_obj.find_pattern(args.pattern)
            print(f"\nFound {len(matches)} matches for pattern '{args.pattern}':")
            for match in matches[:20]:  # Show first 20
                print(f"  {match}")
        elif args.errors_only:
            print(f"\nErrors ({len(parser_obj.errors)}):")
            for error in parser_obj.errors:
                print(f"  {error}")
        elif args.warnings_only:
            print(f"\nWarnings ({len(parser_obj.warnings)}):")
            for warning in parser_obj.warnings:
                print(f"  {warning}")
        else:
            parser_obj.print_summary()
            
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return 1
    except Exception as e:
        print(f"Error parsing log file: {e}")
        return 1
    
    return 0


if __name__ == '__main__':
    exit(main())
