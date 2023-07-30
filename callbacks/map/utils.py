import geojson
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from callbacks.utils import make_human_readable_data
from settings import GEOJSON_PATH

HOVERTEMPLATE: str = (
    '<b>%{customdata[1]}</b><br>'
    '<br><b>%{customdata[2]}</b> - Начислено<br>'
    '<br><b>%{customdata[3]}</b> - Оплачено<br>'
    '<br><b>%{customdata[4]}</b> - Задолженность<br>'
)


def get_geodata(path: str = GEOJSON_PATH) -> geojson.FeatureCollection:
    with open(file=path, encoding='utf-8') as f:
        data: geojson.FeatureCollection = geojson.load(f)
    return data


def get_map(df: pd.DataFrame, value: str) -> go.Figure:
    fig: go.Figure = px.choropleth_mapbox(
        data_frame=df,
        geojson=get_geodata(),
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

    fig.update_traces(
        hovertemplate=HOVERTEMPLATE,
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
