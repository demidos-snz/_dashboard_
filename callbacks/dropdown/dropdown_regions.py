import plotly.graph_objects as go
from dash import html, Output, Input

from app import app
from callbacks.utils import get_charts_by_region
from init_data import df_all
from layouts.dropdown_regions import dropdown_regions_layout


def hide_map_by_dropdown_regions_layout():
    return html.Div(
        # fixme id
        id='',
        children=[
            dropdown_regions_layout(),
        ],
    )


@app.callback(
    [
        Output(component_id='back_to_map', component_property='children', allow_duplicate=True),
        Output(component_id='back_to_map', component_property='style', allow_duplicate=True),

        Output(component_id='div_total_for_russia', component_property='style', allow_duplicate=True),
        Output(component_id='div_map', component_property='style', allow_duplicate=True),
        Output(component_id='div_statistic_settings', component_property='style', allow_duplicate=True),

        Output(component_id='graph_charges_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='div_charges_sum', component_property='style', allow_duplicate=True),
        Output(component_id='graph_already_payed_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='div_already_payed_sum', component_property='style', allow_duplicate=True),
        Output(component_id='graph_debts_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='div_debts_sum', component_property='style', allow_duplicate=True),
        Output(component_id='graph_cr_charges_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='div_cr_charges_sum', component_property='style', allow_duplicate=True),
        Output(component_id='graph_cr_payed_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='div_cr_payed_sum', component_property='style', allow_duplicate=True),
        Output(component_id='div_cr_total_for_russia', component_property='style', allow_duplicate=True),

        Output(component_id='div_regions_list', component_property='style', allow_duplicate=True),

        Output(component_id='region_name', component_property='children', allow_duplicate=True),
        Output(component_id='region_name', component_property='style', allow_duplicate=True),

        Output(component_id='span_cr_charged_sum', component_property='children', allow_duplicate=True),
        Output(component_id='span_cr_payed_sum', component_property='children', allow_duplicate=True),
        Output(component_id='span_cr_debts_sum', component_property='children', allow_duplicate=True),

        Output(component_id='graph_sunburst', component_property='figure', allow_duplicate=True),
        Output(component_id='div_sunburst', component_property='style', allow_duplicate=True),
    ],
    Input(component_id='dropdown_regions', component_property='value'),
    prevent_initial_call=True,
)
def hide_map_by_dropdown_region(region: str) -> tuple[
    html.Button, dict[str, str],

    dict[str, str], dict[str, str], dict[str, str],

    go.Figure, dict[str, str],
    go.Figure, dict[str, str],
    go.Figure, dict[str, str],
    go.Figure, dict[str, str],
    go.Figure, dict[str, str],
    dict[str, str],

    dict[str, str], str, dict[str, str],

    str, str, str,

    go.Figure, dict[str, str],
]:
    return get_charts_by_region(df=df_all, region=region)
