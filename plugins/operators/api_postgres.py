import json, codecs

from airflow.exceptions import AirflowException
from airflow.hooks.http_hook import HttpHook
from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class ApiToPostgresOperator(BaseOperator):

    ui_color = '#f4a460'

    @apply_defaults
    def __init__(self,
                 endpoint,
                 method='POST',
                 xcom_push=False,
                 http_conn_id='http_default',
                 pg_conn_id='postgres_rds',
                 destination_table='staging.table',
                 *args, **kwargs):

        super(ApiToPostgresOperator, self).__init__(*args, **kwargs)
        self.http_conn_id = http_conn_id
        self.method = method
        self.endpoint = endpoint
        self.xcom_push_flag = xcom_push
        self.pg_conn_id = pg_conn_id
        self.destination_table = destination_table

    def execute(self, context):

        http = HttpHook(self.method, http_conn_id=self.http_conn_id)

        self.log.info("Calling HTTP method")

        response = http.run(self.endpoint)

        json_resp = json.loads(response.content)

        self.log.info("Response received, saving results to Postgres")

        pg = PostgresHook(postgres_conn_id=self.pg_conn_id)

        tuples = []

        for res in json_resp:
            vals = list(res.values())
            str_vals = map(lambda x: str(x),vals)
            tuples.append(str_vals)

        self.log.info("Inserting " + str(len(tuples)) + " records to Postgres")

        pg.insert_rows(self.destination_table,tuples)
