"""Network loading utilities for PyPSA Explorer."""

import logging
import os

import matplotlib.pyplot as plt
import pandas as pd
import pypsa

logger = logging.getLogger(__name__)


def load_networks(
    network_input: dict[str, pypsa.Network | str] | str | None = None,
    default_network_path: str = "demo-network.nc",
) -> dict[str, pypsa.Network]:
    """
    Load PyPSA networks from various input formats.

    Parameters
    ----------
    network_input : dict, str, or None
        Can be:
        - dict: {label: network_object_or_path} mapping labels to Network objects or file paths
        - str: Single path to a network file
        - None: Load default demo network
    default_network_path : str
        Path to default network file when network_input is None

    Returns
    -------
    dict[str, pypsa.Network]
        Dictionary mapping labels to loaded Network objects

    Raises
    ------
    FileNotFoundError
        If a specified network file does not exist
    ValueError
        If no valid networks could be loaded
    """
    networks: dict[str, pypsa.Network] = {}

    if network_input is None:
        # Load default network
        if os.path.exists(default_network_path):
            n = pypsa.Network(default_network_path)
            ensure_carriers_defined(n)
            networks = {"Network": n}
        else:
            raise FileNotFoundError(f"Default network file not found: {default_network_path}")

    elif isinstance(network_input, str):
        # Single network path provided
        if os.path.exists(network_input):
            n = pypsa.Network(network_input)
            ensure_carriers_defined(n)
            networks = {"Network": n}
        else:
            raise FileNotFoundError(f"Network file not found: {network_input}")

    elif isinstance(network_input, dict):
        # Dictionary of networks provided
        for label, net_or_path in network_input.items():
            if isinstance(net_or_path, str):
                if os.path.exists(net_or_path):
                    n = pypsa.Network(net_or_path)
                    ensure_carriers_defined(n)
                    networks[label] = n
                else:
                    print(f"Warning: Network file not found: {net_or_path}")
            elif isinstance(net_or_path, pypsa.Network):
                ensure_carriers_defined(net_or_path)
                networks[label] = net_or_path
            else:
                print(f"Warning: Invalid type for network {label}. Skipping.")
    else:
        raise ValueError("network_input must be either a string path, a dictionary {label: path}, or None")

    if not networks:
        raise ValueError("No valid networks were loaded")

    return networks


def parse_cli_network_args(args: list[str]) -> dict[str, str]:
    """
    Parse command line arguments for network loading.

    Format: path:label or just path (label will be derived from filename)

    Parameters
    ----------
    args : list[str]
        Command line arguments in format "path:label" or "path"

    Returns
    -------
    dict[str, str]
        Dictionary mapping labels to file paths
    """
    network_paths = {}

    for arg in args:
        if ":" in arg:
            path, label = arg.split(":", 1)
        else:
            path = arg
            # Create default label from filename
            label = os.path.splitext(os.path.basename(path))[0]

        network_paths[label] = path

    return network_paths


def get_unique_carriers(n: pypsa.Network) -> set[str]:
    """
    Collect all unique carrier values from all network components.

    Parameters
    ----------
    n : pypsa.Network
        The PyPSA network object

    Returns
    -------
    set[str]
        Set of all unique carrier names found in the network
    """
    carriers: set[str] = set()

    for c in n.c.values():
        if c.static.empty or "carrier" not in c.static.columns:
            continue
        comp_carriers = c.static["carrier"].dropna()
        comp_carriers = comp_carriers[comp_carriers != ""]
        carriers.update(comp_carriers.unique())

    return carriers


def generate_colors(n_colors: int, palette: str = "tab10") -> list[str]:
    """
    Generate a list of hex colors from a matplotlib colormap.

    Parameters
    ----------
    n_colors : int
        Number of colors to generate
    palette : str, default "tab10"
        Matplotlib colormap name

    Returns
    -------
    list[str]
        List of hex color strings
    """
    cmap = plt.colormaps.get_cmap(palette)
    colors = []
    for i in range(n_colors):
        rgba = cmap(i % cmap.N)
        r, g, b = int(rgba[0] * 255), int(rgba[1] * 255), int(rgba[2] * 255)
        hex_color = f"#{r:02x}{g:02x}{b:02x}"
        colors.append(hex_color)
    return colors


def ensure_carriers_defined(n: pypsa.Network, palette: str = "tab10") -> None:
    """
    Ensure all carriers used in the network are defined in n.carriers with colors.

    This function:
    1. Collects all carriers used across network components
    2. Adds any missing carriers to n.carriers
    3. Assigns colors to carriers that don't have one

    Parameters
    ----------
    n : pypsa.Network
        The PyPSA network object to process
    palette : str, default "tab10"
        Matplotlib color palette for assigning colors to carriers
    """
    used_carriers = get_unique_carriers(n)
    existing_carriers = set(n.carriers.index)
    missing_carriers = sorted(used_carriers - existing_carriers)

    if missing_carriers:
        logger.info("Adding %d missing carriers: %s", len(missing_carriers), missing_carriers)
        for carrier in missing_carriers:
            n.carriers.loc[carrier] = pd.Series(dtype=object)

    # Assign colors to carriers without a valid color
    carriers_needing_color = []
    for carrier in n.carriers.index:
        color = n.carriers.at[carrier, "color"]
        if pd.isna(color) or color == "":
            carriers_needing_color.append(carrier)

    if carriers_needing_color:
        carriers_needing_color = sorted(carriers_needing_color)
        colors = generate_colors(len(carriers_needing_color), palette)
        for carrier, color in zip(carriers_needing_color, colors, strict=False):
            n.carriers.at[carrier, "color"] = color
        logger.info(
            "Assigned colors to %d carriers using '%s' palette.",
            len(carriers_needing_color),
            palette,
        )
