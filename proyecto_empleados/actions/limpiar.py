import pandas as pd
import numpy as np

def limpiar_empleados(df_empleados:pd.DataFrame):
    df_empleados = df_empleados.drop_duplicates(['nombre', 'departamento', 'puesto', 'salario_bruto', 'fecha_alta', 'jornada', 'evaluacion', 'oficina'])
    df_empleados = df_empleados[(df_empleados['salario_bruto'] > 0) | (df_empleados['salario_bruto'].isnull())]
    df_empleados['departamento'] = df_empleados['departamento'].str.title()
    df_empleados['salario_bruto'] = df_empleados['salario_bruto'].fillna(df_empleados.groupby('departamento')['salario_bruto'].transform('median'))
    df_empleados['evaluacion'] = df_empleados['evaluacion'].fillna(df_empleados.groupby('departamento')['evaluacion'].transform('mean'))
    df_empleados['oficina'] = df_empleados['oficina'].fillna(df_empleados['oficina'].mode()[0])
    df_empleados['jornada'] = df_empleados['jornada'].fillna('completa')
    df_empleados['fecha_alta'] = df_empleados['fecha_alta'].astype('datetime64[ns]')
    df_empleados['antiguedad_anios'] = np.floor((pd.Timestamp.today() - df_empleados['fecha_alta']).dt.days / 365)
    
    return df_empleados

def limpiar_proyectos(df_proyectos:pd.DataFrame):
    df_proyectos = df_proyectos[(df_proyectos['presupuesto'] > 0) | (df_proyectos['presupuesto'].isnull())]
    df_proyectos['estado'] = df_proyectos['estado'].str.lower()
    df_proyectos['prioridad'] = df_proyectos['prioridad'].str.lower()
    df_proyectos['coste_real'] = df_proyectos['coste_real'].fillna(df_proyectos['coste_real'].median())
    df_proyectos['presupuesto'] = df_proyectos['presupuesto'].fillna(df_proyectos['presupuesto'].median())
    df_proyectos['prioridad'] = df_proyectos['prioridad'].fillna("media".lower())
    df_proyectos['fecha_inicio'] = df_proyectos['fecha_inicio'].astype('datetime64[ns]')
    df_proyectos['fecha_fin'] = df_proyectos['fecha_fin'].astype('datetime64[ns]')
    df_proyectos['desviacion_pct'] = (df_proyectos['coste_real'] - df_proyectos['presupuesto']) * 100 / df_proyectos['presupuesto']
    df_proyectos['en_curso'] = np.where((df_proyectos['estado'] == 'activo') | (df_proyectos['fecha_fin'].isna()), True, False)
    
    return df_proyectos

def limpiar_horas_trabajadas(df_horas_trabajadas:pd.DataFrame):
    df_horas_trabajadas = df_horas_trabajadas[((df_horas_trabajadas['horas_normales'] < 48) & (df_horas_trabajadas['horas_normales'] > 0)) | (df_horas_trabajadas['horas_normales'].isna())]
    df_horas_trabajadas['horas_extra'] = np.where((df_horas_trabajadas['horas_extra'] < 0) | (df_horas_trabajadas['horas_extra'].isna()), 0, df_horas_trabajadas['horas_extra'])
    df_horas_trabajadas['horas_normales'] = df_horas_trabajadas['horas_normales'].fillna(df_horas_trabajadas['horas_normales'].median())
    df_horas_trabajadas['tarea'] = df_horas_trabajadas['tarea'].fillna('Sin especificar')
    df_horas_trabajadas['horas_totales'] = df_horas_trabajadas['horas_normales'] + df_horas_trabajadas['horas_extra']
    return df_horas_trabajadas