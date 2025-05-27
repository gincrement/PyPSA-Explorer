# /// script
# requires-python = ">=3.12"
# dependencies = [
#   "plotly",
#   "dash",
#   "folium",
#   "mapclassify",
#   "dash-bootstrap-components",
#   "pypsa @ git+https://github.com/PyPSA/PyPSA.git@master",
# ]
# ///

"""
Interactive PyPSA Network Viewer

This script creates an interactive dashboard to visualize different aspects of an energy system
using PyPSA's interactive plotting capabilities.

Multiple networks can be loaded and viewed through a dropdown selector.
"""

import os
import sys
from typing import Any, Callable

import dash
import dash_bootstrap_components as dbc
import folium
import plotly.graph_objects as go
import plotly.io as pio
import pypsa
import pypsa.consistency
import yaml
from dash import Input, Output, State, dcc, html, no_update
from pypsa.statistics import StatisticsAccessor
import pypsa.examples

# Set default Plotly template for consistent styling
pio.templates.default = "plotly_white"

# Custom Plotly template to match dashboard styling
custom_template = go.layout.Template()
custom_template.layout = go.Layout(
    plot_bgcolor="#f5f7fa",  # Match dashboard background
    paper_bgcolor="#f5f7fa",  # Match dashboard background
    font=dict(family="Roboto, 'Helvetica Neue', sans-serif", color="#2c3e50"),
    xaxis=dict(gridcolor="#e9ecef", zerolinecolor="#e9ecef"),
    yaxis=dict(gridcolor="#e9ecef", zerolinecolor="#e9ecef"),
)
pio.templates["dashboard_theme"] = custom_template
pio.templates.default = "dashboard_theme"

# Custom CSS for the dashboard
dashboard_css = """
/* Custom CSS for improved dashboard styling */
:root {
    --primary-color: #2c3e50; /* Changed primary color to a dark slate blue/grey */
    --secondary-color: #3498db;
    --accent-color: #2ecc71;
    --light-bg: #f8f9fa;
    --dark-bg: #343a40;
    --text-color: var(--primary-color); /* Use primary color as main text color */
    --light-text: #6c757d;
}

/* General styling */
body {
    font-family: 'Roboto', 'Helvetica Neue', sans-serif;
    color: var(--text-color);
    background-color: #f5f7fa;
}

/* Make tab content seamless with background */
.tab-content {
    background-color: transparent !important;
    border: none !important;
}

/* Better card styling - make cards seamless with background */
.card {
    border-radius: 8px;
    box-shadow: none;  /* Remove shadow for cleaner look */
    margin-bottom: 20px;
    border: none;
    background-color: transparent;  /* Make cards transparent */
    transition: transform 0.2s;
}

.card-body {
    background-color: transparent;
    padding: 0;  /* Remove internal padding */
}

/* Header styling */
h1, h2, h3, h4, h5 {
    color: var(--primary-color); /* Use primary color for headings */
    font-weight: 600;
}

/* Better looking tabs for dcc.Tabs */
.tab-container {
    border-bottom: 2px solid var(--light-bg);
    background-color: transparent;
}

.tab {
    border: none;
    color: var(--light-text);
    font-weight: 500;
    padding: 12px 16px;
    margin-right: 4px;
    transition: all 0.2s ease;
    background-color: transparent !important;
    border-bottom: 3px solid transparent;
}

.tab:hover {
    color: var(--secondary-color);
    background-color: rgba(52, 152, 219, 0.1) !important;
}

/* Active/Selected tab styling */
.tab--selected {
    color: var(--secondary-color) !important;
    background-color: #f5f7fa !important;  /* Match dashboard background */
    border-bottom: 3px solid var(--secondary-color) !important;
}

/* Remove default tab styling */
.tab--selected, .tab {
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
}

/* Button styling */
.btn-primary {
    background-color: var(--secondary-color);
    border-color: var(--secondary-color);
}

.btn-primary:hover {
    background-color: #2980b9;
    border-color: #2980b9;
}

/* Dashboard container */
.dashboard-container {
    padding: 20px;
}

/* Welcome page styling */
.welcome-card {
    text-align: center;
    padding: 40px;
    border-radius: 10px;
}

.welcome-header {
    font-size: 3em;
    margin-bottom: 0.5em;
    /* color: var(--primary-color); Inherits from h1 now */
    font-weight: 700;
}

.welcome-subtitle {
    font-size: 1.5em;
    margin-bottom: 1.5em;
    color: var(--primary-color); /* Changed subtitle color for better contrast */
}

.welcome-feature {
    background-color: white;
    border-radius: 8px;
    padding: 20px;
    height: 100%;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s;
}

.welcome-feature:hover {
    transform: translateY(-5px);
}

.feature-icon {
    font-size: 36px;
    margin-bottom: 15px;
    color: var(--secondary-color);
}

.network-item {
    padding: 15px;
    margin: 10px 0;
    background-color: white;
    border-radius: 8px;
    border-left: 4px solid var(--secondary-color);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    transition: transform 0.2s;
}

.network-item:hover {
    transform: translateX(5px);
}

/* Footer styling */
footer {
    margin-top: 50px;
    padding: 20px 0;
    border-top: 1px solid #eee;
}

/* Better dropdown styling */
.Select-control {
    border-radius: 6px;
    border: 1px solid #ced4da;
}

.Select-control:hover {
    border-color: var(--secondary-color);
}

/* Improved button group spacing */
.button-group {
    margin: 20px 0;
}

/* Animation for page transitions */
.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Sidebar filter panel styling */
.sidebar-filter-panel {
    background-color: rgba(255, 255, 255, 0.5);  /* Semi-transparent white */
    border-right: 1px solid rgba(233, 236, 239, 0.5);
    min-height: calc(100vh - 200px);
    padding: 20px;
    border-radius: 8px;
    margin-right: 10px;
}

.sidebar-filter-panel h5 {
    color: var(--primary-color);
    margin-bottom: 15px;
    font-size: 1.1rem;
}

/* Main content area */
.main-content-area {
    padding-left: 20px;
}

/* Sticky sidebar */
.sidebar-container {
    position: sticky;
    top: 20px;
    max-height: calc(100vh - 40px);
    overflow-y: auto;
}

/* Plotly graph styling for seamless integration */
.js-plotly-plot {
    background-color: transparent !important;
}

.js-plotly-plot .plotly {
    border-radius: 8px;
    overflow: hidden;
}

/* Remove Plotly modebar background */
.modebar {
    background-color: transparent !important;
}

.modebar-btn {
    background-color: transparent !important;
}

/* Style the graph containers */
.dash-graph {
    background-color: transparent !important;
    margin-bottom: 20px;
}

/* Remove any borders from graph containers */
.dash-graph > div {
    border: none !important;
}

/* Make tab pane background transparent */
.tab-pane {
    background-color: transparent !important;
}

/* Update welcome card for consistency */
.welcome-card {
    background-color: rgba(255, 255, 255, 0.7);
}

/* Update network metadata display */
#network-metadata {
    background-color: rgba(255, 255, 255, 0.5) !important;
    border: 1px solid rgba(233, 236, 239, 0.5) !important;
}
"""

