import pandas as pd
import numpy as np
from functools import reduce

def clean_timestamps(df: pd.DataFrame):
    df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce", format="mixed")
    df = df[df["timestamp"].notna()]
    df["fecha"] = df["timestamp"].dt.date
    df["hora"] = df["timestamp"].dt.time
    df["dia_semana"] = df["timestamp"].dt.day_of_week
    return df


def clean_sensores_clima(df_sensores_clima: pd.DataFrame):
    df_sensores_clima = df_sensores_clima.drop_duplicates(
        [
            "sensor_id",
            "timestamp",
            "zona",
            "temperatura_c",
            "humedad_pct",
            "presion_hpa",
            "viento_kmh",
            "lluvia_mm",
        ]
    )

    # Manejo de nulos y valores no válidos de temperatura
    df_sensores_clima["temperatura_c"] = df_sensores_clima["temperatura_c"].fillna(
        df_sensores_clima.groupby("zona")["temperatura_c"].transform("median")
    )
    df_sensores_clima = df_sensores_clima[
        (df_sensores_clima["temperatura_c"] >= -20)
        & (df_sensores_clima["temperatura_c"] <= 50)
    ]

    # Manejo de valores nulos y no válidos de humedad
    df_sensores_clima["humedad_pct"] = df_sensores_clima["humedad_pct"].fillna(
        df_sensores_clima["humedad_pct"].median()
    )
    df_sensores_clima = df_sensores_clima[
        (df_sensores_clima["humedad_pct"] >= 0)
        & (df_sensores_clima["humedad_pct"] <= 100)
    ]

    # Manejo de valores nulos y no válidos de presion
    df_sensores_clima["presion_hpa"] = df_sensores_clima["presion_hpa"].fillna(
        df_sensores_clima["presion_hpa"].median()
    )
    df_sensores_clima = df_sensores_clima[
        (df_sensores_clima["presion_hpa"] >= 870)
        & (df_sensores_clima["presion_hpa"] <= 1085)
    ]

    # Manejo de valores nulos y no válidos de viento
    df_sensores_clima["viento_kmh"] = df_sensores_clima["viento_kmh"].fillna(0)
    df_sensores_clima = df_sensores_clima[
        (df_sensores_clima["viento_kmh"] >= 0)
        & (df_sensores_clima["viento_kmh"] <= 200)
    ]

    df_sensores_clima = df_sensores_clima[df_sensores_clima["lluvia_mm"] >= 0]

    df_sensores_clima["sensacion_termica"] = df_sensores_clima["temperatura_c"] - (
        0.4
        * (df_sensores_clima["temperatura_c"] - 10)
        * (1 - df_sensores_clima["humedad_pct"] / 100)
    )

    return df_sensores_clima


def clean_sensores_energia(df_sensores_energia: pd.DataFrame):
    df_sensores_energia = df_sensores_energia.drop_duplicates(
        [
            "sensor_id",
            "timestamp",
            "edificio",
            "consumo_kwh",
            "voltaje_v",
            "corriente_a",
            "factor_potencia",
            "tarifa",
        ]
    )

    df_sensores_energia["consumo_kwh"] = df_sensores_energia["consumo_kwh"].fillna(
        df_sensores_energia.groupby("edificio")["consumo_kwh"].transform("median")
    )
    df_sensores_energia = df_sensores_energia[
        (df_sensores_energia["consumo_kwh"] >= 0)
        & (df_sensores_energia["consumo_kwh"] <= 5000)
    ]

    df_sensores_energia["voltaje_v"] = df_sensores_energia["voltaje_v"].fillna(230)
    df_sensores_energia = df_sensores_energia[
        (df_sensores_energia["voltaje_v"] >= 200)
        & (df_sensores_energia["voltaje_v"] <= 260)
    ]

    df_sensores_energia = df_sensores_energia[df_sensores_energia["corriente_a"] >= 0]

    df_sensores_energia["factor_potencia"] = df_sensores_energia[
        "factor_potencia"
    ].fillna(df_sensores_energia["factor_potencia"].median())
    df_sensores_energia = df_sensores_energia[
        (df_sensores_energia["factor_potencia"] >= 0)
        & (df_sensores_energia["factor_potencia"] <= 1)
    ]

    df_sensores_energia["potencia_activa_kw"] = (
        df_sensores_energia["consumo_kwh"] * df_sensores_energia["factor_potencia"]
    )

    condiciones = [
        df_sensores_energia["tarifa"].str.lower() == "valle",
        df_sensores_energia["tarifa"].str.lower() == "llano",
        df_sensores_energia["tarifa"].str.lower() == "punta",
    ]
    values = [
        df_sensores_energia["consumo_kwh"] * 0.08,
        df_sensores_energia["consumo_kwh"] * 0.13,
        df_sensores_energia["consumo_kwh"] * 0.22,
    ]
    df_sensores_energia["coste_estimado_eur"] = np.select(
        condiciones, values, default=0
    )

    return df_sensores_energia


