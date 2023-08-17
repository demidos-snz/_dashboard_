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
    client.disconnect()
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


def df_sunburst(client: Client) -> pd.DataFrame:
    query: str = """
    with cte as (    
    select	t1.report_year,
        t2.region_name,
        t1.work_type, 
        t1.status,
        CONCAT(t1.work_type, '_', t1.status) as new_status,
        t1.work_sum 
    from ois_visual.capital_repair_work_by_regions t1
    join (select distinct region_code, region_name from ois_visual.stats_by_regions) t2 on t1.region_code = t2.region_code 
    where report_year = 2023
    AND status <> 'PAID'
    ORDER BY region_name, work_type, status DESC),
    cte2 as (
    SELECT cte.region_name, 
        cte.work_type,
        cte.new_status as categories,
        lagInFrame(cte.new_status) over (PARTITION by region_name, work_type order by region_name, work_type, status DESC) as parent,
        round(cte.work_sum) as value
    from cte
    order by region_name)
    select cte2.region_name,
    multiIf(work_type='BASEMENT_REPAIR', 'Ремонт крыш', 
            work_type='ELEVATOR_EQUIPMENT_REPAIR', 'Ремонт лифтов', 
            work_type='FACADE_REPAIR', 'Ремонт фасадов',
            work_type = 'FOUNDATION_REPAIR', 'Ремонт фундамента', 
            work_type='INNER_ENGINEERING_SYSTEMS_REPAIR', 'Ремонт внутридомовых систем',
            work_type='ROOF_REPAIR', 'Ремонт крыш',
            work_type='OTHER', 'Другие работы', NULL) as work_type,
    multiIf(categories='BASEMENT_REPAIR_ACCEPTED', 'Ремонт подвалов одобрен',
            categories='BASEMENT_REPAIR_CONTRACTED', 'Ремонт подвалов контракт',
            categories='BASEMENT_REPAIR_PLANNED', 'Ремонт подвалов план',
            categories='ELEVATOR_EQUIPMENT_REPAIR_ACCEPTED', 'Ремонт лифтов одобрен',
            categories='ELEVATOR_EQUIPMENT_REPAIR_CONTRACTED', 'Ремонт лифтов контракт',
            categories='ELEVATOR_EQUIPMENT_REPAIR_PLANNED',	'Ремонт лифтов план',
            categories='FACADE_REPAIR_ACCEPTED', 'Ремонт фасадов одобрен',
            categories='FACADE_REPAIR_CONTRACTED', 'Ремонт фасадов контракт',
            categories='FACADE_REPAIR_PLANNED', 'Ремонт фасадов план',
            categories='FOUNDATION_REPAIR_ACCEPTED', 'Ремонт фундамента одобрен',
            categories='FOUNDATION_REPAIR_CONTRACTED', 'Ремонт фундамента контракт',
            categories='FOUNDATION_REPAIR_PLANNED', 'Ремонт фундамента план',
            categories='INNER_ENGINEERING_SYSTEMS_REPAIR_ACCEPTED',	'Ремонт внутридомовых систем одобрен',
            categories='INNER_ENGINEERING_SYSTEMS_REPAIR_CONTRACTED', 'Ремонт внутридомовых систем контракт',
            categories='INNER_ENGINEERING_SYSTEMS_REPAIR_PLANNED', 'Ремонт внутридомовых систем план',
            categories='OTHER_ACCEPTED', 'Другие работы одобрены',
            categories='OTHER_CONTRACTED', 'Другие работы контракт',
            categories='OTHER_PLANNED',	'Другие работы план',
            categories='ROOF_REPAIR_ACCEPTED', 'Ремонт крыш одобрен',
            categories='ROOF_REPAIR_CONTRACTED', 'Ремонт крыш контракт',
            categories='ROOF_REPAIR_PLANNED', 'Ремонт крыш план', NULL) as categories,
    multiIf(parent ='BASEMENT_REPAIR_CONTRACTED', 'Ремонт подвалов контракт',
            parent ='BASEMENT_REPAIR_PLANNED', 'Ремонт подвалов план',
            parent ='ELEVATOR_EQUIPMENT_REPAIR_CONTRACTED',	'Ремонт лифтов контракт',
            parent ='ELEVATOR_EQUIPMENT_REPAIR_PLANNED', 'Ремонт лифтов план',
            parent ='FACADE_REPAIR_CONTRACTED',	'Ремонт фасадов контракт',
            parent ='FACADE_REPAIR_PLANNED', 'Ремонт фасадов план',
            parent ='FOUNDATION_REPAIR_CONTRACTED',	'Ремонт фундамента контракт',
            parent ='FOUNDATION_REPAIR_PLANNED', 'Ремонт фундамента план',
            parent ='INNER_ENGINEERING_SYSTEMS_REPAIR_CONTRACTED', 'Ремонт внутридомовых систем контракт',
            parent ='INNER_ENGINEERING_SYSTEMS_REPAIR_PLANNED',	'Ремонт внутридомовых систем план',
            parent ='OTHER_CONTRACTED', 'Другие работы контракт',
            parent ='OTHER_PLANNED', 'Другие работы план',
            parent ='ROOF_REPAIR_CONTRACTED', 'Ремонт крыш контракт',
            parent ='ROOF_REPAIR_PLANNED', 'Ремонт крыш план', '') as parent,
            value
    from cte2
    SETTINGS
         max_bytes_before_external_group_by=20000000000, 
         max_memory_usage=40000000000;
    """
    df: pd.DataFrame = client.query_dataframe(query=query)
    client.disconnect()
    return df
