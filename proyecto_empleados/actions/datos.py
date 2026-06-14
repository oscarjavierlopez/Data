import pandas as pd
def obtener_empleados():
    return pd.read_csv('CSVs/empleados.csv', encoding='utf-8')

def obtener_proyectos():
    return pd.read_csv('CSVs/proyectos.csv', encoding='utf-8')

def obtener_horas_trabajadas():
    return pd.read_csv('CSVs/horas_trabajadas.csv', encoding='utf-8')
