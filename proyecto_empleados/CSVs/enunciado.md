# Proyecto ETL — People Analytics

## Contexto

Trabajas como Data Engineer en el departamento de RRHH de una consultora tecnológica
de tamaño medio. La empresa lleva años acumulando datos en hojas de cálculo y sistemas
distintos, y ahora quieren centralizar toda la información en un único dataset limpio
que permita al equipo de People Analytics responder preguntas de negocio.

Te entregan tres ficheros CSV exportados a mano por tres personas distintas. Como
suele pasar, nadie siguió un criterio uniforme y los datos están llenos de problemas.

Tu misión: construir un pipeline ETL en Python con pandas que limpie, integre y
enriquezca los datos, y deje preparados los datasets finales para análisis.

---

## Los tres ficheros

### `empleados.csv` — 91 filas

Información del personal de la empresa.

| Columna        | Descripción                        |
|----------------|------------------------------------|
| empleado_id    | Identificador único                |
| nombre         | Nombre y apellido                  |
| departamento   | Departamento al que pertenece      |
| puesto         | Cargo dentro del departamento      |
| salario_bruto  | Salario anual en euros             |
| fecha_alta     | Fecha de incorporación (texto)     |
| jornada        | "completa" o "parcial"             |
| evaluacion     | Puntuación de desempeño (1–10)     |
| oficina        | Sede o "Remoto"                    |

**Problemas conocidos:**
- Hay un empleado duplicado con `empleado_id` distinto
- 3 registros tienen `salario_bruto` negativo o cero
- `departamento` tiene valores con capitalización inconsistente ("ventas", "TECNOLOGÍA")
- Nulls en: `salario_bruto` (7), `evaluacion` (6), `oficina` (4), `jornada` (3)
- `fecha_alta` es texto, hay que convertirla a datetime

---

### `proyectos.csv` — 95 filas

Proyectos facturados a clientes externos.

| Columna         | Descripción                                    |
|-----------------|------------------------------------------------|
| proyecto_id     | Identificador único                            |
| nombre          | Nombre del proyecto                            |
| cliente         | Empresa cliente                                |
| responsable_id  | empleado_id del responsable                    |
| presupuesto     | Presupuesto acordado en euros                  |
| coste_real      | Coste final incurrido en euros                 |
| fecha_inicio    | Fecha de inicio (texto)                        |
| fecha_fin       | Fecha de fin (texto, puede ser null si activo) |
| estado          | activo / completado / pausado / cancelado      |
| prioridad       | Alta / Media / Baja                            |

**Problemas conocidos:**
- 3 registros con `presupuesto` negativo o cero
- `estado` con capitalización inconsistente ("Activo", "COMPLETADO")
- `fecha_fin` tiene ~25 nulls legítimos (proyectos en curso) y hay que tratarlos
- Nulls en: `presupuesto` (5), `coste_real` (6), `prioridad` (7)
- Hay proyectos cuyo `responsable_id` no existe en `empleados.csv`

---

### `horas_trabajadas.csv` — 100 filas

Registro semanal de horas por empleado y proyecto.

| Columna         | Descripción                                   |
|-----------------|-----------------------------------------------|
| registro_id     | Identificador único                           |
| empleado_id     | Referencia al empleado                        |
| proyecto_id     | Referencia al proyecto                        |
| semana          | Semana ISO (ej. "2023-W04")                   |
| horas_normales  | Horas de jornada ordinaria en esa semana      |
| horas_extra     | Horas extra realizadas                        |
| tarea           | Tipo de tarea realizada                       |
| facturables     | Si las horas se facturan al cliente (bool)    |

**Problemas conocidos:**
- `horas_normales` tiene valores imposibles (>48 horas semanales y negativos)
- `horas_extra` tiene valores negativos
- Nulls en: `horas_normales` (6), `horas_extra` (7), `tarea` (6)
- Hay registros con `empleado_id` o `proyecto_id` que no existen en sus tablas de origen

---

