import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import html

from init_data import DF_SUNBURST, X_AXIS
from settings import BUTTON_STYLE


def get_cr_total_integer(df: pd.DataFrame, field_name: str, region: str) -> str:
    total_sum: float = round(df[field_name][df['region_name'] == region].max())
    return '{:,}'.format(total_sum).replace(',', ' ')


def get_region_data_for_sunburst(region: str) -> pd.DataFrame:
    return DF_SUNBURST[DF_SUNBURST['region_name'] == region]


def get_charts_by_region(df: pd.DataFrame, region: str, x_axis: tuple[str] = X_AXIS) -> tuple[
    html.Button, dict[str, str],

    dict[str, str], dict[str, str],  dict[str, str],

    go.Figure, dict[str, str],
    go.Figure, dict[str, str],
    go.Figure, dict[str, str],
    go.Figure, dict[str, str],
    go.Figure, dict[str, str],
    dict[str, str],

    dict[str, str],

    str, dict[str, str],

    str, str, str,

    go.Figure, dict[str, str],
]:
    # fixme year
    df_2022: pd.DataFrame = df[(df['year'] == 2022) & (df['region_name'] == region)]
    df_2023: pd.DataFrame = df[(df['year'] == 2023) & (df['region_name'] == region)]
    df: pd.DataFrame = df_2022.merge(df_2023, how='inner', on=['month', 'region_name'])

    fig1: go.Figure = get_figure1(df=df, x_axis=x_axis)
    fig2: go.Figure = get_figure2(df=df, x_axis=x_axis)
    fig3: go.Figure = get_figure3(df=df, x_axis=x_axis)
    fig4: go.Figure = get_figure4(df=df, x_axis=x_axis)
    fig5: go.Figure = get_figure5(df=df, x_axis=x_axis)

    fig_sunburst: go.Figure = get_sunburst(df=get_region_data_for_sunburst(region=region))

    span_cr_charged_sum_value: str = get_cr_total_integer(
        df=df,
        field_name='cr_total_accured_contib_sum_y',
        region=region,
    )

    span_cr_payed_sum: str = get_cr_total_integer(
        df=df,
        field_name='cr_total_paid_contib_sum_y',
        region=region,
    )

    span_cr_debts_sum: str = get_cr_total_integer(
        df=df,
        field_name='cr_debt_sum_y',
        region=region,
    )

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
        fig4,
        {'display': 'block'},
        fig5,
        {'display': 'block'},
        {
            'display': 'block',
            'position': 'relative',
            'padding-left': 70,
        },

        {'display': 'none'},

        region,
        {
            'display': 'block',
            'textAlign': 'center',
            'margin-bottom': 20,
        },

        span_cr_charged_sum_value,
        span_cr_payed_sum,
        span_cr_debts_sum,

        fig_sunburst,
        {'display': 'block'},
    )


# fixme name
def get_figure1(df: pd.DataFrame, x_axis: tuple[str]) -> go.Figure:
    fig: go.Figure = px.line(
        x=x_axis,
        y=df['cpd_charged_sum_x'],
        # fixme year
        color=px.Constant('2022 год'),
        labels=dict(x='', y='', color='Год'),
    )

    fig.update_traces(
        line_color='rgb(245, 153, 46)',
        line_width=3,
        hovertemplate='<br>'.join(['Начислено %{y}']),
    )
    # fixme year
    fig.add_bar(x=x_axis, y=df['cpd_charged_sum_y'], name='2023 год')
    fig.update_traces(
        marker_color='rgb(173, 211, 100)',
        customdata=np.transpose(df['cpd_charged_sum_y']),
        hovertemplate='<br>'.join(['Начислено %{y}']),
    )
    fig.update_layout(
        title='Динамика начислений за ЖКУ, руб.',
        title_x=0.5,
        hovermode='x unified',
        width=600,
        height=500,
        hoverlabel={
            'bordercolor': 'white',
            'font_family': 'Helvetica',
            'font_size': 16,
        },
    )

    return fig


# fixme name
def get_figure2(df: pd.DataFrame, x_axis: tuple[str]) -> go.Figure:
    fig: go.Figure = px.line(
        x=x_axis,
        y=df['cpd_already_payed_sum_x'],
        # fixme year
        color=px.Constant('2022 год'),
        labels=dict(x='', y='', color='Год'),
    )

    fig.update_traces(
        line_color='rgb(245, 153, 46)',
        line_width=3,
        hovertemplate='<br>'.join(['Оплачено %{y}']),
    )
    # fixme year
    fig.add_bar(x=x_axis, y=df['cpd_already_payed_sum_y'], name='2023 год')
    fig.update_traces(
        marker_color='rgb(173, 211, 100)',
        hovertemplate='<br>'.join(['Оплачено %{y}']),
    )
    fig.update_layout(
        title='Динамика оплат за ЖКУ, руб.',
        title_x=0.5,
        hovermode='x unified',
        width=600,
        height=500,
        hoverlabel={
            'bordercolor': 'white',
            'font_family': 'Helvetica',
            'font_size': 16,
        },
    )

    return fig


