# PyPSA Explorer

Interactive dashboard for visualizing and analyzing PyPSA energy system networks using the interactive plotting features of PyPSA.

## Features
- Load one or more PyPSA networks and switch between them via a dropdown selector.
- Interactive tabs for:
  - Energy Balance
  - Aggregated Energy Balance
  - Capacity
  - CAPEX Totals
  - OPEX Totals
  - Network Map
- Filtering by carrier (sector) and country.
- Customizable layout and styling using Dash, Plotly, and Bootstrap.

## Requirements
- Python >= 3.12
- `uv` runner tool (no prior installation required)

Dependencies are declared in the header of `main.py` and will be automatically installed when running via `uv`.

## Usage
Run the dashboard with the default example network:

```bash
uv run main.py
```

Run the dashboard with one or more network files (specify `path:label` pairs; labels are optional):

```bash
uv run main.py /path/to/network1.nc:Region1 /path/to/network2.nc
```

Alternatively, import and run from Python:

```python
from main import run_dashboard

networks = {
    "Region1": "/path/to/network1.nc",
    "Region2": "/path/to/network2.nc",
}
run_dashboard(networks, debug=True)
```

Navigate through the welcome screen, select your network, and explore the interactive visualizations.

## Repository Structure
- `main.py`: Main Dash application script.
- `README.md`: Project overview and instructions.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for bug fixes, enhancements, or new features.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