#  general helpers


def title_except_multi_caps(text: str) -> str:
    """
    Converts all words in a string to title case, except for words
    that already contain multiple uppercase letters.

    Args:
        text (str): The input string to process

    Returns:
        str: The processed string with words in title case,
             except those with multiple uppercase letters
    """
    # Split the text into words
    words = text.split()
    result = []

    for word in words:
        # Count the number of uppercase letters in the word
        uppercase_count = sum(1 for char in word if char.isupper())

        # If the word has multiple uppercase letters, keep it as is
        if uppercase_count > 1:
            result.append(word)
        else:
            # Otherwise, convert to title case
            result.append(word.capitalize())

    # Join the words back together with spaces
    return " ".join(result)


def get_carrier_nice_name(n: pypsa.Network, carrier: str) -> str:
    """
    Retrieves the nice name of a carrier from the network, or falls back to the carrier index if not available.

    Parameters
    ----------
    n : pypsa.Network
        The PyPSA network object.
    carrier : str
        The carrier name to retrieve the nice name for.

    Returns
    -------
    str
        The nice name of the carrier or the carrier index if no nice name is available.
    """
    return title_except_multi_caps(
        n.carriers.nice_name.where(
            n.carriers.nice_name.ne(""), n.carriers.index.to_series()
        ).at[carrier]
    )


def convert_latex_to_html(text: str) -> html.Span:
    """
    Convert LaTeX-style subscripts to HTML.

    Parameters
    ----------
    text : str
        Text that may contain LaTeX subscript notation like H$_2$

    Returns
    -------
    html.Span
        A Dash HTML component with proper subscript formatting
    """
    import re

    # Pattern to match LaTeX subscripts like $_2$ or $_{2}$
    pattern = r"\$_\{?([^$}]+)\}?\$"

    # Split the text by the pattern
    parts = re.split(pattern, text)

    # Build the HTML elements
    elements = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Regular text
            if part:
                elements.append(part)
        else:
            # Subscript text
            elements.append(html.Sub(part))

    return html.Span(elements)


def get_bus_carrier_options(n: pypsa.Network) -> list[dict[str, Any]]:
    """
    Get the bus carrier options for dropdown/checklist components.

    Parameters
    ----------
    n : pypsa.Network
        The PyPSA network object.

    Returns
    -------
    list[dict[str, Any]]
        List of options with label and value for each carrier
    """
    return [
        {
            "label": html.Span(
                [" ", convert_latex_to_html(get_carrier_nice_name(n, carrier))]
            ),  # type: ignore[list-item]
            "value": carrier,
        }
        for carrier in sorted(n.buses.carrier.unique())
        if carrier != "none"
    ]


# --- Standard Message Components ---

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
    """Creates a standardized error message component."""
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


def get_country_filter(
    country_mode: str, selected_countries: list[str]
) -> tuple[str | None, str | None, html.Div | None]:
    """
    Determines the query string and facet column based on country selection.

    Returns:
        tuple: (query, facet_col, error_message_component | None)
    """
    if country_mode == "Specific":
        if not selected_countries:
            return None, None, PLEASE_SELECT_COUNTRY_MSG
        else:
            # Ensure selected_countries are properly formatted for the query
            formatted_countries = [f"'{c}'" for c in selected_countries]
            query = f"country in [{', '.join(formatted_countries)}]"
            return query, "country", None
    # Default is "All" countries
    return None, None, None


# --- Helper Functions for Layout Creation ---


