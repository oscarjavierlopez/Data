from datetime import datetime, timedelta
from airflow import DAG
from airflow.models.param import Param
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.exceptions import AirflowFailException, AirflowSkipException
from airflow.utils.trigger_rule import TriggerRule
import logging

# Crea un formulario para ejecuciones manuales
params = {
    "Manual": Param(
        True,
        type="boolean",
        title="¿Es una ejecución manual?",
        description="Marca esta casilla si estás lanzando el proceso de forma manual para pruebas.",
    )
}


def first_task(**context):
    if context["params"]["Manual"]:
        raise AirflowFailException("Tarea fallida")
    
def second_task():
    logging.info("Hello world")


with DAG(
    dag_id="excepciones_dag",
    start_date=datetime(2024, 6, 17),
    catchup=False,
    default_args={
        "retries": 2,
    },
    tags=["hello_world"],
    params=params,
):
    start = EmptyOperator(task_id="start")
    first_task = PythonOperator(task_id="first_task", python_callable=first_task)
    second_task = PythonOperator(task_id="second_task", python_callable=second_task)
    end = EmptyOperator(task_id="end", trigger_rule=TriggerRule.ONE_SUCCESS)

    start >> [first_task, second_task] >> end
