import calendar
import locale

import geojson
import pandas as pd
import plotly.express as px
from clickhouse_driver import Client
from dash import Dash, html, dcc, Output, Input, State
from dash_bootstrap_components import Alert

from get_data import get_data_from_client, get_df_with_filter
from secrets_ import CONNECT_PARAMS
from settings import (
    DEFAULT_REGION, REGIONS, DEFAULT_RADIO_ITEM,
    ORG_ICON_PATH, MKD_ICON_PATH, JD_ICON_PATH,
)
from utils import (
    get_geodata, b64_image, get_total_integer,
    get_current_month_from_db, get_current_year_from_db, get_all_years_from_db,
    convert_month_from_dashboard_to_int, get_current_month_from_db_int,
)

locale.setlocale(locale.LC_TIME, 'ru_RU')

# fixme
client: Client = Client(**CONNECT_PARAMS)

CURRENT_MONTH_FROM_DB: str = get_current_month_from_db(client=client)
CURRENT_MONTH_FROM_DB_INT: int = get_current_month_from_db_int(client=client)
ALL_YEARS_FROM_DB: list[int] = get_all_years_from_db(client=client)
CURRENT_YEAR_FROM_DB: int = get_current_year_from_db(years=ALL_YEARS_FROM_DB)

lsql = """
select report_month,
    extract(year from report_month) as "year",
    extract(month from report_month) as "month",
    toInt32(region_code) as region_code,
    region_name,
    round(charged_sum) as charged_sum,
    --round(ch_total_sum) as ch_total_sum,
    --payment_document_count,
    --toInt64(objects_count) as objects_count,
    round(already_payed_sum) as already_payed_sum,
    round(previous_period_debts_sum) as previous_period_debts_sum
    --round(beginning_period_advance_sum) as beginning_period_advance_sum,
    --toInt64(objects_with_debts_count) as objects_with_debts_count
from ois_visual.charges_payed_debts_by_regions t1
SETTINGS
     max_bytes_before_external_group_by=20000000000, 
     max_memory_usage=40000000000;
"""
df_all: pd.DataFrame = get_data_from_client(query=lsql)
# df_all.to_csv('df_all.csv', index=False, encoding='cp1251', sep=';')
df_grouped_by_regions_default: pd.DataFrame = get_df_with_filter(
    df=df_all,
    year=CURRENT_YEAR_FROM_DB,
    month=convert_month_from_dashboard_to_int(CURRENT_MONTH_FROM_DB),
)

client.disconnect()

app = Dash(
    name=__name__,
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
)

