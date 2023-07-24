import pandas as pd
from clickhouse_driver import Client

from settings import NEW_TER


def df_all_data_from_client(client: Client) -> pd.DataFrame:
    query: str = """
    select report_month,
        extract(year from report_month) as "year",
        extract(month from report_month) as "month",
        toInt32(region_code) as region_code,
        region_name,
        round(charged_sum) as charged_sum,
        --round(ch_total_sum) as ch_total_sum,
        --payment_document_count,
        --toInt64(objects_count) as objects_count,
        round(already_payed_sum) as already_payed_sum,
        round(previous_period_debts_sum) as previous_period_debts_sum
        --round(beginning_period_advance_sum) as beginning_period_advance_sum,
        --toInt64(objects_with_debts_count) as objects_with_debts_count
    from ois_visual.charges_payed_debts_by_regions t1
    SETTINGS
         max_bytes_before_external_group_by=20000000000, 
         max_memory_usage=40000000000;
    """
    df: pd.DataFrame = client.query_dataframe(query=query)
    df: pd.DataFrame = __convert_columns_type(df=df)
    return df


def __convert_columns_type(df: pd.DataFrame) -> pd.DataFrame:
    df['charged_sum'] = df['charged_sum'].astype('int64')
    df['already_payed_sum'] = df['already_payed_sum'].astype('int64')
    df['previous_period_debts_sum'] = df['previous_period_debts_sum'].astype('int64')
    df['report_month'] = pd.to_datetime(df['report_month'], format='%Y-%m-%d')
    df['year'] = df['report_month'].dt.strftime('%Y').astype('int')
    df['month'] = df['report_month'].dt.strftime('%m').astype('int')
    return df


def df_with_filter(df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    df: pd.DataFrame = df[(df['year'] == year) & (df['month'] == month)]
    df: pd.DataFrame = pd.concat(objs=[df, NEW_TER], ignore_index=True)
    return df
