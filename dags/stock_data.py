
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators import ApiToPostgresOperator
from datetime import datetime, timedelta

pg_conn_id='postgres_rds'
http_conn_id='http_iex'

tasks = [
    {'id':'get_stock_symbols', 'method':'GET', 'endpoint':'1.0/ref-data/symbols', 'destination_table':'staging.stock_symbols'},
    {'id':'get_tops', 'method':'GET', 'endpoint':'1.0/tops', 'destination_table':'staging.iex_tops'},
    {'id':'get_tops_last', 'method':'GET', 'endpoint':'1.0/tops/last', 'destination_table':'staging.iex_tops_last'},
    {'id':'get_stats_recent', 'method':'GET', 'endpoint':'1.0/stats/recent', 'destination_table':'staging.iex_stats_recent'},
]

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 8, 23),
    'email': ['internetdata@internetdata.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'catchup': False,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'stock_data',
    default_args=default_args,
    schedule_interval= '*/10 * * * *')

dummy_start = DummyOperator(
    task_id='start_load',
    dag=dag)

dummy_end = DummyOperator(
    task_id='end_load',
    dag=dag)

for task in tasks:
    api_to_pg_op = ApiToPostgresOperator(
         task_id=task['id'],
         method=task['method'],
         endpoint=task['endpoint'],
         http_conn_id=http_conn_id,
         pg_conn_id=pg_conn_id,
         destination_table=task['destination_table'],
         dag=dag
         )

    dummy_start >> api_to_pg_op >> dummy_end
