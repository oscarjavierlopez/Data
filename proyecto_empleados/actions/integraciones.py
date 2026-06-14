import pandas as pd
import numpy as np


def horas_trabajadas_join_empleados_join_proyectos(
    df_horas_trabajadas: pd.DataFrame,
    df_empleados: pd.DataFrame,
    df_proyectos: pd.DataFrame,
):
    df_horas_trabajadas_empleados_proyectos = df_horas_trabajadas.merge(
        df_empleados[
            ["empleado_id", "nombre", "departamento", "salario_bruto", "evaluacion"]
        ],
        how="left",
        on="empleado_id",
    ).merge(
        df_proyectos[["proyecto_id", "cliente", "estado", "desviacion_pct"]], how="left", on="proyecto_id"
    )
    df_horas_trabajadas_empleados_proyectos = (
        df_horas_trabajadas_empleados_proyectos.rename(
            columns={"nombre": "nombre_empleado"}
        )
    )

    # df en el que aparecerán los registros sin empleado o proyecto
    df_horas_trabajadas_huerfanas = df_horas_trabajadas_empleados_proyectos[
        (df_horas_trabajadas_empleados_proyectos["nombre_empleado"].isna())
        | (df_horas_trabajadas_empleados_proyectos["cliente"].isna())
    ]

    # Eliminamos los registros de df_horas_trabajadas_huerfanas
    df_horas_trabajadas_empleados_proyectos = df_horas_trabajadas_empleados_proyectos[
        ~df_horas_trabajadas_empleados_proyectos["nombre_empleado"].isna()
    ]

    df_horas_trabajadas_empleados_proyectos['coste_horas'] = df_horas_trabajadas_empleados_proyectos['horas_totales'] * df_horas_trabajadas_empleados_proyectos['salario_bruto'] / 1800

    return [df_horas_trabajadas_empleados_proyectos, df_horas_trabajadas_huerfanas]


def obtener_metricas_departamento(
    df_horas_trabajadas_join_empleados_join_proyectos: pd.DataFrame,
):

    df_horas_trabajadas_join_empleados_join_proyectos["horas_facturables"] = np.where(
        df_horas_trabajadas_join_empleados_join_proyectos["facturables"],
        df_horas_trabajadas_join_empleados_join_proyectos["horas_totales"],
        0,
    )

    df_departamento = df_horas_trabajadas_join_empleados_join_proyectos.groupby(
        "departamento"
    ).agg(
        total_empleados=("empleado_id", "count"),
        salario_medio=("salario_bruto", "mean"),
        evaluacion_media=("evaluacion", "mean"),
        horas_totales_trabajadas=("horas_totales", "sum"),
        horas_facturables_totales=("horas_facturables", "sum"),
    )

    return df_departamento


def obtener_metricas_proyecto(
    df_horas_trabajadas_join_empleados_join_proyectos: pd.DataFrame,
):
    df_proyecto = df_horas_trabajadas_join_empleados_join_proyectos.groupby('proyecto_id').agg(
        total_horas_registradas=("horas_totales", "sum"),
        num_empleados=("empleado_id", "count"),
        coste_horas_totales=("coste_horas", "sum"),
        desviacion_pct=("desviacion_pct", "first")
    )

    return df_proyecto
