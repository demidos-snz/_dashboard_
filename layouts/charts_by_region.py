from dash import html, dcc

from init_data import CURRENT_YEAR_FROM_DB


def div_charts_by_region() -> html.Div:
    return html.Div(
        # fixme id
        id='',
        children=[
            html.H3(
                id='region_name',
                style={
                    'display': 'none',
                }
            ),

            html.Div(
                # fixme id
                id='',
                style={
                    'display': 'flex',
                },
                children=[
                    html.Div(
                        id='div_charges_sum',
                        style={
                            'display': 'none',
                            'textAlign': 'center',
                        },
                        children=dcc.Graph(
                            id='graph_charges_sum',
                            config={
                                'scrollZoom': False,
                                'displayModeBar': False,
                            },
                        ),
                    ),

                    html.Div(
                        id='div_already_payed_sum',
                        style={
                            'display': 'none',
                        },
                        children=dcc.Graph(
                            id='graph_already_payed_sum',
                            config={
                                'scrollZoom': False,
                                'displayModeBar': False,
                            },
                        ),
                    ),
                ],
            ),

            html.Div(
                id='div_debts_sum',
                style={
                    'display': 'none',
                },
                children=dcc.Graph(
                    id='graph_debts_sum',
                    config={
                        'scrollZoom': False,
                        'displayModeBar': False,
                    },
                ),
            ),

            html.Div(
                # fixme id
                id='',
                style={
                    'display': 'flex',
                },
                children=[
                    html.Div(
                        id='div_cr_charges_sum',
                        style={
                            'display': 'none',
                            'textAlign': 'center',
                        },
                        children=dcc.Graph(
                            id='graph_cr_charges_sum',
                            config={
                                'scrollZoom': False,
                                'displayModeBar': False,
                            },
                        ),
                    ),

                    html.Div(
                        id='div_cr_payed_sum',
                        style={
                            'display': 'none',
                        },
                        children=dcc.Graph(
                            id='graph_cr_payed_sum',
                            config={
                                'scrollZoom': False,
                                'displayModeBar': False,
                            },
                        ),
                    ),
                ],
            ),

            html.Div(
                id='div_cr_total_for_russia',
                style={
                    'display': 'none',
                    'position': 'relative',
                    'padding-left': 200,
                },
                children=[
                    html.H2(
                        # fixme id
                        id='',
                        style={
                            'fontSize': '19px',
                            'lineHeight': '1.15em',
                            'fontWeight': 'bold',
                            'color': 'rgba(13, 31, 62, 0.74)',
                            'font-family': 'RobotoCondensed-Light',
                        },
                        # fixme year
                        children='Собираемость взносов на счете регионального оператора за 2023 год:',
                    ),

                    html.Div(
                        id='div_cr_charges_total',
                        style={
                            'height': '63px',
                        },
                        children=[
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
                                style={
                                    'fontSize': '19px',
                                    'lineHeight': '1.15em',
                                    'fontWeight': 'bold',
                                    'color': 'rgba(13, 31, 62, 0.74)',
                                    'fontFamily': 'RobotoCondensed-Light',
                                },
                                children=f'начислено взносов с начала {CURRENT_YEAR_FROM_DB} года',
                            ),
                        ],
                    ),

                    html.Div(
                        id='div_cr_payed_total',
                        style={
                            'height': '63px',
                        },
                        children=[
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
                                style={
                                    'fontSize': '19px',
                                    'lineHeight': '1.15em',
                                    'fontWeight': 'bold',
                                    'color': 'rgba(13, 31, 62, 0.74)',
                                    'fontFamily': 'RobotoCondensed-Light',
                                    'padding-right': 15,
                                },
                                children=f'оплачено взносов с начала {CURRENT_YEAR_FROM_DB} года',
                            ),
                        ],
                    ),

                    html.Div(
                        id='div_cr_debt_total',
                        style={
                            'height': '63px',
                        },
                        children=[
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
                                style={
                                    'fontSize': '19px',
                                    'lineHeight': '1.15em',
                                    'fontWeight': 'bold',
                                    'color': 'rgba(13, 31, 62, 0.74)',
                                    'fontFamily': 'RobotoCondensed-Light',
                                    'padding-right': 15,
                                },
                                children=f'задолженность по уплате взносов за {CURRENT_YEAR_FROM_DB} год',
                            ),
                        ],
                    ),
                ],
            ),

            html.Div(
                id='div_sunburst',
                style={
                    'display': 'none',
                },
                children=dcc.Graph(
                    id='graph_sunburst',
                    config={
                        'scrollZoom': False,
                        'displayModeBar': False,
                    },
                ),
            ),
        ],
    )
