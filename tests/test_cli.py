"""Tests for command-line interface."""

from unittest.mock import patch

import pytest

from pypsa_explorer.cli import main


def test_cli_version(capsys):
    """Test --version flag."""
    with pytest.raises(SystemExit) as exc_info:
        with patch("sys.argv", ["pypsa-explorer", "--version"]):
            main()

    assert exc_info.value.code == 0


def test_cli_help(capsys):
    """Test --help flag."""
    with pytest.raises(SystemExit) as exc_info:
        with patch("sys.argv", ["pypsa-explorer", "--help"]):
            main()

    assert exc_info.value.code == 0


@patch("pypsa_explorer.cli.run_dashboard")
def test_cli_default_args(mock_run):
    """Test CLI with default arguments."""
    with patch("sys.argv", ["pypsa-explorer"]):
        try:
            main()
        except SystemExit:
            pass

    # Check run_dashboard was called with expected defaults
    mock_run.assert_called_once()
    call_kwargs = mock_run.call_args.kwargs
    assert call_kwargs["debug"] == True
    assert call_kwargs["host"] == "127.0.0.1"
    assert call_kwargs["port"] == 8050


@patch("pypsa_explorer.cli.run_dashboard")
def test_cli_custom_port(mock_run):
    """Test CLI with custom port."""
    with patch("sys.argv", ["pypsa-explorer", "--port", "9000"]):
        try:
            main()
        except SystemExit:
            pass

    call_kwargs = mock_run.call_args.kwargs
    assert call_kwargs["port"] == 9000


@patch("pypsa_explorer.cli.run_dashboard")
def test_cli_no_debug(mock_run):
    """Test CLI with --no-debug flag."""
    with patch("sys.argv", ["pypsa-explorer", "--no-debug"]):
        try:
            main()
        except SystemExit:
            pass

    call_kwargs = mock_run.call_args.kwargs
    assert call_kwargs["debug"] == False


@patch("pypsa_explorer.cli.run_dashboard")
def test_cli_with_network_file(mock_run):
    """Test CLI with network file argument."""
    with patch("sys.argv", ["pypsa-explorer", "/path/to/network.nc"]):
        try:
            main()
        except SystemExit:
            pass

    mock_run.assert_called_once()
    networks_arg = mock_run.call_args.kwargs["networks_input"]
    assert networks_arg == {"network": "/path/to/network.nc"}


@patch("pypsa_explorer.cli.run_dashboard")
def test_cli_with_labeled_networks(mock_run):
    """Test CLI with labeled network files."""
    with patch("sys.argv", ["pypsa-explorer", "/path/to/n1.nc:Label1", "/path/to/n2.nc:Label2"]):
        try:
            main()
        except SystemExit:
            pass

    networks_arg = mock_run.call_args.kwargs["networks_input"]
    assert networks_arg == {"Label1": "/path/to/n1.nc", "Label2": "/path/to/n2.nc"}
