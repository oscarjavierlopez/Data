# Proyecto ETL — Extracción y Análisis de Facturas en PDF

## Contexto

Trabajas como Data Engineer en el departamento financiero de **DataSoluciones Ibérica S.L.**,
una consultora tecnológica. El equipo de contabilidad lleva meses emitiendo facturas en PDF
y guardándolas en una carpeta sin ningún sistema centralizado. Ahora necesitan analizar
el estado de cobros, los ingresos por cliente y los servicios más demandados.

Tu misión es construir un pipeline ETL que lea los 12 PDFs de la carpeta `facturas/`,
extraiga la información relevante de cada uno, la estructure en un DataFrame de pandas
y la deje lista para análisis financiero.

---

## Los ficheros

La carpeta `facturas/` contiene **12 PDFs**, uno por cada factura emitida entre
enero y junio de 2024. Cada PDF tiene la misma estructura pero los valores varían:
diferente cliente, servicios, importes, fechas y estado de pago.

Cada factura contiene la siguiente información que deberás extraer:

| Campo            | Tipo esperado |
|------------------|---------------|
| Número de factura| str           |
| Cliente          | str           |
| CIF del cliente  | str           |
| Fecha de emisión | date          |
| Fecha de vencimiento | date      |
| Subtotal (EUR)   | float         |
| IVA %            | int           |
| IVA importe (EUR)| float         |
| Total (EUR)      | float         |
| Estado           | str           |

---

## Tareas

### Fase 1 — Extract

Lee los 12 PDFs e inspecciona el texto crudo que contienen antes de escribir
ninguna lógica de extracción.

### Fase 2 — Transform

#### 2.1 Extracción de campos

Extrae todos los campos de la tabla anterior de cada PDF y acumúlalos
en una estructura que te permita construir el DataFrame.

#### 2.2 Construcción del DataFrame

Construye un DataFrame con una fila por factura y todos los campos extraídos
con sus tipos correctos.

#### 2.3 Enriquecimiento

Añade las siguientes columnas calculadas:

- `dias_hasta_vencimiento`: días entre fecha de emisión y fecha de vencimiento
- `dias_vencida`: para facturas con estado "VENCIDA", días transcurridos desde
  la fecha de vencimiento hasta hoy. Para el resto, 0.
- `tipo_cliente`: "S.A." o "S.L." según el CIF del cliente
- `tramo_importe`: categoriza el total en:
  - 0–5.000 → "Pequeña"
  - 5.000–15.000 → "Media"
  - 15.000–50.000 → "Grande"

### Fase 3 — Load

Guarda el DataFrame final en dos formatos dentro de la carpeta `Data/gold/`:

- `facturas_procesadas.csv`
- `facturas_procesadas.xlsx`

---

## Preguntas de negocio al finalizar

Con el DataFrame limpio responde usando pandas:

1. ¿Cuál es el importe total pendiente de cobro (facturas PENDIENTE + VENCIDA)?
2. ¿Qué cliente tiene la factura de mayor importe?
3. ¿Cuántas facturas tienen un IVA distinto del 21%?
4. ¿Cuál es el ticket medio por estado (PAGADA / PENDIENTE / VENCIDA)?
5. ¿Qué mes concentra más ingresos (por fecha de emisión)?
