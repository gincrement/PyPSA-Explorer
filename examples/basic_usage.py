#!/usr/bin/env python
"""
Basic Usage Example for PyPSA Explorer

This example demonstrates the simplest way to run PyPSA Explorer
with a demo network or your own network file.
"""


# Example 1: Run with default demo network
print("Example 1: Running with default demo network...")
# run_dashboard()  # Uncomment to run

# Example 2: Run with a custom network file
print("\nExample 2: Running with custom network...")
# run_dashboard("/path/to/your/network.nc")  # Uncomment and update path

# Example 3: Run with multiple networks
print("\nExample 3: Running with multiple networks...")
networks = {
    "Scenario A": "/path/to/network1.nc",
    "Scenario B": "/path/to/network2.nc",
}
# run_dashboard(networks)  # Uncomment and update paths

# Example 4: Run with custom host and port (for deployment)
print("\nExample 4: Running on custom host and port...")
# run_dashboard(
#     "/path/to/network.nc",
#     debug=False,  # Production mode
#     host="0.0.0.0",  # Listen on all interfaces
#     port=8080,  # Custom port
# )

print("\nUncomment the examples you want to run!")
