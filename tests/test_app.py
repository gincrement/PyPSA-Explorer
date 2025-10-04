"""Tests for main application module."""


from pypsa_explorer.app import create_app


def test_create_app_with_demo_network(demo_network):
    """Test app creation with a demo network."""
    app = create_app({"Test": demo_network})
    assert app is not None
    assert app.title == "PyPSA Explorer"


def test_create_app_with_network_path(demo_network_path):
    """Test app creation with network file path."""
    app = create_app(demo_network_path)
    assert app is not None


def test_create_app_with_dict(networks_dict):
    """Test app creation with multiple networks."""
    app = create_app(networks_dict)
    assert app is not None


def test_create_app_with_none():
    """Test app creation with default network (uses demo-network.nc if available)."""
    # This test will pass if demo-network.nc exists in the project root
    try:
        app = create_app(None)
        assert app is not None
    except FileNotFoundError:
        # This is also acceptable if demo-network.nc doesn't exist
        pass


def test_create_app_custom_title(demo_network):
    """Test app creation with custom title."""
    app = create_app({"Test": demo_network}, title="Custom Dashboard")
    assert app.title == "Custom Dashboard"


def test_app_has_layout(demo_network):
    """Test that created app has a layout."""
    app = create_app({"Test": demo_network})
    assert app.layout is not None


def test_app_has_callbacks(demo_network):
    """Test that callbacks are registered."""
    app = create_app({"Test": demo_network})
    # Check that callbacks exist
    assert len(app.callback_map) > 0
