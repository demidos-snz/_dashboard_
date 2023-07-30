from dash import html
import dash_bootstrap_components as dbc


def modal_warning():
    return html.Div(
        children=[
            dbc.Modal(
                id='modal_backdrop',
                is_open=False,
                children=[
                    dbc.ModalHeader(dbc.ModalTitle('Предупреждение!'), close_button=True),
                    dbc.ModalBody(children='Данные за выбранный период отсутствуют!'),
                ],
            ),
        ],
    )

