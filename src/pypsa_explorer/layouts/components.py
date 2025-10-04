"""Reusable UI components for PyPSA Explorer dashboard."""

from typing import Any

import dash_bootstrap_components as dbc
import pypsa
from dash import dcc, html

# Standard message components
PLEASE_SELECT_CARRIER_MSG = html.Div(
    html.P(
        "Please select one or more carriers.",
        className="lead text-center text-muted my-5",
    ),
    className="w-100",
)

PLEASE_SELECT_COUNTRY_MSG = html.Div(
    html.P(
        "Please select at least one country when 'Select Countries' mode is active.",
        className="lead text-center text-muted my-5",
    ),
    className="w-100",
)

NO_DATA_MSG = html.Div(
    html.P(
        "No data available for the current selection. Try different filters.",
        className="lead text-center text-muted my-5",
    ),
    className="w-100",
)


def create_error_message(context: str, error: Exception) -> html.Div:
    """
    Create a standardized error message component.

    Parameters
    ----------
    context : str
        Description of what was being processed when the error occurred
    error : Exception
        The exception that was raised

    Returns
    -------
    html.Div
        Formatted error message component
    """
    return html.Div(
        [
            html.H5(
                f"Error processing {context}:",
                className="text-danger",
            ),
            html.P(str(error), className="text-muted"),
        ],
        className="text-center p-5 border rounded mb-4",
        style={"background-color": "#f8f9fa"},
    )


def create_header(n: pypsa.Network, network_labels: list[str], active_network_label: str) -> dbc.Row:  # noqa: ARG001
    """
    Create the header section with network selector.

    Parameters
    ----------
    n : pypsa.Network
        The active PyPSA network object
    network_labels : list[str]
        List of available network labels
    active_network_label : str
        Label of the currently active network

    Returns
    -------
    dbc.Row
        Header component with network selector
    """
    return dbc.Row(
        [
            dbc.Col(
                [
                    html.Label("Select Network:", className="fw-bold mt-4"),
                    dcc.Dropdown(
                        id="network-selector",
                        options=[{"label": label, "value": label} for label in network_labels],  # type: ignore[arg-type]
                        value=active_network_label,
                        clearable=False,
                        className="mb-2",
                        style={"width": "100%"},
                    ),
                ],
                width=3,
                className="mt-2",
            ),
            dbc.Col(width=9),
        ]
    )


def create_sidebar_filter_panel(
    bus_carrier_options: list[dict[str, Any]],
    country_options: list[dict[str, str]],
    default_carriers: list[str] | None = None,
) -> html.Div:
    """
    Create a sidebar filter panel for global filters.

    Parameters
    ----------
    bus_carrier_options : list[dict[str, Any]]
        List of carrier options for the checklist
    country_options : list[dict[str, str]]
        List of country options for the dropdown
    default_carriers : list[str] | None
        List of default carriers to select

    Returns
    -------
    html.Div
        Sidebar filter panel component
    """
    # Set default values based on provided carriers
    default_value = []
    if default_carriers:
        valid_carriers = [opt["value"] for opt in bus_carrier_options]
        default_value = [c for c in default_carriers if c in valid_carriers]
    elif bus_carrier_options:
        default_value = [bus_carrier_options[0]["value"]]

    return html.Div(
        [
            html.Div(
                [
                    html.H5("Filters", className="mb-3"),
                    html.Hr(),
                    # Country selection section
                    html.Div(
                        [
                            html.Label(
                                "Countries",
                                className="fw-bold mb-2",
                            ),
                            dcc.RadioItems(
                                id="global-country-mode",
                                options=[  # type: ignore[arg-type]
                                    {"label": " All", "value": "All"},
                                    {"label": " Select", "value": "Specific"},
                                ],
                                value="All",
                                className="mb-2",
                                labelStyle={"display": "block", "marginLeft": "5px"},
                            ),
                            html.Div(
                                [
                                    dcc.Dropdown(
                                        id="global-country-selector",
                                        options=country_options,  # type: ignore[arg-type]
                                        multi=True,
                                        placeholder="Select countries...",
                                        disabled=True,
                                        className="mb-3",
                                    )
                                ],
                                id="global-country-selector-container",
                            ),
                        ],
                        className="mb-4",
                    ),
                    # Carrier selection section
                    html.Div(
                        [
                            html.Label("Sectors", className="fw-bold mb-2"),
                            dcc.Store(id="active-tab-store", data="energy-balance"),
                            html.Div(
                                [
                                    dcc.Checklist(
                                        id="global-carrier-selector",
                                        options=bus_carrier_options,  # type: ignore[arg-type]
                                        value=default_value,
                                        labelStyle={
                                            "display": "block",
                                            "marginLeft": "5px",
                                        },
                                        className="mb-3",
                                    ),
                                ],
                                id="global-carrier-selector-container",
                            ),
                            html.Small(
                                "Not applicable for CAPEX/OPEX",
                                id="carrier-not-applicable-text",
                                className="text-muted",
                                style={"display": "none"},
                            ),
                        ],
                    ),
                ],
                className="sidebar-container",
            )
        ],
        className="sidebar-filter-panel",
    )


def create_footer() -> html.Footer:
    """
    Create the footer section of the dashboard.

    Returns
    -------
    html.Footer
        Footer component
    """
    return html.Footer(
        dbc.Row(
            dbc.Col(
                html.P("Created with PyPSA - Python for Power System Analysis", className="text-center text-muted mt-5 mb-3")
            )
        )
    )
