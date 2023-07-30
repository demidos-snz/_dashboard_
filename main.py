import typing as t

import dash_bootstrap_components as dbc
import geojson
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from clickhouse_driver import Client
from dash import Dash, html, dcc, Output, Input, State

from get_data import df_all_data_from_client, df_with_filter
from secrets_ import CONNECT_PARAMS
from settings import (
    DEFAULT_DROPDOWN_REGIONS_VALUE, REGIONS, DEFAULT_RADIO_ITEM,
    ORG_ICON_PATH, MKD_ICON_PATH, JD_ICON_PATH,
    MONTHS, BUTTON_STYLE, DEFAULT_DROPDOWN_REGIONS_PLACEHOLDER,
    TITLE_APP,
)
from utils import (
    get_geodata, b64_image, get_cpd_total_integer,
    get_current_month_from_db, get_current_year_from_db, get_all_years_from_db,
    convert_month_from_dashboard_to_int, get_current_month_from_db_int, ggg,
    make_human_readable_data,
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

geodata: geojson.FeatureCollection = get_geodata()

app = Dash(
    name=__name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    title=TITLE_APP,
)

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
            style={
                'fontSize': '2.5rem',
                'fontFamily': 'RobotoCondensed-Regular',
            },
        ),

        html.Hr(),

        html.Div(id='back_to_map'),

        html.Div(
            [
                html.Div(
                    [
                        html.H2(
                            children='Всего в системе:',
                            style={
                                'fontSize': '19px',
                                'lineHeight': '1.15em',
                                'fontWeight': 'bold',
                                'color': 'rgba(13, 31, 62, 0.74)',
                                'font-family': 'RobotoCondensed-Light',
                            },
                        ),

                        html.Div(
                            [
                                html.Img(
                                    src=b64_image(ORG_ICON_PATH),
                                    style={
                                        'padding-right': 20,
                                        'margin-bottom': 30,
                                    },
                                ),

                                html.Span(
                                    id='span_charged_sum',
                                    children=get_cpd_total_integer(
                                        df=df_grouped_by_regions_default,
                                        field_name='cpd_charged_sum',
                                    ),
                                    style={
                                        'textAlign': 'left',
                                        'fontSize': '50px',
                                        'lineHeight': '1em',
                                        'fontWeight': 'bold',
                                        'color': '#2aa2cf',
                                        'fontFamily': 'RobotoCondensed-Bold',
                                        'padding-right': 15,
                                    },
                                ),

                                html.Span(
                                    id='span_charged_sum_text',
                                    children=f'начислено за {CURRENT_MONTH_FROM_DB} {CURRENT_YEAR_FROM_DB}',
                                    style={
                                        'fontSize': '19px',
                                        'lineHeight': '1.15em',
                                        'fontWeight': 'bold',
                                        'color': 'rgba(13, 31, 62, 0.74)',
                                        'fontFamily': 'RobotoCondensed-Light',
                                    },
                                ),
                            ],
                            id='div_org_icon',
                            style={
                                'height': '63px',
                            },
                        ),

                        html.Div(
                            [
                                html.Img(
                                    src=b64_image(MKD_ICON_PATH),
                                    style={
                                        'padding-right': 30,
                                        'margin-bottom': 25,
                                    },
                                ),

                                html.Span(
                                    id='span_already_payed_sum',
                                    children=get_cpd_total_integer(
                                        df=df_grouped_by_regions_default,
                                        field_name='cpd_already_payed_sum',
                                    ),
                                    style={
                                        'textAlign': 'left',
                                        'fontSize': '50px',
                                        'lineHeight': '1em',
                                        'fontWeight': 'bold',
                                        'color': '#2aa2cf',
                                        'fontFamily': 'RobotoCondensed-Bold',
                                        'padding-right': 15,
                                    },
                                ),

                                html.Span(
                                    id='span_already_payed_sum_text',
                                    children=f'оплачено за {CURRENT_MONTH_FROM_DB} {CURRENT_YEAR_FROM_DB}',
                                    style={
                                        'fontSize': '19px',
                                        'lineHeight': '1.15em',
                                        'fontWeight': 'bold',
                                        'color': 'rgba(13, 31, 62, 0.74)',
                                        'fontFamily': 'RobotoCondensed-Light',
                                        'padding-right': 15,
                                    },
                                ),
                            ],
                            id='div_mkd_icon',
                            style={
                                'height': '63px',
                            },
                        ),

                        html.Div(
                            [
                                html.Img(
                                    src=b64_image(JD_ICON_PATH),
                                    style={
                                        'padding-right': 25,
                                        'margin-bottom': 25,
                                    },
                                ),

                                html.Span(
                                    id='span_previous_period_debts_sum',
                                    children=get_cpd_total_integer(
                                        df=df_grouped_by_regions_default,
                                        field_name='cpd_previous_period_debts_sum',
                                    ),
                                    style={
                                        'textAlign': 'left',
                                        'fontSize': '50px',
                                        'lineHeight': '1em',
                                        'fontWeight': 'bold',
                                        'color': '#2aa2cf',
                                        'fontFamily': 'RobotoCondensed-Bold',
                                        'padding-right': 15,
                                    },
                                ),

                                html.Span(
                                    id='div_previous_period_debts_sum_text',
                                    children=f'дебиторская задолженность за '
                                             f'{CURRENT_MONTH_FROM_DB} {CURRENT_YEAR_FROM_DB}',
                                    style={
                                        'fontSize': '19px',
                                        'lineHeight': '1.15em',
                                        'fontWeight': 'bold',
                                        'color': 'rgba(13, 31, 62, 0.74)',
                                        'fontFamily': 'RobotoCondensed-Light',
                                        'padding-right': 15,
                                    },
                                ),
                            ],
                            id='div_jd_icon',
                            style={
                                'height': '63px',
                            },
                        ),
                    ],
                    id='div_total_for_russia',
                    style={'display': 'block'}
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
                    style={
                        'width': '300px',
                    },
                ),

                html.Div(
                    dcc.Graph(
                        id='map',
                        config={
                            'scrollZoom': False,
                            'displayModeBar': False,
                        },
                    ),
                    id='div_map',
                    style={
                        'visibility': 'hidden',
                        'display': 'block',
                    },
                ),

                html.Div(
                    [
                        html.Div(
                            [
                                html.Span(
                                    children='Выбрать период:',
                                    style={
                                        'padding-right': 20,
                                        'fontSize': '16px',
                                        'fontFamily': 'RobotoCondensed-Light',
                                        'lineHeight': '1.3em',
                                        'fontWeight': 'bold',
                                        'color': 'black',
                                        'margin-left': '80px',
                                    },
                                ),

                                html.Div(
                                    [
                                        html.Div(
                                            dcc.Dropdown(
                                                id='dropdown_years',
                                                options=[
                                                    {'label': x, 'value': x} for x in ALL_YEARS_FROM_DB
                                                ],
                                                value=CURRENT_YEAR_FROM_DB,
                                                clearable=False,
                                            ),
                                            style={
                                                'width': '250px',
                                                'margin-bottom': 5,
                                            },
                                        ),

                                        html.Div(
                                            dcc.Dropdown(
                                                id='dropdown_months',
                                                options=[
                                                    {'label': x, 'value': x} for x in MONTHS
                                                ],
                                                value=CURRENT_MONTH_FROM_DB,
                                                clearable=False,
                                            ),
                                            style={
                                                'width': '250px',
                                                'margin-bottom': 5,
                                            },
                                        ),
                                    ],
                                    id='div_period_dropdowns',
                                    style={
                                        'display': 'block',
                                    },
                                ),
                            ],
                            style={
                                'display': 'flex',
                                'justify-content': 'left',
                                'alignItems': 'center',
                                'height': 100,
                                'margin-right': 50,
                            },
                        ),

                        html.Div(
                            [
                                html.Span(
                                    children='Отображать статистику:',
                                    style={
                                        'fontSize': '16px',
                                        'margin-right': '20px',
                                        'lineHeight': '1.3em',
                                        'fontWeight': 'bold',
                                        'color': 'black',
                                        'fontFamily': 'RobotoCondensed-Light',
                                        'alignItems': 'center',
                                    },
                                ),

                                dcc.RadioItems(
                                    id='radio_items',
                                    options={
                                        'cpd_charged_sum': '\tпо начислениям',
                                        'cpd_already_payed_sum': '\tпо оплате',
                                        'cpd_previous_period_debts_sum': '\tпо задолженности',
                                    },
                                    value=DEFAULT_RADIO_ITEM,
                                    style={
                                        'width': '200px',
                                        'fontSize': '14px',
                                        'color': 'black',
                                    },
                                ),
                            ],
                            id='div_radio_items',
                            style={
                                'display': 'flex',
                                'justify-content': 'left',
                                'alignItems': 'center',
                                'height': 100,
                            },
                        ),

                        html.Button(
                            children='Обновить данные на карте',
                            id='update_map_data',
                            n_clicks=0,
                            style=BUTTON_STYLE,
                        ),
                    ],
                    id='div_statistic_settings',
                    style={
                        'display': 'flex',
                        'justify-content': 'left',
                        'borderWidth': 2,
                        'borderColor': 'rgb(186, 227, 242)',
                        'borderStyle': 'solid',
                        'alignItems': 'center',
                        'height': 100,
                    },
                ),

                html.H3(
                    id='region_name',
                    style={
                        'display': 'none',
                    }
                ),

                html.Div(
                    [
                        html.Div(
                            dcc.Graph(
                                id='graph_charges_sum',
                                config={
                                    'scrollZoom': False,
                                    'displayModeBar': False,
                                },
                            ),
                            id='div_charges_sum',
                            style={
                                'display': 'none',
                                'textAlign': 'center',
                            },
                        ),

                        html.Div(
                            dcc.Graph(
                                id='graph_already_payed_sum',
                                config={
                                    'scrollZoom': False,
                                    'displayModeBar': False,
                                },
                            ),
                            id='div_already_payed_sum',
                            style={
                                'display': 'none',
                            },
                        ),
                    ],
                    style={
                        'display': 'flex',
                    }
                ),

                html.Div(
                    dcc.Graph(
                        id='graph_debts_sum',
                        config={
                            'scrollZoom': False,
                            'displayModeBar': False,
                        },
                    ),
                    id='div_debts_sum',
                    style={
                        'display': 'none',
                    },
                ),

                # html.Div(
                #     [
                #         html.Div(
                #             dcc.Graph(
                #                 id='graph_cr_charges_sum',
                #                 config={
                #                     'scrollZoom': False,
                #                     'displayModeBar': False,
                #                 },
                #             ),
                #             id='div_cr_charges_sum',
                #             style={
                #                 'display': 'none',
                #                 'textAlign': 'center',
                #             },
                #         ),
                #
                #         html.Div(
                #             dcc.Graph(
                #                 id='graph_cr_payed_sum',
                #                 config={
                #                     'scrollZoom': False,
                #                     'displayModeBar': False,
                #                 },
                #             ),
                #             id='div_cr_payed_sum',
                #             style={
                #                 'display': 'none',
                #             },
                #         ),
                #     ],
                #     style={
                #         'display': 'flex',
                #     }
                # ),

                html.Div(
                    [
                        html.H2(
                            children='Собираемость взносов на счете регионального оператора за 2023 год:',
                            style={
                                'fontSize': '19px',
                                'lineHeight': '1.15em',
                                'fontWeight': 'bold',
                                'color': 'rgba(13, 31, 62, 0.74)',
                                'font-family': 'RobotoCondensed-Light',
                            },
                        ),

                        html.Div(
                            [
                                html.Span(
                                    id='span_cr_charged_sum',
                                    style={
                                        'textAlign': 'left',
                                        'fontSize': '50px',
                                        'lineHeight': '1em',
                                        'fontWeight': 'bold',
                                        'color': '#2aa2cf',
                                        'fontFamily': 'RobotoCondensed-Bold',
                                        'padding-right': 15,
                                    },
                                ),

                                html.Span(
                                    id='span_cr_charged_sum_text',
                                    children=f'начислено взносов с начала {CURRENT_YEAR_FROM_DB} года',
                                    style={
                                        'fontSize': '19px',
                                        'lineHeight': '1.15em',
                                        'fontWeight': 'bold',
                                        'color': 'rgba(13, 31, 62, 0.74)',
                                        'fontFamily': 'RobotoCondensed-Light',
                                    },
                                ),
                            ],
                            id='div_cr_charges_total',
                            style={
                                'height': '63px',
                            },
                        ),

                        html.Div(
                            [
                                html.Span(
                                    id='span_cr_payed_sum',
                                    style={
                                        'textAlign': 'left',
                                        'fontSize': '50px',
                                        'lineHeight': '1em',
                                        'fontWeight': 'bold',
                                        'color': '#2aa2cf',
                                        'fontFamily': 'RobotoCondensed-Bold',
                                        'padding-right': 15,
                                    },
                                ),

                                html.Span(
                                    id='span_cr_payed_sum_text',
                                    children=f'оплачено взносов с начала {CURRENT_YEAR_FROM_DB} года',
                                    style={
                                        'fontSize': '19px',
                                        'lineHeight': '1.15em',
                                        'fontWeight': 'bold',
                                        'color': 'rgba(13, 31, 62, 0.74)',
                                        'fontFamily': 'RobotoCondensed-Light',
                                        'padding-right': 15,
                                    },
                                ),
                            ],
                            id='div_cr_payed_total',
                            style={
                                'height': '63px',
                            },
                        ),

                        html.Div(
                            [
                                html.Span(
                                    id='span_cr_debts_sum',
                                    style={
                                        'textAlign': 'left',
                                        'fontSize': '50px',
                                        'lineHeight': '1em',
                                        'fontWeight': 'bold',
                                        'color': '#2aa2cf',
                                        'fontFamily': 'RobotoCondensed-Bold',
                                        'padding-right': 15,
                                    },
                                ),

                                html.Span(
                                    id='div_cr_debts_sum_text',
                                    children=f'задолженность по уплате взносов за {CURRENT_YEAR_FROM_DB} год',
                                    style={
                                        'fontSize': '19px',
                                        'lineHeight': '1.15em',
                                        'fontWeight': 'bold',
                                        'color': 'rgba(13, 31, 62, 0.74)',
                                        'fontFamily': 'RobotoCondensed-Light',
                                        'padding-right': 15,
                                    },
                                ),
                            ],
                            id='div_cr_debt_total',
                            style={
                                'height': '63px',
                            },
                        ),
                    ],
                    id='div_cr_total_for_russia',
                    style={
                        'display': 'none',
                        'position': 'relative',
                        'padding-left': 200,
                    },
                ),
                html.Div(
                    dcc.Graph(
                        id='graph_sunburst',
                        config={
                            'scrollZoom': False,
                            'displayModeBar': False,
                        },
                    ),
                    id='div_sunburst',
                    style={
                        'display': 'none',
                    },
                ),
            ],
        ),
    ],
    style={
        'position': 'relative',
        'maxWidth': '1200px',
        'margin-bottom': 30,
        'margin-right': 'auto',
        'margin-left': 'auto',
    },
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
def display_map(click: int, value: str, year: int, month: str, ip_open: bool) -> tuple[
    bool, go.Figure, dict[str, str],
    str, str, str,
    str, str, str,
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
        fig,
        {'visibility': 'visible'},
        get_cpd_total_integer(df=df_grouped_by_regions, field_name='cpd_charged_sum'),
        get_cpd_total_integer(df=df_grouped_by_regions, field_name='cpd_already_payed_sum'),
        get_cpd_total_integer(df=df_grouped_by_regions, field_name='cpd_previous_period_debts_sum'),
        f'начислено за {month} {year}',
        f'оплачено за {month} {year}',
        f'дебиторская задолженность за {month} {year}',
        year,
        month,
    )


