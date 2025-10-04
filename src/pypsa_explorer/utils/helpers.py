"""Helper utility functions for PyPSA Explorer."""

import re
from typing import Any

import pypsa
from dash import html


def title_except_multi_caps(text: str) -> str:
    """
    Convert words to title case, except words with multiple uppercase letters.

    Parameters
    ----------
    text : str
        The input string to process

    Returns
    -------
    str
        Processed string with words in title case, except those with multiple uppercase letters
    """
    words = text.split()
    result = []

    for word in words:
        uppercase_count = sum(1 for char in word if char.isupper())
        if uppercase_count > 1:
            result.append(word)
        else:
            result.append(word.capitalize())

    return " ".join(result)


def get_carrier_nice_name(n: pypsa.Network, carrier: str) -> str:
    """
    Retrieve the nice name of a carrier from the network.

    Falls back to the carrier index if not available.

    Parameters
    ----------
    n : pypsa.Network
        The PyPSA network object
    carrier : str
        The carrier name to retrieve the nice name for

    Returns
    -------
    str
        The nice name of the carrier or the carrier index if no nice name is available
    """
    return title_except_multi_caps(
        n.carriers.nice_name.where(n.carriers.nice_name.ne(""), n.carriers.index.to_series()).at[carrier]
    )


def convert_latex_to_html(text: str) -> html.Span:
    """
    Convert LaTeX-style subscripts to HTML.

    Parameters
    ----------
    text : str
        Text that may contain LaTeX subscript notation like H$_2$

    Returns
    -------
    html.Span
        A Dash HTML component with proper subscript formatting
    """
    # Pattern to match LaTeX subscripts like $_2$ or $_{2}$
    pattern = r"\$_\{?([^$}]+)\}?\$"

    # Split the text by the pattern
    parts = re.split(pattern, text)

    # Build the HTML elements
    elements = []
    for i, part in enumerate(parts):
        if i % 2 == 0:
            # Regular text
            if part:
                elements.append(part)
        else:
            # Subscript text
            elements.append(html.Sub(part))

    return html.Span(elements)


def get_bus_carrier_options(n: pypsa.Network) -> list[dict[str, Any]]:
    """
    Get the bus carrier options for dropdown/checklist components.

    Parameters
    ----------
    n : pypsa.Network
        The PyPSA network object

    Returns
    -------
    list[dict[str, Any]]
        List of options with label and value for each carrier
    """
    return [
        {
            "label": html.Span([" ", convert_latex_to_html(get_carrier_nice_name(n, carrier))]),  # type: ignore[list-item]
            "value": carrier,
        }
        for carrier in sorted(n.buses.carrier.unique())
        if carrier != "none"
    ]


def get_country_options(n: pypsa.Network) -> list[dict[str, str]]:
    """
    Get the country options for dropdown components.

    Parameters
    ----------
    n : pypsa.Network
        The PyPSA network object

    Returns
    -------
    list[dict[str, str]]
        Sorted list of country options with label and value
    """
    options = [{"label": country, "value": country} for country in n.buses.country.unique()]
    return sorted(options, key=lambda x: x["label"])


def get_country_filter(country_mode: str, selected_countries: list[str]) -> tuple[str | None, str | None, html.Div | None]:
    """
    Determine the query string and facet column based on country selection.

    Parameters
    ----------
    country_mode : str
        Either "All" or "Specific" to indicate filtering mode
    selected_countries : list[str]
        List of selected country codes

    Returns
    -------
    tuple
        (query, facet_col, error_message_component | None)
    """
    from pypsa_explorer.layouts.components import PLEASE_SELECT_COUNTRY_MSG

    if country_mode == "Specific":
        if not selected_countries:
            return None, None, PLEASE_SELECT_COUNTRY_MSG
        else:
            formatted_countries = [f"'{c}'" for c in selected_countries]
            query = f"country in [{', '.join(formatted_countries)}]"
            return query, "country", None
    # Default is "All" countries
    return None, None, None