def create_header(
    n: pypsa.Network, network_labels: list[str], active_network_label: str
) -> dbc.Row:
    """Creates the header section of the dashboard with network selector."""
    wildcards = n.meta.get("wildcards", {})
    (f"{wildcards.get('run', 'Unnamed')} {wildcards.get('planning_horizons', '')}")
    return dbc.Row(
        [
            # Network selector dropdown - left aligned
            dbc.Col(
                [
                    html.Label("Select Network:", className="fw-bold mt-4"),
                    dcc.Dropdown(
                        id="network-selector",
                        options=[  # type: ignore[arg-type]
                            {"label": label, "value": label} for label in network_labels
                        ],
                        value=active_network_label,
                        clearable=False,
                        className="mb-2",
                        style={"width": "100%"},
                    ),
                ],
                width=3,
                className="mt-2",
            ),
            # Empty column for balance
            dbc.Col(width=9),
        ]
    )


def create_sidebar_filter_panel(
    bus_carrier_options: list[dict[str, Any]],
    country_options: list[dict[str, str]],
    default_carriers: list[str] | None = None,
) -> html.Div:
    """
    Creates a sidebar filter panel that applies to all visualization tabs.

    Parameters
    ----------
    bus_carrier_options : list
        List of carrier options for the checklist
    country_options : list
        List of country options for the dropdown
    default_carriers : list, optional
        List of default carriers to select

    Returns
    -------
    html.Div
        A div containing the sidebar filter controls
    """
    # Set default values based on provided carriers
    default_value = []
    if default_carriers:
        # Validate carriers exist in options
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
                            # Radio buttons for All vs. Specific Countries
                            dcc.RadioItems(
                                id="global-country-mode",
                                options=[  # type: ignore[arg-type]
                                    {
                                        "label": " All",
                                        "value": "All",
                                    },
                                    {
                                        "label": " Select",
                                        "value": "Specific",
                                    },
                                ],
                                value="All",
                                className="mb-2",
                                labelStyle={"display": "block", "marginLeft": "5px"},
                            ),
                            # Country selection dropdown
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
                            # Store to track active tab for conditional display
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


def create_energy_balance_tab() -> dcc.Tab:
    """Creates the content for the Energy Balance (timeseries) tab."""
    return dcc.Tab(
        label="Energy Balance Timeseries",
        value="energy-balance",
        style={
            "padding": "12px 16px",
            "backgroundColor": "transparent",
            "border": "none",
            "borderBottom": "3px solid transparent",
        },
        selected_style={
            "padding": "12px 16px",
            "backgroundColor": "#f5f7fa",
            "border": "none",
            "borderBottom": "3px solid #3498db",
            "color": "#3498db",
        },
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        # Container for the dynamically generated charts
                        html.Div(id="energy-balance-charts-container"),
                    ]
                ),
                className="mt-3",
            )
        ],
    )


def create_energy_balance_aggregated_tab() -> dcc.Tab:
    """Creates the content for the Aggregated Energy Balance tab."""
    return dcc.Tab(
        label="Energy Balance Totals",
        value="energy-balance-aggregated",
        style={
            "padding": "12px 16px",
            "backgroundColor": "transparent",
            "border": "none",
            "borderBottom": "3px solid transparent",
        },
        selected_style={
            "padding": "12px 16px",
            "backgroundColor": "#f5f7fa",
            "border": "none",
            "borderBottom": "3px solid #3498db",
            "color": "#3498db",
        },
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        # Container for the dynamically generated charts
                        html.Div(id="agg-energy-balance-charts-container"),
                    ]
                ),
                className="mt-3",
            )
        ],
    )


def create_capacity_tab() -> dcc.Tab:
    """Creates the content for the Capacity tab."""
    return dcc.Tab(
        label="Capacity Totals",
        value="capacity",
        style={
            "padding": "12px 16px",
            "backgroundColor": "transparent",
            "border": "none",
            "borderBottom": "3px solid transparent",
        },
        selected_style={
            "padding": "12px 16px",
            "backgroundColor": "#f5f7fa",
            "border": "none",
            "borderBottom": "3px solid #3498db",
            "color": "#3498db",
        },
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        # Container for the dynamically generated charts
                        dbc.Row(id="capacity-charts-container"),
                    ]
                ),
                className="mt-3",
            )
        ],
    )


def create_capex_totals_tab() -> dcc.Tab:
    """Creates the content for the CAPEX Totals tab."""
    return dcc.Tab(
        label="CAPEX Totals",
        value="capex",
        style={
            "padding": "12px 16px",
            "backgroundColor": "transparent",
            "border": "none",
            "borderBottom": "3px solid transparent",
        },
        selected_style={
            "padding": "12px 16px",
            "backgroundColor": "#f5f7fa",
            "border": "none",
            "borderBottom": "3px solid #3498db",
            "color": "#3498db",
        },
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        # Container for the dynamically generated charts
                        dbc.Row(id="capex-charts-container"),
                    ]
                ),
                className="mt-3",
            )
        ],
    )


def create_opex_totals_tab() -> dcc.Tab:
    """Creates the content for the OPEX Totals tab."""
    return dcc.Tab(
        label="OPEX Totals",
        value="opex",
        style={
            "padding": "12px 16px",
            "backgroundColor": "transparent",
            "border": "none",
            "borderBottom": "3px solid transparent",
        },
        selected_style={
            "padding": "12px 16px",
            "backgroundColor": "#f5f7fa",
            "border": "none",
            "borderBottom": "3px solid #3498db",
            "color": "#3498db",
        },
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        # Container for the dynamically generated charts
                        dbc.Row(id="opex-charts-container"),
                    ]
                ),
                className="mt-3",
            )
        ],
    )


