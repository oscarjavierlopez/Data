import pandas as pd
from pathlib import Path


def obtener_ruta_carpeta_silver():
    carpeta = Path("data/silver")
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def obtener_ruta_carpeta_gold():
    carpeta = Path("data/gold")
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def load_df_silver(df: pd.DataFrame, nombre: str):
    carpeta = obtener_ruta_carpeta_silver()
    fichero = carpeta / f"{nombre}.csv"
    df.to_csv(fichero, index=False)
    print(f"Almacenado {fichero}")

def load_df_gold(df: pd.DataFrame, nombre: str):
    carpeta = obtener_ruta_carpeta_gold()
    fichero = carpeta / f"{nombre}.csv"
    df.to_csv(fichero)
    print(f"Almacenado {fichero}")
