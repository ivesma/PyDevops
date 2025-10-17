# PyDevops

Scripts and modules in Python geared to DevOps

## Description

PyDevops is a Python package providing utilities and scripts for DevOps tasks. This project aims to simplify common DevOps workflows and automation tasks.

## Installation

### From Source

```bash
git clone https://github.com/ivesma/PyDevops.git
cd PyDevops
pip install -e .
```

### Development Installation

For development, install with dev dependencies:

```bash
pip install -e ".[dev]"
# Or
pip install -r requirements-dev.txt
```

## Project Structure

```
PyDevops/
├── src/
│   └── pydevops/       # Main package directory
│       ├── __init__.py
│       └── utils.py    # Utility functions
├── tests/              # Test directory
│   └── test_utils.py   # Unit tests
├── examples/           # Example scripts
│   └── example_usage.py
├── pyproject.toml      # Project configuration
├── requirements.txt    # Production dependencies
└── requirements-dev.txt # Development dependencies
```

## Usage

### As a Package

```python
from pydevops.utils import hello, get_version

print(hello())
print(get_version())
```

### Running Examples

```bash
python examples/example_usage.py
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black src/ tests/
```

### Linting

```bash
flake8 src/ tests/
```

### Type Checking

```bash
mypy src/
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
