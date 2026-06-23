from datetime import datetime, timedelta
from airflow import DAG
from airflow.models.param import Param
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
import logging


def first_task():
    logging.info("task 1")


def second_task():
    logging.info("task 2")


def third_task():
    logging.info("task 3")


with DAG(
    dag_id="pool_dag",
    start_date=datetime(2024, 6, 17),
    catchup=False,
    default_args={
        "retries": 2,
    },
    tags=["dag_pool"],
):
    start = EmptyOperator(task_id="start")
    first_task = PythonOperator(
        task_id="first_task", python_callable=first_task, pool="my_pool"
    )
    second_task = PythonOperator(
        task_id="second_task", python_callable=second_task, pool="my_pool"
    )
    third_task = PythonOperator(
        task_id="third_task", python_callable=third_task, pool="my_pool"
    )
    end = EmptyOperator(task_id="end")

    start >> [first_task, second_task, third_task] >> end
