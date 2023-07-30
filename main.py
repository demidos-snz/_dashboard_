from dash import html

from app import app
from callbacks.buttons.back_to_map import hide_charts_by_click_return_button
from callbacks.dropdown.dropdown_regions import hide_map_by_dropdown_regions_layout
from callbacks.map.click_by_map import hide_map_by_click_map_layout
from callbacks.buttons.update_map_data import update_map_by_button
from layouts.total_for_russia import div_total_for_russia
from layouts.filters import div_filters
from layouts.header import header
from layouts.modal_warning import modal_warning
from settings import BASE_LAYOUT_STYLE

LAYOUT: html.Div = html.Div(
    children=[
        modal_warning(),
        header(),
        div_total_for_russia(),

        # callbacks layouts
        hide_charts_by_click_return_button(),
        hide_map_by_dropdown_regions_layout(),
        hide_map_by_click_map_layout(),
        update_map_by_button(),

        div_filters(),
    ],
    style=BASE_LAYOUT_STYLE,
)


if __name__ == '__main__':
    app.layout = LAYOUT
    app.run(debug=True)
