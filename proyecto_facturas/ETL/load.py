import logging
import pandas as pd 
from pathlib import Path

logger = logging.getLogger(__name__)

def obtener_ruta_carpeta_silver():
    carpeta = Path("Data/silver")
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta

def obtener_ruta_carpeta_gold():
    carpeta = Path("Data/gold")
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta

def almacenar_df_silver(df: pd.DataFrame, nombre: str):
    carpeta = obtener_ruta_carpeta_silver()
    fichero = carpeta / f"{nombre}.csv"
    df.to_csv(fichero, index=False)
    logger.info("Almacenado %s", fichero)

def load_df_gold(df: pd.DataFrame, nombre: str):
    carpeta = obtener_ruta_carpeta_gold()

    # Almacenar fichero CSV
    fichero_csv = carpeta / f"{nombre}.csv"
    df.to_csv(fichero_csv, index=False)
    logger.info("Almacenado %s", fichero_csv)

    # Almacenar fichero xlsx
    fichero_excel = carpeta / f"{nombre}.xlsx"
    df.to_excel(fichero_excel, sheet_name="Hoja1", index=False)
    logger.info("Almacenado %s", fichero_excel)