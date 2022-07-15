import os
from datetime import datetime

from pendulum import date
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from carga import ingest_callable
from taxi_trip import transform
from apiWeather import weather
#---------------------------------

AIRFLOW_HOME = os.environ.get("AIRFLOW_HOME", "/opt/airflow/")

PG_HOST = 'mypostgres'
PG_USER = 'postgres'
PG_PASSWORD = 'postgres'
PG_PORT = '5432'
PG_DATABASE = 'ny_taxi'

#url = 'curl -sSL https://filesamples.com/samples/document/csv/sample4.csv'

local_workflow = DAG(
    "CargaIncrementalDag",
    schedule_interval="0 6 2 * *",
    start_date=datetime(2018, 1, 1),
    end_date = datetime(2018, 2, 1)
)

#URL_PREFIX = 'https://s3.amazonaws.com/nyc-tlc/trip+data'
URL_PREFIX = 'https://d37ci6vzurychx.cloudfront.net/trip-data'
URL_TEMPLATE = URL_PREFIX + '/yellow_tripdata_{{ execution_date.strftime(\'%Y-%m\') }}.parquet'
OUTPUT_FILE_TEMPLATE = AIRFLOW_HOME + '/output_{{ execution_date.strftime(\'%Y-%m\') }}.parquet'
TABLE_NAME_TEMPLATE = 'yellow_taxi_{{ execution_date.strftime(\'%Y_%m\') }}'
execution = '{execution_date}'
date_inicial = '2018-01-01'


with local_workflow:
    wget_task = BashOperator(
        task_id='wget',
        #bash_command=f'curl -sSL {url} > {OUTPUT_FILE_TEMPLATE}'
        bash_command=f'curl -sSL {URL_TEMPLATE} > {OUTPUT_FILE_TEMPLATE}'
    )

    ###########################
    weather_task = PythonOperator(
        task_id = 'Weather',
        python_callable = weather,
        op_kwargs = dict(
            actual_date = '2018-01-01',
            #directorio_Location = 'logs/taxi_zone_lookup.csv',
            #directorio_calendar = 'logs/calendar.csv',
            execution_date= execution
        ),
    )

    transform_task = PythonOperator(
        task_id = 'yellow_taxi',
        python_callable = transform,
        op_kwargs = dict(
            directorio_parquet = OUTPUT_FILE_TEMPLATE,
            directorio_Location = 'logs/taxi_zone_lookup.csv',
            directorio_calendar = 'logs/calendar.csv',
            execution_date= execution
        ),
    )

    wget_task >> weather_task >> transform_task 