
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators import ApiToPostgresOperator
from datetime import datetime, timedelta


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2018, 8, 1),
    'email': ['internetdata@internetdata.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 3,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG('stock_data', default_args=default_args)

dummy_start = DummyOperator(
    task_id='start_load',
    dag=dag)

dummy_end = DummyOperator(
    task_id='end_load',
    dag=dag)

get_stock_symbols = ApiToPostgresOperator(
    task_id='get_stock_symbols',
    method='GET',
    endpoint='1.0/ref-data/symbols',
    http_conn_id='http_iex',
    pg_conn_id='postgres_rds',
    destination_table='staging.stock_symbols',
    dag=dag
    )

get_tops = ApiToPostgresOperator(
    task_id='get_tops',
    method='GET',
    endpoint='1.0/tops',
    http_conn_id='http_iex',
    pg_conn_id='postgres_rds',
    destination_table='staging.iex_tops',
    dag=dag
)

dummy_start >> get_stock_symbols
get_stock_symbols >> dummy_end
dummy_start >> get_tops
get_tops >> dummy_end