# fixme name
def get_figure3(df: pd.DataFrame, x_axis: tuple[str]) -> go.Figure:
    fig: go.Figure = go.Figure()
    fig.add_trace(
        trace=go.Bar(
            x=x_axis,
            y=df['cpd_charged_sum_y'],
            name='Сумма начислений',
            marker={'color': 'rgb(173, 211, 100)'},
            width=0.2,
            hovertemplate='<br>'.join(['%{y}']),
        ),
    )
    fig.add_trace(
        trace=go.Bar(
            x=x_axis,
            y=df['cpd_already_payed_sum_y'],
            name='Сумма оплат',
            marker={'color': 'rgb(253, 211, 17)'},
            width=0.2,
            hovertemplate='<br>'.join(['%{y}']),
        ),
    )
    fig.add_trace(
        trace=go.Bar(
            x=x_axis,
            y=df['cpd_previous_period_debts_sum_y'],
            name='Дебиторская задолженность',
            marker={'color': 'rgb(239, 75, 46)'},
            width=0.2,
            hovertemplate='<br>'.join(['%{y}']),
        ),
    )
    fig.update_layout(
        # fixme year
        title='Динамика начислений, оплат и задолженности за ЖКУ в 2023 году, руб.',
        title_x=0.1,
        barmode='group',
        hovermode='x unified',
        hoverlabel={
            'bordercolor': 'white',
            'font_family': 'Helvetica',
            'font_size': 16,
        },
    )

    return fig


# fixme name
def get_figure4(df: pd.DataFrame, x_axis: tuple[str]) -> go.Figure:
    fig: go.Figure = px.line(
        x=x_axis,
        y=df['cr_total_accured_contib_sum_x'],
        # fixme year
        color=px.Constant('2022 год'),
        labels=dict(x='', y='', color='Год'),
    )

    fig.update_traces(
        line_color='rgb(176, 101, 194)',
        line_width=3,
        hovertemplate='<br>'.join(['Начислено %{y}']),
    )
    # fixme year
    fig.add_bar(x=x_axis, y=df['cr_total_accured_contib_sum_y'], name='2023 год')
    fig.update_traces(
        marker_color='rgb(61, 165, 226)',
        customdata=np.transpose(df['cr_total_accured_contib_sum_y']),
        hovertemplate='<br>'.join(['Начислено %{y}']),
    )
    fig.update_layout(
        title='Начисление взносов за капительный ремонт, руб.',
        title_x=0.5,
        hovermode='x unified',
        width=600,
        height=500,
        hoverlabel={
            'bordercolor': 'white',
            'font_family': 'Helvetica',
            'font_size': 16,
        },
    )

    return fig


# fixme name
def get_figure5(df: pd.DataFrame, x_axis: tuple[str]) -> go.Figure:
    fig: go.Figure = px.line(
        x=x_axis,
        y=df['cr_total_paid_contib_sum_x'],
        # fixme year
        color=px.Constant('2022 год'),
        labels=dict(x='', y='', color='Год'),
    )

    fig.update_traces(
        line_color='rgb(176, 101, 194)',
        line_width=3,
        hovertemplate='<br>'.join(['Оплачено %{y}']),
    )
    # fixme year
    fig.add_bar(x=x_axis, y=df['cr_total_paid_contib_sum_y'], name='2023 год')
    fig.update_traces(
        marker_color='rgb(61, 165, 226)',
        hovertemplate='<br>'.join(['Оплачено %{y}']),
    )
    fig.update_layout(
        title='Сбор взносов за капитальный ремонт, руб.',
        title_x=0.5,
        hovermode='x unified',
        width=600,
        height=500,
        hoverlabel={
            'bordercolor': 'white',
            'font_family': 'Helvetica',
            'font_size': 16,
        },
    )

    return fig


def get_sunburst(df: pd.DataFrame) -> go.Figure:
    fig: go.Figure = px.sunburst(
        data_frame=df,
        names='categories',
        parents='parent',
        values='value',
        hover_data={
            'parent': False,
        },
        custom_data=[
            df['categories'],
            make_human_readable_data(column=df['value'])
        ]
    )

    hovertemp: str = '<b>%{customdata[0]} - %{customdata[1]} руб.'

    fig.update_layout(
        # fixme year
        title=dict(
            text='Исполнение краткосрочных планов за 2023 год по видам работ',
            font=dict(size=30, family='RobotoCondensed-Regular', color='rgba(13, 31, 62, 0.74)'),
        ),
        title_x=0.5,
        hoverlabel={
            'font_size': 20,
            'font_family': 'Helvetica',
        },
        legend_orientation="h",
        height=900,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )
    fig.update_traces(hovertemplate=hovertemp)
    return fig


def make_human_readable_data(column: pd.Series) -> list[str]:
    return ['{:,}'.format(i).replace(',', ' ') for i in column]
