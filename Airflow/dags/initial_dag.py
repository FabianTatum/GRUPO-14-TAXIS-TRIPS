import os
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from dimension_table import initial_tables
from carga import ingest_callable

PG_HOST = 'mypostgres'
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'
PG_PORT = '5432'
PG_DATABASE = 'ny_taxi'

tables_names_template , tables = initial_tables()
execution = '{execution_date}'

local_workflow = DAG(
    "InitialDag",
    schedule_interval=None,
    start_date=datetime(2018, 1, 1)
)


with local_workflow:

    ingest_task = PythonOperator(
        task_id="ingest",
        python_callable=ingest_callable,
        op_kwargs=dict(
            user=PG_USER,
            password=PG_PASSWORD,
            host=PG_HOST,
            port=PG_PORT,
            db=PG_DATABASE,
            table_name=tables_names_template,
            list_frames=tables,
            execution_date= execution
        ),
    )

    ingest_task