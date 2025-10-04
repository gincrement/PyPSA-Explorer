#!/usr/bin/env python
"""
PyPSA Explorer - Main Entry Point

This script provides backwards compatibility with the original single-file application.
The codebase has been refactored into a proper Python package structure.

Usage:
    python main.py [network_files...]

For the new CLI interface, use:
    pypsa-explorer [options] [network_files...]

For the Python API:
    from pypsa_explorer import run_dashboard
    run_dashboard(networks_input, debug=True)
"""

import sys

from pypsa_explorer.app import run_dashboard
from pypsa_explorer.utils.network_loader import parse_cli_network_args

if __name__ == "__main__":
    # Parse command line arguments
    networks_input = None

    if len(sys.argv) > 1:
        # Parse command line arguments in format path:label
        network_paths = parse_cli_network_args(sys.argv[1:])
        networks_input = network_paths

    # Run the dashboard
    print("Starting PyPSA Explorer...")
    print("Note: This is the legacy entry point. Use 'pypsa-explorer' CLI for production.")
    print()

    run_dashboard(networks_input=networks_input, debug=True)
