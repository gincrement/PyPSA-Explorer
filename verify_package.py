#!/usr/bin/env python
"""
Package Verification Script

Run this script to verify that the package is properly installed and configured.
"""

import sys


def check_import():
    """Check if package can be imported."""
    print("1. Checking package import...")
    try:
        import pypsa_explorer

        print(f"   ✓ Package imported successfully (version {pypsa_explorer.__version__})")
        return True
    except ImportError as e:
        print(f"   ✗ Failed to import package: {e}")
        return False


def check_submodules():
    """Check if all submodules can be imported."""
    print("\n2. Checking submodules...")
    modules = [
        "pypsa_explorer.app",
        "pypsa_explorer.cli",
        "pypsa_explorer.config",
        "pypsa_explorer.callbacks",
        "pypsa_explorer.layouts",
        "pypsa_explorer.utils",
    ]

    all_ok = True
    for module in modules:
        try:
            __import__(module)
            print(f"   ✓ {module}")
        except ImportError as e:
            print(f"   ✗ {module}: {e}")
            all_ok = False

    return all_ok


def check_functions():
    """Check if main functions are available."""
    print("\n3. Checking main functions...")
    try:
        from pypsa_explorer import create_app, load_networks, run_dashboard

        print("   ✓ create_app")
        print("   ✓ run_dashboard")
        print("   ✓ load_networks")
        return True
    except ImportError as e:
        print(f"   ✗ Failed to import functions: {e}")
        return False


def check_cli():
    """Check if CLI module is accessible."""
    print("\n4. Checking CLI...")
    try:
        from pypsa_explorer.cli import main

        print("   ✓ CLI module accessible")
        print("   ℹ Run 'python -m pypsa_explorer.cli --version' to test")
        return True
    except ImportError as e:
        print(f"   ✗ Failed to import CLI: {e}")
        return False


def check_type_hints():
    """Check if type hints are available."""
    print("\n5. Checking type hints...")
    try:
        import pypsa_explorer

        if hasattr(pypsa_explorer, "__annotations__"):
            print("   ✓ Package has type annotations")
        else:
            print("   ℹ Type annotations not found at package level (this is OK)")

        # Check for py.typed marker
        import os

        package_dir = os.path.dirname(pypsa_explorer.__file__)
        py_typed = os.path.join(package_dir, "py.typed")

        if os.path.exists(py_typed):
            print("   ✓ py.typed marker file exists (PEP 561 compliant)")
        else:
            print("   ✗ py.typed marker file not found")

        return True
    except Exception as e:
        print(f"   ✗ Error checking type hints: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 60)
    print("PyPSA Explorer - Package Verification")
    print("=" * 60)

    checks = [
        check_import(),
        check_submodules(),
        check_functions(),
        check_cli(),
        check_type_hints(),
    ]

    print("\n" + "=" * 60)
    if all(checks):
        print("✓ All checks passed! Package is properly installed.")
        print("\nNext steps:")
        print("  - Run tests: pytest")
        print("  - Start dashboard: python -m pypsa_explorer.cli")
        print("  - See examples: examples/")
        return 0
    else:
        print("✗ Some checks failed. Please review the errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