app.layout = html.Div(
    children=[
        html.Div(id='map_alert'),

        html.H1(
            id='label_dashboard',
            children='Мониторинг отрасли ЖКХ',
            style={
                'fontSize': '2.5rem',
                'fontFamily': 'RobotoCondensed-Regular',
            },
        ),

        html.Hr(
            style={
                'margin-top': 5,
                'margin-bottom': 5,
            },
        ),

        html.Div(
            id='back_to_map',
        ),

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
                                        'padding-right': 10,
                                    },
                                ),

                                html.Span(
                                    id='span_charged_sum',
                                    children=get_total_integer(
                                        df=df_grouped_by_regions_default,
                                        field_name='charged_sum',
                                    ),
                                    style={
                                        'textAlign': 'left',
                                        'fontSize': '50px',
                                        'lineHeight': '1em',
                                        'fontWeight': 'bold',
                                        'color': '#2aa2cf',
                                        'fontFamily': 'RobotoCondensed-Bold',
                                        'padding-right': 10,
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
                                        'padding-right': 15,
                                    },
                                ),

                                html.Span(
                                    id='span_already_payed_sum',
                                    children=get_total_integer(
                                        df=df_grouped_by_regions_default,
                                        field_name='already_payed_sum',
                                    ),
                                    style={
                                        'textAlign': 'left',
                                        'fontSize': '50px',
                                        'lineHeight': '1em',
                                        'fontWeight': 'bold',
                                        'color': '#2aa2cf',
                                        'fontFamily': 'RobotoCondensed-Bold',
                                        'padding-right': 10,
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
                                html.Div(
                                    html.Img(
                                        src=b64_image(JD_ICON_PATH),
                                        style={
                                            'padding-top': 10,
                                            'padding-right': 10,
                                        },
                                    ),
                                ),

                                html.Span(
                                    id='span_previous_period_debts_sum',
                                    children=get_total_integer(
                                        df=df_grouped_by_regions_default,
                                        field_name='previous_period_debts_sum',
                                    ),
                                    style={
                                        'textAlign': 'left',
                                        'fontSize': '50px',
                                        'lineHeight': '1em',
                                        'fontWeight': 'bold',
                                        'color': '#2aa2cf',
                                        'fontFamily': 'RobotoCondensed-Bold',
                                        'padding-right': 10,
                                    },
                                ),

                                html.Div(
                                    id='div_previous_period_debts_sum_text',
                                    children=f'задолженность за коммунальные услуги за {CURRENT_MONTH_FROM_DB} '
                                             f'{CURRENT_YEAR_FROM_DB}',
                                    style={
                                        'fontSize': '19px',
                                        'lineHeight': '1.15em',
                                        'fontWeight': 'bold',
                                        'color': 'rgba(13, 31, 62, 0.74)',
                                        'fontFamily': 'RobotoCondensed-Light',
                                        'margin': 5,
                                        'width': '300px',
                                    },
                                ),
                            ],
                            id='div_jd_icon',
                            style={
                                'height': '63px',
                                'display': 'flex',
                                'justify-content': 'left',
                            },
                        ),
                    ],
                    id='div_total_for_russia',
                    style={'display': 'block'}
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
                        # 'height': '1000px',
                        # 'width': '1000px',
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
                                                'width': '200px',
                                                'margin-bottom': 5,
                                            },
                                        ),

                                        html.Div(
                                            dcc.Dropdown(
                                                id='dropdown_months',
                                                options=[
                                                    {'label': x, 'value': x} for x in list(calendar.month_name) if x
                                                ],
                                                value=CURRENT_MONTH_FROM_DB.title(),
                                                clearable=False,
                                            ),
                                            style={
                                                'width': '200px',
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
                                'width': 400,
                                'height': 100,
                                'padding-right': 20,
                            },
                        ),

                        html.Div(
                            [
                                html.Span(
                                    children='Отображать статистику:',
                                    style={
                                        'fontSize': '16px',
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
                                        'charged_sum': 'по начислениям',
                                        'already_payed_sum': 'по оплате',
                                        'previous_period_debts_sum': 'по задолженности',
                                    },
                                    value=DEFAULT_RADIO_ITEM,
                                    style={
                                        'width': '250px',
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
                            style={
                                'fontFamily': 'RobotoCondensed-Light',
                                'margin-right': 20,
                            },
                        ),

                        html.Div(
                            dcc.Dropdown(
                                id='dropdown_regions',
                                options=REGIONS,
                                value=DEFAULT_REGION,
                                clearable=False,
                            ),
                            id='div_regions_list',
                            style={
                                'width': '300px',
                                'margin-bottom': 5,
                            },
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
                        'padding': 10,
                        'height': 100,
                    },
                ),

                html.Div(
                    [
                        html.H3(
                            id='label_statistic_for_region',
                            children='Статистика по региону:',
                        ),

                        html.Div(
                            id='div_table_statistic_for_region',
                        ),
                    ],
                    id='div_statistic_for_region',
                    style={
                        'display': 'none',
                    },
                ),

                # html.Div(
                #     [
                #         html.H3(
                #             id='label_statistics_on_provider_of_region',
                #             children='Статистика по региону:',
                #         ),
                #
                #         html.Div(
                #             id='div_table_statistics_on_provider_of_region',
                #         ),
                #     ],
                #     id='div_statistics_on_provider_of_region',
                #     style={
                #         'display': 'none',
                #     },
                # ),
            ],
        ),
    ],
    style={
        'position': 'relative',
        'maxWidth': '1200px',
        'margin-right': 'auto',
        'margin-left': 'auto',
    },
)


