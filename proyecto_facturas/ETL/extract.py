from PyPDF2 import PdfReader
import pandas as pd
import os
import re
from typing import Dict, Any


def extraer_contenido_pdf(pdf: str, datos: dict[str, list[Any]]):
    # Comprobamos que el fichero sea pdf
    if pdf.lower().endswith(".pdf"):
        with open(pdf, "rb") as archivo:
            # Creamos el objeto lector
            lector = PdfReader(archivo)

            # Extraer el texto de toda la pagina
            factura = lector.pages[0].extract_text()

            # Extraer partes de la pagina y añadirlas al diccionario de datos
            numero_factura = factura.split("N.º")[1].split("CIF")[0].strip()
            datos["numero_factura"].append(numero_factura)

            cliente = (
                factura.split("DATOS DE FACTURA")[1].split("Fecha emisión:")[0].strip()
            )
            datos["cliente"].append(cliente)

            cif = factura.split("CIF/NIF:")[1].split("Forma de pago:")[0].strip()
            datos["cif"].append(cif)

            fecha_emision = factura.split("Fecha emisión:")[1].splitlines()[1].strip()
            datos["fecha_emision"].append(fecha_emision)

            fecha_vencimiento = (
                factura.split("Fecha vencimiento:")[1].splitlines()[1].strip()
            )
            datos["fecha_vencimiento"].append(fecha_vencimiento)

            subtotal = factura.split("Subtotal:")[1].split("EUR")[0].strip()
            datos["subtotal"].append(subtotal)

            iva_porcentaje = factura.split("IVA (")[1].split("%")[0].strip()
            datos["iva_porcentaje"].append(iva_porcentaje)

            iva_importe = re.split(r"\([0-9]+%\):", factura)[1].split("EUR")[0].strip()
            datos["iva_importe"].append(iva_importe)

            total = factura.split("TOTAL:")[1].split("EUR")[0].strip()
            datos["total"].append(total)

            estado = factura.split("CIF:")[1].splitlines()[1].strip()
            datos["estado"].append(estado)


def crear_dataframe(carpeta: str):
    datos = {
        "numero_factura": [],
        "cliente": [],
        "cif": [],
        "fecha_emision": [],
        "fecha_vencimiento": [],
        "subtotal": [],
        "iva_porcentaje": [],
        "iva_importe": [],
        "total": [],
        "estado": [],
    }

    for pdf in os.listdir(carpeta):
        factura = os.path.join(carpeta, pdf).replace("\\", "/")
        extraer_contenido_pdf(factura, datos)

    # Crear dataframe a partir del diccionario con los datos de las facturas
    df_facturas = pd.DataFrame(datos)
    return df_facturas