def create_network_map_tab() -> dcc.Tab:
    """Creates the content for the Network Configuration tab with map and metadata."""
    return dcc.Tab(
        label="Network Configuration",
        value="network-config",
        style={
            "padding": "12px 16px",
            "backgroundColor": "transparent",
            "border": "none",
            "borderBottom": "3px solid transparent",
        },
        selected_style={
            "padding": "12px 16px",
            "backgroundColor": "#f5f7fa",
            "border": "none",
            "borderBottom": "3px solid #3498db",
            "color": "#3498db",
        },
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                # Left column: Network Metadata
                                dbc.Col(
                                    [
                                        html.H4("Network Metadata", className="mb-3"),
                                        html.Div(
                                            id="network-metadata",
                                            className="bg-light p-3 border rounded",
                                            style={
                                                "height": "700px",
                                                "overflow": "auto",
                                                "white-space": "pre-wrap",
                                                "font-family": "monospace",
                                            },
                                        ),
                                    ],
                                    width=6,
                                ),
                                # Right column: Network Map
                                dbc.Col(
                                    [
                                        html.H4("Network Map", className="mb-3"),
                                        html.Iframe(
                                            id="network-map",
                                            style={
                                                "width": "100%",
                                                "height": "700px",
                                                "border": "1px solid #ddd",
                                            },
                                        ),
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Refresh Map",
                                                    id="refresh-map-button",
                                                    color="primary",
                                                    className="mt-3",
                                                )
                                            ],
                                            className="text-center",
                                        ),
                                    ],
                                    width=6,
                                ),
                            ]
                        ),
                    ]
                ),
                className="mt-3",
            )
        ],
    )


def create_footer() -> html.Footer:
    """Creates the footer section of the dashboard."""
    return html.Footer(
        dbc.Row(
            dbc.Col(
                html.P(
                    "Created with PyPSA - Python for Power System Analysis",
                    className="text-center text-muted mt-5 mb-3",
                )
            )
        )
    )


def create_welcome_page() -> dbc.Card:
    """Creates the welcome page for the dashboard."""
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
                        html.Hr(className="my-4"),  # Add horizontal line here
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
                                        html.Div(
                                            className="feature-icon",
                                            children=html.I(
                                                className="fas fa-chart-area"
                                            ),
                                        ),
                                        html.H5("Energy Balance Timeseries"),
                                        html.P(
                                            "Visualize energy flows over time for different carriers and countries."
                                        ),
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
                                        html.Div(
                                            className="feature-icon",
                                            children=html.I(
                                                className="fas fa-chart-bar"
                                            ),
                                        ),
                                        html.H5("Energy Balance Totals"),
                                        html.P(
                                            "Analyze aggregated energy balances across the system."
                                        ),
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
                                        html.Div(
                                            className="feature-icon",
                                            children=html.I(
                                                className="fas fa-solar-panel"
                                            ),
                                        ),
                                        html.H5("Capacity Totals"),
                                        html.P(
                                            "Explore optimal capacity distribution by carrier and country."
                                        ),
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
                                        html.Div(
                                            className="feature-icon",
                                            children=html.I(className="fas fa-coins"),
                                        ),
                                        html.H5("CAPEX Totals"),
                                        html.P(
                                            "Analyze capital expenditure distribution across the network."
                                        ),
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
                                            className="feature-icon",
                                            children=html.I(
                                                className="fas fa-file-invoice-dollar"
                                            ),
                                        ),
                                        html.H5("OPEX Totals"),
                                        html.P(
                                            "Review operational expenditure patterns by carrier."
                                        ),
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
                                            className="feature-icon",
                                            children=html.I(
                                                className="fas fa-project-diagram"
                                            ),
                                        ),
                                        html.H5("Network Configuration"),
                                        html.P(
                                            "Explore network topology and metadata through interactive maps."
                                        ),
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
            ]
        ),
        className="mt-3",
    )


# --- Main Application Setup ---

# Dictionary to store multiple networks
networks: dict[str, pypsa.Network] = {}
active_network: pypsa.Network | None = None

# Initialize Dash app with Bootstrap themes
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title="",
)

