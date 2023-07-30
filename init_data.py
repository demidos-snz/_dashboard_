import pandas as pd
from clickhouse_driver import Client

from constants import MONTHS
from get_data import df_all_data_from_client, df_with_filter
from secrets_ import CONNECT_PARAMS
from settings import SUNBURST_CSV_PATH
from utils import (
    get_current_month_from_db, get_current_year_from_db, get_all_years_from_db,
    convert_month_from_dashboard_to_int, get_current_month_from_db_int,
)

# fixme move later
client: Client = Client(**CONNECT_PARAMS)

CURRENT_MONTH_FROM_DB: str = get_current_month_from_db(client=client)
CURRENT_MONTH_FROM_DB_INT: int = get_current_month_from_db_int(client=client)
ALL_YEARS_FROM_DB: list[int] = get_all_years_from_db(client=client)
CURRENT_YEAR_FROM_DB: int = get_current_year_from_db(years=ALL_YEARS_FROM_DB)

X_AXIS: tuple[str] = MONTHS[:CURRENT_MONTH_FROM_DB_INT]

df_all: pd.DataFrame = df_all_data_from_client(client=client)
df_grouped_by_regions_default: pd.DataFrame = df_with_filter(
    df=df_all,
    year=CURRENT_YEAR_FROM_DB,
    month=convert_month_from_dashboard_to_int(CURRENT_MONTH_FROM_DB),
)

client.disconnect()

DF_SUNBURST: pd.DataFrame = pd.read_csv(filepath_or_buffer=SUNBURST_CSV_PATH, encoding='cp1251', sep=';')
