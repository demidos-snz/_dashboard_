from dash import html

from init_data import df_grouped_by_regions_default, CURRENT_MONTH_FROM_DB, CURRENT_YEAR_FROM_DB
from constants import ORG_ICON_PATH, MKD_ICON_PATH, JD_ICON_PATH
from layouts.utils import b64_image
from utils import get_cpd_total_integer


def div_total_for_russia() -> html.Div:
    return html.Div(
        id='div_total_for_russia',
        style={'display': 'block'},
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
                children='Всего в системе:',
            ),

            html.Div(
                id='div_org_icon',
                style={
                    'height': '63px',
                },
                children=[
                    html.Img(
                        # fixme id
                        id='',
                        style={
                            'padding-right': 20,
                            'margin-bottom': 30,
                        },
                        src=b64_image(image_filename=ORG_ICON_PATH),
                    ),

                    html.Span(
                        id='span_charged_sum',
                        style={
                            'textAlign': 'left',
                            'fontSize': '50px',
                            'lineHeight': '1em',
                            'fontWeight': 'bold',
                            'color': '#2aa2cf',
                            'fontFamily': 'RobotoCondensed-Bold',
                            'padding-right': 15,
                        },
                        children=get_cpd_total_integer(
                            df=df_grouped_by_regions_default,
                            field_name='cpd_charged_sum',
                        ),
                    ),

                    html.Span(
                        id='span_charged_sum_text',
                        style={
                            'fontSize': '19px',
                            'lineHeight': '1.15em',
                            'fontWeight': 'bold',
                            'color': 'rgba(13, 31, 62, 0.74)',
                            'fontFamily': 'RobotoCondensed-Light',
                        },
                        children=f'начислено за {CURRENT_MONTH_FROM_DB} {CURRENT_YEAR_FROM_DB}',
                    ),
                ],
            ),

            html.Div(
                id='div_mkd_icon',
                style={
                    'height': '63px',
                },
                children=[
                    html.Img(
                        # fixme id
                        id='',
                        style={
                            'padding-right': 30,
                            'margin-bottom': 25,
                        },
                        src=b64_image(image_filename=MKD_ICON_PATH),
                    ),

                    html.Span(
                        id='span_already_payed_sum',
                        style={
                            'textAlign': 'left',
                            'fontSize': '50px',
                            'lineHeight': '1em',
                            'fontWeight': 'bold',
                            'color': '#2aa2cf',
                            'fontFamily': 'RobotoCondensed-Bold',
                            'padding-right': 15,
                        },
                        children=get_cpd_total_integer(
                            df=df_grouped_by_regions_default,
                            field_name='cpd_already_payed_sum',
                        ),
                    ),

                    html.Span(
                        id='span_already_payed_sum_text',
                        style={
                            'fontSize': '19px',
                            'lineHeight': '1.15em',
                            'fontWeight': 'bold',
                            'color': 'rgba(13, 31, 62, 0.74)',
                            'fontFamily': 'RobotoCondensed-Light',
                            'padding-right': 15,
                        },
                        children=f'оплачено за {CURRENT_MONTH_FROM_DB} {CURRENT_YEAR_FROM_DB}',
                    ),
                ],
            ),

            html.Div(
                id='div_jd_icon',
                style={
                    'height': '63px',
                },
                children=[
                    html.Img(
                        # fixme id
                        id='',
                        style={
                            'padding-right': 25,
                            'margin-bottom': 25,
                        },
                        src=b64_image(image_filename=JD_ICON_PATH),
                    ),

                    html.Span(
                        id='span_previous_period_debts_sum',
                        style={
                            'textAlign': 'left',
                            'fontSize': '50px',
                            'lineHeight': '1em',
                            'fontWeight': 'bold',
                            'color': '#2aa2cf',
                            'fontFamily': 'RobotoCondensed-Bold',
                            'padding-right': 15,
                        },
                        children=get_cpd_total_integer(
                            df=df_grouped_by_regions_default,
                            field_name='cpd_previous_period_debts_sum',
                        ),
                    ),

                    html.Span(
                        id='div_previous_period_debts_sum_text',
                        style={
                            'fontSize': '19px',
                            'lineHeight': '1.15em',
                            'fontWeight': 'bold',
                            'color': 'rgba(13, 31, 62, 0.74)',
                            'fontFamily': 'RobotoCondensed-Light',
                            'padding-right': 15,
                        },
                        children=f'дебиторская задолженность за '
                                 f'{CURRENT_MONTH_FROM_DB} {CURRENT_YEAR_FROM_DB}',
                    ),
                ],
            ),
        ],
    )
