from actions.datos import obtener_empleados, obtener_proyectos, obtener_horas_trabajadas
from actions.limpiar import (
    limpiar_empleados,
    limpiar_proyectos,
    limpiar_horas_trabajadas,
)
from actions.integraciones import (
    horas_trabajadas_join_empleados_join_proyectos,
    obtener_metricas_departamento,
    obtener_metricas_proyecto,
)
from actions.load import (
    guardar_empleados,
    guardar_proyectos,
    guardar_horas,
    guardar_analitico_horas,
    guardar_resumen_departamento,
    guardar_resumen_proyecto,
)
import pandas as pd


def main():
    df_empleados = obtener_empleados()
    df_proyectos = obtener_proyectos()
    df_horas_trabajadas = obtener_horas_trabajadas()

    df_empleados = limpiar_empleados(df_empleados)
    df_proyectos = limpiar_proyectos(df_proyectos)
    df_horas_trabajadas = limpiar_horas_trabajadas(df_horas_trabajadas)

    df_horas_trabajadas_empleados_proyectos, df_horas_trabajadas_huerfanas = (
        horas_trabajadas_join_empleados_join_proyectos(
            df_horas_trabajadas, df_empleados, df_proyectos
        )
    )

    df_metricas_departamento = obtener_metricas_departamento(
        df_horas_trabajadas_empleados_proyectos
    )
    df_metricas_proyecto = obtener_metricas_proyecto(
        df_horas_trabajadas_empleados_proyectos
    )

    # guardar_empleados(df_empleados)
    # guardar_proyectos(df_proyectos)
    # guardar_horas(df_horas_trabajadas)
    # guardar_analitico_horas(df_horas_trabajadas_empleados_proyectos)
    # guardar_resumen_departamento(df_metricas_departamento)
    # guardar_resumen_proyecto(df_metricas_proyecto)


    #1. ¿Qué departamento tiene el salario medio más alto?
    print(
        df_metricas_departamento[
            df_metricas_departamento["salario_medio"]
            == df_metricas_departamento["salario_medio"].max()
        ]
    )

    #2. ¿Cuáles son los 3 proyectos con mayor desviación de presupuesto (en %)?
    print(df_proyectos.sort_values("desviacion_pct", ascending=False).iloc[:3])

    #3. ¿Qué empleado ha registrado más horas totales en el año?
    df_empleados_horas = df_horas_trabajadas.groupby("empleado_id").agg(horas_totales=("horas_totales", "sum"))
    print(df_empleados_horas[df_empleados_horas["horas_totales"]==df_empleados_horas["horas_totales"].max()])

    #4. ¿Qué porcentaje de las horas totales son facturables?
    horas_totales = df_horas_trabajadas_empleados_proyectos["horas_totales"].sum()
    horas_facturables = df_horas_trabajadas_empleados_proyectos["horas_facturables"].sum()
    porcentaje_horas_facturaables = horas_facturables * 100 / horas_totales
    print(f'Porcentaje de horas facturables respecto a las totales: {porcentaje_horas_facturaables}%')

    #5. ¿Existe correlación entre la evaluación del empleado y sus horas extra?
    #print(df_horas_trabajadas_empleados_proyectos["empleado_id","evaluacion", "horas_extra"].groupby("empleado_id").corr())
    print(df_empleados.merge(df_horas_trabajadas, how="inner", on="empleado_id").groupby("empleado_id").agg(horas_Extra=("horas_extra", "sum"), evaluacion=("evaluacion", "first")).corr())
    


main()
