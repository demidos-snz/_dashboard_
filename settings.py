import pandas as pd


DEFAULT_REGION: str = ''
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

RADIO_ITEMS: dict[str, str] = {
    'accounts_count': 'Количество актуальных ЛС',
    'payment_documents_count': 'Количество размещенных платежных документов',
    'charges_sum': 'Всего начислено',
}
DEFAULT_RADIO_ITEM: str = 'charged_sum'

ORG_ICON_PATH: str = 'assets/icons/org-icon.png'
MKD_ICON_PATH: str = 'assets/icons/mkd-icon.png'
JD_ICON_PATH: str = 'assets/icons/jd-icon.png'

DATATABLE_HEADER_STYLE: dict[str, str] = {
    'backgroundColor': '#f2f5f8',
    'fontWeight': 'bold',
    'color': 'black',
    'textAlign': 'center',
    'fontFamily': 'RobotoCondensed-Light',
    'fontSize': '1.2rem',
}
DATATABLE_DATA_STYLE: dict[str, str] = {
    'textAlign': 'center',
    'color': 'black',
}

# fixme rename
COLUMNS: list[str] = [
    'region_code', 'charged_sum', 'ch_total_sum',
    'already_payed_sum', 'previous_period_debts_sum', 'beginning_period_advance_sum',
]
NEW_TER: pd.DataFrame = pd.DataFrame(
    data={
        # 'report_month': ['2023-05-01', '2023-05-01','2023-05-01','2023-05-01'],
        # 'year': [2023,2023,2023,2023],
        # 'month': [5, 5, 5, 5],
        'region_code': [93, 94, 95, 96],
        'region_name': [
            'Донецкая Народная республика',
            'Луганская Народная республика',
            'Запорожская область',
            'Херсонская область',
        ],
        'charged_sum': [0, 0, 0, 0],
        'already_payed_sum': [0, 0, 0, 0],
        'previous_period_debts_sum': [0, 0, 0, 0],
        # 'ch_total_sum': [0, 0, 0, 0],
        # 'oayment_document_count': [0, 0, 0, 0],
        # 'objects_count': [0, 0, 0, 0],
        # 'objects_count': [0, 0, 0, 0],
    }
)