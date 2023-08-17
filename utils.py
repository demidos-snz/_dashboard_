import base64
import calendar
import locale
from time import strptime

import geojson
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from clickhouse_driver import Client
from dash import html

from get_data import df_sunburst
from secrets_ import CONNECT_PARAMS
from settings import RADIO_ITEM_STATS_CATEGORY

locale.setlocale(locale.LC_TIME, 'ru_RU')
# locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
# morph = pymorphy2.MorphAnalyzer()

# SUNBURST_CSV_PATH: str = os.path.normpath('sunburst.csv')
# DF_SUNBURST: pd.DataFrame = pd.read_csv(SUNBURST_CSV_PATH,
#                                         encoding='cp1251',
#                                         sep=';')
client: Client = Client(**CONNECT_PARAMS)
DF_SUNBURST = df_sunburst(client=client)


def get_cpd_total_integer(df: pd.DataFrame, field_name: str) -> str:
    total_sum: float = round(df[field_name].sum())
    return '{:,}'.format(total_sum).replace(',', ' ')


def get_cr_total_integer(df: pd.DataFrame, field_name: str, region: str) -> str:
    total_sum: float = round(df[field_name][df['region_name'] == region].max())
    return '{:,}'.format(total_sum).replace(',', ' ')


def get_geodata(path: str = 'result.geojson') -> geojson.FeatureCollection:
    with open(file=path, encoding='utf-8') as f:
        data = geojson.load(f)
    return data


geodata: geojson.FeatureCollection = get_geodata()


def b64_image(image_filename: str) -> str:
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


def make_human_readable_data(column: pd.Series) -> list[str]:
    return ['{:,}'.format(i).replace(',', ' ') for i in column]


def show_charts_with_region_selection(df: pd.DataFrame,
                                      region: str,
                                      x_axis: tuple[str],
                                      value: str,
                                      new_region_value: str) -> tuple[
    html.Button, dict[str, str],
    dict[str, str], dict[str, str],  dict[str, str],
    go.Figure,
    go.Figure,
    go.Figure,
    go.Figure,
    go.Figure,
    go.Figure,
    dict[str, str], dict[str, str],
    dict[str, str],
    str, dict[str, str],
    str
]:
    # fixme year
    df_2022 = df[(df['year'] == 2022) & (df['region_name'] == region)]
    df_2023 = df[(df['year'] == 2023) & (df['region_name'] == region)]
    df = df_2022.merge(df_2023, how='inner', on=['month', 'region_name'])

    fig1 = get_figure1(df=df, x_axis=x_axis)
    fig2 = get_figure2(df=df, x_axis=x_axis)
    fig3 = get_figure3(df=df, x_axis=x_axis)
    fig4 = get_figure4(df=df, x_axis=x_axis)
    fig5 = get_figure5(df=df, x_axis=x_axis)

    fig_sunburst: go.Figure = get_sunburst(df=get_region_data_for_sunburst(region=region))

    if value == RADIO_ITEM_STATS_CATEGORY[0]:
        return (
            html.Button(
                children='Вернуться на карту',
                id='button_back_to_map',
                className='button',
                n_clicks=0,
            ),
            {'display': 'block'},

            {'display': 'none'},
            {'display': 'none'},
            {'display': 'none'},

            fig1,
            fig2,
            fig3,
            fig4,
            fig5,
            fig_sunburst,

            {'display': 'block'},
            {'display': 'none'},

            {'display': 'none'},

            region,
            {'display': 'block'},
            new_region_value
        )
    else:
        return (
            html.Button(
                children='Вернуться на карту',
                id='button_back_to_map',
                className='button',
                n_clicks=0,
            ),
            {'display': 'block'},

            {'display': 'none'},
            {'display': 'none'},
            {'display': 'none'},

            fig1,
            fig2,
            fig3,
            fig4,
            fig5,
            fig_sunburst,

            {'display': 'none'},
            {'display': 'block'},

            {'display': 'none'},

            region,
            {'display': 'block'},
            new_region_value
        )


