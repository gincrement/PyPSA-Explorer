#!/usr/bin/env python
"""
Programmatic Usage Example for PyPSA Explorer

This example shows how to use PyPSA Explorer programmatically,
creating the app instance and running it with custom configurations.
"""

import pypsa

from pypsa_explorer import create_app

# Example 1: Create app with PyPSA Network object
print("Creating app with PyPSA Network object...")

# Load a network
n = pypsa.Network()
# Add some components (or load from file)
n.add("Bus", "bus1", carrier="AC", x=0, y=0, country="DE")
n.add("Bus", "bus2", carrier="AC", x=1, y=1, country="FR")
n.add("Carrier", "wind", nice_name="Wind", color="#74c6f2")
n.add("Generator", "gen1", bus="bus1", carrier="wind", p_nom=100)

# Create app
app = create_app({"My Network": n}, title="Custom Dashboard")

# Run app
# app.run(debug=True, host="127.0.0.1", port=8050)

# Example 2: Create app with multiple networks
print("\nCreating app with multiple network objects...")

n1 = pypsa.Network()
n1.add("Bus", "bus1", carrier="AC", x=0, y=0)
n1.add("Carrier", "solar", nice_name="Solar", color="#ffea00")

n2 = pypsa.Network()
n2.add("Bus", "bus1", carrier="AC", x=0, y=0)
n2.add("Carrier", "wind", nice_name="Wind", color="#74c6f2")

networks = {
    "Solar Scenario": n1,
    "Wind Scenario": n2,
}

app = create_app(networks, title="Scenario Comparison")

# Example 3: Integrate with existing Flask/Dash infrastructure
print("\nIntegrating with existing infrastructure...")

# Get the Dash app instance
app = create_app("/path/to/network.nc")

# Access the underlying Flask server
# server = app.server

# Add custom routes or middleware
# @server.route('/health')
# def health_check():
#     return {'status': 'healthy'}

# Run with gunicorn in production
# gunicorn --bind 0.0.0.0:8050 app:server

print("\nApp created successfully!")
print("Uncomment the app.run() lines to start the server.")
