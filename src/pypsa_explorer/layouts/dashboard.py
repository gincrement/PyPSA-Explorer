"""Main dashboard layout for PyPSA Explorer."""

import dash_bootstrap_components as dbc
import pypsa
from dash import dcc, html

from pypsa_explorer.config import DEFAULT_CARRIERS
from pypsa_explorer.layouts.components import (
    create_data_explorer_modal,
    create_footer,
    create_header,
    create_sidebar_filter_panel,
    create_top_bar,
)
from pypsa_explorer.layouts.tabs import (
    create_capacity_tab,
    create_capex_totals_tab,
    create_energy_balance_aggregated_tab,
    create_energy_balance_tab,
    create_network_map_tab,
    create_opex_totals_tab,
)
from pypsa_explorer.layouts.welcome import create_welcome_page
from pypsa_explorer.utils.helpers import get_bus_carrier_options, get_country_options


def create_dashboard_layout(networks: dict[str, pypsa.Network], active_network_label: str) -> dbc.Container:
    """
    Create the complete dashboard layout.

    Parameters
    ----------
    networks : dict[str, pypsa.Network]
        Dictionary of loaded networks
    active_network_label : str
        Label of the initially active network

    Returns
    -------
    dbc.Container
        Complete dashboard layout
    """
    n = networks[active_network_label]
    network_labels = list(networks.keys())

    # Get options for filters
    bus_carrier_options = get_bus_carrier_options(n)
    country_options = get_country_options(n)

    # Prepare network info for welcome page
    networks_info = {
        label: {
            "buses": len(net.buses),
            "links": len(net.links),
            "lines": len(net.lines),
        }
        for label, net in networks.items()
    }

    return dbc.Container(
        fluid=True,
        children=[
            # Store component to manage page state
            dcc.Store(id="page-state", data={"current_page": "welcome"}),
            # Store component for dark mode state (cached)
            dcc.Store(id="dark-mode-store", data=False),
            # Data explorer modal
            create_data_explorer_modal(),
            # Main application layout with conditional display
            html.Div(
                id="app-container",
                className="",
                children=[
                    create_top_bar(network_labels, active_network_label),
                    html.Div(
                        id="main-content",
                        className="fade-in",
                        children=[
                            # Welcome page content will be shown initially
                            html.Div(
                                id="welcome-content",
                                children=[create_welcome_page(network_labels, networks_info)],
                            ),
                            # Main dashboard content (initially hidden)
                            html.Div(
                                id="dashboard-content",
                                style={"display": "none"},
                                children=[
                                    create_header(n),
                                    # Main content with sidebar layout
                                    dbc.Row(
                                        [
                                            # Sidebar with filters
                                            dbc.Col(
                                                create_sidebar_filter_panel(
                                                    bus_carrier_options,
                                                    country_options,
                                                    default_carriers=DEFAULT_CARRIERS,
                                                ),
                                                width=3,
                                                className="p-0",
                                            ),
                                            # Main content area
                                            dbc.Col(
                                                dcc.Tabs(
                                                    id="tabs",
                                                    style={
                                                        "borderBottom": "2px solid transparent",
                                                        "marginBottom": "20px",
                                                    },
                                                    parent_style={
                                                        "borderRadius": "16px",
                                                        "overflow": "hidden",
                                                    },
                                                    children=[
                                                        create_energy_balance_tab(),
                                                        create_energy_balance_aggregated_tab(),
                                                        create_capacity_tab(),
                                                        create_capex_totals_tab(),
                                                        create_opex_totals_tab(),
                                                        create_network_map_tab(),
                                                    ],
                                                ),
                                                width=9,
                                                className="main-content-area",
                                            ),
                                        ],
                                        className="g-0",  # Remove gutter between columns
                                    ),
                                ],
                            ),
                            create_footer(),
                        ],
                    ),
                ],
            ),
        ],
    )
