from dash import html, dcc

from constants import MONTHS
from init_data import ALL_YEARS_FROM_DB, CURRENT_YEAR_FROM_DB, CURRENT_MONTH_FROM_DB
from settings import BUTTON_STYLE, DEFAULT_RADIO_ITEM


def div_filters() -> html.Div:
    return html.Div(
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
        children=[
            html.Div(
                # fixme id
                id='',
                style={
                    'display': 'flex',
                    'justify-content': 'left',
                    'alignItems': 'center',
                    'height': 100,
                    'margin-right': 50,
                },
                children=[
                    html.Span(
                        # fixme id
                        id='',
                        style={
                            'padding-right': 20,
                            'fontSize': '16px',
                            'fontFamily': 'RobotoCondensed-Light',
                            'lineHeight': '1.3em',
                            'fontWeight': 'bold',
                            'color': 'black',
                            'margin-left': '80px',
                        },
                        children='Выбрать период:',
                    ),

                    html.Div(
                        id='div_period_dropdowns',
                        style={
                            'display': 'block',
                        },
                        children=[
                            html.Div(
                                # fixme id
                                id='',
                                style={
                                    'width': '250px',
                                    'margin-bottom': 5,
                                },
                                children=dcc.Dropdown(
                                    id='dropdown_years',
                                    options=[
                                        {'label': x, 'value': x} for x in ALL_YEARS_FROM_DB
                                    ],
                                    value=CURRENT_YEAR_FROM_DB,
                                    clearable=False,
                                ),
                            ),

                            html.Div(
                                # fixme id
                                id='',
                                style={
                                    'width': '250px',
                                    'margin-bottom': 5,
                                },
                                children=dcc.Dropdown(
                                    id='dropdown_months',
                                    options=[
                                        {'label': x, 'value': x} for x in MONTHS
                                    ],
                                    value=CURRENT_MONTH_FROM_DB,
                                    clearable=False,
                                ),
                            ),
                        ],
                    ),
                ],
            ),

            html.Div(
                id='div_radio_items',
                style={
                    'display': 'flex',
                    'justify-content': 'left',
                    'alignItems': 'center',
                    'height': 100,
                },
                children=[
                    html.Span(
                        # fixme id
                        id='',
                        style={
                            'fontSize': '16px',
                            'margin-right': '20px',
                            'lineHeight': '1.3em',
                            'fontWeight': 'bold',
                            'color': 'black',
                            'fontFamily': 'RobotoCondensed-Light',
                            'alignItems': 'center',
                        },
                        children='Отображать статистику:',
                    ),

                    dcc.RadioItems(
                        id='radio_items',
                        style={
                            'width': '200px',
                            'fontSize': '14px',
                            'color': 'black',
                        },
                        options={
                            'cpd_charged_sum': '\tпо начислениям',
                            'cpd_already_payed_sum': '\tпо оплате',
                            'cpd_previous_period_debts_sum': '\tпо задолженности',
                        },
                        value=DEFAULT_RADIO_ITEM,
                    ),
                ],
            ),

            html.Button(
                id='update_map_data',
                style=BUTTON_STYLE,
                children='Обновить данные на карте',
                n_clicks=0,
            ),
        ],
    )
