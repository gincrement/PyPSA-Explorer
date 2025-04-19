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

import dash
import dash_bootstrap_components as dbc
import plotly.io as pio
import pypsa
import pypsa.consistency
import yaml
from dash import Input, Output, State, dcc, html
import pypsa.examples

# Set default Plotly template for consistent styling
pio.templates.default = "plotly_white"

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

/* Better card styling */
.card {
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    margin-bottom: 20px;
    border: none;
    transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
    box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

/* Header styling */
h1, h2, h3, h4, h5 {
    color: var(--primary-color); /* Use primary color for headings */
    font-weight: 600;
}

/* Better looking tabs */
.nav-tabs {
    border-bottom: 2px solid var(--light-bg);
}

.nav-tabs .nav-link {
    border: none;
    color: var(--light-text);
    font-weight: 500;
    padding: 12px 16px;
    margin-right: 4px;
    transition: all 0.2s ease;
}

.nav-tabs .nav-link:hover {
    color: var(--secondary-color);
    background-color: rgba(52, 152, 219, 0.1);
    border-color: transparent;
}

.nav-tabs .nav-link.active {
    color: var(--secondary-color);
    background-color: white;
    border-bottom: 3px solid var(--secondary-color);
    border-top: none;
    border-left: none;
    border-right: none;
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
"""

#  general helpers


def title_except_multi_caps(text):
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


# --- Helper Functions for Layout Creation ---


def create_header(n, network_labels, active_network_label):
    """Creates the header section of the dashboard with network selector."""
    wildcards = n.meta.get("wildcards", {})
    from_meta = (
        f"{wildcards.get('run', 'Unnamed')} {wildcards.get('planning_horizons', '')}"
    )
    return dbc.Row(
        [
            # Network selector dropdown - left aligned
            dbc.Col(
                [
                    html.Label("Select Network:", className="fw-bold mt-4"),
                    dcc.Dropdown(
                        id="network-selector",
                        options=[
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
            # Main title - center aligned
            dbc.Col(
                [
                    html.H1(
                        "ESM Network Viewer",
                        className="text-center my-4",
                    ),
                    html.H3(
                        f"Network: {n.name or from_meta}",
                        id="network-title",
                        className="text-center",
                    ),
                ],
                width=6,
            ),
            # Empty column for balance
            dbc.Col(width=3),
        ]
    )


def create_selection_panel(
    id_prefix, bus_carrier_options, country_options, default_carriers=None
):
    """
    Creates a reusable selection panel for countries and carriers.

    Parameters
    ----------
    id_prefix : str
        Prefix for the component IDs (e.g., 'balance' or 'agg-balance')
    bus_carrier_options : list
        List of carrier options for the dropdown
    country_options : list
        List of country options for the dropdown
    default_carriers : list, optional
        List of default carriers to select

    Returns
    -------
    dash component
        A column containing the selection controls
    """
    # Add "all" option if it should be the default
    carrier_options = bus_carrier_options.copy()

    # Set default values based on provided carriers
    default_value = []
    if default_carriers:
        # Validate carriers exist in options
        valid_carriers = [opt["value"] for opt in carrier_options]
        default_value = [c for c in default_carriers if c in valid_carriers]
    elif carrier_options:
        default_value = [carrier_options[0]["value"]]

    return dbc.Col(
        [
            # Country selection section
            html.Label(
                "Select Countries:",
                className="fw-bold mb-2",
            ),
            # Radio buttons for All vs. Specific Countries
            dcc.RadioItems(
                id=f"{id_prefix}-country-mode",
                options=[
                    {
                        "label": " All Countries",
                        "value": "All",
                    },
                    {
                        "label": " Select Countries",
                        "value": "Specific",
                    },
                ],
                value="All",
                className="mb-2",
                labelStyle={"display": "block"},
            ),
            # Country selection dropdown, shown only when specific countries are selected
            html.Div(
                [
                    dcc.Dropdown(
                        id=f"{id_prefix}-country-selector",
                        options=country_options,
                        multi=True,
                        placeholder="Select countries...",
                        disabled=True,
                        className="mb-3",
                    )
                ],
                id=f"{id_prefix}-country-selector-container",
            ),
            # Carrier selection section
            html.Label("Select Sectors:", className="fw-bold mb-2"),
            dcc.Checklist(
                id=f"{id_prefix}-bus-carrier",
                options=carrier_options,
                value=default_value,
                labelStyle={"display": "block"},
                className="mb-3",
            ),
        ],
        width=2,
        className="mb-4",
    )


def create_country_selection_panel(id_prefix, country_options):
    """
    Creates a country selection panel without carrier selection.

    Parameters
    ----------
    id_prefix : str
        Prefix for the component IDs (e.g., 'capex' or 'opex')
    country_options : list
        List of country options for the dropdown

    Returns
    -------
    dash component
        A column containing the country selection controls
    """
    return dbc.Col(
        [
            # Country selection section
            html.Label(
                "Select Countries:",
                className="fw-bold mb-2",
            ),
            # Radio buttons for All vs. Specific Countries
            dcc.RadioItems(
                id=f"{id_prefix}-country-mode",
                options=[
                    {
                        "label": " All Countries",
                        "value": "All",
                    },
                    {
                        "label": " Select Countries",
                        "value": "Specific",
                    },
                ],
                value="All",
                className="mb-2",
                labelStyle={"display": "block"},
            ),
            # Country selection dropdown, shown only when specific countries are selected
            html.Div(
                [
                    dcc.Dropdown(
                        id=f"{id_prefix}-country-selector",
                        options=country_options,
                        multi=True,
                        placeholder="Select countries...",
                        disabled=True,
                        className="mb-3",
                    )
                ],
                id=f"{id_prefix}-country-selector-container",
            ),
        ],
        width=2,
        className="mb-4",
    )


def create_energy_balance_tab(bus_carrier_options):
    """Creates the content for the Energy Balance (timeseries) tab."""
    return dcc.Tab(
        label="Energy Balance Timeseries",  # Renamed tab label
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                # Use the reusable selection panel
                                create_selection_panel(
                                    "balance",
                                    bus_carrier_options,
                                    country_options,
                                    default_carriers=[
                                        "AC",
                                        "Hydrogen Storage",
                                        "Low Voltage",
                                    ],
                                ),
                                dbc.Col(
                                    # Container for the dynamically generated charts
                                    html.Div(id="energy-balance-charts-container"),
                                    width=10,
                                ),
                            ],
                        ),
                    ]
                ),
                className="mt-3",
            )
        ],
    )


def create_energy_balance_aggregated_tab(bus_carrier_options):
    """Creates the content for the Aggregated Energy Balance tab."""
    return dcc.Tab(
        label="Energy Balance Totals",
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                # Use the reusable selection panel
                                create_selection_panel(
                                    "agg-balance",
                                    bus_carrier_options,
                                    country_options,
                                    default_carriers=[
                                        "AC",
                                        "Hydrogen Storage",
                                        "Low Voltage",
                                    ],
                                ),
                                dbc.Col(
                                    # Container for the dynamically generated charts
                                    dbc.Row(id="agg-energy-balance-charts-container"),
                                    width=10,
                                ),
                            ],
                        ),
                    ]
                ),
                className="mt-3",
            )
        ],
    )


def create_capacity_tab(bus_carrier_options):
    """Creates the content for the Capacity tab."""
    return dcc.Tab(
        label="Capacity Totals",
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                # Use the reusable selection panel without "all" option
                                create_selection_panel(
                                    "capacity",
                                    bus_carrier_options,
                                    country_options,
                                    default_carriers=[
                                        "AC",
                                        "Hydrogen Storage",
                                        "Low Voltage",
                                    ],
                                ),
                                dbc.Col(
                                    # Container for the dynamically generated charts
                                    dbc.Row(id="capacity-charts-container"),
                                    width=10,
                                ),
                            ],
                        ),
                    ]
                ),
                className="mt-3",
            )
        ],
    )


def create_capex_totals_tab():
    """Creates the content for the CAPEX Totals tab."""
    return dcc.Tab(
        label="CAPEX Totals",
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                # Use the country selection panel
                                create_country_selection_panel(
                                    "capex", country_options
                                ),
                                dbc.Col(
                                    # Container for the dynamically generated charts
                                    dbc.Row(id="capex-charts-container"),
                                    width=10,
                                ),
                            ],
                        ),
                    ]
                ),
                className="mt-3",
            )
        ],
    )


def create_opex_totals_tab():
    """Creates the content for the OPEX Totals tab."""
    return dcc.Tab(
        label="OPEX Totals",
        children=[
            dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Row(
                            [
                                # Use the country selection panel
                                create_country_selection_panel("opex", country_options),
                                dbc.Col(
                                    # Container for the dynamically generated charts
                                    dbc.Row(id="opex-charts-container"),
                                    width=10,
                                ),
                            ],
                        ),
                    ]
                ),
                className="mt-3",
            )
        ],
    )


def create_network_map_tab():
    """Creates the content for the Network Configuration tab with map and metadata."""
    return dcc.Tab(
        label="Network Configuration",
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


def create_footer():
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


def create_welcome_page():
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
networks = {}
active_network = None

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


def load_network_from_paths(path_dict=None):
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
        n = pypsa.examples.ac_dc_meshed()
        n.optimize()
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
network_labels = list(networks.keys())
active_network_label = network_labels[0]
n = networks[active_network_label]

# Ensure plotting consistency for active network
pypsa.consistency.plotting_consistency_check(n)

# Access statistics
s = n.statistics

# Get unique bus carriers for the dropdown
bus_carrier_options = [
    {
        "label": f" {
            title_except_multi_caps(
                n.carriers.nice_name.where(
                    n.carriers.nice_name.ne(''), n.carriers.index.to_series()
                ).at[carrier]
            )
        }",
        "value": carrier,
    }
    for carrier in sorted(n.buses.carrier.unique())
    if carrier != "none"
]

# Get unique countries for the country selector dropdown
country_options = [
    {"label": country, "value": country} for country in n.buses.country.unique()
]
# Sort country options alphabetically for better UX
country_options.sort(key=lambda x: x["label"])
# Add "All" option at the beginning
country_all_option = {"label": "All", "value": "All"}

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
                                    children=[
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
                        dcc.Tabs(
                            id="tabs",
                            children=[
                                create_energy_balance_tab(bus_carrier_options),
                                create_energy_balance_aggregated_tab(
                                    bus_carrier_options
                                ),
                                create_capacity_tab(bus_carrier_options),
                                create_capex_totals_tab(),
                                create_opex_totals_tab(),
                                create_network_map_tab(),
                            ],
                        ),
                    ],
                ),
                create_footer(),
            ],
        ),
    ],
)

# --- Callbacks ---


def create_toggle_callback(prefix):
    """
    Creates a callback function for toggling country selector dropdowns.

    Parameters
    ----------
    prefix : str
        Prefix for the component IDs

    Returns
    -------
    function
        A callback function for toggling country selectors
    """

    def toggle_country_selector(mode):
        if mode == "All":
            # If "All" is selected, disable the dropdown and clear its value
            return True, []
        else:
            # If "Specific" is selected, enable the dropdown
            return False, []

    return toggle_country_selector


def create_energy_balance_callback(aggregated=False):
    """
    Creates a callback function for updating energy balance charts.

    Parameters
    ----------
    aggregated : bool
        Whether to create a callback for aggregated (True) or timeseries (False) views

    Returns
    -------
    function
        A callback function for updating energy balance charts
    """

    def update_energy_balance(selected_carriers, country_mode, selected_countries):
        if not selected_carriers:
            message = html.Div(
                html.P(
                    "Please select one or more carriers.",
                    className="lead text-center text-muted my-5",
                ),
                className="w-100",
            )
            return [message] if aggregated else message

        # Handle country filtering
        facet_col = None
        query = None

        # If specific countries are selected, set up the query and facet_col
        if country_mode == "Specific" and selected_countries:
            facet_col = "country"
            query = f"country in {selected_countries}"
        elif country_mode == "Specific" and not selected_countries:
            message = html.Div(
                html.P(
                    "Please select at least one country.",
                    className="lead text-center text-muted my-5",
                ),
                className="w-100",
            )
            return [message] if aggregated else message

        charts = []

        # For aggregated view, calculate column width
        col_width = None
        if aggregated:
            col_width = (
                max(1, 12 // len(selected_carriers)) if selected_carriers else 12
            )

        for carrier in selected_carriers:
            try:
                # Generate plot based on view type
                if aggregated:
                    # Bar plot for aggregated view
                    fig = s.energy_balance.iplot.bar(
                        x="value",
                        y="carrier",
                        color="carrier",
                        bus_carrier=carrier,
                        nice_names=False,
                        width=None,
                        query=query,
                        facet_col=facet_col,
                    )

                else:
                    # Area plot for timeseries view
                    fig = s.energy_balance.iplot.area(
                        x="snapshot",
                        y="value",
                        color="carrier",
                        stacked=True,
                        bus_carrier=carrier,
                        nice_names=False,
                        height=500,
                        width=None,
                        query=query,
                        facet_col=facet_col,
                    )

                    # Adjust layout for area plot
                    fig.update_layout(
                        legend_title="Component Carrier",
                        hovermode="closest",
                    )

                # Common title setting
                title = f"{'Aggregated Balance' if aggregated else 'Energy Balance'} for {carrier}"
                if country_mode == "Specific" and selected_countries:
                    countries_str = ", ".join(selected_countries)
                    title += f" (Countries: {countries_str})"

                fig.update_layout(title=title)

                charts.append(dcc.Graph(figure=fig))

            except Exception as e:
                # Create a user-friendly message
                message = html.Div(
                    [
                        html.H5(
                            f"Error {e} for selected carrier {carrier}",
                            className="text-muted",
                        ),
                    ],
                    className="text-center p-5 border rounded",
                    style={"background-color": "#f8f9fa"},
                )

                # Add to charts with appropriate wrapping
                if aggregated:
                    charts.append(dbc.Col(message, width=col_width))
                else:
                    charts.append(message)

        # If no charts were created successfully, show a message
        if not charts:
            message = html.Div(
                html.P(
                    "No data available for the current selection. Try different filters.",
                    className="lead text-center text-muted my-5",
                ),
                className="w-100",
            )
            return [message] if aggregated else message

        return charts

    return update_energy_balance


# Callback for Energy Balance charts (timeseries view)
@app.callback(
    Output("energy-balance-charts-container", "children"),
    [
        Input("balance-bus-carrier", "value"),
        Input("balance-country-mode", "value"),
        Input("balance-country-selector", "value"),
        Input("network-selector", "value"),
    ],
)
def update_energy_balance(
    selected_carriers, country_mode, selected_countries, selected_network_label
):
    n = networks[selected_network_label]
    s = n.statistics  # noqa: F841
    return create_energy_balance_callback(aggregated=False)(
        selected_carriers, country_mode, selected_countries
    )


# Callback for Aggregated Energy Balance charts
@app.callback(
    Output("agg-energy-balance-charts-container", "children"),
    [
        Input("agg-balance-bus-carrier", "value"),
        Input("agg-balance-country-mode", "value"),
        Input("agg-balance-country-selector", "value"),
        Input("network-selector", "value"),
    ],
)
def update_energy_balance_aggregated(
    selected_carriers, country_mode, selected_countries, selected_network_label
):
    n = networks[selected_network_label]
    s = n.statistics  # noqa: F841
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
def update_map(n_clicks, selected_network_label):
    n = networks[selected_network_label]
    try:
        # Create a folium map using PyPSA's explore method
        map_obj = n.plot.explore(
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
def update_metadata(n_clicks, selected_network_label):
    n = networks[selected_network_label]
    try:
        # Convert network metadata to YAML format
        metadata_yaml = yaml.dump(n.meta, default_flow_style=False, sort_keys=False)

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


# Callbacks for enabling/disabling country selectors based on mode
@app.callback(
    [
        Output("balance-country-selector", "disabled"),
        Output("balance-country-selector", "value"),
    ],
    [Input("balance-country-mode", "value")],
)
def toggle_balance_country_selector(mode):
    return create_toggle_callback("balance")(mode)


@app.callback(
    [
        Output("agg-balance-country-selector", "disabled"),
        Output("agg-balance-country-selector", "value"),
    ],
    [Input("agg-balance-country-mode", "value")],
)
def toggle_agg_balance_country_selector(mode):
    return create_toggle_callback("agg-balance")(mode)


@app.callback(
    [
        Output("capacity-country-selector", "disabled"),
        Output("capacity-country-selector", "value"),
    ],
    [Input("capacity-country-mode", "value")],
)
def toggle_capacity_country_selector(mode):
    return create_toggle_callback("capacity")(mode)


# Callback for Capacity charts
@app.callback(
    Output("capacity-charts-container", "children"),
    [
        Input("capacity-bus-carrier", "value"),
        Input("capacity-country-mode", "value"),
        Input("capacity-country-selector", "value"),
        Input("network-selector", "value"),
    ],
)
def update_capacity_charts(
    selected_carriers, country_mode, selected_countries, selected_network_label
):
    n = networks[selected_network_label]
    s = n.statistics
    if not selected_carriers:
        return [
            html.Div(
                html.P(
                    "Please select one or more carriers.",
                    className="lead text-center text-muted my-5",
                ),
                className="w-100",
            )
        ]

    # Handle country filtering
    facet_col = None
    query = None

    # If specific countries are selected, set up the query and facet_col
    if country_mode == "Specific" and selected_countries:
        facet_col = "country"
        query = f"country in {selected_countries}"
    elif country_mode == "Specific" and not selected_countries:
        return [
            html.Div(
                html.P(
                    "Please select at least one country.",
                    className="lead text-center text-muted my-5",
                ),
                className="w-100",
            )
        ]

    # Remove column width calculation since we want charts stacked vertically
    charts = []

    for carrier in selected_carriers:
        try:
            # Generate capacity bar chart directly with carrier
            fig = s.optimal_capacity.iplot.bar(
                x="value",
                y="carrier",
                color="carrier",
                bus_carrier=carrier,
                width=None,
                height=500,
                nice_names=False,
                query=query,
                facet_col=facet_col,
            )

            # Set title based on selections
            title = f"Optimal Capacity for {carrier}"
            if country_mode == "Specific" and selected_countries:
                countries_str = ", ".join(selected_countries)
                title += f" (Countries: {countries_str})"

            # Add the graph without wrapping in dbc.Col so it takes full width
            charts.append(dcc.Graph(figure=fig, className="mb-4"))

        except Exception as e:
            # Create a user-friendly error message
            message = html.Div(
                [
                    html.H5(
                        f"Error {e} for selected carrier {carrier}",
                        className="text-muted",
                    ),
                ],
                className="text-center p-5 border rounded mb-4",
                style={"background-color": "#f8f9fa"},
            )
            charts.append(message)

    # If no charts were created successfully, show a message
    if not charts:
        return [
            html.Div(
                html.P(
                    "No data available for the current selection. Try different filters.",
                    className="lead text-center text-muted my-5",
                ),
                className="w-100",
            )
        ]

    return charts


# Callbacks for enabling/disabling country selectors for CAPEX and OPEX tabs
@app.callback(
    [
        Output("capex-country-selector", "disabled"),
        Output("capex-country-selector", "value"),
    ],
    [Input("capex-country-mode", "value")],
)
def toggle_capex_country_selector(mode):
    return create_toggle_callback("capex")(mode)


@app.callback(
    [
        Output("opex-country-selector", "disabled"),
        Output("opex-country-selector", "value"),
    ],
    [Input("opex-country-mode", "value")],
)
def toggle_opex_country_selector(mode):
    return create_toggle_callback("opex")(mode)


# Callback for CAPEX charts
@app.callback(
    Output("capex-charts-container", "children"),
    [
        Input("capex-country-mode", "value"),
        Input("capex-country-selector", "value"),
        Input("network-selector", "value"),
    ],
)
def update_capex_charts(country_mode, selected_countries, selected_network_label):
    n = networks[selected_network_label]
    s = n.statistics
    # Handle country filtering
    facet_col = None
    query = None

    # If specific countries are selected, set up the query and facet_col
    if country_mode == "Specific" and selected_countries:
        facet_col = "country"
        query = f"country in {selected_countries}"
    elif country_mode == "Specific" and not selected_countries:
        return [
            html.Div(
                html.P(
                    "Please select at least one country.",
                    className="lead text-center text-muted my-5",
                ),
                className="w-100",
            )
        ]

    try:
        # Generate CAPEX bar chart
        fig = s.capex.iplot.bar(
            x="value",
            y="carrier",
            color="carrier",
            nice_names=False,
            height=1000,
            width=None,
            query=query,
            facet_col=facet_col,
        )

        # Set title based on selections
        title = "Capital Expenditure Totals"
        if country_mode == "Specific" and selected_countries:
            countries_str = ", ".join(selected_countries)
            title += f" (Countries: {countries_str})"

        # Apply robust height settings to prevent resizing
        fig.update_layout(
            title=title,
            height=1000,
            margin=dict(l=50, r=50, t=100, b=50),
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
        # Create a user-friendly error message
        message = html.Div(
            [
                html.H5(
                    f"Error generating CAPEX chart: {e}",
                    className="text-muted",
                ),
            ],
            className="text-center p-5 border rounded mb-4",
            style={"background-color": "#f8f9fa"},
        )
        return [message]


# Callback for OPEX charts
@app.callback(
    Output("opex-charts-container", "children"),
    [
        Input("opex-country-mode", "value"),
        Input("opex-country-selector", "value"),
        Input("network-selector", "value"),
    ],
)
def update_opex_charts(country_mode, selected_countries, selected_network_label):
    n = networks[selected_network_label]
    s = n.statistics
    # Handle country filtering
    facet_col = None
    query = None

    # If specific countries are selected, set up the query and facet_col
    if country_mode == "Specific" and selected_countries:
        facet_col = "country"
        query = f"country in {selected_countries}"
    elif country_mode == "Specific" and not selected_countries:
        return [
            html.Div(
                html.P(
                    "Please select at least one country.",
                    className="lead text-center text-muted my-5",
                ),
                className="w-100",
            )
        ]

    try:
        # Generate OPEX bar chart
        fig = s.opex.iplot.bar(
            x="value",
            y="carrier",
            color="carrier",
            nice_names=False,
            height=1000,
            width=None,
            query=query,
            facet_col=facet_col,
        )

        # Set title based on selections
        title = "Operational Expenditure Totals"
        if country_mode == "Specific" and selected_countries:
            countries_str = ", ".join(selected_countries)
            title += f" (Countries: {countries_str})"

        # Apply robust height settings to prevent resizing
        fig.update_layout(
            title=title,
            height=1000,
            margin=dict(l=50, r=50, t=100, b=50),
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
        # Create a user-friendly error message
        message = html.Div(
            [
                html.H5(
                    f"Error generating OPEX chart: {e}",
                    className="text-muted",
                ),
            ],
            className="text-center p-5 border rounded mb-4",
            style={"background-color": "#f8f9fa"},
        )
        return [message]


# Callback for network selector
@app.callback(
    [
        Output("network-title", "children"),
        Output("balance-bus-carrier", "options"),
        Output("agg-balance-bus-carrier", "options"),
        Output("capacity-bus-carrier", "options"),
        Output("balance-country-selector", "options"),
        Output("agg-balance-country-selector", "options"),
        Output("capacity-country-selector", "options"),
        Output("capex-country-selector", "options"),
        Output("opex-country-selector", "options"),
    ],
    [Input("network-selector", "value")],
)
def update_selected_network(selected_network_label):
    """Update the active network when user selects a different network"""
    global n, s

    # Update the active network
    n = networks[selected_network_label]

    # Ensure plotting consistency for the newly selected network
    pypsa.consistency.plotting_consistency_check(n)

    # Update statistics for the new network
    s = n.statistics

    # Create network title
    wildcards = n.meta.get("wildcards", {})
    from_meta = (
        f"{wildcards.get('run', 'Unnamed')} {wildcards.get('planning_horizons', '')}"
    )
    network_title = f"Network: {n.name or from_meta}"

    # Update bus carrier options for the new network
    updated_bus_carrier_options = [
        {
            "label": f" {
                title_except_multi_caps(
                    n.carriers.nice_name.where(
                        n.carriers.nice_name.ne(''), n.carriers.index.to_series()
                    ).at[carrier]
                )
            }",
            "value": carrier,
        }
        for carrier in sorted(n.buses.carrier.unique())
        if carrier != "none"
    ]

    # Update country options for the new network
    updated_country_options = [
        {"label": country, "value": country} for country in n.buses.country.unique()
    ]
    # Sort country options alphabetically for better UX
    updated_country_options.sort(key=lambda x: x["label"])

    # Return all updated values
    return (
        network_title,
        updated_bus_carrier_options,
        updated_bus_carrier_options,
        updated_bus_carrier_options,
        updated_country_options,
        updated_country_options,
        updated_country_options,
        updated_country_options,
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
def navigate_pages(n_clicks, page_state):
    """Manage navigation between welcome page and dashboard"""
    if n_clicks and page_state["current_page"] == "welcome":
        return {"display": "none"}, {"display": "block"}, {"current_page": "dashboard"}
    return {"display": "block"}, {"display": "none"}, page_state


# Run the app
if __name__ == "__main__":
    print("Starting Energy System Dashboard...")
    # Consider adding host='0.0.0.0' if running in a container or VM
    app.run(debug=True)


# Function to run the dashboard with multiple networks
def run_dashboard(networks_dict=None, debug=True):
    """
    Run the dashboard with one or more networks.

    Parameters
    ----------
    networks_dict : dict, optional
        A dictionary of {label: network} containing PyPSA networks.
        If not provided, will attempt to load a default network.
    debug : bool, default True
        Whether to run the app in debug mode
    """
    global networks, n, s, network_labels, active_network_label

    if networks_dict is not None:
        if not isinstance(networks_dict, dict):
            raise ValueError(
                "networks_dict must be a dictionary in the form {label: network}"
            )

        # Store the provided networks
        networks = networks_dict

        # Set up the active network
        network_labels = list(networks.keys())
        if not network_labels:
            raise ValueError("The networks dictionary is empty")

        active_network_label = network_labels[0]
        n = networks[active_network_label]

        # Ensure plotting consistency for active network
        pypsa.consistency.plotting_consistency_check(n)

        # Access statistics
        s = n.statistics

    print("Starting Energy System Dashboard...")
    app.run_server(debug=debug)
