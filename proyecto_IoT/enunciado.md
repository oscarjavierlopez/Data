# Proyecto ETL — IoT & Smart City

## Contexto

El Ayuntamiento de una ciudad inteligente ha desplegado tres redes de sensores
distribuidos por el municipio: sensores climáticos, de tráfico y de consumo
energético. Cada sensor envía lecturas periódicas que se acumulan en ficheros CSV
sin ningún control de calidad.

Trabajas como Data Engineer en el equipo de ciudad inteligente. Tu misión es
construir un pipeline ETL que ingiera estas ráfagas de datos crudos, las limpie,
las agregue en ventanas temporales y las deje preparadas para que el equipo de
análisis predictivo pueda trabajar con ellas.

Los datos cubren **5 días** de lecturas (del 1 al 5 de marzo de 2024).

---

## Los tres ficheros

### `sensores_clima.csv` — 96 filas

Lecturas de 25 sensores meteorológicos repartidos por zonas de la ciudad.

| Columna        | Descripción                              | Rango válido         |
|----------------|------------------------------------------|----------------------|
| lectura_id     | Identificador único de lectura           | —                    |
| sensor_id      | Código del sensor (ej. CLM-001)          | —                    |
| timestamp      | Fecha y hora de la lectura               | Formato ISO          |
| zona           | Zona de la ciudad                        | —                    |
| temperatura_c  | Temperatura en grados Celsius            | -20 a 50             |
| humedad_pct    | Humedad relativa en %                    | 0 a 100              |
| presion_hpa    | Presión atmosférica en hPa               | 870 a 1085           |
| viento_kmh     | Velocidad del viento en km/h             | 0 a 200              |
| lluvia_mm      | Precipitación acumulada en mm            | ≥ 0                  |

**Problemas conocidos:**
- 1 lectura duplicada con `lectura_id` distinto
- Valores físicamente imposibles en `temperatura_c`, `humedad_pct` y `presion_hpa`
- 2 timestamps con formato no estándar que pandas no parsea directamente
- Nulls en: `temperatura_c` (7), `humedad_pct` (5), `presion_hpa` (4), `viento_kmh` (5)

---

### `sensores_trafico.csv` — 100 filas

Lecturas de 30 sensores de tráfico instalados en las principales vías.

| Columna         | Descripción                              | Rango válido         |
|-----------------|------------------------------------------|----------------------|
| lectura_id      | Identificador único de lectura           | —                    |
| sensor_id       | Código del sensor (ej. TRF-001)          | —                    |
| timestamp       | Fecha y hora de la lectura               | Formato ISO          |
| calle           | Nombre de la vía                         | —                    |
| vehiculos_hora  | Vehículos contados en la última hora     | 0 a 3000             |
| velocidad_media | Velocidad media de los vehículos en km/h | 0 a 130              |
| ocupacion_pct   | % de ocupación del carril                | 0 a 100              |
| incidencia      | Tipo de incidencia activa (puede ser null)| —                   |
| tipo_via        | Categoría de la vía                      | —                    |

**Problemas conocidos:**
- Valores negativos y fuera de rango en `vehiculos_hora`, `velocidad_media` y `ocupacion_pct`
- 2 timestamps con formato inválido
- `incidencia` tiene ~70% de nulls — esto **no es un error**, significa que no hay incidencia activa
- Nulls en: `vehiculos_hora` (7), `velocidad_media` (5), `ocupacion_pct` (7)

---

### `sensores_energia.csv` — 91 filas

Lecturas de 20 sensores de consumo eléctrico en edificios municipales.

| Columna          | Descripción                              | Rango válido         |
|------------------|------------------------------------------|----------------------|
| lectura_id       | Identificador único de lectura           | —                    |
| sensor_id        | Código del sensor (ej. ENR-001)          | —                    |
| timestamp        | Fecha y hora de la lectura               | Formato ISO          |
| edificio         | Nombre del edificio                      | —                    |
| consumo_kwh      | Consumo eléctrico en kWh                 | 0 a 5000             |
| voltaje_v        | Voltaje registrado en voltios            | 200 a 260            |
| corriente_a      | Intensidad en amperios                   | ≥ 0                  |
| factor_potencia  | Factor de potencia del circuito          | 0 a 1                |
| tarifa           | Franja tarifaria activa                  | —                    |

**Problemas conocidos:**
- 1 lectura duplicada con `lectura_id` distinto
- Valores imposibles en `consumo_kwh`, `voltaje_v` y `factor_potencia`
- 2 timestamps completamente inválidos ("hoy", "2024-13-01 25:00:00")
- Nulls en: `consumo_kwh` (6), `voltaje_v` (5), `factor_potencia` (7)

---

## Tareas

### Fase 1 — Extract

Carga los tres ficheros y genera un informe de diagnóstico que muestre:
- Número de filas y columnas por DataFrame
- Conteo de nulls por columna
- Tipos de datos actuales
- Rango real (mín/máx) de las columnas numéricas principales

---

### Fase 2 — Transform

#### 2.1 Limpieza de timestamps (los tres datasets)

Los timestamps son la columna más crítica en datos IoT: sin ellos no puedes
agrupar por ventana temporal.

- Intentar parsear `timestamp` con `pd.to_datetime(..., errors="coerce")`
- Los timestamps que no se puedan parsear quedarán como `NaT`
- **Eliminar** las filas con `NaT` en timestamp: sin fecha no hay lectura válida
- Extraer columnas auxiliares: `fecha` (date), `hora` (int 0-23), `dia_semana` (int 0-6)

