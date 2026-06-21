from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import logging


def print_hello():
    logging.info("Hello World")


with DAG(
    dag_id="hello_world_dag",
    start_date=datetime(2024, 6, 17),
    catchup=False,
    default_args={
        "retries": 2,
    },
    tags=["hello_world"],
):
    start = EmptyOperator(task_id="start")
    print_hello_task = PythonOperator(
        task_id="print_hello_task", python_callable=print_hello
    )
    end = EmptyOperator(task_id="end")

    start >> print_hello_task >> end
