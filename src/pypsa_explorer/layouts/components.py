"""Reusable UI components for PyPSA Explorer dashboard."""

from typing import Any

import dash_bootstrap_components as dbc
import pypsa
from dash import dash_table, dcc, html

from pypsa_explorer.utils.data_table import DATATABLE_BASE_CONFIG

# Standard message components with enhanced visuals
PLEASE_SELECT_CARRIER_MSG = html.Div(
    [
        html.Div(
            [html.I(className="fas fa-filter", style={"fontSize": "3rem", "color": "#4ECDC4", "marginBottom": "20px"})],
        ),
        html.H4("Select Carriers", style={"marginBottom": "12px", "fontWeight": "600"}),
        html.P(
            "Please select one or more energy carriers to view data.",
            className="text-muted",
            style={"fontSize": "1rem"},
        ),
    ],
    className="text-center my-5 p-5 empty-state",
)

PLEASE_SELECT_COUNTRY_MSG = html.Div(
    [
        html.Div(
            [html.I(className="fas fa-globe", style={"fontSize": "3rem", "color": "#4ECDC4", "marginBottom": "20px"})],
        ),
        html.H4("Select Countries", style={"marginBottom": "12px", "fontWeight": "600"}),
        html.P(
            "Please select at least one country when 'Select Countries' mode is active.",
            className="text-muted",
            style={"fontSize": "1rem"},
        ),
    ],
    className="text-center my-5 p-5 empty-state",
)

NO_DATA_MSG = html.Div(
    [
        html.Div(
            [
                html.I(
                    className="fas fa-database",
                    style={"fontSize": "3rem", "color": "#FFB84D", "marginBottom": "20px"},
                )
            ],
        ),
        html.H4("No Data Available", style={"marginBottom": "12px", "fontWeight": "600"}),
        html.P(
            "No data found for the current selection. Try adjusting your filters.",
            className="text-muted",
            style={"fontSize": "1rem"},
        ),
    ],
    className="text-center my-5 p-5 empty-state empty-state--warning",
)


def create_dark_mode_toggle() -> html.Div:
    """Create the dark mode toggle control."""

    return html.Div(
        [
            html.Div(
                [
                    html.I(className="fas fa-moon", style={"marginRight": "8px", "fontSize": "0.9rem"}),
                    html.Span("Dark Mode", style={"fontSize": "0.9rem", "fontWeight": "600"}),
                ],
                className="dark-mode-toggle-label",
                style={"display": "flex", "alignItems": "center"},
            ),
            dbc.Checklist(
                id="dark-mode-toggle",
                options=[{"label": "", "value": "dark"}],
                value=[],
                switch=True,
                persistence=True,
                persistence_type="local",
                style={"transform": "scale(1.05)"},
            ),
        ],
        id="dark-mode-toggle-container",
        className="dark-mode-toggle",
    )


def create_top_bar(network_labels: list[str], active_network_label: str) -> html.Div:
    """Create the primary top bar with branding, network selection, and display controls."""

    return html.Div(
        [
            html.Div(
                [
                    html.H1("⚡ PyPSA Explorer", className="utility-brand__title"),
                    html.Span(
                        "Energy System Analysis & Visualization",
                        className="utility-brand__subtitle",
                    ),
                ],
                className="utility-bar__brand",
            ),
            html.Div(
                [
                    html.Div(
                        [
                            html.Span("Network", className="utility-label d-none d-md-inline"),
                            html.Div(
                                [
                                    html.Button(
                                        label,
                                        id={"type": "network-button", "index": label},
                                        n_clicks=0,
                                        className=f"network-button {'network-button-active' if label == active_network_label else ''}",
                                    )
                                    for label in network_labels
                                ],
                                className="network-button-group",
                            ),
                            # Hidden store to track selected network
                            dcc.Store(id="network-selector", data=active_network_label),
                        ],
                        id="top-bar-network-selector",
                        className="top-bar__selector",
                        style={"display": "flex" if len(network_labels) > 1 else "none"},
                    ),
                    html.Div(
                        [
                            create_dark_mode_toggle(),
                        ],
                        className="utility-bar__controls",
                    ),
                ],
                className="utility-bar__actions",
            ),
        ],
        className="utility-bar",
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
        style={"background-color": "#FAFBFC"},
    )


