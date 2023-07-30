import os
import typing as t

BASE_LAYOUT_STYLE: dict[str, t.Any] = {
    'position': 'relative',
    'maxWidth': '1200px',
    'margin-bottom': 30,
    'margin-right': 'auto',
    'margin-left': 'auto',
}

DEFAULT_RADIO_ITEM: str = 'cpd_charged_sum'

BUTTON_STYLE: dict[str, t.Any] = {
    'fontFamily': 'RobotoCondensed-Light',
    'margin-right': 20,
    'display': 'inline-block',
    'height': '36px',
    'color': '#555',
    'textAlign': 'center',
    'font-size': '11px',
    'line-height': '37px',
    'letterSpacing': '.1rem',
    'text-transform': 'uppercase',
    'font-weight': 'bold',
    'text-decoration': 'none',
    'white-space': 'nowrap',
    'background-color': 'transparent',
    'border-radius': '4px',
    'border': '1px solid #bbb',
    'cursor': 'pointer',
    'box-sizing': 'border-box',
}

SUNBURST_CSV_PATH: str = os.path.normpath('sunburst.csv')
GEOJSON_PATH: str = os.path.normpath('result.geojson')