@app.callback(
    [
        Output(component_id='map_alert', component_property='children'),
        Output(component_id='map', component_property='figure'),
        Output(component_id='div_map', component_property='style'),
        Output(component_id='span_charged_sum', component_property='children'),
        Output(component_id='span_already_payed_sum', component_property='children'),
        Output(component_id='span_previous_period_debts_sum', component_property='children'),
        Output(component_id='span_charged_sum_text', component_property='children'),
        Output(component_id='span_already_payed_sum_text', component_property='children'),
        Output(component_id='div_previous_period_debts_sum_text', component_property='children'),
    ],
    [
        Input(component_id='update_map_data', component_property='n_clicks'),
    ],
    [
        State(component_id='radio_items', component_property='value'),
        State(component_id='dropdown_years', component_property='value'),
        State(component_id='dropdown_months', component_property='value'),
    ],
)
def display_map(click: int, value: str, year: int, month: str):
    # fixme
    # -> tuple[Figure, dict[str, str]]:
    month_int: int = convert_month_from_dashboard_to_int(month=month)

    if month_int > CURRENT_MONTH_FROM_DB_INT and year == CURRENT_YEAR_FROM_DB:
        month: str = CURRENT_MONTH_FROM_DB
        df_grouped_by_regions: pd.DataFrame = get_df_with_filter(df=df_all, year=year, month=CURRENT_MONTH_FROM_DB_INT)
        color_alert: str = 'danger'
        # fixme
        text_alert: str = f'Select correct month, example {month}'
        style_alert: dict[str, str] = {'visibility': 'visible'}
    else:
        month: str = month.lower()
        df_grouped_by_regions: pd.DataFrame = get_df_with_filter(df=df_all, year=year, month=month_int)
        color_alert: str = 'success'
        text_alert: str = ''
        style_alert: dict[str, str] = {'visibility': 'hidden'}

    fig = get_figure(df_grouped_by_regions=df_grouped_by_regions, value=value)

    return (
        Alert(
            children=text_alert,
            color=color_alert,
            dismissable=True,
            style=style_alert,
        ),
        fig,
        {'visibility': 'visible'},
        get_total_integer(df=df_grouped_by_regions, field_name='charged_sum'),
        get_total_integer(df=df_grouped_by_regions, field_name='already_payed_sum'),
        get_total_integer(df=df_grouped_by_regions, field_name='previous_period_debts_sum'),
        f'начислено за {month} {year}',
        f'оплачено за {month} {year}',
        f'задолженность за коммунальные услуги за {month} {year}',
    )


def get_figure(df_grouped_by_regions: pd.DataFrame, value: str):
    # fixme ->
    fig = px.choropleth_mapbox(
        data_frame=df_grouped_by_regions,
        geojson=geodata,
        locations=df_grouped_by_regions.region_code,
        color=value,
        hover_name=df_grouped_by_regions.region_name,
        hover_data={
            'region_code': False,
            'charged_sum': True,
            'already_payed_sum': True,
            'previous_period_debts_sum': True
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
            'charged_sum': '',
            'already_payed_sum': '',
            'previous_period_debts_sum': '',
        },
        custom_data=[
            df_grouped_by_regions['region_code'],
            df_grouped_by_regions['region_name'],
            df_grouped_by_regions['charged_sum'],
            df_grouped_by_regions['already_payed_sum'],
            df_grouped_by_regions['previous_period_debts_sum'],
        ],
    )
    hovertemp = '<b>%{customdata[1]}</b><br>'
    hovertemp += '<br><b>%{customdata[2]}</b> - Начислено<br>'
    hovertemp += '<br><b>%{customdata[3]}</b> - Оплачено<br>'
    hovertemp += '<br><b>%{customdata[4]:.0f}</b> - Задолженность<br>'
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


