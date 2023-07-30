from dash import html, dcc


def map_layout():
    return html.Div(
        id='div_map',
        style={
            'visibility': 'hidden',
            'display': 'block',
        },
        children=dcc.Graph(
            id='map',
            config={
                'scrollZoom': False,
                'displayModeBar': False,
            },
        ),
    )