def get_map(df: pd.DataFrame, value: str) -> go.Figure:
    fig = px.choropleth_mapbox(
        data_frame=df,
        geojson=geodata,
        locations=df.region_code,
        color=value,
        hover_name=df.region_name,
        hover_data={
            'region_code': False,
            'cpd_charged_sum': True,
            'cpd_already_payed_sum': True,
            'cpd_previous_period_debts_sum': True,
        },
        color_continuous_scale=[
            (0, 'rgb(186, 227, 242)'), (0.00001, 'rgb(186, 227, 242)'),
            (0.00001, 'rgb(239, 75, 46)'), (0.0001, 'rgb(239, 75, 46)'),
            (0.0001, 'rgb(245, 153, 46)'), (0.1, 'rgb(245, 153, 46)'),
            (0.1, 'rgb(253, 211, 17)'), (0.2, 'rgb(253, 211, 17)'),
            (0.2, 'rgb(173, 211, 100)'), (1, 'rgb(173, 211, 100)'),
        ],
        featureidkey='properties.cartodb_id',
        mapbox_style='white-bg',
        zoom=1.9,
        center={'lat': 69, 'lon': 105},
        labels={
            'cpd_charged_sum': '',
            'cpd_already_payed_sum': '',
            'cpd_previous_period_debts_sum': '',
        },
        custom_data=[
            df['region_code'],
            df['region_name'],
            make_human_readable_data(column=df['cpd_charged_sum']),
            make_human_readable_data(column=df['cpd_already_payed_sum']),
            make_human_readable_data(column=df['cpd_previous_period_debts_sum']),
        ],
    )
    hovertemp: str = '<b>%{customdata[1]}</b><br>'
    hovertemp += '<br><b>%{customdata[2]}</b> - Начислено<br>'
    hovertemp += '<br><b>%{customdata[3]}</b> - Оплачено<br>'
    hovertemp += '<br><b>%{customdata[4]}</b> - Задолженность<br>'

    fig.update_traces(
        hovertemplate=hovertemp,
        marker_line_width=1,
        marker_line_color='white',
    )
    fig.update_layout(
        height=730,
        hoverlabel={
            'bgcolor': 'white',
            'bordercolor': '#dee2e6',
            'font_size': 16,
            'font_family': 'Helvetica',
            'align': 'left',
        },
        hoverlabel_font_color='black',
    )
    return fig


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
        # Output(component_id='graph_cr_charges_sum', component_property='figure', allow_duplicate=True),
        # Output(component_id='div_cr_charges_sum', component_property='style', allow_duplicate=True),
        # Output(component_id='graph_cr_payed_sum', component_property='figure', allow_duplicate=True),
        # Output(component_id='div_cr_payed_sum', component_property='style', allow_duplicate=True),
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
    Input(component_id='map', component_property='clickData'),
    prevent_initial_call=True,
)
def hide_map_by_click_map(clickData: dict[str, list[dict[str, t.Any]]]) -> tuple[
    html.Button, dict[str, str],
    dict[str, str], dict[str, str], dict[str, str],
    go.Figure, dict[str, str],
    go.Figure, dict[str, str],
    go.Figure, dict[str, str],
    # go.Figure, dict[str, str],
    # go.Figure, dict[str, str],
    dict[str, str],
    dict[str, str], str, dict[str, str],
    str, str, str,
    go.Figure, dict[str, str],
]:
    if clickData is not None:
        region: str = clickData['points'][0]['hovertext']

        return ggg(df=df_all, region=region, x_axis=X_AXIS)


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
        # Output(component_id='graph_cr_charges_sum', component_property='figure', allow_duplicate=True),
        # Output(component_id='div_cr_charges_sum', component_property='style', allow_duplicate=True),
        # Output(component_id='graph_cr_payed_sum', component_property='figure', allow_duplicate=True),
        # Output(component_id='div_cr_payed_sum', component_property='style', allow_duplicate=True),
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
    # go.Figure, dict[str, str],
    # go.Figure, dict[str, str],
    dict[str, str],
    dict[str, str], str, dict[str, str],
    str, str, str,
    go.Figure, dict[str, str],
]:
    return ggg(df=df_all, region=region, x_axis=X_AXIS)


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
def back_to_map(n_clicks: int) -> tuple[
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


if __name__ == '__main__':
    app.run(debug=True)
