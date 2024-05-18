import json
from airflow.hooks.http_hook import HttpHook
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator
from datetime import datetime, timedelta


def extract_data_from_api(execution_date, **kwargs):
    http_hook = HttpHook(method='POST', http_conn_id='http_job_1')
    headers = {"Content-Type": "application/json"}

    # Dynamically create the data payload with the execution date
    data = {
        "date": execution_date.strftime("%Y-%m-%d"),  # Formatting the date as a string
        "raw_dir": "/home/dima_study/homework-assignments/lesson_02/file_storage/raw"  # Your static raw_dir path
    }

    # Make the HTTP POST request
    response = http_hook.run(endpoint='', headers=headers, data=json.dumps(data))
    print(response.text)  # Print the response body to check what was returned

def convert_to_avro():
    http_hook = HttpHook(method='POST', http_conn_id='http_job_2')
    headers = {"Content-Type": "application/json"}

    data = {
        "raw_dir": "/home/dima_study/homework-assignments/lesson_02/file_storage/raw",  # Your static raw_dir path
        "stg_dir": "/home/dima_study/homework-assignments/lesson_02/file_storage/stg"
    }

    response = http_hook.run(endpoint='', headers=headers, data=json.dumps(data))
    print(response.text)  # Print the response body to check what was returned

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 0,
    'retry_delay': timedelta(minutes=5),
    'start_date': datetime(2022, 8, 9),
}

with DAG(
        dag_id='process_sales',
        default_args=default_args,
        schedule_interval='0 1 * * *',
        start_date=datetime(2022, 8, 9),
        catchup=True,
        max_active_runs=1
) as dag:
    start = DummyOperator(task_id='start')

    extract_data_task = PythonOperator(
        task_id='extract_data_task',
        python_callable=extract_data_from_api,
        provide_context=True  # Ensures that context variables like `execution_date` are passed to the function
    )

    convert_to_avro_task = PythonOperator(
        task_id='convert_to_avro_task',
        python_callable=convert_to_avro,
        provide_context=True  # Ensures that context variables like `execution_date` are passed to the function
    )

    start >> extract_data_task >> convert_to_avro_task