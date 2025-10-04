"""Configuration settings for PyPSA Explorer dashboard."""

import plotly.graph_objects as go
import plotly.io as pio

# Color scheme and theme settings - Modern energy-themed palette
COLORS = {
    "primary": "#1a237e",  # Deep indigo
    "secondary": "#00bcd4",  # Cyan/teal
    "accent": "#00e676",  # Bright green
    "warning": "#ff6f00",  # Orange
    "light_bg": "#f8f9fa",  # Light grey
    "dark_bg": "#0d1b2a",  # Deep navy
    "text": "#1a1a1a",  # Almost black
    "light_text": "#6c757d",  # Light grey text
    "background": "#f0f4f8",  # Soft blue-grey background
    "gradient_start": "#667eea",  # Purple-blue
    "gradient_end": "#764ba2",  # Deep purple
    "glass_bg": "rgba(255, 255, 255, 0.75)",  # Glass morphism
    "glass_border": "rgba(255, 255, 255, 0.18)",  # Glass border
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
/* Modern Energy Dashboard - Enhanced Styling */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

:root {
    --primary-color: #1a237e;
    --secondary-color: #00bcd4;
    --accent-color: #00e676;
    --warning-color: #ff6f00;
    --light-bg: #f8f9fa;
    --dark-bg: #0d1b2a;
    --text-color: #1a1a1a;
    --light-text: #6c757d;
    --gradient-start: #667eea;
    --gradient-end: #764ba2;
    --glass-bg: rgba(255, 255, 255, 0.75);
    --glass-border: rgba(255, 255, 255, 0.18);
    --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.05);
    --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.1);
    --shadow-lg: 0 8px 24px rgba(0, 0, 0, 0.15);
    --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
    --transition-slow: 350ms cubic-bezier(0.4, 0, 0.2, 1);
}

* {
    box-sizing: border-box;
}

body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    color: var(--text-color);
    background: linear-gradient(135deg, #f0f4f8 0%, #e2e8f0 100%);
    background-attachment: fixed;
    margin: 0;
    padding: 0;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    position: relative;
}

body::before {
    content: '';
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-image:
        radial-gradient(circle at 20% 50%, rgba(102, 126, 234, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 80% 80%, rgba(0, 188, 212, 0.03) 0%, transparent 50%),
        radial-gradient(circle at 40% 20%, rgba(118, 75, 162, 0.02) 0%, transparent 50%);
    pointer-events: none;
    z-index: 0;
}

body > div {
    position: relative;
    z-index: 1;
}

/* ===== TYPOGRAPHY ===== */
h1, h2, h3, h4, h5, h6 {
    color: var(--text-color);
    font-weight: 600;
    letter-spacing: -0.02em;
    line-height: 1.3;
}

h1 { font-size: 2.5rem; font-weight: 800; }
h2 { font-size: 2rem; font-weight: 700; }
h3 { font-size: 1.5rem; font-weight: 600; }
h4 { font-size: 1.25rem; font-weight: 600; }
h5 { font-size: 1.1rem; font-weight: 600; }

/* ===== CARDS & CONTAINERS ===== */
.card {
    border-radius: 16px;
    box-shadow: var(--shadow-md);
    margin-bottom: 24px;
    border: none;
    background: white;
    transition: all var(--transition-base);
    overflow: hidden;
}

.card:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.card-body {
    padding: 24px;
}

.tab-content {
    background-color: transparent !important;
    border: none !important;
}

/* ===== TABS ===== */
.tab-container {
    border-bottom: 2px solid rgba(0, 0, 0, 0.06);
    background: white;
    border-radius: 12px 12px 0 0;
    padding: 0 16px;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.02);
}

.tab {
    border: none;
    color: var(--light-text);
    font-weight: 500;
    font-size: 0.95rem;
    padding: 16px 24px;
    margin-right: 4px;
    transition: all var(--transition-base);
    background-color: transparent !important;
    border-bottom: 3px solid transparent;
    position: relative;
    border-radius: 8px 8px 0 0;
}

.tab::before {
    content: '';
    position: absolute;
    bottom: -3px;
    left: 0;
    right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--gradient-start), var(--gradient-end));
    transform: scaleX(0);
    transition: transform var(--transition-base);
}

.tab:hover {
    color: var(--secondary-color);
    background-color: rgba(0, 188, 212, 0.08) !important;
}

