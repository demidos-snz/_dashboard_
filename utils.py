import base64
import typing as t

import geojson
import pandas as pd

from settings import DEFAULT_REGION


# fixme path
def get_df(path: str = 'начисления_v2.csv') -> pd.DataFrame:
    df = pd.read_csv(
        filepath_or_buffer=path,
        encoding='cp1251',
        sep=';',
        on_bad_lines='skip',
        low_memory=False,
    )
    df = df.fillna(0)
    df['payment_documents_count'] = df['payment_documents_count'].astype('int64')
    df['charges_sum'] = df['charges_sum'].astype('float')
    return df


def get_df_grouped_by_regions(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby(['year', 'month', 'region', 'id']).agg({
        'accounts_count': 'sum',
        'payment_documents_count': 'sum',
        'charges_sum': 'sum',
    }).reset_index()


def get_total_integer(df: pd.DataFrame, field_name: str) -> str:
    total_sum: float = round(df[field_name].sum())
    return '{:,}'.format(total_sum).replace(',', ' ')


def get_organizations_by_region(df: pd.DataFrame, region: str) -> list[dict[str, t.Any]]:
    return df[
        [
            'region', 'organization_name', 'inn',
            'accounts_count', 'payment_documents_count', 'charges_sum',
        ]
    ][
        df['region'] == region
    ].sort_values(ascending=False, by='accounts_count').head(10).to_dict('records')


def get_region_data(df: pd.DataFrame, region: str = DEFAULT_REGION) -> list[dict[str, t.Any]]:
    df_grouped_by_regions = get_df_grouped_by_regions(df=df)

    df_grouped_by_regions = df_grouped_by_regions[
        [
            'region',
            'accounts_count',
            'payment_documents_count',
            'charges_sum',
        ]
    ].sort_values(ascending=False, by='accounts_count')
    return df_grouped_by_regions[df_grouped_by_regions['region'] == region].to_dict('records')


# fixme path
def get_geodata(path: str = 'result.geojson') -> geojson.FeatureCollection:
    with open(file=path, encoding='utf-8') as f:
        data = geojson.load(f)
    return data


def b64_image(image_filename: str) -> str:
    with open(image_filename, 'rb') as f:
        image = f.read()
    return 'data:image/png;base64,' + base64.b64encode(image).decode('utf-8')
