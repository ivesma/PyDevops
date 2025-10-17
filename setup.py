"""
PyDevops Setup Script
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / 'README.md'
long_description = readme_file.read_text() if readme_file.exists() else ''

setup(
    name='pydevops',
    version='0.1.0',
    description='Scripts and modules in Python geared to DevOps',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='PyDevops Contributors',
    url='https://github.com/ivesma/PyDevops',
    packages=find_packages(where='modules'),
    package_dir={'': 'modules'},
    install_requires=[
        'psutil>=5.9.0',
        'requests>=2.31.0',
        'PyYAML>=6.0',
    ],
    scripts=[
        'scripts/system_monitor.py',
        'scripts/log_parser.py',
        'scripts/backup.py',
        'scripts/health_check.py',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Topic :: System :: Systems Administration',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
)
