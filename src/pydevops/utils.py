"""
Utility functions for PyDevops package.
"""


def hello():
    """
    A simple hello function to demonstrate the package structure.

    Returns:
        str: A greeting message
    """
    return "Hello from PyDevops!"


def get_version():
    """
    Get the version of PyDevops.

    Returns:
        str: The version string
    """
    from . import __version__

    return __version__