def get_map(df: pd.DataFrame, value: str) -> go.Figure:
    if value in ['cpd_previous_period_debts_sum', 'cr_debt_sum']:
        color_continuous_scale = [
            (0, 'rgb(186, 227, 242)'), (0, 'rgb(186, 227, 242)'),
            (0.0001, 'rgb(173, 211, 100)'), (0.15, 'rgb(173, 211, 100)'),
            (0.15, 'rgb(173, 211, 100)'), (0.4, 'rgb(173, 211, 100)'),
            (0.4, 'rgb(253, 211, 17)'), (0.6, 'rgb(253, 211, 17)'),
            (0.6, 'rgb(245, 153, 46)'), (0.8, 'rgb(245, 153, 46)'),
            (0.8, 'rgb(239, 75, 46)'), (1, 'rgb(239, 75, 46)'),
        ]
    else:
        color_continuous_scale = [
            (0, 'rgb(186, 227, 242)'), (0.00001, 'rgb(186, 227, 242)'),
            (0.00001, 'rgb(239, 75, 46)'), (0.0001, 'rgb(239, 75, 46)'),
            (0.0001, 'rgb(245, 153, 46)'), (0.1, 'rgb(245, 153, 46)'),
            (0.1, 'rgb(253, 211, 17)'), (0.2, 'rgb(253, 211, 17)'),
            (0.2, 'rgb(173, 211, 100)'), (1, 'rgb(173, 211, 100)'),
        ]
    if value.startswith('cpd'):
        custom_data = [df['region_name'],
                       make_human_readable_data(column=df['cpd_charged_sum']),
                       make_human_readable_data(column=df['cpd_already_payed_sum']),
                       make_human_readable_data(column=df['cpd_previous_period_debts_sum'])]
        hovertemp: str = '<b>%{customdata[0]}</b><br>'
        hovertemp += '<br><b>Собираемость платежей за ЖКУ</b><br>'
        hovertemp += '<br><b>%{customdata[1]}</b> - Начислено<br>'
        hovertemp += '<br><b>%{customdata[2]}</b> - Оплачено<br>'
        hovertemp += '<br><b>%{customdata[3]}</b> - Задолженность<br>'
    else:
        custom_data = [df['region_name'],
                       make_human_readable_data(column=df['cr_total_accured_contib_sum']),
                       make_human_readable_data(column=df['cr_total_paid_contib_sum']),
                       make_human_readable_data(column=df['cr_debt_sum'])]
        hovertemp: str = '<b>%{customdata[0]}</b><br>'
        hovertemp += '<br><b>Собираемость взносов на капремонт</b><br>'
        hovertemp += '<br><b>%{customdata[1]}</b> - Начислено<br>'
        hovertemp += '<br><b>%{customdata[2]}</b> - Оплачено<br>'
        hovertemp += '<br><b>%{customdata[3]}</b> - Задолженность<br>'

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
            'cr_total_accured_contib_sum': True,
            'cr_total_paid_contib_sum': True,
            'cr_debt_sum': True,
        },
        color_continuous_scale=color_continuous_scale,
        featureidkey='properties.cartodb_id',
        mapbox_style='white-bg',
        zoom=2,
        center={'lat': 69, 'lon': 105},
        labels={
            'cpd_charged_sum': '',
            'cpd_already_payed_sum': '',
            'cpd_previous_period_debts_sum': '',
            'cr_total_accured_contib_sum': '',
            'cr_total_paid_contib_sum': '',
            'cr_debt_sum': '',
        },
        custom_data=custom_data,
    )

    fig.update_traces(
        hovertemplate=hovertemp,
        marker_line_width=1,
        marker_line_color='white',
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        height=730,
        # clickmode='event+select',
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


# fixme name
def get_figure1(df: pd.DataFrame, x_axis: tuple[str]) -> go.Figure:
    fig = px.line(
        x=x_axis,
        y=df['cpd_charged_sum_x'],
        # fixme year
        color=px.Constant('2022 год'),
        labels=dict(x='', y='', color='Год'),
    )

    fig.update_traces(
        line_color='rgb(245, 153, 46)',
        line_width=3,
        hovertemplate='<br>'.join(['Начислено %{y:.0f} руб.']),
    )
    # fixme year
    fig.add_bar(x=x_axis, y=df['cpd_charged_sum_y'], name='2023 год')
    fig.update_traces(
        marker_color='rgb(173, 211, 100)',
        hovertemplate='<br>'.join(['Начислено %{y:.0f} руб.']),
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
    fig = px.line(
        x=x_axis,
        y=df['cpd_already_payed_sum_x'],
        # fixme year
        color=px.Constant('2022 год'),
        labels=dict(x='', y='', color='Год'),
    )

    fig.update_traces(
        line_color='rgb(245, 153, 46)',
        line_width=3,
        hovertemplate='<br>'.join(['Оплачено %{y:.0f} руб.']),
    )
    # fixme year
    fig.add_bar(x=x_axis, y=df['cpd_already_payed_sum_y'], name='2023 год')
    fig.update_traces(
        marker_color='rgb(173, 211, 100)',
        hovertemplate='<br>'.join(['Оплачено %{y:.0f} руб.']),
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
    fig = go.Figure()
    fig.add_trace(
        trace=go.Bar(
            x=x_axis,
            y=df['cpd_charged_sum_y'],
            name='Сумма начислений',
            marker={'color': 'rgb(173, 211, 100)'},
            width=0.2,
            hovertemplate='<br>'.join(['%{y:.0f} руб.']),
        ),
    )
    fig.add_trace(
        trace=go.Bar(
            x=x_axis,
            y=df['cpd_already_payed_sum_y'],
            name='Сумма оплат',
            marker={'color': 'rgb(253, 211, 17)'},
            width=0.2,
            hovertemplate='<br>'.join(['%{y:.0f} руб.']),
        ),
    )
    fig.add_trace(
        trace=go.Bar(
            x=x_axis,
            y=df['cpd_previous_period_debts_sum_y'],
            name='Дебиторская задолженность',
            marker={'color': 'rgb(239, 75, 46)'},
            width=0.2,
            hovertemplate='<br>'.join(['%{y:.0f} руб.']),
        ),
    )
    fig.update_layout(
        # fixme year
        title='Динамика начислений, оплат и задолженности за ЖКУ в 2023 году, руб.',
        title_x=0.5,
        barmode='group',
        hovermode='x unified',
        hoverlabel={
            'bordercolor': 'white',
            'font_family': 'Helvetica',
            'font_size': 16,
        },
    )
    return fig


def get_figure4(df: pd.DataFrame, x_axis: tuple[str]) -> go.Figure:
    fig = px.line(
        x=x_axis,
        y=df['cr_total_accured_contib_sum_x'],
        color=px.Constant('2022 год'),
        labels=dict(x='', y='', color='Год'),
    )

    fig.update_traces(
        line_color='rgb(176, 101, 194)',
        line_width=3,
        hovertemplate='<br>'.join(['Начислено %{y:.0f} руб.']),
    )
    fig.add_bar(x=x_axis, y=df['cr_total_accured_contib_sum_y'], name='2023 год')
    fig.update_traces(
        marker_color='rgb(61, 165, 226)',
        customdata=np.transpose(df['cr_total_accured_contib_sum_y']),
        hovertemplate='<br>'.join(['Начислено %{y:.0f} руб.']),
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


def get_figure5(df: pd.DataFrame, x_axis: tuple[str]) -> go.Figure:
    fig = px.line(
        x=x_axis,
        y=df['cr_total_paid_contib_sum_x'],
        color=px.Constant('2022 год'),
        labels=dict(x='', y='', color='Год'),
    )

    fig.update_traces(
        line_color='rgb(176, 101, 194)',
        line_width=3,
        hovertemplate='<br>'.join(['Оплачено %{y:.0f} руб.']),
    )
    fig.add_bar(x=x_axis, y=df['cr_total_paid_contib_sum_y'], name='2023 год')
    fig.update_traces(
        marker_color='rgb(61, 165, 226)',
        hovertemplate='<br>'.join(['Оплачено %{y:.0f} руб.']),
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
    fig = px.sunburst(
        data_frame=df,
        names='categories',
        parents='parent',
        values='value',
        branchvalues='remainder',
        custom_data=[
            df['categories'],
            make_human_readable_data(column=df['value'])
        ],
    )

    hovertemp: str = '<b>%{customdata[0]} - %{customdata[1]} руб.'

    fig.update_layout(
        title=dict(
            text='Исполнение краткосрочных планов за 2023 год по видам работ',
            font=dict(size=25, family='RobotoCondensed-Regular', color='rgba(13, 31, 62, 0.74)'),
        ),
        title_x=0.5,
        hoverlabel={
            'font_size': 20,
            'font_family': 'Helvetica',
        },
        legend_orientation="h",
        height=900,
        # uniformtext=dict(minsize=14, mode='hide')
    )
    fig.update_traces(
        hovertemplate=hovertemp,
        marker={'line': {'width': 2}},
    )
    return fig


def get_current_month_from_db(client: Client) -> str:
    month: int = get_current_month_from_db_int(client=client)
    return calendar.month_name[month]
    # return morph.parse(calendar.month_name[month])[0].normal_form.lower()


def get_current_month_from_db_int(client: Client) -> int:
    for row in client.execute(query="""
    select extract(month from max(report_month)) as month
    from ois_visual.stats_by_regions t1
    """):
        return row[0]


def get_all_years_from_db(client: Client) -> list[int]:
    return [tuple_year[0] for tuple_year in client.execute(query="""
    select distinct(extract(year from (report_month))) as year
    from ois_visual.stats_by_regions t1
    """)]


def get_current_year_from_db(years: list[int]) -> int:
    return sorted(years, reverse=True)[0]


def convert_month_from_dashboard_to_int(month: str) -> int:
    return strptime(month, '%B').tm_mon
    # monthes_list = ['январь', 'февраль', 'март', 'апрель', 'май', 'июнь', 'июль',
    #                 'август', 'сентябрь', 'октябрь', 'ноябрь', 'декабрь']
    # return monthes_list.index(month) + 1


def get_region_data_for_sunburst(region: str) -> pd.DataFrame:
    return DF_SUNBURST[DF_SUNBURST['region_name'] == region]
