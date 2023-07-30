import typing as t

from dash import Output, Input, html

from app import app
from layouts.back_to_map import back_to_map_layout


def hide_charts_by_click_return_button():
    return html.Div(
        # fixme id
        id='',
        children=[
            back_to_map_layout(),
        ],
    )


@app.callback(
    [
        Output(component_id='back_to_map', component_property='style', allow_duplicate=True),

        Output(component_id='div_total_for_russia', component_property='style', allow_duplicate=True),
        Output(component_id='div_map', component_property='style', allow_duplicate=True),
        Output(component_id='div_statistic_settings', component_property='style', allow_duplicate=True),

        Output(component_id='div_charges_sum', component_property='style', allow_duplicate=True),
        Output(component_id='div_already_payed_sum', component_property='style', allow_duplicate=True),
        Output(component_id='div_debts_sum', component_property='style', allow_duplicate=True),
        Output(component_id='div_cr_total_for_russia', component_property='style', allow_duplicate=True),
        # Output(component_id='div_cr_charges_sum', component_property='style', allow_duplicate=True),
        # Output(component_id='div_cr_payed_sum', component_property='style', allow_duplicate=True),
        Output(component_id='div_regions_list', component_property='style', allow_duplicate=True),

        Output(component_id='region_name', component_property='style', allow_duplicate=True),

        Output(component_id='div_sunburst', component_property='style', allow_duplicate=True),
    ],
    Input(component_id='back_to_map', component_property='n_clicks'),
    prevent_initial_call=True,
)
def back_to_map(_: int) -> tuple[
    dict[str, str],
    dict[str, str], dict[str, t.Any], dict[str, str],
    dict[str, str], dict[str, str], dict[str, str],
    dict[str, str], dict[str, str],
    # dict[str, str], dict[str, str],
    dict[str, str],
    dict[str, str],
]:
    return (
        {'display': 'none'},

        {'display': 'block'},
        {'display': 'block'},
        {
            'display': 'flex',
            'justify-content': 'left',
            'borderWidth': 2,
            'borderColor': 'rgb(186, 227, 242)',
            'borderStyle': 'solid',
            'alignItems': 'center',
            'padding': 10,
            'height': 100,
        },

        {'display': 'none'},
        {'display': 'none'},
        {'display': 'none'},
        {'display': 'none'},
        # {'display': 'none'},
        # {'display': 'none'},
        {
            'display': 'block',
            'width': '300px',
        },

        {
            'display': 'none',
            'width': '300px',
        },

        {'display': 'none'},
    )
