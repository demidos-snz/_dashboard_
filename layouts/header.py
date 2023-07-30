from dash import html


def header() -> html.Div:
    return html.Div(
        children=[
            html.H1(
                id='label_dashboard',
                children='Мониторинг отрасли ЖКХ',
                style={
                    'fontSize': '2.5rem',
                    'fontFamily': 'RobotoCondensed-Regular',
                },
            ),

            html.Hr(),
        ],
    )
