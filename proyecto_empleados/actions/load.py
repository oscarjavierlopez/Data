import pandas as pd
from pathlib import Path


def obtener_ruta_carpeta_output():
    carpeta = Path("output")
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def guardar_empleados(df_empleados: pd.DataFrame):
    carpeta = obtener_ruta_carpeta_output()
    empleados_limpios_csv = carpeta / "emplados_limpios.csv"
    df_empleados.to_csv(empleados_limpios_csv, index=False)


def guardar_proyectos(df_proyectos: pd.DataFrame):
    carpeta = obtener_ruta_carpeta_output()
    proyectos_limpios_csv = carpeta / "proyectos_limpios.csv"
    df_proyectos.to_csv(proyectos_limpios_csv, index=False)


def guardar_horas(df_horas_trabajadas:pd.DataFrame):
    carpeta = obtener_ruta_carpeta_output()
    horas_limpias_csv = carpeta / "horas_limpias.csv"
    df_horas_trabajadas.to_csv(horas_limpias_csv, index=False)

def guardar_analitico_horas(df_horas_trabajadas_empleados_proyectos:pd.DataFrame):
    carpeta = obtener_ruta_carpeta_output()
    analitico_horas_csv = carpeta / "analitico_horas.csv"
    df_horas_trabajadas_empleados_proyectos.to_csv(analitico_horas_csv, index=False)

def guardar_resumen_departamento(df_metricas_departamento:pd.DataFrame):
    carpeta = obtener_ruta_carpeta_output()
    resumen_departamento_csv = carpeta / "resumen_departamento.csv"
    df_metricas_departamento.to_csv(resumen_departamento_csv)

def guardar_resumen_proyecto(df_metricas_proyecto:pd.DataFrame):
    carpeta = obtener_ruta_carpeta_output()
    resumen_proyecto_csv = carpeta / "resumen_proyecto.csv"
    df_metricas_proyecto.to_csv(resumen_proyecto_csv)