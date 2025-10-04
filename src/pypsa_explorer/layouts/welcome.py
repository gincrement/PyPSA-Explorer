"""Welcome page layout for PyPSA Explorer dashboard."""

import dash_bootstrap_components as dbc
from dash import html


def create_welcome_page(network_labels: list[str], networks_info: dict[str, dict[str, int]]) -> dbc.Card:
    """
    Create the welcome page for the dashboard.

    Parameters
    ----------
    network_labels : list[str]
        List of available network labels
    networks_info : dict[str, dict[str, int]]
        Dictionary with network info: {label: {"buses": count, "links": count, "lines": count}}

    Returns
    -------
    dbc.Card
        Welcome page component
    """
    return dbc.Card(
        dbc.CardBody(
            [
                # OET logo in the upper right
                html.Div(
                    html.Img(
                        src="https://openenergytransition.org/assets/img/oet-logo-red-n-subtitle.png",
                        style={
                            "height": "60px",
                            "position": "absolute",
                            "top": "15px",
                            "right": "15px",
                        },
                    ),
                ),
                html.Div(
                    [
                        html.H1(
                            "Welcome to the Energy System Dashboard",
                            className="welcome-header",
                        ),
                        html.P(
                            "Explore energy systems with interactive visualizations.",
                            className="welcome-subtitle",
                        ),
                        html.Hr(className="my-4"),
                    ],
                    className="welcome-card mb-4",
                ),
                dbc.Row(
                    [
                        # Energy Balance Timeseries
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(className="feature-icon", children=html.I(className="fas fa-chart-area")),
                                        html.H5("Energy Balance Timeseries"),
                                        html.P("Visualize energy flows over time for different carriers and countries."),
                                    ]
                                ),
                                className="welcome-feature",
                            ),
                            width=4,
                            className="mb-3",
                        ),
                        # Energy Balance Totals
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(className="feature-icon", children=html.I(className="fas fa-chart-bar")),
                                        html.H5("Energy Balance Totals"),
                                        html.P("Analyze aggregated energy balances across the system."),
                                    ]
                                ),
                                className="welcome-feature",
                            ),
                            width=4,
                            className="mb-3",
                        ),
                        # Capacity Totals
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(className="feature-icon", children=html.I(className="fas fa-solar-panel")),
                                        html.H5("Capacity Totals"),
                                        html.P("Explore optimal capacity distribution by carrier and country."),
                                    ]
                                ),
                                className="welcome-feature",
                            ),
                            width=4,
                            className="mb-3",
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row(
                    [
                        # CAPEX Totals
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(className="feature-icon", children=html.I(className="fas fa-coins")),
                                        html.H5("CAPEX Totals"),
                                        html.P("Analyze capital expenditure distribution across the network."),
                                    ]
                                ),
                                className="welcome-feature",
                            ),
                            width=4,
                            className="mb-3",
                        ),
                        # OPEX Totals
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            className="feature-icon", children=html.I(className="fas fa-file-invoice-dollar")
                                        ),
                                        html.H5("OPEX Totals"),
                                        html.P("Review operational expenditure patterns by carrier."),
                                    ]
                                ),
                                className="welcome-feature",
                            ),
                            width=4,
                            className="mb-3",
                        ),
                        # Network Configuration
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        html.Div(
                                            className="feature-icon", children=html.I(className="fas fa-project-diagram")
                                        ),
                                        html.H5("Network Configuration"),
                                        html.P("Explore network topology and metadata through interactive maps."),
                                    ]
                                ),
                                className="welcome-feature",
                            ),
                            width=4,
                            className="mb-3",
                        ),
                    ],
                    className="mb-4",
                ),
                # Available networks section
                html.Div(
                    [
                        html.H3("Available Networks", className="mt-4 mb-3"),
                        html.Div(
                            id="network-list",
                            children=[  # type: ignore[list-item]
                                html.Div(
                                    [
                                        html.H5(label),
                                        html.P(
                                            f"Nodes: {networks_info[label]['buses']}, "
                                            f"Links: {networks_info[label]['links']}, "
                                            f"Lines: {networks_info[label]['lines']}"
                                        ),
                                    ],
                                    className="network-item",
                                )
                                for label in network_labels
                            ],
                        ),
                        # Enter dashboard button
                        html.Div(
                            [
                                dbc.Button(
                                    "Enter Dashboard",
                                    id="enter-dashboard-btn",
                                    color="primary",
                                    size="lg",
                                    className="mt-4",
                                )
                            ],
                            className="text-center mt-4 mb-5",
                        ),
                    ],
                    className="mt-4",
                ),
            ]
        ),
        className="mt-3",
    )
