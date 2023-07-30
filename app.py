import dash_bootstrap_components as dbc
from dash import Dash

from constants import TITLE_APP


app: Dash = Dash(
    name=__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title=TITLE_APP,
)
