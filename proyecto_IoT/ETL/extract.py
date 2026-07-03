import pandas as pd


def extract_sensores_clima():
    return pd.read_csv("data/bronze/sensores_clima.csv", encoding="utf-8")


def extract_sensores_energia():
    return pd.read_csv("data/bronze/sensores_energia.csv", encoding="utf-8")


def extract_sensores_trafico():
    return pd.read_csv("data/bronze/sensores_trafico.csv", encoding="utf-8")


def obtener_info(df: pd.DataFrame):
    info = {}
    info["conteo"] = df.shape
    info["nulos"] = df.isna().sum()
    info["tipos"] = df.dtypes
    info['min_max'] = df.select_dtypes(include='number').agg(["min", "max"])
    return info
