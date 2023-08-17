import typing as t

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go
from clickhouse_driver import Client
from dash import Dash, html, dcc, Output, Input, State

from get_data import df_all_data_from_client, df_with_filter
from secrets_ import CONNECT_PARAMS
from settings import (
    DEFAULT_DROPDOWN_REGIONS_VALUE, REGIONS, ORG_ICON_PATH, MKD_ICON_PATH, JD_ICON_PATH,
    MONTHS, DEFAULT_DROPDOWN_REGIONS_PLACEHOLDER,
    TITLE_APP, FIELDS_NAMES_CR, FIELDS_NAMES_CPD, RADIO_ITEM_STATS_CATEGORY, CONFIGS_FOR_GRAPHS,
)
from utils import (
    b64_image, get_cpd_total_integer,
    get_current_month_from_db, get_current_year_from_db, get_all_years_from_db,
    convert_month_from_dashboard_to_int, get_current_month_from_db_int, get_map, show_charts_with_region_selection,
)

# fixme move later
client: Client = Client(**CONNECT_PARAMS)

CURRENT_MONTH_FROM_DB: str = get_current_month_from_db(client=client)
CURRENT_MONTH_FROM_DB_INT: int = get_current_month_from_db_int(client=client)
ALL_YEARS_FROM_DB: list[int] = get_all_years_from_db(client=client)
CURRENT_YEAR_FROM_DB: int = get_current_year_from_db(years=ALL_YEARS_FROM_DB)

X_AXIS: tuple[str] = MONTHS[:CURRENT_MONTH_FROM_DB_INT]

df_all: pd.DataFrame = df_all_data_from_client(client=client)
df_grouped_by_regions_default: pd.DataFrame = df_with_filter(
    df=df_all,
    year=CURRENT_YEAR_FROM_DB,
    month=convert_month_from_dashboard_to_int(CURRENT_MONTH_FROM_DB),
)

client.disconnect()

# server = flask.Flask(__name__)

app = Dash(
    name=__name__,
    # server=server,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title=TITLE_APP,
)

# app.config.suppress_callback_exceptions = True