#
# @app.callback(
#     [
#         Output(component_id='back_to_map', component_property='children', allow_duplicate=True),
#         Output(component_id='back_to_map', component_property='style', allow_duplicate=True),
#         Output(component_id='div_table_statistic_for_region', component_property='children', allow_duplicate=True),
#         # Output(component_id='div_table_statistics_on_provider_of_region', component_property='children', allow_duplicate=True),
#         Output(component_id='div_map', component_property='style', allow_duplicate=True),
#         Output(component_id='div_statistic_settings', component_property='style', allow_duplicate=True),
#         Output(component_id='div_total_for_russia', component_property='style', allow_duplicate=True),
#         # Output(component_id='div_statistics_on_provider_of_region', component_property='style', allow_duplicate=True),
#         Output(component_id='div_statistic_for_region', component_property='style', allow_duplicate=True),
#     ],
#     Input(component_id='map', component_property='clickData'),
#     prevent_initial_call=True,
# )
# # fixme name
# def hide_map(clickData: dict[str, list[dict[str, t.Any]]]) -> tuple[
#     html.Button, dict[str, str], DataTable, dict[str, str], dict[str, str],
#     dict[str, str], dict[str, str],
# ]:
#     if clickData is not None:
#         region = clickData['points'][0]['hovertext']
#
#         return (
#             html.Button(
#                 children='Вернуться на карту',
#                 id='button_back_to_map',
#                 n_clicks=0,
#                 style={'fontFamily': 'RobotoCondensed-Light'},
#             ),
#             {'display': 'block'},
#             DataTable(
#                 id='table_statistic_for_region',
#                 data=get_region_data(region=region, df=df),
#                 page_size=10,
#                 style_header=DATATABLE_HEADER_STYLE,
#                 style_data=DATATABLE_DATA_STYLE,
#             ),
#             {'display': 'none'},
#             {'display': 'none'},
#             {'display': 'none'},
#             {'display': 'block'},
#             # {'display': 'block'},
#         )
#
#
# @app.callback(
#     [
#         Output(component_id='back_to_map', component_property='children', allow_duplicate=True),
#         Output(component_id='back_to_map', component_property='style', allow_duplicate=True),
#         Output(component_id='div_table_statistic_for_region', component_property='children', allow_duplicate=True),
#         # Output(component_id='div_table_statistics_on_provider_of_region', component_property='children', allow_duplicate=True),
#         Output(component_id='div_map', component_property='style', allow_duplicate=True),
#         Output(component_id='div_statistic_settings', component_property='style', allow_duplicate=True),
#         Output(component_id='div_total_for_russia', component_property='style', allow_duplicate=True),
#         # Output(component_id='div_statistics_on_provider_of_region', component_property='style', allow_duplicate=True),
#         Output(component_id='div_statistic_for_region', component_property='style', allow_duplicate=True),
#     ],
#     Input(component_id='dropdown_regions', component_property='value'),
#     prevent_initial_call=True,
# )
# def hide_map(value: str) -> tuple[
#     html.Button, dict[str, str], DataTable, dict[str, str], dict[str, str],
#     dict[str, str], dict[str, str],
# ]:
#     return (
#         html.Button(
#             children='Вернуться на карту',
#             id='button_back_to_map',
#             n_clicks=0,
#             style={'fontFamily': 'RobotoCondensed-Light'},
#         ),
#         {'display': 'block'},
#         DataTable(
#             id='table_statistic_for_region',
#             data=get_region_data(region=value, df=df),
#             page_size=10,
#             style_header=DATATABLE_HEADER_STYLE,
#             style_data=DATATABLE_DATA_STYLE,
#         ),
#
#         {'display': 'none'},
#         {'display': 'none'},
#         {'display': 'none'},
#         {'display': 'block'},
#     )
#
#
# @app.callback(
#     [
#         Output(component_id='back_to_map', component_property='style', allow_duplicate=True),
#         Output(component_id='div_map', component_property='style', allow_duplicate=True),
#         Output(component_id='div_statistic_settings', component_property='style', allow_duplicate=True),
#         Output(component_id='div_total_for_russia', component_property='style', allow_duplicate=True),
#         # Output(component_id='div_statistics_on_provider_of_region', component_property='style', allow_duplicate=True),
#         Output(component_id='div_statistic_for_region', component_property='style', allow_duplicate=True),
#     ],
#     Input(component_id='back_to_map', component_property='n_clicks'),
#     prevent_initial_call=True,
# )
# def back_to_map(n_clicks: int) -> tuple[
#     dict[str, str], dict[str, str], dict[str, t.Any],
#     dict[str, str], dict[str, str]
# ]:
#     return (
#         {'display': 'none'},
#         {'display': 'block'},
#         {
#             'display': 'flex',
#             'justify-content': 'left',
#             'borderWidth': 2,
#             'borderColor': 'rgb(186, 227, 242)',
#             'borderStyle': 'solid',
#             'alignItems': 'center',
#             'padding': 10,
#             'height': 100,
#         },
#         {'display': 'block'},
#         {'display': 'none'},
#         # {'display': 'none'},
#     )


if __name__ == '__main__':
    geodata: geojson.FeatureCollection = get_geodata()
    app.run(debug=True)