#### 2.2 Limpieza de `sensores_clima`

- Eliminar duplicados por `lectura_id`
- Descartar filas fuera de rango en `temperatura_c`, `humedad_pct` y `presion_hpa`
  usando los rangos válidos de la tabla anterior
- Imputar `temperatura_c` nula con la **mediana de la zona**
- Imputar `humedad_pct` nula con la **mediana global**
- Imputar `presion_hpa` nula con la **mediana global**
- Imputar `viento_kmh` nulo con 0 (sin dato = sin viento registrado)
- Crear columna `sensacion_termica`: temperatura_c - (0.4 × (temperatura_c - 10) × (1 - humedad_pct/100))

#### 2.3 Limpieza de `sensores_trafico`

- Descartar filas fuera de rango en `vehiculos_hora`, `velocidad_media` y `ocupacion_pct`
- Imputar nulos numéricos con la **mediana de la calle** (groupby + transform)
- Tratar `incidencia`: los nulls son válidos, reemplazarlos por el string `"sin_incidencia"`
- Crear columna `nivel_congestion` usando `pd.cut()` sobre `ocupacion_pct`:
  - 0–30 → "fluido"
  - 30–60 → "denso"
  - 60–85 → "congestionado"
  - 85–100 → "colapsado"

#### 2.4 Limpieza de `sensores_energia`

- Eliminar duplicados por `lectura_id`
- Descartar filas fuera de rango en `consumo_kwh`, `voltaje_v` y `factor_potencia`
- Imputar `consumo_kwh` nulo con la **mediana del edificio**
- Imputar `voltaje_v` nulo con 230.0 (valor nominal de red)
- Imputar `factor_potencia` nulo con la **mediana global**
- Crear columna `potencia_activa_kw`: consumo_kwh × factor_potencia
- Crear columna `coste_estimado_eur`: consumo_kwh × tarifa en €/kWh, donde:
  - "valle" → 0.08 €/kWh
  - "llano" → 0.13 €/kWh
  - "punta" → 0.22 €/kWh

#### 2.5 Agregación por ventana temporal (núcleo del proyecto)

Esta es la transformación central en pipelines IoT: convertir lecturas individuales
en resúmenes por ventana de tiempo.

Usando el timestamp limpio, agrupa **cada dataset por franja horaria** (`fecha` + `hora`)
y calcula las siguientes métricas:

**Clima por hora:**
- `temperatura_media`, `temperatura_min`, `temperatura_max`
- `humedad_media`
- `presion_media`
- `viento_max`
- `lluvia_total` (suma)
- `num_lecturas` (conteo de sensores activos en esa hora)

**Tráfico por hora:**
- `vehiculos_total` (suma)
- `velocidad_media`
- `ocupacion_media`
- `num_incidencias` (conteo de filas donde incidencia ≠ "sin_incidencia")
- `nivel_congestion_predominante` (moda de `nivel_congestion`)

**Energía por hora:**
- `consumo_total_kwh` (suma)
- `potencia_media_kw`
- `coste_total_eur` (suma)
- `voltaje_medio`
- `num_edificios_activos` (conteo de edificios distintos con lectura en esa hora)

#### 2.6 Dataset unificado

Haz un **JOIN** de los tres resúmenes horarios por `fecha` + `hora` para obtener
un único DataFrame con todas las métricas de la ciudad por franja horaria.

- Usa OUTER JOIN para conservar todas las horas aunque algún sensor no tenga datos
- Anota cuántas franjas horarias quedan sin datos de alguna de las tres redes

---

### Fase 3 — Load

Guarda en una carpeta `output/` los siguientes ficheros:

| Fichero                      | Contenido                                      |
|------------------------------|------------------------------------------------|
| `clima_limpio.csv`           | Lecturas de clima limpias con columnas nuevas  |
| `trafico_limpio.csv`         | Lecturas de tráfico limpias con nivel_congestion|
| `energia_limpia.csv`         | Lecturas de energía limpias con coste estimado |
| `resumen_clima_hora.csv`     | Clima agregado por hora                        |
| `resumen_trafico_hora.csv`   | Tráfico agregado por hora                      |
| `resumen_energia_hora.csv`   | Energía agregada por hora                      |
| `ciudad_por_hora.csv`        | Dataset unificado de las tres redes            |

---

## Preguntas de negocio al finalizar

1. ¿En qué franja horaria se registra el mayor consumo energético medio?
2. ¿Qué zona tiene la temperatura media más alta durante los 5 días?
3. ¿Existe correlación entre la `ocupacion_pct` del tráfico y el `consumo_total_kwh`
   de energía? _(une los resúmenes horarios y usa `.corr()`)_
4. ¿Cuántas horas del periodo analizado han tenido nivel de congestión "colapsado"?
5. ¿En qué edificio se concentra el mayor coste energético estimado total?

---

## Conceptos clave que practicarás

`pd.to_datetime` con `errors="coerce"` · `NaT` · `.dt.hour` · `.dt.date` · `.dt.dayofweek` ·
`pd.cut` · `groupby` + `transform` · `groupby` + `agg` con múltiples funciones ·
`merge` con `how="outer"` · `value_counts` · `map` con diccionario · `.corr()` ·
validación por rangos con condiciones booleanas · `clip` · `mode()`
