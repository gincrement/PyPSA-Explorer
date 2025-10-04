"""Command-line interface for PyPSA Explorer."""

import argparse
import sys

from pypsa_explorer import __version__
from pypsa_explorer.app import run_dashboard
from pypsa_explorer.utils.network_loader import parse_cli_network_args


def main() -> None:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="PyPSA Explorer - Interactive dashboard for visualizing PyPSA energy system networks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Run with default demo network
  pypsa-explorer

  # Run with a single network
  pypsa-explorer /path/to/network.nc

  # Run with multiple networks (with labels)
  pypsa-explorer /path/to/network1.nc:Region1 /path/to/network2.nc:Region2

  # Run with custom host and port
  pypsa-explorer --host 0.0.0.0 --port 8080

  # Run in production mode (no debug)
  pypsa-explorer --no-debug
        """,
    )

    parser.add_argument(
        "networks",
        nargs="*",
        help="Network files to load. Format: path or path:label",
    )

    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="Host to run the server on (default: 127.0.0.1)",
    )

    parser.add_argument(
        "--port",
        type=int,
        default=8050,
        help="Port to run the server on (default: 8050)",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        default=True,
        help="Run in debug mode (default: True)",
    )

    parser.add_argument(
        "--no-debug",
        action="store_true",
        help="Disable debug mode",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"pypsa-explorer {__version__}",
    )

    args = parser.parse_args()

    # Parse network arguments
    networks_input = None
    if args.networks:
        network_paths = parse_cli_network_args(args.networks)
        networks_input = network_paths

    # Determine debug mode
    debug = args.debug and not args.no_debug

    # Run the dashboard
    try:
        run_dashboard(
            networks_input=networks_input,
            debug=debug,
            host=args.host,
            port=args.port,
        )
    except KeyboardInterrupt:
        print("\nShutting down PyPSA Explorer...")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
