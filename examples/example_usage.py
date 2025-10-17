#!/usr/bin/env python3
"""
Example script demonstrating PyDevops usage.

This is a simple example showing how to use the PyDevops package.
"""

from pydevops.utils import hello, get_version


def main():
    """Main function for the example script."""
    print(hello())
    print(f"PyDevops version: {get_version()}")


if __name__ == "__main__":
    main()
