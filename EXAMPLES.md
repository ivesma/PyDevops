# PyDevops Examples

This directory contains example code and usage patterns for PyDevops scripts and modules.

## Examples

### Using ConfigManager

```python
from pydevops import ConfigManager

# Create and save a configuration
config = ConfigManager()
config.set('app.name', 'MyApp')
config.set('app.version', '1.0.0')
config.set('database.host', 'localhost')
config.set('database.port', 5432)
config.save('config.yaml')

# Load and use configuration
config = ConfigManager('config.yaml')
config.load()
print(f"App: {config.get('app.name')} v{config.get('app.version')}")
```

### Using Logger

```python
from pydevops import setup_logger

# Setup logger with file output
logger = setup_logger('myapp', level='INFO', log_file='application.log')

# Log messages
logger.info('Application started')
logger.warning('Low disk space')
logger.error('Database connection failed')
```

### Using File Operations

```python
from pydevops.fileops import safe_copy, find_files, get_file_size

# Copy files safely
success = safe_copy('source.txt', 'backup/source.txt')
if success:
    print('File copied successfully')

# Find all log files
log_files = find_files('/var/log', '*.log')
for log in log_files:
    size = get_file_size(log, human_readable=True)
    print(f"{log}: {size}")
```

## Script Examples

### System Monitoring

Monitor system resources every 10 seconds for 5 iterations:
```bash
python scripts/system_monitor.py -i 10 -c 5
```

### Log Analysis

Analyze application logs and find error patterns:
```bash
python scripts/log_parser.py /var/log/app.log -p "ERROR|FATAL"
```

### Backup

Create daily backups with timestamps:
```bash
python scripts/backup.py /important/data -d /backup/location
```

### Health Checks

Monitor multiple services from a file:
```bash
# Create services.txt with URLs
echo "https://example.com" > services.txt
echo "https://api.example.com/health" >> services.txt

# Run health check
python scripts/health_check.py -f services.txt -v
```
