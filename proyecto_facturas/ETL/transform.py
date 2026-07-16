import logging
import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def limpiar_dataframe_facturas(df_facturas: pd.DataFrame):
    logger.info("Iniciando limpieza del DataFrame")
    df_facturas["fecha_emision"] = pd.to_datetime(df_facturas["fecha_emision"])
    df_facturas["fecha_vencimiento"] = pd.to_datetime(df_facturas["fecha_vencimiento"])
    df_facturas["subtotal"] = df_facturas["subtotal"].str.replace(",", "").astype(float)
    df_facturas["iva_porcentaje"] = df_facturas["iva_porcentaje"].astype(int)
    df_facturas["iva_importe"] = (
        df_facturas["iva_importe"].str.replace(",", "").astype(float)
    )
    df_facturas["total"] = df_facturas["total"].str.replace(",", "").astype(float)
    logger.info("Limpieza completada — %d filas procesadas", len(df_facturas))

    return df_facturas


def enriquecer_dataframe_facturas(df_facturas: pd.DataFrame):
    # Columna dias_hasta_vencimiento
    df_facturas["dias_hasta_vencimiento"] = (
        df_facturas["fecha_vencimiento"] - df_facturas["fecha_emision"]
    ).dt.days
    
    # Columna dias_vencida para facturas con estado vencida
    df_facturas["dias_vencida"] = np.where(
        df_facturas["estado"].str.upper() == "VENCIDA".upper(),
        (pd.to_datetime("today").normalize() - df_facturas["fecha_vencimiento"]).dt.days,
        0,
    )

    # Columna tipo_cliente(S.L. o S.A.)
    pattern = r"(S\.[LA]\.)"
    df_facturas["tipo_cliente"] = df_facturas["cliente"].str.extract(pattern)

    # Columna tramo_importe(Pequeña, Media o Grande)
    condiciones = [(df_facturas["total"] > 0) & (df_facturas["total"] <= 5000),
                    (df_facturas["total"] > 5000) & (df_facturas["total"] <= 15000),
                      (df_facturas["total"] > 15000) & (df_facturas["total"] <= 50000)]
    opciones = ["Pequeña", "Media", "Grande"]
    df_facturas["tramo_importe"] = np.select(condiciones, opciones, default='')

    logger.info("Enriquecimiento completado — %d columnas en total", len(df_facturas.columns))

    return df_facturas
