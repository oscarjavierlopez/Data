from ETL.extract import (
    extract_sensores_trafico,
    extract_sensores_clima,
    extract_sensores_energia,
    obtener_info,
)
from ETL.transform import (
    clean_timestamps,
    clean_sensores_clima,
    clean_sensores_energia,
    clean_sensores_trafico,
    get_resumen_clima_hora,
    get_resumen_trafico_hora,
    get_resumen_energia_hora,
    get_resumen_ciudad_hora,
)
from ETL.load import load_df_silver, load_df_gold


def main():
    # Extraer CSVs
    df_sensores_trafico_bronze = extract_sensores_trafico()
    df_sensores_clima_bronze = extract_sensores_clima()
    df_sensores_energia_bronze = extract_sensores_energia()

    # Limpiar timestamps
    df_sensores_trafico_silver = clean_timestamps(df_sensores_trafico_bronze)
    df_sensores_clima_silver = clean_timestamps(df_sensores_clima_bronze)
    df_sensores_energia_silver = clean_timestamps(df_sensores_energia_bronze)

    # Limpiar CSVs
    df_sensores_clima_silver = clean_sensores_clima(df_sensores_clima_silver)
    df_sensores_trafico_silver = clean_sensores_trafico(df_sensores_trafico_silver)
    df_sensores_energia_silver = clean_sensores_energia(df_sensores_energia_silver)

    # Guardar CSVs limpios en la capa silver
    load_df_silver(df_sensores_clima_silver, "clima_limpio")
    load_df_silver(df_sensores_trafico_silver, "trafico_limpio")
    load_df_silver(df_sensores_energia_silver, "energia_limpia")

    # Obtenemos métricas de agregación por ventana temporal
    df_sensores_clima_gold = get_resumen_clima_hora(df_sensores_clima_silver)
    df_sensores_trafico_gold = get_resumen_trafico_hora(df_sensores_trafico_silver)
    df_sensores_energia_gold = get_resumen_energia_hora(df_sensores_energia_silver)
    df_ciudad_hora_gold = get_resumen_ciudad_hora(
        df_sensores_clima_gold, df_sensores_trafico_gold, df_sensores_energia_gold
    )

    # Guardar CSVs con métricas de agregación por ventana temporal
    load_df_gold(df_sensores_clima_gold, "resumen_clima_hora")
    load_df_gold(df_sensores_trafico_gold, "resumen_trafico_hora")
    load_df_gold(df_sensores_energia_gold, "resumen_energia_hora")
    load_df_gold(df_ciudad_hora_gold, "ciudad_por_hora")


if __name__ == "__main__":
    main()