## Tareas

### Fase 1 — Extract
Carga los tres ficheros y genera un informe de diagnóstico que muestre:
- Número de filas y columnas de cada DataFrame
- Conteo de nulls por columna
- Tipos de datos actuales

### Fase 2 — Transform

#### 2.1 Limpieza de `empleados`
- Detectar y eliminar el registro duplicado
- Descartar filas con `salario_bruto` inválido (≤ 0)
- Estandarizar `departamento` a formato título (`str.title()`)
- Imputar `salario_bruto` nulo con la **mediana del departamento**
- Imputar `evaluacion` nula con la **media del departamento**
- Imputar `oficina` nula con el valor más frecuente (moda)
- Imputar `jornada` nula con "completa"
- Convertir `fecha_alta` a datetime y crear la columna `antiguedad_anios`

#### 2.2 Limpieza de `proyectos`
- Descartar filas con `presupuesto` inválido (≤ 0)
- Estandarizar `estado` y `prioridad` a minúsculas
- Imputar `coste_real` nulo con la mediana global
- Imputar `presupuesto` nulo con la mediana global
- Imputar `prioridad` nula con "media"
- Convertir fechas a datetime
- Crear columna `desviacion_pct`: diferencia porcentual entre `coste_real` y `presupuesto`
- Crear columna `en_curso` (bool): True si `fecha_fin` es null o el estado es "activo"

#### 2.3 Limpieza de `horas_trabajadas`
- Descartar filas donde `horas_normales` > 48 o < 0
- Convertir a 0 las `horas_extra` negativas
- Imputar `horas_extra` nulas con 0
- Imputar `horas_normales` nulas con la mediana
- Imputar `tarea` nula con "Sin especificar"
- Crear columna `horas_totales` = `horas_normales` + `horas_extra`

#### 2.4 Integraciones
- Hacer un **LEFT JOIN** de `horas_trabajadas` con `empleados` (por `empleado_id`)
  para añadir `nombre`, `departamento` y `salario_bruto`
- Añadir a ese resultado el `cliente` y `estado` del proyecto (JOIN con `proyectos`)
- Detectar y anotar cuántos registros de horas quedan sin empleado o proyecto válido

#### 2.5 Métricas agregadas
Construye **dos DataFrames resumen**:

**Por departamento:**
- Total de empleados
- Salario medio
- Evaluación media
- Total de horas trabajadas
- Total de horas facturables

**Por proyecto:**
- Total de horas registradas
- Número de empleados distintos que trabajaron en él
- Coste en horas (horas_totales × coste_hora, donde coste_hora = salario_bruto / 1800)
- Desviación del presupuesto

### Fase 3 — Load
Guarda en una carpeta `output/` los siguientes ficheros:
- `empleados_limpios.csv`
- `proyectos_limpios.csv`
- `horas_limpias.csv`
- `analitico_horas.csv` (el join enriquecido)
- `resumen_departamento.csv`
- `resumen_proyecto.csv`

---

## Preguntas de negocio que debes poder responder al final

Una vez completado el pipeline, el equipo de People Analytics necesita que respondas
estas preguntas usando únicamente pandas sobre los datos limpios:

1. ¿Qué departamento tiene el salario medio más alto?
2. ¿Cuáles son los 3 proyectos con mayor desviación de presupuesto (en %)?
3. ¿Qué empleado ha registrado más horas totales en el año?
4. ¿Qué porcentaje de las horas totales son facturables?
5. ¿Existe correlación entre la evaluación del empleado y sus horas extra?
   _(Calcula el coeficiente de correlación de Pearson con `.corr()`)_

---

## Conceptos clave que practicarás

`read_csv` · `isnull` · `fillna` · `dropna` · `drop_duplicates` ·
`str.title` · `str.lower` · `pd.to_datetime` · `dt.year` ·
`groupby` + `transform` · `groupby` + `agg` · `merge` ·
`pd.cut` · `np.where` · `clip` · `value_counts` · `corr`