app.layout = html.Div(
    children=[
        dbc.Modal(
            [
                dbc.ModalHeader(dbc.ModalTitle('Предупреждение!'), close_button=True),
                dbc.ModalBody(children='Данные за выбранный период отсутствуют!'),
            ],
            id='modal_backdrop',
            is_open=False,
        ),

        html.H1(
            id='label_dashboard',
            children='Мониторинг отрасли ЖКХ',
        ),

        html.Hr(),

        html.Div(id='back_to_map'),

        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            id='header_for_russian_stats',
                            children=f'Всего в системе ({RADIO_ITEM_STATS_CATEGORY[0]}):',
                        ),

                        html.Div(
                            [
                                html.Img(
                                    id='org_icon',
                                    src=b64_image(ORG_ICON_PATH),
                                ),

                                html.Span(
                                    id='span_charged_sum',
                                    className='all_russia_stats',
                                    children=get_cpd_total_integer(
                                        df=df_grouped_by_regions_default,
                                        field_name='cpd_charged_sum',
                                    ),
                                ),

                                html.Span(
                                    id='span_charged_sum_text',
                                    className='all_russia_stats_text',
                                    children=f'начислено за {CURRENT_MONTH_FROM_DB} {CURRENT_YEAR_FROM_DB}',
                                ),
                            ],
                            id='div_org_icon',
                        ),

                        html.Div(
                            [
                                html.Img(
                                    id='mkd_icon',
                                    src=b64_image(MKD_ICON_PATH),
                                ),

                                html.Span(
                                    id='span_already_payed_sum',
                                    className='all_russia_stats',
                                    children=get_cpd_total_integer(
                                        df=df_grouped_by_regions_default,
                                        field_name='cpd_already_payed_sum',
                                    ),
                                ),

                                html.Span(
                                    id='span_already_payed_sum_text',
                                    className='all_russia_stats_text',
                                    children=f'оплачено за {CURRENT_MONTH_FROM_DB} {CURRENT_YEAR_FROM_DB}',

                                ),
                            ],
                            id='div_mkd_icon',
                        ),

                        html.Div(
                            [
                                html.Img(
                                    id='jd_icon',
                                    src=b64_image(JD_ICON_PATH),
                                ),

                                html.Span(
                                    id='span_previous_period_debts_sum',
                                    className='all_russia_stats',
                                    children=get_cpd_total_integer(
                                        df=df_grouped_by_regions_default,
                                        field_name='cpd_previous_period_debts_sum',
                                    ),
                                ),

                                html.Span(
                                    id='div_previous_period_debts_sum_text',
                                    className='all_russia_stats_text',
                                    children=f'задолженность за {CURRENT_MONTH_FROM_DB} {CURRENT_YEAR_FROM_DB}',
                                ),
                            ],
                            id='div_jd_icon',
                        ),
                    ],
                    id='div_total_for_russia',
                ),

                html.Div(
                    dcc.Dropdown(
                        id='dropdown_regions',
                        options=REGIONS,
                        value=DEFAULT_DROPDOWN_REGIONS_VALUE,
                        clearable=False,
                        placeholder=DEFAULT_DROPDOWN_REGIONS_PLACEHOLDER,
                    ),
                    id='div_regions_list',
                ),

                html.Div(
                    dcc.Graph(
                        id='map',
                        config={
                            'scrollZoom': False,
                            'displayModeBar': False,
                            'doubleClick': 'reset'
                        },
                    ),
                    id='div_map',
                    style={
                        'visibility': 'hidden',
                    },
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.Span(
                                    children='Выбрать период:',
                                    className='panel_text',
                                ),

                                html.Div(
                                    [
                                        html.Div(
                                            dcc.Dropdown(
                                                id='dropdown_years',
                                                options=ALL_YEARS_FROM_DB,
                                                value=CURRENT_YEAR_FROM_DB,
                                                clearable=False,
                                            ),
                                        ),

                                        html.Div(
                                            dcc.Dropdown(
                                                id='dropdown_months',
                                                options=MONTHS,
                                                value=CURRENT_MONTH_FROM_DB,
                                                clearable=False,
                                            ),
                                        ),
                                    ],
                                ),
                            ],
                            id='div_period_dropdowns',
                        ),

                        html.Div(
                            [
                                html.Span(
                                    children='Отображать на карте статистику:',
                                    className='panel_text',
                                ),

                                dcc.RadioItems(
                                    id='radio_items_stats_category',
                                    options=RADIO_ITEM_STATS_CATEGORY,
                                    value=RADIO_ITEM_STATS_CATEGORY[0],
                                ),

                                dcc.RadioItems(
                                    id='radio_items',
                                    options={
                                        FIELDS_NAMES_CPD[0]: '\tначисления',
                                        FIELDS_NAMES_CPD[1]: '\tоплата',
                                        FIELDS_NAMES_CPD[2]: '\tзадолженность',
                                    },
                                    value=FIELDS_NAMES_CPD[0],
                                ),
                            ],
                            id='div_radio_items',
                        ),

                        html.Button(
                            children='Обновить данные на карте',
                            id='update_map_data',
                            className='button',
                            n_clicks=0,
                        ),
                    ],
                    id='div_statistic_settings',
                ),

                html.H3(
                    id='region_name',
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id='graph_charges_sum',
                                    config=CONFIGS_FOR_GRAPHS,
                                ),

                                dcc.Graph(
                                    id='graph_already_payed_sum',
                                    config=CONFIGS_FOR_GRAPHS,
                                ),
                            ],
                            className='two_graphs_in_row',
                        ),

                        dcc.Graph(
                            id='graph_debts_sum',
                            config=CONFIGS_FOR_GRAPHS,
                        ),
                    ],
                    id='div_payment_service',
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(
                                    id='graph_cr_charges_sum',
                                    config=CONFIGS_FOR_GRAPHS,
                                ),

                                dcc.Graph(
                                    id='graph_cr_payed_sum',
                                    config=CONFIGS_FOR_GRAPHS,
                                ),
                            ],
                            className='two_graphs_in_row',
                        ),

                        dcc.Graph(
                            id='graph_sunburst',
                            config=CONFIGS_FOR_GRAPHS,
                        ),
                    ],
                    id='div_capital_repair',
                )
            ],
        ),
    ],
    id='big_div'
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
        Output(component_id='radio_items', component_property='options'),
        Output(component_id='radio_items', component_property='value'),
        Output(component_id='header_for_russian_stats', component_property='children'),
    ],
    Input(component_id='update_map_data', component_property='n_clicks'),
    [
        State(component_id='radio_items', component_property='value'),
        State(component_id='radio_items_stats_category', component_property='value'),
        State(component_id='dropdown_years', component_property='value'),
        State(component_id='dropdown_months', component_property='value'),
        State(component_id='modal_backdrop', component_property='is_open'),
    ],
)
def display_map(click: int, value: str, stats_category_value: str, year: int, month: str, ip_open: bool) -> tuple[
    bool, go.Figure, dict[str, str],
    str, str, str,
    str, str, str,
    int, str, dict,
    str, str
]:
    month_int: int = convert_month_from_dashboard_to_int(month=month)

    if month_int > CURRENT_MONTH_FROM_DB_INT and year == CURRENT_YEAR_FROM_DB:
        month: str = CURRENT_MONTH_FROM_DB
        df_grouped_by_regions: pd.DataFrame = df_with_filter(df=df_all, year=year, month=CURRENT_MONTH_FROM_DB_INT)
        ip_open: bool = True
    else:
        month: str = month
        df_grouped_by_regions: pd.DataFrame = df_with_filter(df=df_all, year=year, month=month_int)

    if stats_category_value == RADIO_ITEM_STATS_CATEGORY[0]:
        field_names = FIELDS_NAMES_CPD
        if not value.startswith('cpd'):
            value = FIELDS_NAMES_CPD[FIELDS_NAMES_CR.index(value)]
    else:
        field_names = FIELDS_NAMES_CR
        if not value.startswith('cr'):
            value = FIELDS_NAMES_CR[FIELDS_NAMES_CPD.index(value)]

    fig: go.Figure = get_map(df=df_grouped_by_regions, value=value)

    return (
        ip_open,
        fig,
        {'visibility': 'visible'},
        get_cpd_total_integer(df=df_grouped_by_regions, field_name=field_names[0]),
        get_cpd_total_integer(df=df_grouped_by_regions, field_name=field_names[1]),
        get_cpd_total_integer(df=df_grouped_by_regions, field_name=field_names[2]),
        f'начислено за {month} {year}',
        f'оплачено за {month} {year}',
        f'задолженность за {month} {year}',
        year,
        month,
        {field_names[0]: '\tначисления',
         field_names[1]: '\tоплата',
         field_names[2]: '\tзадолженность'},
        value,
        f'Всего в системе ({stats_category_value}):'
    )


