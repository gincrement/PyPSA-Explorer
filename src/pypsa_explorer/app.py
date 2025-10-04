"""Main application module for PyPSA Explorer dashboard."""


import dash
import dash_bootstrap_components as dbc
import pypsa
import pypsa.consistency

from pypsa_explorer.callbacks import register_all_callbacks
from pypsa_explorer.config import get_html_template, setup_plotly_theme
from pypsa_explorer.layouts.dashboard import create_dashboard_layout
from pypsa_explorer.utils.network_loader import load_networks


def create_app(
    networks_input: dict[str, pypsa.Network | str] | str | None = None,
    title: str = "PyPSA Explorer",
    debug: bool = False,
) -> dash.Dash:
    """
    Create and configure the Dash application.

    Parameters
    ----------
    networks_input : dict, str, or None
        Networks to load. Can be:
        - dict: {label: network_object_or_path}
        - str: Path to a single network file
        - None: Load default demo network
    title : str
        Dashboard title
    debug : bool
        Whether to run in debug mode

    Returns
    -------
    dash.Dash
        Configured Dash application instance
    """
    # Setup Plotly theme
    setup_plotly_theme()

    # Load networks
    networks = load_networks(networks_input)

    # Get the first network as the active network initially
    network_labels = list(networks.keys())
    active_network_label = network_labels[0]
    n = networks[active_network_label]

    # Initialize Dash app
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        title=title,
    )

    # Set custom HTML template with embedded CSS
    app.index_string = get_html_template()

    # Create layout
    app.layout = create_dashboard_layout(networks, active_network_label)

    # Register all callbacks
    register_all_callbacks(app, networks)

    return app


def run_dashboard(
    networks_input: dict[str, pypsa.Network | str] | str | None = None,
    debug: bool = True,
    host: str = "127.0.0.1",
    port: int = 8050,
) -> None:
    """
    Run the PyPSA Explorer dashboard.

    Parameters
    ----------
    networks_input : dict, str, or None
        Networks to load. Can be:
        - dict: {label: network_object_or_path} mapping labels to Network objects or file paths
        - str: Single path to a network file
        - None: Load default demo network
    debug : bool
        Whether to run in debug mode
    host : str
        Host to run the server on
    port : int
        Port to run the server on
    """
    app = create_app(networks_input, debug=debug)

    print(f"Starting PyPSA Explorer Dashboard on http://{host}:{port}")
    print("Press Ctrl+C to stop the server")

    app.run(debug=debug, host=host, port=port)
