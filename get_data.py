import pandas as pd
from clickhouse_driver import Client

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
    },
)


def df_all_data_from_client(client: Client) -> pd.DataFrame:
    query: str = """
    select report_month,
        extract(year from report_month) as "year",
        extract(month from report_month) as "month",
        toInt32(region_code) as region_code,
        region_name,
        round(cpd_charged_sum) as cpd_charged_sum,
        round(cpd_already_payed_sum) as cpd_already_payed_sum,
        round(cpd_previous_period_debts_sum) as cpd_previous_period_debts_sum,
        round(cr_total_accured_contib_sum) as cr_total_accured_contib_sum,
        round(cr_total_paid_contib_sum) as cr_total_paid_contib_sum,
        round(cr_debt_sum) as cr_debt_sum
    from ois_visual.stats_by_regions t1
    SETTINGS
         max_bytes_before_external_group_by=20000000000, 
         max_memory_usage=40000000000;
    """
    df: pd.DataFrame = client.query_dataframe(query=query)
    df: pd.DataFrame = __convert_columns_type(df=df)
    return df


def __convert_columns_type(df: pd.DataFrame) -> pd.DataFrame:
    df['cpd_charged_sum'] = df['cpd_charged_sum'].astype('int64')
    df['cpd_already_payed_sum'] = df['cpd_already_payed_sum'].astype('int64')
    df['cpd_previous_period_debts_sum'] = df['cpd_previous_period_debts_sum'].astype('int64')
    df['cr_total_accured_contib_sum'] = df['cr_total_accured_contib_sum'].astype('int64')
    df['cr_total_paid_contib_sum'] = df['cr_total_paid_contib_sum'].astype('int64')
    df['cr_debt_sum'] = df['cr_debt_sum'].astype('int64')
    df['report_month'] = pd.to_datetime(df['report_month'], format='%Y-%m-%d')
    df['year'] = df['report_month'].dt.strftime('%Y').astype('int')
    df['month'] = df['report_month'].dt.strftime('%m').astype('int')
    return df


def df_with_filter(df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    df: pd.DataFrame = df[(df['year'] == year) & (df['month'] == month)]
    df: pd.DataFrame = pd.concat(objs=[df, NEW_TER], ignore_index=True)
    return df
