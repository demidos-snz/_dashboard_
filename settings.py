import calendar
import locale
import os
import typing as t

import pandas as pd

locale.setlocale(locale.LC_TIME, 'ru_RU')
# locale.setlocale(locale.LC_TIME, 'ru_RU.UTF-8')
# morph = pymorphy2.MorphAnalyzer()

TITLE_APP: str = 'Мониторинг отрасли ЖКХ'

DEFAULT_DROPDOWN_REGIONS_VALUE: str = ''
DEFAULT_DROPDOWN_REGIONS_PLACEHOLDER: str = 'Российская Федерация'
REGIONS: tuple[str, ...] = (
    'г. Москва',
    'г. Санкт-Петербург',
    'г. Севастополь',
    'Алтайский край',
    'Амурская область',
    'Архангельская область',
    'Астраханская область',
    'Белгородская область',
    'Брянская область',
    'Владимирская область',
    'Волгоградская область',
    'Вологодская область',
    'Воронежская область',
    'Донецкая Народная республика',
    'Еврейская автономная область',
    'Забайкальский край',
    'Запорожская область',
    'Ивановская область',
    'Иркутская область',
    'Кабардино-Балкарская Республика',
    'Калининградская область',
    'Калужская область',
    'Камчатский край',
    'Кемеровская область',
    'Кировская область',
    'Костромская область',
    'Краснодарский край',
    'Красноярский край',
    'Курганская область',
    'Курская область',
    'Ленинградская область',
    'Липецкая область',
    'Луганская Народная республика',
    'Магаданская область',
    'Московская область',
    'Мурманская область',
    'Ненецкий автономный округ',
    'Нижегородская область',
    'Новгородская область',
    'Новосибирская область',
    'Омская область',
    'Оренбургская область',
    'Орловская область',
    'Пензенская область',
    'Пермский край',
    'Приморский край',
    'Псковская область',
    'Республика Адыгея',
    'Республика Алтай',
    'Республика Башкортостан',
    'Республика Бурятия',
    'Республика Дагестан',
    'Республика Ингушетия',
    'Республика Калмыкия',
    'Республика Карачаево-Черкесская',
    'Республика Карелия',
    'Республика Коми',
    'Республика Крым',
    'Республика Марий Эл',
    'Республика Мордовия',
    'Республика Саха (Якутия)',
    'Республика Северная Осетия - Алания',
    'Республика Татарстан',
    'Республика Тыва',
    'Республика Хакасия',
    'Ростовская область',
    'Рязанская область',
    'Самарская область',
    'Саратовская область',
    'Сахалинская область',
    'Свердловская область',
    'Смоленская область',
    'Ставропольский край',
    'Тамбовская область',
    'Тверская область',
    'Томская область',
    'Тульская область',
    'Тюменская область',
    'Удмуртская Республика',
    'Ульяновская область',
    'Хабаровский край',
    'Ханты-Мансийский автономный округ - Югра ',
    'Херсонская область',
    'Челябинская область',
    'Чеченская Республика',
    'Чувашская Республика - Чувашия',
    'Чукотский автономный округ',
    'Ямало-Ненецкий автономный округ',
    'Ярославская область',
)

FIELDS_NAMES_CPD: list = ['cpd_charged_sum', 'cpd_already_payed_sum', 'cpd_previous_period_debts_sum']
FIELDS_NAMES_CR: list = ['cr_total_accured_contib_sum', 'cr_total_paid_contib_sum', 'cr_debt_sum']
RADIO_ITEM_STATS_CATEGORY = ['\tплатежи за ЖКУ', '\tкапремонт']

ORG_ICON_PATH: str = os.path.normpath('assets/icons/org-icon.png')
MKD_ICON_PATH: str = os.path.normpath('assets/icons/mkd-icon.png')
JD_ICON_PATH: str = os.path.normpath('assets/icons/jd-icon.png')

NEW_TER: pd.DataFrame = pd.DataFrame(
    data={
        'region_code': [93, 94, 95, 96],
        'region_name': [
            'Донецкая Народная республика',
            'Луганская Народная республика',
            'Запорожская область',
            'Херсонская область',
        ],
        'cpd_charged_sum': [0, 0, 0, 0],
        'cpd_already_payed_sum': [0, 0, 0, 0],
        'cpd_previous_period_debts_sum': [0, 0, 0, 0],
        'cr_total_accured_contib_sum': [0, 0, 0, 0],
        'cr_total_paid_contib_sum': [0, 0, 0, 0],
        'cr_debt_sum': [0, 0, 0, 0],
    },
)

MONTHS: tuple[str] = tuple(month for month in list(calendar.month_name) if month)
# MONTHS = tuple(morph.parse(month)[0].normal_form.lower() for month in list(calendar.month_name) if month)

BUTTON_STYLE: dict[str, t.Any] = {
    'fontFamily': 'RobotoCondensed-Light',
    'margin-right': 20,
    'display': 'inline-block',
    'height': '36px',
    'color': '#555',
    'textAlign': 'center',
    'font-size': '11px',
    'line-height': '37px',
    'letterSpacing': '.1rem',
    'text-transform': 'uppercase',
    'font-weight': 'bold',
    'text-decoration': 'none',
    'white-space': 'nowrap',
    'background-color': 'transparent',
    'border-radius': '4px',
    'border': '1px solid #bbb',
    'cursor': 'pointer',
    'box-sizing': 'border-box',
}