.tab:hover::before {
    transform: scaleX(0.5);
}

.tab--selected {
    color: var(--secondary-color) !important;
    background-color: rgba(0, 188, 212, 0.12) !important;
    font-weight: 600;
}

.tab--selected::before {
    transform: scaleX(1) !important;
}

.tab--selected, .tab {
    border-top: none !important;
    border-left: none !important;
    border-right: none !important;
    border-bottom: 3px solid transparent !important;
}

/* ===== BUTTONS ===== */
.btn {
    border-radius: 10px;
    font-weight: 500;
    padding: 12px 24px;
    transition: all var(--transition-base);
    border: none;
    font-size: 0.95rem;
    letter-spacing: 0.02em;
    box-shadow: var(--shadow-sm);
}

.btn-primary {
    background: linear-gradient(135deg, var(--secondary-color) 0%, #00acc1 100%);
    border: none;
    color: white;
}

.btn-primary:hover {
    background: linear-gradient(135deg, #00acc1 0%, #0097a7 100%);
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.btn-lg {
    padding: 16px 32px;
    font-size: 1.05rem;
    border-radius: 12px;
}

.dashboard-container {
    padding: 24px;
    max-width: 1920px;
    margin: 0 auto;
}

/* ===== WELCOME PAGE ===== */
.welcome-card {
    text-align: center;
    padding: 60px 40px;
    border-radius: 20px;
    background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
    border: 1px solid rgba(255, 255, 255, 0.5);
    position: relative;
    overflow: hidden;
}

.welcome-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
}

.welcome-header {
    font-size: 3.5rem;
    margin-bottom: 0.5em;
    font-weight: 800;
    background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.03em;
}

.welcome-subtitle {
    font-size: 1.5rem;
    margin-bottom: 1.5em;
    color: var(--light-text);
    font-weight: 400;
}

.welcome-feature {
    background: white;
    border-radius: 16px;
    padding: 32px 24px;
    height: 100%;
    box-shadow: var(--shadow-md);
    transition: all var(--transition-base);
    border: 1px solid rgba(0, 0, 0, 0.05);
    position: relative;
    overflow: hidden;
}

.welcome-feature::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 4px;
    background: linear-gradient(90deg, var(--secondary-color) 0%, var(--accent-color) 100%);
    transform: scaleX(0);
    transform-origin: left;
    transition: transform var(--transition-base);
}

.welcome-feature:hover::before {
    transform: scaleX(1);
}

.welcome-feature:hover {
    transform: translateY(-8px);
    box-shadow: var(--shadow-lg);
}

.feature-icon {
    font-size: 48px;
    margin-bottom: 20px;
    color: var(--secondary-color);
    display: inline-block;
    transition: all var(--transition-base);
}

.welcome-feature:hover .feature-icon {
    transform: scale(1.1) rotate(5deg);
}

.network-item {
    padding: 20px;
    margin: 12px 0;
    background: white;
    border-radius: 12px;
    border-left: 4px solid var(--secondary-color);
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-base);
}

.network-item:hover {
    transform: translateX(8px);
    box-shadow: var(--shadow-md);
    border-left-color: var(--accent-color);
}

/* ===== SIDEBAR - GLASS MORPHISM ===== */
.sidebar-filter-panel {
    background: var(--glass-bg);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid var(--glass-border);
    border-radius: 20px;
    min-height: calc(100vh - 200px);
    padding: 28px;
    margin-right: 20px;
    box-shadow: var(--shadow-md);
    transition: all var(--transition-base);
}

.sidebar-filter-panel:hover {
    box-shadow: var(--shadow-lg);
}

.sidebar-filter-panel h5 {
    color: var(--text-color);
    margin-bottom: 20px;
    font-size: 1.2rem;
    font-weight: 700;
    letter-spacing: -0.02em;
}

.sidebar-filter-panel hr {
    margin: 16px 0;
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 0, 0, 0.1), transparent);
}

.sidebar-filter-panel label {
    font-weight: 500;
    color: var(--text-color);
    margin-bottom: 8px;
}

/* Radio buttons styling */
.sidebar-filter-panel input[type="radio"] {
    margin-right: 8px;
    accent-color: var(--secondary-color);
    cursor: pointer;
}