# Add the custom CSS to the app by including it in the layout
app.index_string = (
    """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
"""
    + dashboard_css
    + """
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""
)


def load_network_from_paths(
    path_dict: dict[str, str] | str | None = None,
) -> dict[str, pypsa.Network]:
    """
    Load networks from a dictionary of paths or a single path

    Parameters
    ----------
    path_dict : dict or str
        Either a dictionary {label: path} or a single path string.
        For multiple networks, provide a JSON file path with the format:
        {
            "Network Label 1": "/path/to/network1.nc",
            "Network Label 2": "/path/to/network2.nc"
        }

    Returns
    -------
    dict
        Dictionary of loaded networks {label: network}
    """
    global networks

    if path_dict is None:
        # Default example network if nothing is provided
        n = pypsa.Network("demo-network.nc")
        networks = {"Network": n}
    elif isinstance(path_dict, str):
        # Single network path provided
        if os.path.exists(path_dict):
            networks = {"Network": pypsa.Network(path_dict)}
        else:
            raise FileNotFoundError(f"Network file not found: {path_dict}")
    elif isinstance(path_dict, dict):
        # Dictionary of networks provided
        networks = {}
        for label, path in path_dict.items():
            if os.path.exists(path):
                networks[label] = pypsa.Network(path)
            else:
                print(f"Warning: Network file not found: {path}")
    else:
        raise ValueError(
            "path_dict must be either a string path or a dictionary {label: path}"
        )

    if not networks:
        raise ValueError("No valid networks were loaded")

    return networks


if len(sys.argv) > 1:
    # Parse command line arguments in format path:label
    network_paths = {}
    for arg in sys.argv[1:]:
        if ":" in arg:
            path, label = arg.split(":", 1)
        else:
            path = arg
            # Create default label from filename
            label = os.path.splitext(os.path.basename(path))[0]
        network_paths[label] = path
    networks = load_network_from_paths(network_paths)
else:
    # Use default
    networks = load_network_from_paths()

# Get the first network as the active network initially
network_labels: list[str] = list(networks.keys())
active_network_label: str = network_labels[0]
n: pypsa.Network = networks[active_network_label]

# Ensure plotting consistency for active network
pypsa.consistency.plotting_consistency_check(n)

# Access statistics
s: StatisticsAccessor = n.statistics

# Get unique bus carriers for the dropdown
bus_carrier_options: list[dict[str, Any]] = get_bus_carrier_options(n)

# Get unique countries for the country selector dropdown
country_options: list[dict[str, str]] = [
    {"label": country, "value": country} for country in n.buses.country.unique()
]
# Sort country options alphabetically for better UX
country_options.sort(key=lambda x: x["label"])
# Add "All" option at the beginning
country_all_option: dict[str, str] = {"label": "All", "value": "All"}

# Create layout using helper functions
app.layout = dbc.Container(
    fluid=True,
    children=[
        # Store component to manage page state
        dcc.Store(id="page-state", data={"current_page": "welcome"}),
        # Main application layout with conditional display
        html.Div(
            id="main-content",
            className="fade-in",
            children=[
                # Welcome page content will be shown initially
                html.Div(
                    id="welcome-content",
                    children=[
                        create_welcome_page(),
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
                                                    f"Nodes: {len(networks[label].buses)}, "
                                                    f"Links: {len(networks[label].links)}, "
                                                    f"Lines: {len(networks[label].lines)}"
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
                    ],
                ),
                # Main dashboard content (initially hidden)
                html.Div(
                    id="dashboard-content",
                    style={"display": "none"},
                    children=[
                        create_header(n, network_labels, active_network_label),
                        # Main content with sidebar layout
                        dbc.Row(
                            [
                                # Sidebar with filters
                                dbc.Col(
                                    create_sidebar_filter_panel(
                                        bus_carrier_options,
                                        country_options,
                                        default_carriers=[
                                            "AC",
                                            "Hydrogen Storage",
                                            "Low Voltage",
                                        ],
                                    ),
                                    width=3,
                                    className="p-0",
                                ),
                                # Main content area
                                dbc.Col(
                                    dcc.Tabs(
                                        id="tabs",
                                        style={
                                            "borderBottom": "2px solid #f8f9fa",
                                            "marginBottom": "20px",
                                        },
                                        parent_style={"backgroundColor": "#f5f7fa"},
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
)

# --- Callbacks ---


def create_energy_balance_callback(
    aggregated: bool = False,
) -> Callable[
    [list[str], str, list[str]],
    Any,  # Simplified return type hint
]:
    """
    Creates a callback function for updating energy balance charts.

    Parameters
    ----------
    aggregated : bool
        Whether to create a callback for aggregated (True) or timeseries (False) views

    Returns
    -------
    Callable[[list[str], str, list[str]], list[dbc.Col | html.Div | dcc.Graph] | html.Div]
        A callback function for updating energy balance charts
    """

    def update_energy_balance(
        selected_carriers: list[str], country_mode: str, selected_countries: list[str]
    ) -> list[dbc.Col | html.Div | dcc.Graph] | html.Div:
        if not selected_carriers:
            # Use standard message
            return (
                [PLEASE_SELECT_CARRIER_MSG] if aggregated else PLEASE_SELECT_CARRIER_MSG
            )

        # Use helper for country filtering
        query, facet_col, error_message = get_country_filter(
            country_mode, selected_countries
        )
        if error_message:
            return [error_message] if aggregated else error_message

        charts: list[dbc.Col | html.Div | dcc.Graph] = []

        for carrier in selected_carriers:
            try:
                # Generate plot based on view type
                fig: go.Figure
                plot_args = {
                    "x": "value",
                    "y": "carrier",
                    "color": "carrier",
                    "bus_carrier": carrier,
                    "nice_names": True,
                    "width": None,
                    "query": query,
                    "facet_col": facet_col,
                }
                if aggregated:
                    # Bar plot for aggregated view
                    fig = s.energy_balance.iplot.bar(**plot_args)
                else:
                    # Area plot for timeseries view
                    # Update args for area plot
                    plot_args.update(
                        {
                            "x": "snapshot",
                            "y": "value",
                            "stacked": True,
                            "height": 500,
                        }
                    )
                    fig = s.energy_balance.iplot.area(**plot_args)
                    # Adjust layout for area plot
                    fig.update_layout(
                        legend_title="Component Carrier",
                        hovermode="closest",
                        paper_bgcolor="#f5f7fa",
                        plot_bgcolor="#f5f7fa",
                    )

                # Common title setting
                carrier_name = get_carrier_nice_name(n, carrier)

                title = f"{'Aggregated Balance' if aggregated else 'Energy Balance'} for {carrier_name}"
                if facet_col and selected_countries:  # Check if filtering applied
                    countries_str = ", ".join(selected_countries)
                    title += f" (Countries: {countries_str})"

                fig.update_layout(
                    title=title, paper_bgcolor="#f5f7fa", plot_bgcolor="#f5f7fa"
                )

                graph_component = dcc.Graph(figure=fig)
                charts.append(graph_component)

            except Exception as e:
                # Use standard error message function
                error_context = f"carrier '{carrier}'"
                carrier_error_message = create_error_message(error_context, e)
                charts.append(carrier_error_message)

        # If no charts were created successfully, show a message
        if not charts:
            # Use standard message
            return [NO_DATA_MSG] if aggregated else NO_DATA_MSG

        return charts

    return update_energy_balance


# Callback for Energy Balance charts (timeseries view)
@app.callback(
    Output("energy-balance-charts-container", "children"),
    [
        Input("global-carrier-selector", "value"),
        Input("global-country-mode", "value"),
        Input("global-country-selector", "value"),
        Input("network-selector", "value"),
    ],
)
def update_energy_balance(
    selected_carriers: list[str],
    country_mode: str,
    selected_countries: list[str],
    selected_network_label: str,
) -> list[dbc.Col | html.Div | dcc.Graph] | html.Div:
    global n, s
    n = networks[selected_network_label]
    s = n.statistics
    return create_energy_balance_callback(aggregated=False)(
        selected_carriers, country_mode, selected_countries
    )


# Callback for Aggregated Energy Balance charts
@app.callback(
    Output("agg-energy-balance-charts-container", "children"),
    [
        Input("global-carrier-selector", "value"),
        Input("global-country-mode", "value"),
        Input("global-country-selector", "value"),
        Input("network-selector", "value"),
    ],
)
def update_energy_balance_aggregated(
    selected_carriers: list[str],
    country_mode: str,
    selected_countries: list[str],
    selected_network_label: str,
) -> list[dbc.Col | html.Div | dcc.Graph] | html.Div:
    global n, s
    n = networks[selected_network_label]
    s = n.statistics
    return create_energy_balance_callback(aggregated=True)(
        selected_carriers, country_mode, selected_countries
    )


# Callback for the network map
@app.callback(
    Output("network-map", "srcDoc"),
    [
        Input("refresh-map-button", "n_clicks"),
        Input("network-selector", "value"),
    ],
)
def update_map(n_clicks: int | None, selected_network_label: str) -> str:
    n = networks[selected_network_label]
    try:
        # Create a folium map using PyPSA's explore method
        map_obj: folium.Map = n.plot.explore(
            tooltip=True, popup=True, components=["Bus", "Line", "Link"]
        )
        return map_obj._repr_html_()
    except Exception as e:
        print(f"Error creating map: {e}")
        # Return a placeholder when map creation fails
        return f"<div style='padding:20px;'><h2>Map visualization unavailable</h2><p>Error: {str(e)}</p></div>"


# Callback to display network metadata
@app.callback(
    Output("network-metadata", "children"),
    [
        Input("refresh-map-button", "n_clicks"),
        Input("network-selector", "value"),
    ],
)
def update_metadata(
    n_clicks: int | None, selected_network_label: str
) -> html.Pre | html.Div:
    n = networks[selected_network_label]
    try:
        # Convert network metadata to YAML format
        metadata_yaml: str = yaml.dump(
            n.meta, default_flow_style=False, sort_keys=False
        )

        # Create a pre-formatted block with syntax highlighting for displaying YAML
        return html.Pre(
            metadata_yaml,
            style={
                "background-color": "#f8f9fa",
                "padding": "10px",
                "border-radius": "5px",
                "color": "var(--text-color)",
            },
        )
    except Exception as e:
        print(f"Error displaying metadata: {e}")
        # Return a placeholder when metadata display fails
        return html.Div(
            [
                html.H5("Metadata Unavailable", className="text-muted"),
                html.P(f"Error: {str(e)}", className="text-danger"),
            ]
        )


# Callback for enabling/disabling global country selector based on mode
@app.callback(
    [
        Output("global-country-selector", "disabled"),
        Output("global-country-selector", "value"),
    ],
    [Input("global-country-mode", "value")],
)
def toggle_global_country_selector(mode: str) -> tuple[bool, list[Any]]:
    if mode == "All":
        # If "All" is selected, disable the dropdown and clear its value
        return True, []
    else:
        # If "Specific" is selected, enable the dropdown and clear value
        return False, []


# Callback for Capacity charts
@app.callback(
    Output("capacity-charts-container", "children"),
    [
        Input("global-carrier-selector", "value"),
        Input("global-country-mode", "value"),
        Input("global-country-selector", "value"),
        Input("network-selector", "value"),
    ],
)
def update_capacity_charts(
    selected_carriers: list[str],
    country_mode: str,
    selected_countries: list[str],
    selected_network_label: str,
) -> list[dcc.Graph | html.Div]:
    global n, s
    n = networks[selected_network_label]
    s = n.statistics
    if not selected_carriers:
        # Use standard message
        return [PLEASE_SELECT_CARRIER_MSG]

    # Use helper for country filtering
    query, facet_col, error_message = get_country_filter(
        country_mode, selected_countries
    )
    if error_message:
        return [error_message]

    charts: list[dcc.Graph | html.Div] = []

    for carrier in selected_carriers:
        try:
            # Generate capacity bar chart directly with carrier
            fig: go.Figure = s.optimal_capacity.iplot.bar(
                x="value",
                y="carrier",
                color="carrier",
                bus_carrier=carrier,
                width=None,
                height=500,
                nice_names=True,
                query=query,
                facet_col=facet_col,
            )

            # Set title based on selections
            carrier_name = get_carrier_nice_name(n, carrier)
            title = f"Optimal Capacity for {carrier_name}"
            if facet_col and selected_countries:  # Check if filtering applied
                countries_str = ", ".join(selected_countries)
                title += f" (Countries: {countries_str})"

            fig.update_layout(
                title=title, paper_bgcolor="#f5f7fa", plot_bgcolor="#f5f7fa"
            )  # Update title in layout

            # Add the graph without wrapping in dbc.Col so it takes full width
            charts.append(dcc.Graph(figure=fig, className="mb-4"))

        except Exception as e:
            # Use standard error message function
            message = create_error_message(f"carrier '{carrier}'", e)
            charts.append(message)

    # If no charts were created successfully, show a message
    if not charts:
        # Use standard message
        return [NO_DATA_MSG]

    return charts


# Callback to handle tab-specific UI elements (hide carrier selection for CAPEX/OPEX)
@app.callback(
    [
        Output("global-carrier-selector-container", "style"),
        Output("carrier-not-applicable-text", "style"),
        Output("active-tab-store", "data"),
    ],
    [Input("tabs", "value")],
)
def handle_tab_specific_ui(
    active_tab: str,
) -> tuple[dict[str, str], dict[str, str], str]:
    """Handle UI elements based on the active tab."""
    if active_tab in ["capex", "opex"]:
        # Hide carrier selector for CAPEX/OPEX tabs
        return {"display": "none"}, {"display": "block"}, active_tab
    else:
        # Show carrier selector for other tabs
        return {"display": "block"}, {"display": "none"}, active_tab


# Callback for CAPEX charts
@app.callback(
    Output("capex-charts-container", "children"),
    [
        Input("global-country-mode", "value"),
        Input("global-country-selector", "value"),
        Input("network-selector", "value"),
    ],
)
def update_capex_charts(
    country_mode: str, selected_countries: list[str], selected_network_label: str
) -> list[dcc.Graph | html.Div]:
    global n, s
    n = networks[selected_network_label]
    s = n.statistics

    # Use helper for country filtering
    query, facet_col, error_message = get_country_filter(
        country_mode, selected_countries
    )
    if error_message:
        return [error_message]

    try:
        # Generate CAPEX bar chart
        fig: go.Figure = s.capex.iplot.bar(
            x="value",
            y="carrier",
            color="carrier",
            nice_names=True,
            height=1000,
            width=None,
            query=query,
            facet_col=facet_col,
        )

        # Set title based on selections
        title = "Capital Expenditure Totals"
        if facet_col and selected_countries:  # Check if filtering applied
            countries_str = ", ".join(selected_countries)
            title += f" (Countries: {countries_str})"

        # Apply robust height settings to prevent resizing
        fig.update_layout(
            title=title,
            height=1000,
            margin=dict(l=50, r=50, t=100, b=50),
            paper_bgcolor="#f5f7fa",
            plot_bgcolor="#f5f7fa",
        )

        # Return the graph with explicit height in component
        return [
            dcc.Graph(
                figure=fig,
                className="mb-4",
                style={"height": "1000px"},
            )
        ]

    except Exception as e:
        # Use standard error message function
        message = create_error_message("CAPEX chart", e)
        return [message]


# Callback for OPEX charts
@app.callback(
    Output("opex-charts-container", "children"),
    [
        Input("global-country-mode", "value"),
        Input("global-country-selector", "value"),
        Input("network-selector", "value"),
    ],
)
def update_opex_charts(
    country_mode: str, selected_countries: list[str], selected_network_label: str
) -> list[dcc.Graph | html.Div]:
    global n, s
    n = networks[selected_network_label]
    s = n.statistics

    # Use helper for country filtering
    query, facet_col, error_message = get_country_filter(
        country_mode, selected_countries
    )
    if error_message:
        return [error_message]

    try:
        # Generate OPEX bar chart
        fig: go.Figure = s.opex.iplot.bar(
            x="value",
            y="carrier",
            color="carrier",
            nice_names=True,
            height=1000,
            width=None,
            query=query,
            facet_col=facet_col,
        )

        # Set title based on selections
        title = "Operational Expenditure Totals"
        if facet_col and selected_countries:  # Check if filtering applied
            countries_str = ", ".join(selected_countries)
            title += f" (Countries: {countries_str})"

        # Apply robust height settings to prevent resizing
        fig.update_layout(
            title=title,
            height=1000,
            margin=dict(l=50, r=50, t=100, b=50),
            paper_bgcolor="#f5f7fa",
            plot_bgcolor="#f5f7fa",
        )

        # Return the graph with explicit height in component
        return [
            dcc.Graph(
                figure=fig,
                className="mb-4",
                style={"height": "1000px"},
            )
        ]

    except Exception as e:
        # Use standard error message function
        message = create_error_message("OPEX chart", e)
        return [message]


# Callback for network selector
@app.callback(
    [
        Output("global-carrier-selector", "options"),
        Output("global-country-selector", "options"),
    ],
    [Input("network-selector", "value")],
)
def update_selected_network(
    selected_network_label: str,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, str]],
]:
    """Update the active network when user selects a different network"""
    global n, s  # Indicate modification of globals

    # Update the active network
    n = networks[selected_network_label]

    # Ensure plotting consistency for the newly selected network
    pypsa.consistency.plotting_consistency_check(n)

    # Update statistics for the new network
    s = n.statistics

    # Update bus carrier options for the new network
    updated_bus_carrier_options = get_bus_carrier_options(n)

    # Update country options for the new network
    updated_country_options = sorted(
        [{"label": c, "value": c} for c in n.buses.country.unique()],
        key=lambda x: x["label"],
    )

    # Return all updated values
    return (
        updated_bus_carrier_options,
        updated_country_options,
    )


# Callback for managing page state and navigation
@app.callback(
    [
        Output("welcome-content", "style"),
        Output("dashboard-content", "style"),
        Output("page-state", "data"),
    ],
    [Input("enter-dashboard-btn", "n_clicks")],
    [State("page-state", "data")],
)
def navigate_pages(
    n_clicks: int | None, page_state: dict[str, str]
) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
    """Manage navigation between welcome page and dashboard"""
    if n_clicks and page_state["current_page"] == "welcome":
        return {"display": "none"}, {"display": "block"}, {"current_page": "dashboard"}
    # Return current state if no click or already on dashboard
    return no_update, no_update, no_update  # type: ignore[return-value]


# Run the app
if __name__ == "__main__":
    print("Starting Energy System Dashboard...")
    # Consider adding host='0.0.0.0' if running in a container or VM
    app.run(debug=True)


# Function to run the dashboard with multiple networks
def run_dashboard(
    networks_dict: dict[str, pypsa.Network | str] | None = None, debug: bool = True
) -> None:
    """
    Run the dashboard with one or more networks.

    Parameters
    ----------
    networks_dict : dict, optional
        A dictionary of {label: network_object_or_path} containing PyPSA networks
        or paths to network files. If not provided, will attempt to load a default network.
    debug : bool, default True
        Whether to run the app in debug mode
    """
    global \
        networks, \
        n, \
        s, \
        network_labels, \
        active_network_label, \
        bus_carrier_options, \
        country_options

    temp_networks: dict[str, pypsa.Network] = {}
    if networks_dict is not None:
        if not isinstance(networks_dict, dict):
            raise ValueError(
                "networks_dict must be a dictionary in the form {label: network_or_path}"
            )

        # Load networks if paths are provided
        for label, net_or_path in networks_dict.items():
            if isinstance(net_or_path, str):
                if os.path.exists(net_or_path):
                    temp_networks[label] = pypsa.Network(net_or_path)
                else:
                    print(f"Warning: Network file not found: {net_or_path}")
            elif isinstance(net_or_path, pypsa.Network):
                temp_networks[label] = net_or_path
            else:
                print(f"Warning: Invalid type for network {label}. Skipping.")

        if not temp_networks:
            raise ValueError("No valid networks could be loaded from networks_dict")

        # Store the loaded networks globally
        networks = temp_networks

        # Set up the active network
        network_labels = list(networks.keys())
        active_network_label = network_labels[0]
        n = networks[active_network_label]

        # Ensure plotting consistency for active network
        pypsa.consistency.plotting_consistency_check(n)

        # Access statistics
        s = n.statistics

        # Update global options based on the loaded network
        bus_carrier_options = get_bus_carrier_options(n)
        country_options = [
            {"label": country, "value": country} for country in n.buses.country.unique()
        ]
        country_options.sort(key=lambda x: x["label"])

        # --- Need to update the layout components with new options ---
        # This part is tricky because the layout is defined globally before this function runs.
        # A better approach would be to define the layout *inside* a function or update
        # the relevant components directly here if possible, but Dash layout is static by default.
        # For now, we assume the initial layout creation uses the first network loaded via CLI or default.
        # If run_dashboard is the primary entry point, layout generation needs rethinking.
        print("Warning: Layout options might not reflect the network passed to ")
        print(
            "run_dashboard if it differs significantly from the initially loaded one."
        )

    elif not networks:  # If no networks_dict and no networks loaded via CLI
        print("Loading default network for run_dashboard...")
        networks = load_network_from_paths()  # Load default
        # Re-initialize globals based on default network
        network_labels = list(networks.keys())
        active_network_label = network_labels[0]
        n = networks[active_network_label]
        pypsa.consistency.plotting_consistency_check(n)
        s = n.statistics
        bus_carrier_options = get_bus_carrier_options(n)
        country_options = [
            {"label": country, "value": country} for country in n.buses.country.unique()
        ]
        country_options.sort(key=lambda x: x["label"])
        # Again, layout components need updating ideally.

    print("Starting Energy System Dashboard...")
    # Use run_server for programmatic execution
    app.run_server(debug=debug)
