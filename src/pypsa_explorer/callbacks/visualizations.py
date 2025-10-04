"""Visualization callbacks for PyPSA Explorer dashboard."""

from collections.abc import Callable

import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pypsa
from dash import Input, Output, dcc, html

from pypsa_explorer.layouts.components import NO_DATA_MSG, PLEASE_SELECT_CARRIER_MSG, create_error_message
from pypsa_explorer.utils.helpers import get_carrier_nice_name, get_country_filter


def register_visualization_callbacks(app, networks: dict[str, pypsa.Network]) -> None:
    """Register visualization-related callbacks."""

    def create_energy_balance_callback(aggregated: bool = False) -> Callable:
        """
        Create a callback function for updating energy balance charts.

        Parameters
        ----------
        aggregated : bool
            Whether to create a callback for aggregated (True) or timeseries (False) views

        Returns
        -------
        Callable
            Callback function for updating energy balance charts
        """

        def update_energy_balance(
            selected_carriers: list[str],
            country_mode: str,
            selected_countries: list[str],
            selected_network_label: str,
        ) -> list[dbc.Col | html.Div | dcc.Graph] | html.Div:
            n = networks[selected_network_label]
            s = n.statistics

            if not selected_carriers:
                return [PLEASE_SELECT_CARRIER_MSG] if aggregated else PLEASE_SELECT_CARRIER_MSG

            # Use helper for country filtering
            query, facet_col, error_message = get_country_filter(country_mode, selected_countries)
            if error_message:
                return [error_message] if aggregated else error_message

            charts: list[dbc.Col | html.Div | dcc.Graph] = []

            for carrier in selected_carriers:
                try:
                    # Generate plot based on view type
                    plot_args = {
                        "x": "value",
                        "y": "carrier",
                        "color": "carrier",
                        "bus_carrier": carrier,
                        "nice_names": True,
                        "width": None,
                        "query": query,
                        "facet_col": facet_col,
                    }

                    if aggregated:
                        # Bar plot for aggregated view
                        fig = s.energy_balance.iplot.bar(**plot_args)
                    else:
                        # Area plot for timeseries view
                        plot_args.update(
                            {
                                "x": "snapshot",
                                "y": "value",
                                "stacked": True,
                                "height": 500,
                            }
                        )
                        fig = s.energy_balance.iplot.area(**plot_args)
                        # Adjust layout for area plot
                        fig.update_layout(
                            legend_title="Component Carrier",
                            hovermode="closest",
                            paper_bgcolor="#f5f7fa",
                            plot_bgcolor="#f5f7fa",
                        )

                    # Common title setting
                    carrier_name = get_carrier_nice_name(n, carrier)

                    title = f"{'Aggregated Balance' if aggregated else 'Energy Balance'} for {carrier_name}"
                    if facet_col and selected_countries:
                        countries_str = ", ".join(selected_countries)
                        title += f" (Countries: {countries_str})"

                    fig.update_layout(title=title, paper_bgcolor="#f5f7fa", plot_bgcolor="#f5f7fa")

                    graph_component = dcc.Graph(figure=fig)
                    charts.append(graph_component)

                except Exception as e:
                    error_context = f"carrier '{carrier}'"
                    carrier_error_message = create_error_message(error_context, e)
                    charts.append(carrier_error_message)

            # If no charts were created successfully, show a message
            if not charts:
                return [NO_DATA_MSG] if aggregated else NO_DATA_MSG

            return charts

        return update_energy_balance

    # Callback for Energy Balance charts (timeseries view)
    @app.callback(
        Output("energy-balance-charts-container", "children"),
        [
            Input("global-carrier-selector", "value"),
            Input("global-country-mode", "value"),
            Input("global-country-selector", "value"),
            Input("network-selector", "value"),
        ],
    )
    def update_energy_balance(
        selected_carriers: list[str],
        country_mode: str,
        selected_countries: list[str],
        selected_network_label: str,
    ) -> list[dbc.Col | html.Div | dcc.Graph] | html.Div:
        return create_energy_balance_callback(aggregated=False)(
            selected_carriers, country_mode, selected_countries, selected_network_label
        )

    # Callback for Aggregated Energy Balance charts
    @app.callback(
        Output("agg-energy-balance-charts-container", "children"),
        [
            Input("global-carrier-selector", "value"),
            Input("global-country-mode", "value"),
            Input("global-country-selector", "value"),
            Input("network-selector", "value"),
        ],
    )
    def update_energy_balance_aggregated(
        selected_carriers: list[str],
        country_mode: str,
        selected_countries: list[str],
        selected_network_label: str,
    ) -> list[dbc.Col | html.Div | dcc.Graph] | html.Div:
        return create_energy_balance_callback(aggregated=True)(
            selected_carriers, country_mode, selected_countries, selected_network_label
        )

    # Callback for Capacity charts
    @app.callback(
        Output("capacity-charts-container", "children"),
        [
            Input("global-carrier-selector", "value"),
            Input("global-country-mode", "value"),
            Input("global-country-selector", "value"),
            Input("network-selector", "value"),
        ],
    )
    def update_capacity_charts(
        selected_carriers: list[str],
        country_mode: str,
        selected_countries: list[str],
        selected_network_label: str,
    ) -> list[dcc.Graph | html.Div]:
        n = networks[selected_network_label]
        s = n.statistics

        if not selected_carriers:
            return [PLEASE_SELECT_CARRIER_MSG]

        # Use helper for country filtering
        query, facet_col, error_message = get_country_filter(country_mode, selected_countries)
        if error_message:
            return [error_message]

        charts: list[dcc.Graph | html.Div] = []

        for carrier in selected_carriers:
            try:
                # Generate capacity bar chart directly with carrier
                fig: go.Figure = s.optimal_capacity.iplot.bar(
                    x="value",
                    y="carrier",
                    color="carrier",
                    bus_carrier=carrier,
                    width=None,
                    height=500,
                    nice_names=True,
                    query=query,
                    facet_col=facet_col,
                )

                # Set title based on selections
                carrier_name = get_carrier_nice_name(n, carrier)
                title = f"Optimal Capacity for {carrier_name}"
                if facet_col and selected_countries:
                    countries_str = ", ".join(selected_countries)
                    title += f" (Countries: {countries_str})"

                fig.update_layout(title=title, paper_bgcolor="#f5f7fa", plot_bgcolor="#f5f7fa")

                # Add the graph without wrapping in dbc.Col so it takes full width
                charts.append(dcc.Graph(figure=fig, className="mb-4"))

            except Exception as e:
                message = create_error_message(f"carrier '{carrier}'", e)
                charts.append(message)

        # If no charts were created successfully, show a message
        if not charts:
            return [NO_DATA_MSG]

        return charts

    # Callback for CAPEX charts
    @app.callback(
        Output("capex-charts-container", "children"),
        [
            Input("global-country-mode", "value"),
            Input("global-country-selector", "value"),
            Input("network-selector", "value"),
        ],
    )
    def update_capex_charts(
        country_mode: str, selected_countries: list[str], selected_network_label: str
    ) -> list[dcc.Graph | html.Div]:
        n = networks[selected_network_label]
        s = n.statistics

        # Use helper for country filtering
        query, facet_col, error_message = get_country_filter(country_mode, selected_countries)
        if error_message:
            return [error_message]

        try:
            # Generate CAPEX bar chart
            fig: go.Figure = s.capex.iplot.bar(
                x="value",
                y="carrier",
                color="carrier",
                nice_names=True,
                height=1000,
                width=None,
                query=query,
                facet_col=facet_col,
            )

            # Set title based on selections
            title = "Capital Expenditure Totals"
            if facet_col and selected_countries:
                countries_str = ", ".join(selected_countries)
                title += f" (Countries: {countries_str})"

            # Apply robust height settings to prevent resizing
            fig.update_layout(
                title=title,
                height=1000,
                margin=dict(l=50, r=50, t=100, b=50),
                paper_bgcolor="#f5f7fa",
                plot_bgcolor="#f5f7fa",
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
            message = create_error_message("CAPEX chart", e)
            return [message]

    # Callback for OPEX charts
    @app.callback(
        Output("opex-charts-container", "children"),
        [
            Input("global-country-mode", "value"),
            Input("global-country-selector", "value"),
            Input("network-selector", "value"),
        ],
    )
    def update_opex_charts(
        country_mode: str, selected_countries: list[str], selected_network_label: str
    ) -> list[dcc.Graph | html.Div]:
        n = networks[selected_network_label]
        s = n.statistics

        # Use helper for country filtering
        query, facet_col, error_message = get_country_filter(country_mode, selected_countries)
        if error_message:
            return [error_message]

        try:
            # Generate OPEX bar chart
            fig: go.Figure = s.opex.iplot.bar(
                x="value",
                y="carrier",
                color="carrier",
                nice_names=True,
                height=1000,
                width=None,
                query=query,
                facet_col=facet_col,
            )

            # Set title based on selections
            title = "Operational Expenditure Totals"
            if facet_col and selected_countries:
                countries_str = ", ".join(selected_countries)
                title += f" (Countries: {countries_str})"

            # Apply robust height settings to prevent resizing
            fig.update_layout(
                title=title,
                height=1000,
                margin=dict(l=50, r=50, t=100, b=50),
                paper_bgcolor="#f5f7fa",
                plot_bgcolor="#f5f7fa",
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
            message = create_error_message("OPEX chart", e)
            return [message]