@app.callback(
    [
        Output(component_id='back_to_map', component_property='children', allow_duplicate=True),
        Output(component_id='back_to_map', component_property='style', allow_duplicate=True),

        Output(component_id='div_total_for_russia', component_property='style', allow_duplicate=True),
        Output(component_id='div_map', component_property='style', allow_duplicate=True),
        Output(component_id='div_statistic_settings', component_property='style', allow_duplicate=True),

        Output(component_id='graph_charges_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='graph_already_payed_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='graph_debts_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='graph_cr_charges_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='graph_cr_payed_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='graph_sunburst', component_property='figure', allow_duplicate=True),

        Output(component_id='div_payment_service', component_property='style', allow_duplicate=True),
        Output(component_id='div_capital_repair', component_property='style', allow_duplicate=True),

        Output(component_id='div_regions_list', component_property='style', allow_duplicate=True),
        Output(component_id='region_name', component_property='children', allow_duplicate=True),
        Output(component_id='region_name', component_property='style', allow_duplicate=True),
        Output(component_id='dropdown_regions', component_property='value', allow_duplicate=True),
    ],
    Input(component_id='map', component_property='clickData'),
    State(component_id='radio_items_stats_category', component_property='value'),
    prevent_initial_call=True,
)
def hide_map_by_click_map(clickData: dict[str, list[dict[str, t.Any]]], state_category_value: str) -> tuple[
    html.Button, dict[str, str],
    dict[str, str], dict[str, str], dict[str, str],
    go.Figure,
    go.Figure,
    go.Figure,
    go.Figure,
    go.Figure,
    go.Figure,
    dict[str, str], dict[str, str],
    dict[str, str], str, dict[str, str],
    str
]:
    if clickData is not None:
        region: str = clickData['points'][0]['hovertext']
        return show_charts_with_region_selection(df=df_all,
                                                 region=region,
                                                 x_axis=X_AXIS,
                                                 value=state_category_value,
                                                 new_region_value=region)


@app.callback(
    [
        Output(component_id='back_to_map', component_property='children', allow_duplicate=True),
        Output(component_id='back_to_map', component_property='style', allow_duplicate=True),

        Output(component_id='div_total_for_russia', component_property='style', allow_duplicate=True),
        Output(component_id='div_map', component_property='style', allow_duplicate=True),
        Output(component_id='div_statistic_settings', component_property='style', allow_duplicate=True),

        Output(component_id='graph_charges_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='graph_already_payed_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='graph_debts_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='graph_cr_charges_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='graph_cr_payed_sum', component_property='figure', allow_duplicate=True),
        Output(component_id='graph_sunburst', component_property='figure', allow_duplicate=True),

        Output(component_id='div_payment_service', component_property='style', allow_duplicate=True),
        Output(component_id='div_capital_repair', component_property='style', allow_duplicate=True),

        Output(component_id='div_regions_list', component_property='style', allow_duplicate=True),
        Output(component_id='region_name', component_property='children', allow_duplicate=True),
        Output(component_id='region_name', component_property='style', allow_duplicate=True),
        Output(component_id='dropdown_regions', component_property='value', allow_duplicate=True),
    ],
    Input(component_id='dropdown_regions', component_property='value'),
    State(component_id='radio_items_stats_category', component_property='value'),
    prevent_initial_call=True,
)
def hide_map_by_dropdown_region(region: str, state_category_value: str) -> tuple[
    html.Button, dict[str, str],
    dict[str, str], dict[str, str], dict[str, str],
    go.Figure,
    go.Figure,
    go.Figure,
    go.Figure,
    go.Figure,
    go.Figure,
    dict[str, str], dict[str, str],
    dict[str, str], str, dict[str, str],
    str
]:
    return show_charts_with_region_selection(df=df_all,
                                             region=region,
                                             x_axis=X_AXIS,
                                             value=state_category_value,
                                             new_region_value='')


@app.callback(
    [
        Output(component_id='back_to_map', component_property='style', allow_duplicate=True),

        Output(component_id='div_total_for_russia', component_property='style', allow_duplicate=True),
        Output(component_id='div_map', component_property='style', allow_duplicate=True),
        Output(component_id='div_statistic_settings', component_property='style', allow_duplicate=True),

        Output(component_id='div_payment_service', component_property='style', allow_duplicate=True),
        Output(component_id='div_capital_repair', component_property='style', allow_duplicate=True),

        Output(component_id='div_regions_list', component_property='style', allow_duplicate=True),
        Output(component_id='region_name', component_property='style', allow_duplicate=True),
    ],
    Input(component_id='back_to_map', component_property='n_clicks'),
    prevent_initial_call=True,
)
def back_to_map(n_clicks: int) -> tuple[
    dict[str, str],
    dict[str, str], dict[str, t.Any], dict[str, str],
    dict[str, str], dict[str, str],
    dict[str, str], dict[str, str],
]:
    return (
        {'display': 'none'},

        {'display': 'block'},
        {'display': 'block'},
        {'display': 'flex'},

        {'display': 'none'},
        {'display': 'none'},

        {'display': 'block'},
        {'display': 'none'},
    )


if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='0.0.0.0', debug=True)
