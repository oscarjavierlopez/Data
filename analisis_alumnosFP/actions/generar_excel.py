import pandas as pd
from datetime import datetime
from pathlib import Path

def guardar_excel(df_alumnos: pd.DataFrame):
    anio_actual = datetime.now().year
    carpeta = Path(f'{anio_actual}_alumnos_practicas')
    carpeta.mkdir(parents=True, exist_ok=True)
    fichero_excel = carpeta / f'{anio_actual}_alumnos_practicas_smart_track.xlsx'
    df_alumnos.to_excel(fichero_excel, index=False)
    print(f'fichero excel almacenado en {fichero_excel}')