import base64
import typing as t
import calendar
from time import strptime

import geojson
import pandas as pd
from clickhouse_driver import Client
from dash import html
from dash.dash_table import DataTable

from settings import DEFAULT_REGION, DATATABLE_DATA_STYLE, DATATABLE_HEADER_STYLE


# fixme path
def get_df(path: str = 'начисления_v2.csv') -> pd.DataFrame:
    df: pd.DataFrame = pd.read_csv(
        filepath_or_buffer=path,
        encoding='cp1251',
        sep=';',
        # on_bad_lines='skip',
        low_memory=False,
    )
    df: pd.DataFrame = df.fillna(0)
    df['payment_documents_count']: pd.Series = df['payment_documents_count'].astype('int64')
    df['charges_sum']: pd.Series = df['charges_sum'].astype('float')
    return df


def get_df_grouped_by_regions_start(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(['year', 'month', 'region', 'id']).agg({
        'accounts_count': 'sum',
        'payment_documents_count': 'sum',
        'charges_sum': 'sum',
    }).reset_index()
    # fixme new version
    # return df.groupby(['year', 'month', 'region_name', 'region_code']).agg({
    #     'charged_sum': 'sum',
    #     'already_payed_sum': 'sum',
    #     'previous_period_debts_sum': 'sum',
    # }).reset_index()


def get_total_integer(df: pd.DataFrame, field_name: str) -> str:
    total_sum: float = round(df[field_name].sum())
    return '{:,}'.format(total_sum).replace(',', ' ')


def get_organizations_by_region(df: pd.DataFrame, region: str) -> list[dict[str, t.Any]]:
    df: pd.DataFrame = df[[
        'region', 'organization_name', 'inn',
        'accounts_count', 'payment_documents_count', 'charges_sum'
    ]][df['region'] == region].sort_values(ascending=False, by='accounts_count').head(n=10)

    df.columns: pd.Index = pd.Index(data=[
        'Регион', 'Наименование организации', 'ИНН',
        'Количество лицевых счетов', 'Количество платежных документов', 'Итого начислено к оплате',
    ])
    return df.to_dict('records')


def get_region_data(df: pd.DataFrame, region: str = DEFAULT_REGION) -> list[dict[str, t.Any]]:
    df_grouped_by_regions: pd.DataFrame = get_df_grouped_by_regions_start(df=df)

    df_grouped_by_regions: pd.DataFrame = df_grouped_by_regions[
        [
            'region_name',
            'charged_sum',
            'already_payed_sum',
            'previous_period_debts_sum',
        ]
    ].sort_values(ascending=False, by='accounts_count')

    df_grouped_by_regions.columns: pd.Index = pd.Index(data=[
        'Регион',
        'Начислено',
        'Оплачено',
        'Задолженность',
    ])
    return df_grouped_by_regions[df_grouped_by_regions['Регион'] == region].to_dict('records')


# fixme path
def get_geodata(path: str = 'result.geojson') -> geojson.FeatureCollection:
    with open(file=path, encoding='utf-8') as f:
        data = geojson.load(f)
    return data


def b64_image(image_filename: str) -> str:
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')


# fixme naming + args df
def ggg(df: pd.DataFrame, region: str) -> tuple[
    html.Button, dict[str, str], DataTable,
    DataTable, dict[str, str], dict[str, str],
    dict[str, str], dict[str, str]
]:
    return (
        html.Button(
            children='Вернуться на карту',
            id='button_back_to_map',
            n_clicks=0,
            style={'fontFamily': 'RobotoCondensed-Light'},
        ),
        {'display': 'block'},
        DataTable(
            id='table_statistic_for_region',
            data=get_region_data(region=region, df=df),
            page_size=10,
            style_header=DATATABLE_HEADER_STYLE,
            style_data=DATATABLE_DATA_STYLE,
        ),
        DataTable(
            id='table_statistics_on_provider_of_region',
            data=get_organizations_by_region(region=region, df=df),
            page_size=10,
            style_header=DATATABLE_HEADER_STYLE,
            style_data=DATATABLE_DATA_STYLE,
        ),
        {'display': 'none'},
        {'display': 'none'},
        {'display': 'none'},
        {'display': 'block'},
        # {'display': 'block'},
    )


def get_current_month_from_db(client: Client) -> str:
    month: int = get_current_month_from_db_int(client=client)
    return calendar.month_name[month].lower()


def get_current_month_from_db_int(client: Client) -> int:
    for row in client.execute(query="""
    select extract(month from max(report_month)) as month
    from ois_visual.charges_payed_debts_by_regions t1
    """):
        return row[0]


def get_all_years_from_db(client: Client) -> list[int]:
    return [tuple_year[0] for tuple_year in client.execute(query="""
    select distinct(extract(year from (report_month))) as year
    from ois_visual.charges_payed_debts_by_regions t1
    """)]


def get_current_year_from_db(years: list[int]) -> int:
    return sorted(years, reverse=True)[0]


def convert_month_from_dashboard_to_int(month: str) -> int:
    return strptime(month, '%B').tm_mon
