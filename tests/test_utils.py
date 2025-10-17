"""
Tests for the utils module.
"""

from pydevops.utils import hello, get_version


def test_hello():
    """Test the hello function."""
    result = hello()
    assert result == "Hello from PyDevops!"
    assert isinstance(result, str)


def test_get_version():
    """Test the get_version function."""
    version = get_version()
    assert version == "0.1.0"
    assert isinstance(version, str)
