import base64
import calendar
from time import strptime

import geojson
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from clickhouse_driver import Client
from dash import html

from settings import BUTTON_STYLE


def get_total_integer(df: pd.DataFrame, field_name: str) -> str:
    total_sum: float = round(df[field_name].sum())
    return '{:,}'.format(total_sum).replace(',', ' ')


# fixme path
def get_geodata(path: str = 'result.geojson') -> geojson.FeatureCollection:
    with open(file=path, encoding='utf-8') as f:
        data = geojson.load(f)
    return data


def b64_image(image_filename: str) -> str:
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


def make_human_readable_data(column: pd.Series) -> list[str]:
    return ['{:,}'.format(i).replace(',', ' ') for i in column]


# fixme naming + args df
def ggg(df: pd.DataFrame, region: str, x_axis: tuple[str]) -> tuple[
    html.Button, dict[str, str], dict[str, str],
    dict[str, str],  dict[str, str], go.Figure,
    dict[str, str], go.Figure, dict[str, str],
    go.Figure, dict[str, str], str, dict[str, str]
]:
    df_2022 = df[(df['year'] == 2022) & (df['region_name'] == region)]
    df_2023 = df[(df['year'] == 2023) & (df['region_name'] == region)]
    df = df_2022.merge(df_2023, how='inner', on=['month', 'region_name'])

    fig1 = get_figure1(df=df, x_axis=x_axis)
    fig2 = get_figure2(df=df, x_axis=x_axis)
    fig3 = get_figure3(df=df, x_axis=x_axis)

    return (
        html.Button(
            children='Вернуться на карту',
            id='button_back_to_map',
            n_clicks=0,
            style=BUTTON_STYLE,
        ),
        {'display': 'block'},

        {'display': 'none'},
        {'display': 'none'},
        {'display': 'none'},

        fig1,
        {'display': 'block'},
        fig2,
        {'display': 'block'},
        fig3,
        {'display': 'block'},

        region,
        {
            'display': 'block',
            'textAlign': 'center',
            'margin-bottom': 20,
        },
    )


# fixme name
def get_figure1(df: pd.DataFrame, x_axis: tuple[str]) -> go.Figure:
    fig = px.line(
        x=x_axis,
        y=df['charged_sum_x'],
        color=px.Constant('2022 год'),
        # labels=dict(x='Месяц', y='Начисления, в руб', color='Год'),
        labels=dict(x='', y='', color='Год'),
    )

    fig.update_traces(
        line_color='rgb(245, 153, 46)',
        line_width=3,
        hovertemplate='<br>'.join(['Начислено %{y}']),
    )
    # fixme year
    fig.add_bar(x=x_axis, y=df['charged_sum_y'], name='2023 год')
    fig.update_traces(
        marker_color='rgb(173, 211, 100)',
        customdata=np.transpose(df['charged_sum_y']),
        hovertemplate='<br>'.join(['Начислено %{y}']),
    )
    fig.update_layout(
        title='Динамика начислений за ЖКУ, руб.',
        hovermode='x unified',
        width=600,
        height=500,
    )

    return fig


# fixme name
def get_figure2(df: pd.DataFrame, x_axis: tuple[str]) -> go.Figure:
    fig = px.line(
        x=x_axis,
        y=df['already_payed_sum_x'],
        color=px.Constant('2022 год'),
        # labels=dict(x='Месяц', y='Сумма оплат, в руб', color='Год'),
        labels=dict(x='', y='', color='Год'),
    )

    fig.update_traces(
        line_color='rgb(245, 153, 46)',
        line_width=3,
        hovertemplate='<br>'.join(['Оплачено %{y}']),
    )
    # fixme year
    fig.add_bar(x=x_axis, y=df['already_payed_sum_y'], name='2023 год')
    fig.update_traces(
        marker_color='rgb(173, 211, 100)',
        hovertemplate='<br>'.join(['Оплачено %{y}']),
    )
    fig.update_layout(
        title='Динамика оплат за ЖКУ, руб.',
        hovermode='x unified',
        width=600,
        height=500,
    )

    return fig


# fixme name
def get_figure3(df: pd.DataFrame, x_axis: tuple[str]) -> go.Figure:
    fig = go.Figure()
    fig.add_trace(
        trace=go.Bar(
            x=x_axis,
            y=df['charged_sum_y'],
            name='Сумма начислений',
            marker={'color': 'rgb(173, 211, 100)'},
            width=0.2,
            hovertemplate='<br>'.join(['Начислено %{y}']),
        ),
    )
    fig.add_trace(
        trace=go.Bar(
            x=x_axis,
            y=df['already_payed_sum_y'],
            name='Сумма оплат',
            marker={'color': 'rgb(253, 211, 17)'},
            width=0.2,
            hovertemplate='<br>'.join(['Оплачено %{y}']),
        ),
    )
    fig.add_trace(
        trace=go.Bar(
            x=x_axis,
            y=df['previous_period_debts_sum_y'],
            name='Дебиторская задолженность',
            marker={'color': 'rgb(239, 75, 46)'},
            width=0.2,
            hovertemplate='<br>'.join(['Дебиторская задолженность %{y}']),
        ),
    )
    fig.update_layout(
        title='Динамика начислений, оплат и задолженности за ЖКУ, руб.',
        barmode='group',
        hovermode='x unified',
    )

    return fig


def get_current_month_from_db(client: Client) -> str:
    month: int = get_current_month_from_db_int(client=client)
    return calendar.month_name[month].lower()


def get_current_month_from_db_int(client: Client) -> int:
    for row in client.execute(query="""
    select extract(month from max(report_month)) as month
    from ois_visual.charges_payed_debts_by_regions t1
    """):
        return row[0]


def get_all_years_from_db(client: Client) -> list[int]:
    return [tuple_year[0] for tuple_year in client.execute(query="""
    select distinct(extract(year from (report_month))) as year
    from ois_visual.charges_payed_debts_by_regions t1
    """)]


def get_current_year_from_db(years: list[int]) -> int:
    return sorted(years, reverse=True)[0]


def convert_month_from_dashboard_to_int(month: str) -> int:
    return strptime(month, '%B').tm_mon
