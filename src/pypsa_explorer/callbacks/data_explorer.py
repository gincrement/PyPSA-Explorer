"""Data explorer callbacks for interactive component dataframe viewing."""

import pandas as pd
import pypsa
from dash import Input, Output, State, ctx, no_update

from pypsa_explorer.utils.data_table import dataframe_to_datatable, get_timeseries_attributes

# Mapping of KPI card IDs to component names
KPI_COMPONENT_MAP = {
    "kpi-card-buses": "buses",
    "kpi-card-generators": "generators",
    "kpi-card-lines": "lines",
    "kpi-card-links": "links",
    "kpi-card-storage_units": "storage_units",
    "kpi-card-stores": "stores",
}

# Human-readable labels for components
COMPONENT_LABELS = {
    "buses": "Nodes",
    "generators": "Generators",
    "lines": "Lines",
    "links": "Links",
    "storage_units": "Storage Units",
    "stores": "Stores",
}


def register_data_explorer_callbacks(app, networks: dict[str, pypsa.Network]) -> None:
    """Register callbacks for the data explorer modal."""

    @app.callback(
        [
            Output("data-explorer-modal", "is_open"),
            Output("data-explorer-modal-title", "children"),
            Output("static-data-table", "data"),
            Output("static-data-table", "columns"),
            Output("timeseries-attribute-selector", "options"),
            Output("timeseries-attribute-selector", "value"),
            Output("active-component-store", "data"),
        ],
        [
            Input("kpi-card-buses", "n_clicks"),
            Input("kpi-card-generators", "n_clicks"),
            Input("kpi-card-lines", "n_clicks"),
            Input("kpi-card-links", "n_clicks"),
            Input("kpi-card-storage_units", "n_clicks"),
            Input("kpi-card-stores", "n_clicks"),
            Input("close-data-explorer-modal", "n_clicks"),
        ],
        [
            State("network-selector", "value"),
            State("data-explorer-modal", "is_open"),
        ],
    )
    def toggle_modal_and_load_data(
        buses_clicks: int,  # noqa: ARG001
        generators_clicks: int,  # noqa: ARG001
        lines_clicks: int,  # noqa: ARG001
        links_clicks: int,  # noqa: ARG001
        storage_units_clicks: int,  # noqa: ARG001
        stores_clicks: int,  # noqa: ARG001
        close_clicks: int,  # noqa: ARG001
        network_label: str,
        is_open: bool,  # noqa: ARG001
    ) -> tuple:
        """Toggle modal and load component data when KPI card is clicked."""
        # Get the ID of the component that triggered the callback
        triggered_id = ctx.triggered_id

        # If close button was clicked, close the modal
        if triggered_id == "close-data-explorer-modal":
            return False, no_update, no_update, no_update, no_update, no_update, no_update

        # If no KPI card was clicked, don't update
        if triggered_id not in KPI_COMPONENT_MAP:
            return no_update, no_update, no_update, no_update, no_update, no_update, no_update

        # Get the component name from the triggered card
        component_name = KPI_COMPONENT_MAP[triggered_id]
        component_label = COMPONENT_LABELS[component_name]

        # Get the active network
        n = networks[network_label]

        # Get the component dataframe
        if not hasattr(n, component_name):
            return (
                True,
                f"{component_label} - No Data Available",
                [],
                [],
                [],
                None,
                component_name,
            )

        component_df = getattr(n, component_name)

        # Convert dataframe to dict for DataTable using utility
        if isinstance(component_df, pd.DataFrame):
            data, columns = dataframe_to_datatable(component_df)
        else:
            data = []
            columns = []

        # Get available time-series attributes using efficient utility
        timeseries_attrs = get_timeseries_attributes(n, component_name)
        timeseries_options = [{"label": attr, "value": attr} for attr in timeseries_attrs]

        return (
            True,  # Open modal
            f"{component_label} Data ({len(component_df):,} records)",
            data,
            columns,
            timeseries_options,
            timeseries_options[0]["value"] if timeseries_options else None,
            component_name,  # Store component name for efficient lookup
        )

    @app.callback(
        [
            Output("timeseries-data-table", "data"),
            Output("timeseries-data-table", "columns"),
        ],
        [
            Input("timeseries-attribute-selector", "value"),
        ],
        [
            State("active-component-store", "data"),
            State("network-selector", "value"),
        ],
    )
    def update_timeseries_data(
        selected_attribute: str | None,
        component_name: str | None,
        network_label: str,
    ) -> tuple:
        """Update time-series data table when attribute is selected."""
        if not selected_attribute or not component_name:
            return [], []

        # Get the active network
        n = networks[network_label]

        # Get time-series data
        timeseries_component = f"{component_name}_t"
        if not hasattr(n, timeseries_component):
            return [], []

        ts_obj = getattr(n, timeseries_component)
        if not hasattr(ts_obj, selected_attribute):
            return [], []

        ts_df = getattr(ts_obj, selected_attribute)

        if isinstance(ts_df, pd.DataFrame):
            # Use utility function for efficient conversion with uniform sampling
            data, columns = dataframe_to_datatable(ts_df, max_rows=5000)
            return data, columns

        return [], []
