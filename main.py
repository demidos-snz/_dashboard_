import typing as t
from datetime import date

import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Output, Input
from dash.dash_table import DataTable as Table
from plotly.graph_objs import Figure

from settings import DEFAULT_REGION, REGIONS, DEFAULT_RADIO_ITEM, ORG_ICON_PATH, MKD_ICON_PATH, JD_ICON_PATH
from utils import (
    get_df, get_geodata, get_df_grouped_by_regions,
    get_organizations_by_region, get_region_data, b64_image,
    get_total_integer,
)

app = Dash(
    name=__name__,
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'],
)

app.layout = html.Div(
    children=[

        html.H1(
            id='label_dashboard',
            className='row',
            children='Мониторинг отрасли ЖКХ',
        ),

        html.Hr(),

        html.Div(
            [
                html.Div(
                    [
                        html.Div(
                            dcc.Dropdown(
                                id='dropdown_years',
                                # fixme 2020
                                # options=[{'label': x, 'value': x} for x in range(2020, date.today().year + 1)],
                                options=[2023],
                                value=date.today().year,
                            ),
                            style={
                                'width': '300px',
                                'margin-left': 20,
                                'margin-bottom': 5,
                            },
                        ),

                        html.Div(
                            dcc.Dropdown(
                                id='dropdown_month',
                                # options=[{'label': x, 'value': x} for x in list(calendar.month_name) if x],
                                options=['May'],
                                # value=date.today().strftime('%B'),
                                value='May',
                            ),
                            style={
                                'width': '300px',
                                'margin-left': 20,
                                'margin-bottom': 5,
                            },
                        ),
                    ],
                    id='div_month_list',
                    style={
                        'display': 'flex',
                        'justify-content': 'left',
                    },
                ),

                html.H3(
                    children='Всего в системе:',
                    style={
                        'fontSize': '19px',
                        'lineHeight': '1.15em',
                        'fontWeight': 'bold',
                        'color': 'rgba(13, 31, 62, 0.74)',
                        'font-family': 'RobotoCondensed-Light',
                        'margin': 35,
                    },
                ),

                html.Div(
                    [
                        html.Img(
                            src=b64_image(ORG_ICON_PATH),
                            style={
                                'margin-right': 5
                            },
                        ),

                        html.Span(
                            children=get_total_integer(df=get_df(), field_name='accounts_count'),
                            style={
                                'textAlign': 'left',
                                'fontSize': '50px',
                                'lineHeight': '1em',
                                'fontWeight': 'bold',
                                'color': '#2aa2cf',
                                'fontFamily': 'RobotoCondensed-Bold',
                                'margin': 5,
                            },
                        ),

                        html.Span(
                            children='лицевых счетов',
                            style={
                                'fontSize': '19px',
                                'lineHeight': '1.15em',
                                'fontWeight': 'bold',
                                'color': 'rgba(13, 31, 62, 0.74)',
                                'font-family': 'RobotoCondensed-Light',
                                'margin': 10,
                            },
                        ),
                    ],
                    style={
                        'height': '73px',
                        'margin-left': 35,
                    },
                ),

                html.Div(
                    [
                        html.Img(
                            src=b64_image(MKD_ICON_PATH),
                            style={
                                'margin-right': 15,
                            },
                        ),

                        html.Span(
                            children=get_total_integer(df=get_df(), field_name='payment_documents_count'),
                            style={
                                'textAlign': 'left',
                                'fontSize': '50px',
                                'lineHeight': '1em',
                                'fontWeight': 'bold',
                                'color': '#2aa2cf',
                                'fontFamily': 'RobotoCondensed-Bold',
                                'margin': 5,
                            },
                        ),

                        html.Span(
                            # fixme month
                            children='платежных документов размещено в мае',
                            style={
                                'fontSize': '19px',
                                'lineHeight': '1.15em',
                                'font-weight': 'bold',
                                'color': 'rgba(13, 31, 62, 0.74)',
                                'font-family': 'RobotoCondensed-Light',
                                'margin': 5,
                            },
                        ),
                    ],
                    style={
                        'height': '73px',
                        'margin-left': 35,
                    },
                ),

                html.Div(
                    [
                        html.Div(
                            html.Img(
                                src=b64_image(JD_ICON_PATH),
                                style={
                                    'margin-right': 5,
                                    'margin-top': 15,
                                },
                            ),
                        ),

                        html.Span(
                            children=get_total_integer(df=get_df(), field_name='charges_sum'),
                            style={
                                'textAlign': 'left',
                                'fontSize': '50px',
                                'lineHeight': '1em',
                                'fontWeight': 'bold',
                                'color': '#2aa2cf',
                                'fontFamily': 'RobotoCondensed-Bold',
                                'margin': 5,
                            },
                        ),

                        # fixme month
                        html.Div(
                            children='рублей начислено за коммунальные услуги в мае',
                            style={
                                'fontSize': '19px',
                                'lineHeight': '1.15em',
                                'font-weight': 'bold',
                                'color': 'rgba(13, 31, 62, 0.74)',
                                'font-family': 'RobotoCondensed-Light',
                                'margin': 5,
                                'width': '300px',
                            },
                        ),
                    ],
                    style={
                        'height': '73px',
                        'margin-left': 35,
                        'display': 'flex',
                        'justify-content': 'left',
                    },
                ),

                html.Div(
                    id='back_to_map',
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
                        'width': '1200px',
                        'visibility': 'hidden',
                        'display': 'block',
                    },
                ),

                html.Div(
                    [
                        html.Div(
                            dcc.Dropdown(
                                id='dropdown_regions',
                                options=REGIONS,
                                value=DEFAULT_REGION,
                            ),
                            id='div_regions_list',
                            style={
                                'width': '300px',
                                'margin-left': 20,
                                'margin-bottom': 5,
                            },
                        ),

                        html.Div(
                            [
                                html.Span(
                                    children='Отображать на карте статистику:',
                                    style={
                                        'fontSize': '15px',
                                        'lineHeight': '1.3em',
                                        'fontWeight': 'bold',
                                        'color': 'black',
                                        'fontFamily': 'RobotoCondensed-Light',
                                        'margin': 10,
                                    },
                                ),

                                dcc.RadioItems(
                                    id='radio_items',
                                    options={
                                        'accounts_count': 'по лицевым счетам',
                                        'payment_documents_count': 'по платежным документам',
                                        'charges_sum': 'по начислениям',
                                    },
                                    value=DEFAULT_RADIO_ITEM,
                                    style={
                                        'width': '300px',
                                        'fontSize': '12px',
                                        'color': 'black',
                                    },
                                ),
                            ],
                            id='div_radio_items',
                            style={
                                'display': 'flex',
                                'justify-content': 'left',
                                'width': 500,
                                'height': 100,
                                'margin-left': 20,
                                'margin-bottom': 20,
                                'borderWidth': 2,
                                'borderColor': 'rgb(186, 227, 242)',
                                'borderStyle': 'solid',
                                'alignItems': 'center',
                            },
                        ),
                    ],
                    style={
                        'display': 'flex',
                        'justify-content': 'left',
                    },
                ),

                html.H3(
                    id='label_statistic_for_region',
                    children='Статистика по региону:',
                ),

                html.Div(
                    id='div_statistic_for_region',
                    style={
                        'margin': 20,
                    },
                ),

                html.H3(
                    id='label_statistics_on_provider_of_region',
                    children='Статистика по поставщикам региона (ТОП 10):',
                ),

                html.Div(
                    id='div_statistics_on_provider_of_region',
                    style={
                        'margin': 20,
                    },
                ),
            ],
        ),
    ],
    style={
        'position': 'relative',
        'maxWidth': '1170px',
        'margin-right': 'auto',
        'margin-left': 'auto',
    },
)


