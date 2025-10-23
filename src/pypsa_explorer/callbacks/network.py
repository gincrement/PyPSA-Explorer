"""Network-related callbacks for PyPSA Explorer dashboard."""

from typing import Any

import folium
import pypsa
import pypsa.consistency
import yaml
from dash import ALL, Input, Output, State, ctx, html

from pypsa_explorer.layouts.components import create_header
from pypsa_explorer.utils.helpers import get_bus_carrier_options, get_country_options


def register_network_callbacks(app, networks: dict[str, pypsa.Network]) -> None:
    """Register network-related callbacks."""

    @app.callback(
        [
            Output("network-selector", "data"),
            Output({"type": "network-button", "index": ALL}, "className"),
        ],
        [Input({"type": "network-button", "index": ALL}, "n_clicks")],
        [
            State({"type": "network-button", "index": ALL}, "id"),
            State("network-selector", "data"),
        ],
    )
    def handle_network_button_click(
        n_clicks: list[int],  # noqa: ARG001
        button_ids: list[dict],
        current_network: str,
    ) -> tuple[str, list[str]]:
        """Handle network button clicks and update active state."""
        if not ctx.triggered_id:
            # Initial load - set active button
            class_names = [
                "network-button network-button-active" if btn["index"] == current_network else "network-button"
                for btn in button_ids
            ]
            return current_network, class_names

        # Get the clicked button's network label
        clicked_network = ctx.triggered_id["index"]

        # Update button styles
        class_names = [
            "network-button network-button-active" if btn["index"] == clicked_network else "network-button"
            for btn in button_ids
        ]

        return clicked_network, class_names

    @app.callback(
        [
            Output("global-carrier-selector", "options"),
            Output("global-country-selector", "options"),
        ],
        [Input("network-selector", "data")],
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
        Output("kpi-header-container", "children"),
        [Input("network-selector", "data")],
    )
    def update_kpi_header(selected_network_label: str) -> html.Div:
        """Update KPI header when network changes."""
        n = networks[selected_network_label]
        return create_header(n)

    @app.callback(
        Output("network-map", "srcDoc"),
        [
            Input("refresh-map-button", "n_clicks"),
            Input("network-selector", "data"),
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
            Input("network-selector", "data"),
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
