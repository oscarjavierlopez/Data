import logging
import os
from ETL.extract import crear_dataframe
from ETL.transform import limpiar_dataframe_facturas, enriquecer_dataframe_facturas
from ETL.load import almacenar_df_silver, load_df_gold

# Configuracion del logger
LOG_DIR = "Logs"
os.makedirs(LOG_DIR, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(
            os.path.join(LOG_DIR, "faturas.log"), encoding="utf-8"
        ),  # Para que los logs vayan al fichero de logs
        logging.StreamHandler(),  # Para que los logs se vean por consola
    ],
)

logger = logging.getLogger(__name__)


def main():
    logger.info("─" * 40)
    logger.info("Inicio del proceso ETL")
    # Extraemos info de las facturas
    df_facturas = crear_dataframe("Data/bronze")

    # Modificamos los tipos y almacenamos el dataset en la capa silver
    df_facturas_limpio = limpiar_dataframe_facturas(df_facturas)
    almacenar_df_silver(df_facturas_limpio, "facturas_limpio")

    # Enriquecemos el dataset y lo almacenamos en la capa gold
    df_facturas_enriquecido = enriquecer_dataframe_facturas(df_facturas_limpio)
    load_df_gold(df_facturas_enriquecido, "facturas_procesadas")

    logger.info("Proceso ETL finalizado correctamente")

    # Preguntas de negocio
    # print(
    #     "¿Cuál es el importe total pendiente de cobro (facturas PENDIENTE + VENCIDA)?",
    #     df_facturas_enriquecido.groupby("estado")["total"].sum()["PENDIENTE"]
    #     + df_facturas_enriquecido.groupby("estado")["total"].sum()["VENCIDA"],
    # )

    # print(
    #     "¿Qué cliente tiene la factura de mayor importe?",
    #     df_facturas_enriquecido[
    #         df_facturas_enriquecido["total"] == df_facturas_enriquecido["total"].max()
    #     ]["cliente"],
    # )

    # print(
    #     "¿Cuántas facturas tienen un IVA distinto del 21%?",
    #     df_facturas_enriquecido.groupby("iva_porcentaje")["cif"]
    #     .count()[
    #         df_facturas_enriquecido.groupby("iva_porcentaje")["cif"].count().index != 21
    #     ]
    #     .sum(),
    # )

    # print("¿Cuál es el ticket medio por estado (PAGADA / PENDIENTE / VENCIDA)?", df_facturas_enriquecido.groupby("estado")["total"].mean())

    # df_facturas_enriquecido["month"] = df_facturas_enriquecido["fecha_emision"].dt.month
    # print("¿Qué mes concentra más ingresos (por fecha de emisión)?", df_facturas_enriquecido.groupby("month")["total"].sum())


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.exception("Error en el proceso ETL: %s", e)
