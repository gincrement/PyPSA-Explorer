"""Navigation callbacks for PyPSA Explorer dashboard."""

from dash import Input, Output, State, no_update


def register_navigation_callbacks(app) -> None:
    """Register navigation-related callbacks."""

    @app.callback(
        [
            Output("welcome-content", "style"),
            Output("dashboard-content", "style"),
            Output("page-state", "data"),
        ],
        [Input("enter-dashboard-btn", "n_clicks")],
        [State("page-state", "data")],
    )
    def navigate_pages(
        n_clicks: int | None, page_state: dict[str, str]
    ) -> tuple[dict[str, str], dict[str, str], dict[str, str]]:
        """Manage navigation between welcome page and dashboard."""
        if n_clicks and page_state["current_page"] == "welcome":
            return {"display": "none"}, {"display": "block"}, {"current_page": "dashboard"}
        # Return current state if no click or already on dashboard
        return no_update, no_update, no_update  # type: ignore[return-value]
