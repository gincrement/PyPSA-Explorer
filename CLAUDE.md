# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Running the Application
```bash
# Run with default demo network
uv run main.py

# Run with specific network file(s)
uv run main.py /path/to/network.nc
uv run main.py /path/to/network1.nc:Label1 /path/to/network2.nc:Label2
```

### Code Quality
```bash
# Format code using ruff
ruff format main.py

# Lint code
ruff check main.py --fix

# Type checking
mypy main.py
```

### Pre-commit hooks
The project uses pre-commit hooks with ruff for code formatting and linting. The configuration is in `.pre-commit-config.yaml` with a line length of 125 characters.

## Architecture Overview

This is a PyPSA network visualization dashboard built with Dash and Plotly. The application provides interactive visualizations for energy system analysis.

### Main Components

1. **main.py** - Single-file Dash application containing:
   - Dashboard layout with multiple tabs (Energy Balance, Capacity, CAPEX/OPEX, Network Map)
   - Callbacks for interactive filtering by carrier and country
   - Network loading and switching functionality
   - Welcome page with navigation to main dashboard

2. **Key Features**:
   - Multi-network support with dropdown selector
   - Interactive filtering by energy carrier (sector) and country
   - Six visualization tabs:
     - Energy Balance Timeseries
     - Energy Balance Totals
     - Capacity Totals
     - CAPEX Totals
     - OPEX Totals
     - Network Configuration (map + metadata)

3. **Dependencies** (declared in script header):
   - Uses `uv` runner for dependency management
   - Key packages: pypsa (from git), plotly, dash, folium, dash-bootstrap-components
   - Requires Python >= 3.12

### Data Flow
1. Networks are loaded from .nc (NetCDF) files containing PyPSA network objects
2. Statistics are accessed via `network.statistics` accessor
3. Interactive plots are generated using PyPSA's built-in plotting methods
4. Dash callbacks handle user interactions and update visualizations

### Important Patterns
- Reusable UI components for country/carrier selection panels
- Standardized error handling and user messages
- Callbacks use global network state that updates when switching networks
- Custom CSS styling embedded in the application