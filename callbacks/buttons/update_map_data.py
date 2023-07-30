import pandas as pd
import plotly.graph_objects as go
from dash import Output, Input, State, html

from app import app
from callbacks.map.utils import get_map
from get_data import df_with_filter
from init_data import CURRENT_MONTH_FROM_DB, CURRENT_YEAR_FROM_DB, CURRENT_MONTH_FROM_DB_INT, df_all
from layouts.map import map_layout
from utils import convert_month_from_dashboard_to_int, get_cpd_total_integer


def update_map_by_button() -> html.Div:
    return html.Div(
        # fixme id
        id='',
        children=[
            map_layout(),
        ],
    )


@app.callback(
    [
        Output(component_id='modal_backdrop', component_property='is_open'),

        Output(component_id='map', component_property='figure'),
        Output(component_id='div_map', component_property='style'),

        Output(component_id='span_charged_sum', component_property='children'),
        Output(component_id='span_already_payed_sum', component_property='children'),
        Output(component_id='span_previous_period_debts_sum', component_property='children'),
        Output(component_id='span_charged_sum_text', component_property='children'),
        Output(component_id='span_already_payed_sum_text', component_property='children'),
        Output(component_id='div_previous_period_debts_sum_text', component_property='children'),

        Output(component_id='dropdown_years', component_property='value'),
        Output(component_id='dropdown_months', component_property='value'),
    ],
    Input(component_id='update_map_data', component_property='n_clicks'),
    [
        State(component_id='radio_items', component_property='value'),
        State(component_id='dropdown_years', component_property='value'),
        State(component_id='dropdown_months', component_property='value'),
        State(component_id='modal_backdrop', component_property='is_open'),
    ],
)
def display_map(_: int, value: str, year: int, month: str, ip_open: bool) -> tuple[
    bool,
    go.Figure, dict[str, str],
    str, str, str, str, str, str,
    int, str,
]:
    month_int: int = convert_month_from_dashboard_to_int(month=month)

    if month_int > CURRENT_MONTH_FROM_DB_INT and year == CURRENT_YEAR_FROM_DB:
        month: str = CURRENT_MONTH_FROM_DB
        df_grouped_by_regions: pd.DataFrame = df_with_filter(df=df_all, year=year, month=CURRENT_MONTH_FROM_DB_INT)
        ip_open: bool = True
    else:
        month: str = month.lower()
        df_grouped_by_regions: pd.DataFrame = df_with_filter(df=df_all, year=year, month=month_int)

    fig: go.Figure = get_map(df=df_grouped_by_regions, value=value)

    return (
        ip_open,

        fig, {'visibility': 'visible'},

        get_cpd_total_integer(df=df_grouped_by_regions, field_name='cpd_charged_sum'),
        get_cpd_total_integer(df=df_grouped_by_regions, field_name='cpd_already_payed_sum'),
        get_cpd_total_integer(df=df_grouped_by_regions, field_name='cpd_previous_period_debts_sum'),
        f'начислено за {month} {year}',
        f'оплачено за {month} {year}',
        f'дебиторская задолженность за {month} {year}',

        year, month,
    )
