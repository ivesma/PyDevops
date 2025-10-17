# PyDevops

Scripts and modules in Python geared to DevOps

## Overview

PyDevops is a collection of Python scripts and reusable modules designed to help with common DevOps tasks such as system monitoring, log analysis, backup management, and service health checks.

## Installation

### Install from source

```bash
git clone https://github.com/ivesma/PyDevops.git
cd PyDevops
pip install -r requirements.txt
```

### Install as package

```bash
pip install -e .
```

## Scripts

### System Monitor (`scripts/system_monitor.py`)

Monitor system resources including CPU, memory, and disk usage.

**Usage:**
```bash
# Monitor with 5-second interval
python scripts/system_monitor.py

# Monitor with custom interval
python scripts/system_monitor.py -i 10

# Run for specific number of iterations
python scripts/system_monitor.py -i 5 -c 3
```

**Options:**
- `-i, --interval`: Monitoring interval in seconds (default: 5)
- `-c, --count`: Number of iterations (default: infinite)

### Log Parser (`scripts/log_parser.py`)

Parse and analyze log files to identify errors, warnings, and patterns.

**Usage:**
```bash
# Analyze log file
python scripts/log_parser.py /var/log/application.log

# Search for specific pattern
python scripts/log_parser.py /var/log/app.log -p "error|exception"

# Show only errors
python scripts/log_parser.py /var/log/app.log -e

# Show only warnings
python scripts/log_parser.py /var/log/app.log -w
```

**Options:**
- `-p, --pattern`: Search for specific pattern (regex)
- `-e, --errors-only`: Show only errors
- `-w, --warnings-only`: Show only warnings

### Backup Script (`scripts/backup.py`)

Create backups of files and directories with timestamp and compression.

**Usage:**
```bash
# Create compressed backup
python scripts/backup.py /path/to/source

# Create backup to specific destination
python scripts/backup.py /path/to/source -d /path/to/backups

# Create uncompressed backup
python scripts/backup.py /path/to/source --no-compress

# List existing backups
python scripts/backup.py -l -d /path/to/backups
```

**Options:**
- `-d, --destination`: Destination directory for backups (default: ./backups)
- `-c, --compress`: Compress backup as tar.gz (default: True)
- `--no-compress`: Do not compress backup
- `-l, --list`: List existing backups

### Health Check (`scripts/health_check.py`)

Check the health of web services and APIs.

**Usage:**
```bash
# Check single service
python scripts/health_check.py https://example.com

# Check multiple services
python scripts/health_check.py https://example.com https://api.example.com

# Check services from file
python scripts/health_check.py -f services.txt

# Set custom timeout
python scripts/health_check.py https://example.com -t 10

# Save results to JSON
python scripts/health_check.py https://example.com -o results.json
```

**Options:**
- `-f, --file`: File containing URLs (one per line)
- `-t, --timeout`: Request timeout in seconds (default: 5)
- `-v, --verbose`: Verbose output
- `-o, --output`: Save results to JSON file

## Modules

### ConfigManager (`modules/pydevops/config.py`)

Manage configuration files in JSON and YAML formats.

**Example:**
```python
from pydevops import ConfigManager

# Load configuration
config = ConfigManager('config.yaml')
config.load()

# Get configuration values
db_host = config.get('database.host', 'localhost')

# Set configuration values
config.set('database.port', 5432)

# Save configuration
config.save()
```

### Logger (`modules/pydevops/logger.py`)

Setup logging with console and file output.

**Example:**
```python
from pydevops import setup_logger

# Create logger
logger = setup_logger('myapp', level='INFO', log_file='app.log')

# Use logger
logger.info('Application started')
logger.error('An error occurred')
```

### File Operations (`modules/pydevops/fileops.py`)

Utilities for safe file operations.

**Example:**
```python
from pydevops.fileops import safe_copy, find_files, get_file_size

# Copy file safely
safe_copy('/path/to/source.txt', '/path/to/dest.txt')

# Find all Python files
python_files = find_files('/path/to/directory', '*.py')

# Get file size
size = get_file_size('/path/to/file.txt', human_readable=True)
```

## Requirements

- Python 3.7+
- psutil >= 5.9.0
- requests >= 2.31.0
- PyYAML >= 6.0

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
