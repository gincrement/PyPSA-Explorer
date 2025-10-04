# PyPSA Explorer Examples

This directory contains example scripts and notebooks demonstrating various ways to use PyPSA Explorer.

## Quick Start Examples

### 1. Basic Usage (`basic_usage.py`)

Demonstrates the simplest ways to run PyPSA Explorer:
- With default demo network
- With custom network file
- With multiple networks
- With custom host/port settings

```bash
python basic_usage.py
```

### 2. Programmatic Usage (`programmatic_usage.py`)

Shows how to use PyPSA Explorer programmatically:
- Creating app with PyPSA Network objects
- Multiple network scenarios
- Integration with existing Flask/Dash infrastructure
- Production deployment with gunicorn

```bash
python programmatic_usage.py
```

## Command-Line Examples

### Run with demo network
```bash
pypsa-explorer
```

### Run with your network
```bash
pypsa-explorer /path/to/network.nc
```

### Run with multiple networks
```bash
pypsa-explorer \
    /path/to/network1.nc:Scenario_A \
    /path/to/network2.nc:Scenario_B
```

### Production deployment
```bash
pypsa-explorer \
    /path/to/network.nc \
    --host 0.0.0.0 \
    --port 8080 \
    --no-debug
```

## Python API Examples

### Simple usage
```python
from pypsa_explorer import run_dashboard

run_dashboard("/path/to/network.nc")
```

### With multiple networks
```python
from pypsa_explorer import run_dashboard

networks = {
    "Scenario A": "/path/to/network1.nc",
    "Scenario B": "/path/to/network2.nc",
}

run_dashboard(networks, debug=True, host="0.0.0.0", port=8050)
```

### With Network objects
```python
import pypsa
from pypsa_explorer import run_dashboard

n1 = pypsa.Network("network1.nc")
n2 = pypsa.Network("network2.nc")

run_dashboard({"Network 1": n1, "Network 2": n2})
```

### Programmatic app creation
```python
from pypsa_explorer import create_app

app = create_app(
    networks_input="/path/to/network.nc",
    title="My Custom Dashboard"
)

# Run with custom settings
app.run(debug=True, host="0.0.0.0", port=8050)
```

## Advanced Usage

### Custom Styling

Modify `src/pypsa_explorer/config.py` to customize colors and themes:

```python
COLORS = {
    "primary": "#your-color",
    "secondary": "#your-color",
    # ...
}
```

### Integration with Jupyter

```python
# In a Jupyter notebook
from pypsa_explorer import create_app
import pypsa

n = pypsa.Network("network.nc")
app = create_app({"My Network": n})

# Run in notebook (requires jupyter-dash)
app.run_server(mode='inline', port=8050)
```

### Docker Deployment

Create a `Dockerfile`:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY . .

RUN pip install pypsa-explorer

EXPOSE 8050

CMD ["pypsa-explorer", "--host", "0.0.0.0", "--port", "8050", "--no-debug"]
```

Build and run:

```bash
docker build -t pypsa-explorer .
docker run -p 8050:8050 -v /path/to/networks:/data pypsa-explorer /data/network.nc
```

## Creating Custom Networks

### Minimal Example

```python
import pypsa

n = pypsa.Network()

# Add buses
n.add("Bus", "bus1", carrier="AC", x=0, y=0, country="DE")
n.add("Bus", "bus2", carrier="AC", x=1, y=1, country="FR")

# Add carriers
n.add("Carrier", "wind", nice_name="Wind", color="#74c6f2")
n.add("Carrier", "solar", nice_name="Solar", color="#ffea00")

# Add generators
n.add("Generator", "wind_gen", bus="bus1", carrier="wind", p_nom=100)
n.add("Generator", "solar_gen", bus="bus2", carrier="solar", p_nom=50)

# Add transmission
n.add("Line", "line1", bus0="bus1", bus1="bus2", x=0.1, r=0.01, s_nom=100)

# Add metadata
n.meta = {
    "name": "Example Network",
    "version": "1.0",
    "wildcards": {
        "run": "example",
        "planning_horizons": "2030"
    }
}

# Save and use with PyPSA Explorer
n.export_to_netcdf("example_network.nc")
```

## Tips and Best Practices

1. **Network Size**: For large networks (>10k buses), consider:
   - Aggregating the network first
   - Using spatial filtering
   - Increasing server timeout settings

2. **Multiple Networks**: When comparing scenarios:
   - Use consistent naming conventions
   - Ensure networks have compatible structures
   - Use the same carriers and countries

3. **Performance**: For better performance:
   - Run in production mode (`--no-debug`)
   - Use a production WSGI server (gunicorn, waitress)
   - Enable caching for static assets

4. **Deployment**: For production deployment:
   - Use environment variables for configuration
   - Set up proper logging
   - Use a reverse proxy (nginx, Apache)
   - Enable HTTPS

## Need Help?

- Check the [main README](../README.md)
- See [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines
- Open an issue on [GitHub](https://github.com/openenergytransition/pypsa-explorer/issues)
