from datetime import datetime
from airflow import DAG
from airflow.decorators import task

with DAG(
    dag_id="dag_task_api",
    start_date=datetime(2026, 1, 1),
    catchup=False,
) as dag:

    @task
    def extraer_facebook():
        return "Datos FB"

    @task
    def extraer_instagram():
        return "Datos IG"

    @task
    def extraer_tiktok():
        return "Datos TK"

    @task
    def consolidar_datos(fb, ig, tk):
        print(f"Consolidando: {fb}, {ig}, {tk}")

    # --- AQUÍ SE GENERA EL PARALELISMO ---
    # Al llamarlas de forma independiente, Airflow sabe que las tres pueden correr a la vez
    datos_fb = extraer_facebook()
    datos_ig = extraer_instagram()
    datos_tk = extraer_tiktok()

    # La tarea final "espera" a las tres en paralelo porque necesita todos los inputs
    consolidar_datos(fb=datos_fb, ig=datos_ig, tk=datos_tk)