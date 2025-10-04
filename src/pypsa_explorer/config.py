"""Configuration settings for PyPSA Explorer dashboard."""

import plotly.graph_objects as go
import plotly.io as pio

# Color scheme and theme settings
COLORS = {
    "primary": "#2c3e50",  # Dark slate blue/grey
    "secondary": "#3498db",  # Blue
    "accent": "#2ecc71",  # Green
    "light_bg": "#f8f9fa",  # Light grey
    "dark_bg": "#343a40",  # Dark grey
    "text": "#2c3e50",  # Primary color for text
    "light_text": "#6c757d",  # Light grey text
    "background": "#f5f7fa",  # Main background color
}

# Plotly template configuration
PLOTLY_TEMPLATE_NAME = "dashboard_theme"


def setup_plotly_theme() -> None:
    """Configure Plotly theme for consistent styling across the dashboard."""
    pio.templates.default = "plotly_white"

    custom_template = go.layout.Template()
    custom_template.layout = go.Layout(
        plot_bgcolor=COLORS["background"],
        paper_bgcolor=COLORS["background"],
        font={"family": "Roboto, 'Helvetica Neue', sans-serif", "color": COLORS["text"]},
        xaxis={"gridcolor": "#e9ecef", "zerolinecolor": "#e9ecef"},
        yaxis={"gridcolor": "#e9ecef", "zerolinecolor": "#e9ecef"},
    )
    pio.templates[PLOTLY_TEMPLATE_NAME] = custom_template
    pio.templates.default = PLOTLY_TEMPLATE_NAME


# Dashboard layout configuration
LAYOUT_CONFIG = {
    "sidebar_width": 3,
    "main_content_width": 9,
    "chart_height": 500,
    "map_height": 700,
}

# Default carriers for initial selection
DEFAULT_CARRIERS = ["AC", "Hydrogen Storage", "Low Voltage"]

# Custom CSS for the dashboard
DASHBOARD_CSS = """
/* Custom CSS for improved dashboard styling */
:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --accent-color: #2ecc71;
    --light-bg: #f8f9fa;
    --dark-bg: #343a40;
    --text-color: var(--primary-color);
    --light-text: #6c757d;
}

body {
    font-family: 'Roboto', 'Helvetica Neue', sans-serif;
    color: var(--text-color);
    background-color: #f5f7fa;
}

.tab-content {
    background-color: transparent !important;
    border: none !important;
}

.card {
    border-radius: 8px;
    box-shadow: none;
    margin-bottom: 20px;
    border: none;
    background-color: transparent;
    transition: transform 0.2s;
}

.card-body {
    background-color: transparent;
    padding: 0;
}

h1, h2, h3, h4, h5 {
    color: var(--primary-color);
    font-weight: 600;
}

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

.tab--selected {
    color: var(--secondary-color) !important;
    background-color: #f5f7fa !important;
    border-bottom: 3px solid var(--secondary-color) !important;
}

.tab--selected, .tab {
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
}

.btn-primary {
    background-color: var(--secondary-color);
    border-color: var(--secondary-color);
}

.btn-primary:hover {
    background-color: #2980b9;
    border-color: #2980b9;
}

.dashboard-container {
    padding: 20px;
}

.welcome-card {
    text-align: center;
    padding: 40px;
    border-radius: 10px;
}

.welcome-header {
    font-size: 3em;
    margin-bottom: 0.5em;
    font-weight: 700;
}

.welcome-subtitle {
    font-size: 1.5em;
    margin-bottom: 1.5em;
    color: var(--primary-color);
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

footer {
    margin-top: 50px;
    padding: 20px 0;
    border-top: 1px solid #eee;
}

.Select-control {
    border-radius: 6px;
    border: 1px solid #ced4da;
}

.Select-control:hover {
    border-color: var(--secondary-color);
}

.button-group {
    margin: 20px 0;
}

.fade-in {
    animation: fadeIn 0.5s ease-in;
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

.sidebar-filter-panel {
    background-color: rgba(255, 255, 255, 0.5);
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

.main-content-area {
    padding-left: 20px;
}

.sidebar-container {
    position: sticky;
    top: 20px;
    max-height: calc(100vh - 40px);
    overflow-y: auto;
}

.js-plotly-plot {
    background-color: transparent !important;
}

.js-plotly-plot .plotly {
    border-radius: 8px;
    overflow: hidden;
}

.modebar {
    background-color: transparent !important;
}

.modebar-btn {
    background-color: transparent !important;
}

.dash-graph {
    background-color: transparent !important;
    margin-bottom: 20px;
}

.dash-graph > div {
    border: none !important;
}

.tab-pane {
    background-color: transparent !important;
}

.welcome-card {
    background-color: rgba(255, 255, 255, 0.7);
}

#network-metadata {
    background-color: rgba(255, 255, 255, 0.5) !important;
    border: 1px solid rgba(233, 236, 239, 0.5) !important;
}
"""


def get_html_template() -> str:
    """Return the custom HTML template with embedded CSS."""
    return f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <style>
{DASHBOARD_CSS}
        </style>
    </head>
    <body>
        {{%app_entry%}}
        <footer>
            {{%config%}}
            {{%scripts%}}
            {{%renderer%}}
        </footer>
    </body>
</html>
"""
