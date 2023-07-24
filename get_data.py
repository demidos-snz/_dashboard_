import pandas as pd
from clickhouse_driver import Client

from secrets_ import CONNECT_PARAMS
from settings import NEW_TER


def get_data_from_client(query: str) -> pd.DataFrame:
    client: Client = Client(**CONNECT_PARAMS)
    df: pd.DataFrame = client.query_dataframe(query=query)
    df: pd.DataFrame = convert_columns_type(df=df)
    client.disconnect()
    return df


def get_df_with_filter(df: pd.DataFrame, year: int, month: int) -> pd.DataFrame:
    df: pd.DataFrame = df[(df['year'] == year) & (df['month'] == month)]
    df: pd.DataFrame = pd.concat(objs=[df, NEW_TER], ignore_index=True)
    return df


def convert_columns_type(df: pd.DataFrame) -> pd.DataFrame:
    df['charged_sum'] = df['charged_sum'].astype('int64')
    df['already_payed_sum'] = df['already_payed_sum'].astype('int64')
    df['previous_period_debts_sum'] = df['previous_period_debts_sum'].astype('int64')
    df['report_month'] = pd.to_datetime(df['report_month'], format='%Y-%m-%d')
    df['year'] = df['report_month'].dt.strftime('%Y').astype('int')
    df['month'] = df['report_month'].dt.strftime('%m').astype('int')
    return df


# def get_total_for_month(df):
#     stat_by_month = df.groupby(['year', 'month'])[['charged_sum', 'ch_total_sum', 'payment_document_count',
#                                                    'objects_count', 'already_payed_sum', 'previous_period_debts_sum',
#                                                    'beginning_period_advance_sum', 'objects_with_debts_count']] \
#         .sum().reset_index()
#     return stat_by_month


# def get_total_integer(df: pd.DataFrame, field_name: str) -> str:
#     total_sum: float = round(df[field_name].sum())
#     return '{:,}'.format(total_sum).replace(',', ' ')
#
#
# new_data = run_query(lsql=lsql)
# total_charged = get_total_integer(df=new_data, field_name='charged_sum')
# total = get_total_for_month(df=new_data)
# print(total)


# if __name__ == '__main__':
#     lsql = """
#     select report_month,
#         extract(year from report_month) as "year",
#         extract(month from report_month) as "month",
#         toInt32(region_code) as region_code,
#         region_name,
#         round(charged_sum) as charged_sum,
#         --round(ch_total_sum) as ch_total_sum,
#         --payment_document_count,
#         --toInt64(objects_count) as objects_count,
#         round(already_payed_sum) as already_payed_sum,
#         round(previous_period_debts_sum) as previous_period_debts_sum
#         --round(beginning_period_advance_sum) as beginning_period_advance_sum,
#         --toInt64(objects_with_debts_count) as objects_with_debts_count
#     from ois_visual.charges_payed_debts_by_regions t1
#     SETTINGS
#          max_bytes_before_external_group_by=20000000000,
#          max_memory_usage=40000000000;
#     """
#
#     df = get_data_from_client(query=lsql)
#     df = run_query(df=df)
