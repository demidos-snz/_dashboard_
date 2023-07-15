import typing as t

import geojson
import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Output, Input
from dash.dash_table import DataTable as Table
from plotly.graph_objs import Figure

from settings import DEFAULT_REGION, REGIONS, RADIO_ITEMS, DEFAULT_RADIO_ITEM, STYLE_FOR_LABEL
from utils import get_df, get_geodata, get_df_grouped_by_regions, get_organizations_by_region, get_region_data

app = Dash(__name__)


app.layout = html.Div(
    children=[

        html.H1(
            id='label_dashboard',
            className='row',
            children='Мониторинг отрасли ЖКХ',
            style={
                'textAlign': 'center',
                'fontSize': 25,
                'font-family': 'Arial Black',
            },
        ),

        html.Hr(),

        html.Div(
            [
                dcc.Dropdown(
                    id='dropdown_regions',
                    options=REGIONS,
                    value=DEFAULT_REGION,
                    style={
                        'width': '300px',
                        'margin-right': 20,
                    },
                ),
            ],
            id='div_regions_list',
            style={
                'display': 'flex',
                'justify-content': 'right',
            },
        ),

        # fixme DELETE in future
        html.Div(
            [
                dcc.RadioItems(
                    id='radio_items',
                    options=RADIO_ITEMS,
                    value=DEFAULT_RADIO_ITEM,
                    style={
                        'width': '300px',
                        'margin-right': 20,
                    },
                ),
            ],
            id='div_radio_items',
            style={
                'display': 'flex',
                'justify-content': 'right',
            },
        ),

        html.Div(
            [
                dcc.Graph(
                    id='map',
                    config={
                        'scrollZoom': False,
                        'displayModeBar': False,
                    },
                ),
            ],
            id='div_map',
            style={
                'margin': 50,
                'width': '1500px'
            },
        ),

        html.H3(
            id='label_statistic_for_region',
            children='Статистика по региону:',
            style=STYLE_FOR_LABEL,
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
            style=STYLE_FOR_LABEL,
        ),


        html.Div(
            id='div_statistics_on_provider_of_region',
            style={
                'margin': 20,
            },
        ),

    ],
)


@app.callback(
    Output(component_id='map', component_property='figure'),
    Input(component_id='radio_items', component_property='value'),
)
def display_map(value: str) -> Figure:
    fig = px.choropleth_mapbox(
        data_frame=df_grouped_by_regions,
        geojson=geodata,
        locations=df_grouped_by_regions.id,
        color=value,
        hover_name=df_grouped_by_regions.region,
        hover_data={
            'id': False,
        },
        color_continuous_scale=[
            (0, 'rgb(186, 227, 242)'),
            (0.0001, 'rgb(239, 75, 46)'),
            (0.1, 'rgb(245, 153, 46)'),
            (0.2, 'rgb(253, 211, 17)'),
            (1, 'rgb(174, 209, 54)'),
        ],
        featureidkey='properties.cartodb_id',
        mapbox_style='white-bg',
        zoom=2,
        center={'lat': 71, 'lon': 105},
        labels=RADIO_ITEMS,
    )
    fig.update_layout(
        height=790,
        width=1215,
        hoverlabel={
            'bgcolor': 'white',
        },
    )
    return fig


@app.callback(
    [
        Output(component_id='div_statistic_for_region', component_property='children'),
        Output(component_id='div_statistics_on_provider_of_region', component_property='children'),
        Output(component_id='dropdown_regions', component_property='value'),
    ],
    Input(component_id='map', component_property='clickData'),
)
def update_tables_with_statistics_by_region(clickData: t.Optional[dict[str, list]]) -> tuple[Table, Table, str]:
    region: str = DEFAULT_REGION if clickData is None else clickData['points'][0]['hovertext']

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
        Output(component_id='div_statistic_for_region', component_property='children', allow_duplicate=True),
        Output(
            component_id='div_statistics_on_provider_of_region',
            component_property='children',
            allow_duplicate=True,
        ),
    ],
    [
        Input(component_id='dropdown_regions', component_property='value'),
    ],
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
    geodata: geojson.FeatureCollection = get_geodata()

    app.run(debug=True)