def create_header(n: pypsa.Network) -> html.Div:
    """Create the KPI section for the active network."""

    total_buses = len(n.buses)
    total_generators = len(n.generators) if hasattr(n, "generators") else 0
    total_lines = len(n.lines) if hasattr(n, "lines") else 0
    total_links = len(n.links) if hasattr(n, "links") else 0
    total_storage_units = len(n.storage_units) if hasattr(n, "storage_units") else 0
    total_stores = len(n.stores) if hasattr(n, "stores") else 0

    return html.Div(
        [
            dbc.Row(
                [
                    dbc.Col(
                        html.Div(
                            [
                                html.Div([html.I(className="fas fa-circle-nodes")], className="kpi-icon"),
                                html.Div(str(total_buses), className="kpi-value"),
                                html.Div("Nodes", className="kpi-label"),
                            ],
                            id="kpi-card-buses",
                            n_clicks=0,
                            className="kpi-card kpi-card-clickable",
                            role="button",
                            tabIndex="0",
                            **{"aria-label": "View detailed bus data"},
                        ),
                        xs=12,
                        sm=6,
                        md=4,
                        lg=2,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div([html.I(className="fas fa-bolt")], className="kpi-icon"),
                                html.Div(str(total_generators), className="kpi-value"),
                                html.Div("Generators", className="kpi-label"),
                            ],
                            id="kpi-card-generators",
                            n_clicks=0,
                            className="kpi-card kpi-card-clickable",
                            role="button",
                            tabIndex="0",
                            **{"aria-label": "View detailed generator data"},
                        ),
                        xs=12,
                        sm=6,
                        md=4,
                        lg=2,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div([html.I(className="fas fa-bezier-curve")], className="kpi-icon"),
                                html.Div(str(total_lines), className="kpi-value"),
                                html.Div("Lines", className="kpi-label"),
                            ],
                            id="kpi-card-lines",
                            n_clicks=0,
                            className="kpi-card kpi-card-clickable",
                            role="button",
                            tabIndex="0",
                            **{"aria-label": "View detailed line data"},
                        ),
                        xs=12,
                        sm=6,
                        md=4,
                        lg=2,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div([html.I(className="fas fa-link")], className="kpi-icon"),
                                html.Div(str(total_links), className="kpi-value"),
                                html.Div("Links", className="kpi-label"),
                            ],
                            id="kpi-card-links",
                            n_clicks=0,
                            className="kpi-card kpi-card-clickable",
                            role="button",
                            tabIndex="0",
                            **{"aria-label": "View detailed link data"},
                        ),
                        xs=12,
                        sm=6,
                        md=4,
                        lg=2,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div([html.I(className="fas fa-battery-three-quarters")], className="kpi-icon"),
                                html.Div(str(total_storage_units), className="kpi-value"),
                                html.Div("Storage Units", className="kpi-label"),
                            ],
                            id="kpi-card-storage_units",
                            n_clicks=0,
                            className="kpi-card kpi-card-clickable",
                            role="button",
                            tabIndex="0",
                            **{"aria-label": "View detailed storage unit data"},
                        ),
                        xs=12,
                        sm=6,
                        md=4,
                        lg=2,
                    ),
                    dbc.Col(
                        html.Div(
                            [
                                html.Div([html.I(className="fas fa-warehouse")], className="kpi-icon"),
                                html.Div(str(total_stores), className="kpi-value"),
                                html.Div("Stores", className="kpi-label"),
                            ],
                            id="kpi-card-stores",
                            n_clicks=0,
                            className="kpi-card kpi-card-clickable",
                            role="button",
                            tabIndex="0",
                            **{"aria-label": "View detailed store data"},
                        ),
                        xs=12,
                        sm=6,
                        md=4,
                        lg=2,
                    ),
                ],
                className="g-3",
            )
        ],
        className="app-header",
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


def create_data_explorer_modal() -> dbc.Modal:
    """
    Create a modal for exploring component dataframes.

    Returns
    -------
    dbc.Modal
        Modal component with tabs for static and time-series data
    """
    return dbc.Modal(
        [
            # Store for tracking active component (avoids fragile string parsing)
            dcc.Store(id="active-component-store", data=None),
            dbc.ModalHeader(
                dbc.ModalTitle(id="data-explorer-modal-title", children="Component Data"),
                close_button=True,
            ),
            dbc.ModalBody(
                [
                    # Tabs for static vs time-series data
                    dbc.Tabs(
                        id="data-explorer-tabs",
                        active_tab="static-data",
                        children=[
                            dbc.Tab(
                                label="Static Data",
                                tab_id="static-data",
                                children=[
                                    html.Div(
                                        id="static-data-container",
                                        className="mt-3",
                                        children=[
                                            dash_table.DataTable(
                                                id="static-data-table",
                                                **DATATABLE_BASE_CONFIG,
                                            )
                                        ],
                                    )
                                ],
                            ),
                            dbc.Tab(
                                label="Time-Series Data",
                                tab_id="timeseries-data",
                                children=[
                                    html.Div(
                                        className="mt-3",
                                        children=[
                                            # Time-series attribute selector
                                            html.Div(
                                                [
                                                    html.Label(
                                                        "Select Attribute:",
                                                        className="fw-bold mb-2",
                                                    ),
                                                    dcc.Dropdown(
                                                        id="timeseries-attribute-selector",
                                                        placeholder="Select time-series attribute...",
                                                        className="mb-2",
                                                    ),
                                                    html.Small(
                                                        [
                                                            html.I(className="fas fa-info-circle me-1"),
                                                            "Large datasets (>5000 rows) are sampled for display. Use CSV export for full data.",
                                                        ],
                                                        className="text-muted d-block mb-3",
                                                    ),
                                                ],
                                                id="timeseries-controls",
                                            ),
                                            # Time-series data display
                                            html.Div(
                                                id="timeseries-data-container",
                                                children=[
                                                    dash_table.DataTable(
                                                        id="timeseries-data-table",
                                                        **DATATABLE_BASE_CONFIG,
                                                    )
                                                ],
                                            ),
                                        ],
                                    )
                                ],
                            ),
                        ],
                    )
                ]
            ),
            dbc.ModalFooter(dbc.Button("Close", id="close-data-explorer-modal", className="ms-auto", n_clicks=0)),
        ],
        id="data-explorer-modal",
        size="xl",
        is_open=False,
        scrollable=True,
        labelledby="data-explorer-modal-title",
    )
