"""Network-related callbacks for PyPSA Explorer dashboard."""

from typing import Any

import folium
import pypsa
import pypsa.consistency
import yaml
from dash import Input, Output, html

from pypsa_explorer.utils.helpers import get_bus_carrier_options, get_country_options


def register_network_callbacks(app, networks: dict[str, pypsa.Network]) -> None:
    """Register network-related callbacks."""

    @app.callback(
        [
            Output("global-carrier-selector", "options"),
            Output("global-country-selector", "options"),
        ],
        [Input("network-selector", "value")],
    )
    def update_selected_network(selected_network_label: str) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
        """Update filter options when user selects a different network."""
        n = networks[selected_network_label]

        # Update bus carrier options for the new network
        updated_bus_carrier_options = get_bus_carrier_options(n)

        # Update country options for the new network
        updated_country_options = get_country_options(n)

        return updated_bus_carrier_options, updated_country_options

    @app.callback(
        Output("network-map", "srcDoc"),
        [
            Input("refresh-map-button", "n_clicks"),
            Input("network-selector", "value"),
        ],
    )
    def update_map(n_clicks: int | None, selected_network_label: str) -> str:  # noqa: ARG001
        """Update network map visualization."""
        n = networks[selected_network_label]
        try:
            # Create a folium map using PyPSA's explore method
            # Note: popup and components parameters removed for PyPSA v1.0 compatibility
            map_obj: folium.Map = n.plot.explore(tooltip=True)
            return map_obj._repr_html_()
        except Exception as e:
            print(f"Error creating map: {e}")
            return f"<div style='padding:20px;'><h2>Map visualization unavailable</h2><p>Error: {str(e)}</p></div>"

    @app.callback(
        Output("network-metadata", "children"),
        [
            Input("refresh-map-button", "n_clicks"),
            Input("network-selector", "value"),
        ],
    )
    def update_metadata(n_clicks: int | None, selected_network_label: str) -> html.Pre | html.Div:  # noqa: ARG001
        """Display network metadata."""
        n = networks[selected_network_label]
        try:
            # Convert network metadata to YAML format
            metadata_yaml: str = yaml.dump(n.meta, default_flow_style=False, sort_keys=False)

            return html.Pre(
                metadata_yaml,
                style={
                    "background-color": "#FAFBFC",
                    "padding": "10px",
                    "border-radius": "5px",
                    "color": "var(--text-color)",
                },
            )
        except Exception as e:
            print(f"Error displaying metadata: {e}")
            return html.Div(
                [
                    html.H5("Metadata Unavailable", className="text-muted"),
                    html.P(f"Error: {str(e)}", className="text-danger"),
                ]
            )