def clean_sensores_trafico(df_sensores_trafico: pd.DataFrame):
    # Manejo de nulos y valores no válidos de vehiculos_hora
    df_sensores_trafico["vehiculos_hora"] = df_sensores_trafico[
        "vehiculos_hora"
    ].fillna(df_sensores_trafico.groupby("calle")["vehiculos_hora"].transform("median"))
    df_sensores_trafico = df_sensores_trafico[
        (df_sensores_trafico["vehiculos_hora"] >= 0)
        & (df_sensores_trafico["vehiculos_hora"] <= 3000)
    ]

    # Manejo de nulos y valores no válidos de velocidad_media
    df_sensores_trafico["velocidad_media"] = df_sensores_trafico[
        "velocidad_media"
    ].fillna(
        df_sensores_trafico.groupby("calle")["velocidad_media"].transform("median")
    )
    df_sensores_trafico = df_sensores_trafico[
        (df_sensores_trafico["velocidad_media"] >= 0)
        & (df_sensores_trafico["velocidad_media"] <= 130)
    ]

    # Manejo de nulos y valores no válidos de ocupacion_pct
    df_sensores_trafico["ocupacion_pct"] = df_sensores_trafico["ocupacion_pct"].fillna(
        df_sensores_trafico.groupby("calle")["ocupacion_pct"].transform("median")
    )
    df_sensores_trafico = df_sensores_trafico[
        (df_sensores_trafico["ocupacion_pct"] >= 0)
        & (df_sensores_trafico["ocupacion_pct"] <= 100)
    ]

    df_sensores_trafico["incidencia"] = df_sensores_trafico["incidencia"].fillna(
        "sin_incidencia"
    )

    condiciones = [
        df_sensores_trafico["ocupacion_pct"] < 30,
        df_sensores_trafico["ocupacion_pct"] < 60,
        df_sensores_trafico["ocupacion_pct"] < 85,
        df_sensores_trafico["ocupacion_pct"] > 85,
    ]
    values = ["fluido", "denso", "congestionado", "colapsado"]
    df_sensores_trafico["nivel_congestion"] = np.select(
        condiciones, values, default="fluido"
    )
    return df_sensores_trafico


def get_resumen_clima_hora(df_sensores_clima: pd.DataFrame):
    df_sensores_clima = df_sensores_clima.groupby(["fecha", "hora"]).agg(
        temperatura_media=("temperatura_c", "mean"),
        temperatura_min=("temperatura_c", "min"),
        temperatura_max=("temperatura_c", "max"),
        humedad_media=("humedad_pct", "mean"),
        presion_media=("presion_hpa", "mean"),
        viento_max=("viento_kmh", "max"),
        lluvia_total=("lluvia_mm", "sum"),
        num_lecturas=("sensor_id", "count"),
    )

    return df_sensores_clima


def get_resumen_trafico_hora(df_sensores_trafico: pd.DataFrame):
    df_sensores_trafico = df_sensores_trafico.groupby(["fecha", "hora"]).agg(
        vehiculos_total=("vehiculos_hora", "sum"),
        velocidad_media=("velocidad_media", "mean"),
        ocupacion_media=("ocupacion_pct", "mean"),
        num_incidencias=("incidencia", lambda x: (x != "sin_incidencia").sum()),
        nivel_congestion_predominante=(
            "nivel_congestion",
            lambda x: x.mode().iloc[0],
        ),
    )

    return df_sensores_trafico

def get_resumen_energia_hora(df_sensores_energia:pd.DataFrame):
    df_sensores_energia = df_sensores_energia.groupby(["fecha", "hora"]).agg(
        consumo_total_kwh=("consumo_kwh", "sum"),
        potencia_media_kw=("potencia_activa_kw", "mean"),
        coste_total_eur=("coste_estimado_eur", "sum"),
        voltaje_medio=("voltaje_v", "mean"),
        num_edificios_activos=("edificio", lambda x: x.nunique())
    )
    return df_sensores_energia

def get_resumen_ciudad_hora(df_sensores_clima: pd.DataFrame, df_sensores_trafico: pd.DataFrame, df_sensores_energia:pd.DataFrame):
    df_list = [df_sensores_clima, df_sensores_trafico, df_sensores_energia]
    df_ciudad_hora = reduce(lambda left, right: pd.merge(left, right, how="outer", on=["fecha", "hora"]), df_list)
    return df_ciudad_hora