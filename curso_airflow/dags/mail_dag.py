from datetime import datetime, timedelta
from airflow import DAG
from airflow.models.param import Param
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.email import EmailOperator
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
    logging.info(context["params"])


with DAG(
    dag_id="email_dag",
    start_date=datetime(2024, 6, 17),
    catchup=False,
    default_args={
        "retries": 2,
    },
    tags=["email_dag"],
    params=params,
):
    start = EmptyOperator(task_id="start")
    first_task = PythonOperator(task_id="first_task", python_callable=first_task)
    enviar_correo = EmailOperator(
        task_id="enviar_correo",
        conn_id="gmail_conexion",
        to="oscarljavierlopez@gmail.com",
        subject="Notificación de DAG ejecutado",
        html_content="""
        <h3>Reporte de Ejecución</h3>
        <p>La tarea se ha ejecutado correctamente</p>
        """,
    )
    end = EmptyOperator(task_id="end")

    start >> first_task >> enviar_correo >> end
