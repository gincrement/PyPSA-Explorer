"""Theme callbacks for dark mode toggle."""

from dash import Input, Output, callback


def register_theme_callbacks(app) -> None:
    """
    Register callbacks for theme/dark mode functionality.

    Parameters
    ----------
    app : dash.Dash
        The Dash application instance
    """

    @callback(
        Output("app-container", "className"),
        Input("dark-mode-toggle", "value"),
        prevent_initial_call=False,
    )
    def toggle_dark_mode(toggle_value):
        """Apply the appropriate theme class based on toggle state."""

        is_dark = "dark" in (toggle_value or [])
        return "dark-mode" if is_dark else ""
