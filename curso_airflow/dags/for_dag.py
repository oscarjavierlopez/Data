from datetime import datetime, timedelta
from airflow import DAG
from airflow.models.param import Param
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import logging


tasks = {1: "Task 1", 2: "Task 2", 3: "Task 3", 4: "Task 4"}


def create_task(message):
    def task_callable():
        logging.info(message)

    return task_callable


with DAG(
    dag_id="for_dag",
    start_date=datetime(2026, 6, 23),
    catchup=False,
    default_args={
        "retries": 2,
    },
    tags=["for_dag"],
):
    start = EmptyOperator(task_id="start")
    end = EmptyOperator(task_id="end")

    for key, value in tasks.items():
        message = tasks[key]
        task = PythonOperator(
            task_id=f"task_{key}", pool="my_pool", python_callable=create_task(message)
        )

    start >> task >> end