/* Checkbox styling */
.sidebar-filter-panel input[type="checkbox"] {
    margin-right: 8px;
    accent-color: var(--secondary-color);
    cursor: pointer;
    width: 18px;
    height: 18px;
}

/* Improve label spacing */
.sidebar-filter-panel .form-check-label {
    cursor: pointer;
    padding: 4px 0;
    transition: color var(--transition-fast);
}

.sidebar-filter-panel .form-check-label:hover {
    color: var(--secondary-color);
}

/* "Not applicable" text styling */
.sidebar-filter-panel small {
    display: block;
    padding: 12px;
    background: rgba(255, 111, 0, 0.08);
    border-left: 3px solid var(--warning-color);
    border-radius: 8px;
    color: var(--warning-color);
    font-weight: 500;
    margin-top: 12px;
}

.sidebar-container {
    position: sticky;
    top: 20px;
    max-height: calc(100vh - 40px);
    overflow-y: auto;
    overflow-x: hidden;
}

.sidebar-container::-webkit-scrollbar {
    width: 6px;
}

.sidebar-container::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.05);
    border-radius: 10px;
}

.sidebar-container::-webkit-scrollbar-thumb {
    background: var(--secondary-color);
    border-radius: 10px;
}

.main-content-area {
    padding-left: 0;
}

/* ===== FORMS & INPUTS ===== */
.Select-control {
    border-radius: 10px;
    border: 1px solid rgba(0, 0, 0, 0.1);
    transition: all var(--transition-base);
}

.Select-control:hover {
    border-color: var(--secondary-color);
    box-shadow: 0 0 0 3px rgba(0, 188, 212, 0.1);
}

.VirtualizedSelectOption {
    transition: all var(--transition-fast);
}

/* Dropdown styling */
.Select.is-focused .Select-control {
    border-color: var(--secondary-color);
    box-shadow: 0 0 0 3px rgba(0, 188, 212, 0.15);
}

