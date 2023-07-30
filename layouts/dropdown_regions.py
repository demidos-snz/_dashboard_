from dash import html, dcc

from constants import REGIONS, DEFAULT_DROPDOWN_REGIONS_VALUE, DEFAULT_DROPDOWN_REGIONS_PLACEHOLDER


def dropdown_regions_layout():
    return html.Div(
        id='div_regions_list',
        style={
            'width': '300px',
        },
        children=dcc.Dropdown(
            id='dropdown_regions',
            options=REGIONS,
            value=DEFAULT_DROPDOWN_REGIONS_VALUE,
            clearable=False,
            placeholder=DEFAULT_DROPDOWN_REGIONS_PLACEHOLDER,
        ),
    )