@app.callback(
    [
        Output(component_id='map', component_property='figure'),
        Output(component_id='div_map', component_property='style'),
    ],
    Input(component_id='radio_items', component_property='value'),
)
def display_map(value: str) -> tuple[Figure, dict[str, str]]:
    fig = px.choropleth_mapbox(
        data_frame=df_grouped_by_regions,
        geojson=get_geodata(),
        locations=df_grouped_by_regions.id,
        color=value,
        hover_name=df_grouped_by_regions.region,
        hover_data={
            'id': False,
            'accounts_count': True,
            'payment_documents_count': True,
            'charges_sum': True
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
        center={'lat': 68, 'lon': 105},
        labels={
            'accounts_count': '',
            'payment_documents_count': '',
            'charges_sum': '',
        },
        custom_data=[
            df_grouped_by_regions['id'],
            df_grouped_by_regions['region'],
            df_grouped_by_regions['accounts_count'],
            df_grouped_by_regions['payment_documents_count'],
            df_grouped_by_regions['charges_sum'],
        ],
    )

    hovertemp = '<b>%{customdata[1]}</b><br><br><b>%{customdata[2]}</b> - Количество актуальных ЛС<br>'
    # fixme month
    hovertemp += '<br><b>%{customdata[3]}</b> - Количество платежных документов, размещенных в мае<br>'
    # fixme month
    hovertemp += '<br><b>%{customdata[4]:.0f}</b> - Начислено за КУ в мае<br>'

    fig.update_traces(
        hovertemplate=hovertemp,
        marker_line_width=1,
        marker_line_color='white',
    )

    fig.update_layout(
        height=760,
        hoverlabel={
            'bgcolor': 'white',
            'font_size': 18,
        },
    )
    return fig, {'visibility': 'visible'}


@app.callback(
    [
        Output(component_id='div_statistic_for_region', component_property='children'),
        Output(component_id='div_statistics_on_provider_of_region', component_property='children'),
        Output(component_id='dropdown_regions', component_property='value'),
    ],
    Input(component_id='map', component_property='hoverData'),
)
def update_tables_with_statistics_by_region(hoverData: t.Optional[dict[str, list]]) -> tuple[Table, Table, str]:
    region: str = DEFAULT_REGION if hoverData is None else hoverData['points'][0]['hovertext']

    return Table(
        id='table_statistic_for_region',
        data=get_region_data(region=region, df=df),
        page_size=10,
    ), Table(
        id='table_statistics_on_provider_of_region',
        data=get_organizations_by_region(region=region, df=df),
        page_size=10,
    ), region


@app.callback(
    [
        Output(component_id='div_map', component_property='style', allow_duplicate=True),
        Output(component_id='div_radio_items', component_property='style', allow_duplicate=True),
        Output(component_id='back_to_map', component_property='children', allow_duplicate=True),
        Output(component_id='back_to_map', component_property='style', allow_duplicate=True)
    ],
    Input(component_id='map', component_property='clickData'),
    prevent_initial_call=True
)
def hide_map(clickData) -> tuple[dict, dict, html.Button, dict]:
    if clickData is not None:
        return (
            {'display': 'none'},
            {'display': 'none'},
            html.Button(
                children='Вернуться на карту',
                id='button_back_to_map',
                n_clicks=0,
                style={'fontFamily': 'RobotoCondensed-Light'},
            ),
            {
                'display': 'block',
                'margin': 20,
            },
        )


@app.callback(
    [
        Output(component_id='div_map', component_property='style', allow_duplicate=True),
        Output(component_id='div_radio_items', component_property='style', allow_duplicate=True),
        Output(component_id='back_to_map', component_property='style', allow_duplicate=True),
    ],
    Input(component_id='back_to_map', component_property='n_clicks'),
    prevent_initial_call=True,
)
def back_to_map(n_clicks: int) -> tuple[dict[str, t.Any], dict[str, t.Any], dict[str, t.Any]]:
    return (
        {'display': 'block'},
        {
            'display': 'flex',
            'justify-content': 'left',
            'width': 500,
            'height': 100,
            'margin-left': 20,
            'margin-bottom': 20,
            'borderWidth': 2,
            'borderColor': 'rgb(186, 227, 242)',
            'borderStyle': 'solid',
            'alignItems': 'center',
        },
        {'display': 'none'},
    )


@app.callback(
    [
        Output(component_id='div_statistic_for_region', component_property='children', allow_duplicate=True),
        Output(component_id='div_statistics_on_provider_of_region', component_property='children',
               allow_duplicate=True),
    ],
    Input(component_id='dropdown_regions', component_property='value'),
    prevent_initial_call=True,
)
def update_tables_with_statistics_by_region_(value: t.Optional[str]) -> tuple[Table, Table]:
    region: str = DEFAULT_REGION if value is None else value

    return Table(
        id='table_statistic_for_region',
        data=get_region_data(region=region, df=df),
        page_size=10,
    ), Table(
        id='table_statistics_on_provider_of_region',
        data=get_organizations_by_region(region=region, df=df),
        page_size=10,
    )


if __name__ == '__main__':
    df: pd.DataFrame = get_df()
    df_grouped_by_regions: pd.DataFrame = get_df_grouped_by_regions(df=df)

    app.run(debug=True)