/* Multi-select value styling */
.Select-value {
    background: linear-gradient(135deg, var(--secondary-color), #00acc1);
    border: none;
    border-radius: 6px;
    color: white;
    padding: 4px 8px;
}

.Select-value-icon {
    border-right: 1px solid rgba(255, 255, 255, 0.3);
    padding: 2px 6px;
}

.Select-value-icon:hover {
    background-color: rgba(0, 0, 0, 0.1);
    color: white;
}

/* ===== ANIMATIONS ===== */
.fade-in {
    animation: fadeIn 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(10px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes slideInLeft {
    from {
        opacity: 0;
        transform: translateX(-20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

@keyframes slideInRight {
    from {
        opacity: 0;
        transform: translateX(20px);
    }
    to {
        opacity: 1;
        transform: translateX(0);
    }
}

/* ===== FOOTER ===== */
footer {
    margin-top: 60px;
    padding: 24px 0;
    border-top: 1px solid rgba(0, 0, 0, 0.08);
    background: rgba(255, 255, 255, 0.5);
    backdrop-filter: blur(10px);
}

/* ===== PLOTLY CHARTS ===== */
.js-plotly-plot {
    background-color: transparent !important;
}

.js-plotly-plot .plotly {
    border-radius: 16px;
    overflow: hidden;
    background: white;
    box-shadow: var(--shadow-md);
    border: 1px solid rgba(0, 0, 0, 0.05);
}

.modebar {
    background-color: rgba(255, 255, 255, 0.95) !important;
    border-radius: 8px;
    padding: 4px;
    box-shadow: var(--shadow-sm);
}

.modebar-btn {
    background-color: transparent !important;
    transition: all var(--transition-fast);
    border-radius: 6px;
}

.modebar-btn:hover {
    background-color: rgba(0, 188, 212, 0.15) !important;
}

.dash-graph {
    background-color: transparent !important;
    margin-bottom: 24px;
}

.dash-graph > div {
    border: none !important;
}

.tab-pane {
    background-color: transparent !important;
}

/* Chart container improvements */
#energy-balance-charts-container,
#agg-energy-balance-charts-container,
#capacity-charts-container,
#capex-charts-container,
#opex-charts-container {
    padding: 20px;
    background: rgba(255, 255, 255, 0.6);
    border-radius: 16px;
    backdrop-filter: blur(10px);
}

/* Add subtle section headers */
.chart-section-header {
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-color);
    margin-bottom: 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid rgba(0, 188, 212, 0.2);
}

/* ===== NETWORK METADATA ===== */
#network-metadata {
    background: var(--glass-bg) !important;
    backdrop-filter: blur(10px);
    border: 1px solid var(--glass-border) !important;
    border-radius: 16px;
    padding: 24px;
    box-shadow: var(--shadow-md);
}

/* ===== HEADER & NAVIGATION ===== */
.app-header {
    background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
    padding: 20px 32px;
    border-radius: 20px;
    margin-bottom: 32px;
    box-shadow: var(--shadow-lg);
    color: white;
}

.app-header h1 {
    color: white;
    margin: 0;
    font-size: 2rem;
    font-weight: 700;
}

/* ===== KPI CARDS ===== */
.kpi-card {
    background: white;
    border-radius: 10px;
    padding: 12px 16px;
    box-shadow: var(--shadow-sm);
    transition: all var(--transition-base);
    border-left: 3px solid var(--secondary-color);
    position: relative;
    overflow: hidden;
}

.kpi-card::before {
    content: '';
    position: absolute;
    top: 0;
    right: 0;
    width: 60px;
    height: 60px;
    background: linear-gradient(135deg, transparent 50%, rgba(0, 188, 212, 0.05) 50%);
    border-radius: 0 10px 0 100%;
}

.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

/* Clickable KPI Cards */
.kpi-card-clickable {
    cursor: pointer;
    user-select: none;
}

.kpi-card-clickable:hover {
    transform: translateY(-4px);
    box-shadow: var(--shadow-lg);
}

.kpi-card-clickable:active {
    transform: translateY(-2px);
    box-shadow: var(--shadow-md);
}

.kpi-card:nth-child(1) {
    border-left-color: #667eea;
}

.kpi-card:nth-child(2) {
    border-left-color: #00e676;
}

.kpi-card:nth-child(3) {
    border-left-color: #ff6f00;
}

.kpi-card:nth-child(4) {
    border-left-color: #00bcd4;
}

.kpi-card:nth-child(5) {
    border-left-color: #f50057;
}

.kpi-card:nth-child(6) {
    border-left-color: #ffc107;
}

.kpi-value {
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--text-color);
    margin: 4px 0;
    position: relative;
    z-index: 1;
    line-height: 1;
}

.kpi-label {
    font-size: 0.7rem;
    color: var(--light-text);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    font-weight: 600;
    position: relative;
    z-index: 1;
}

.kpi-icon {
    font-size: 1.25rem;
    opacity: 0.85;
    position: relative;
    z-index: 1;
    margin-bottom: 2px;
}

.kpi-card:nth-child(1) .kpi-icon {
    color: #667eea;
}

.kpi-card:nth-child(2) .kpi-icon {
    color: #00e676;
}

.kpi-card:nth-child(3) .kpi-icon {
    color: #ff6f00;
}

.kpi-card:nth-child(4) .kpi-icon {
    color: #00bcd4;
}

.kpi-card:nth-child(5) .kpi-icon {
    color: #f50057;
}

.kpi-card:nth-child(6) .kpi-icon {
    color: #ffc107;
}

/* ===== LOADING STATES ===== */
.loading-skeleton {
    background: linear-gradient(90deg, #f0f0f0 25%, #e0e0e0 50%, #f0f0f0 75%);
    background-size: 200% 100%;
    animation: loading 1.5s ease-in-out infinite;
    border-radius: 8px;
}

@keyframes loading {
    0% { background-position: 200% 0; }
    100% { background-position: -200% 0; }
}

.spinner {
    width: 40px;
    height: 40px;
    border: 4px solid rgba(0, 188, 212, 0.1);
    border-top-color: var(--secondary-color);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* ===== UTILITIES ===== */
.text-gradient {
    background: linear-gradient(135deg, var(--gradient-start) 0%, var(--gradient-end) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border: 1px solid var(--glass-border);
    border-radius: 16px;
    padding: 24px;
    box-shadow: var(--shadow-md);
}

.pulse {
    animation: pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
}
"""


def get_html_template() -> str:
    """Return the custom HTML template with embedded CSS and Font Awesome."""
    return f"""
<!DOCTYPE html>
<html>
    <head>
        {{%metas%}}
        <title>{{%title%}}</title>
        {{%favicon%}}
        {{%css%}}
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
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
