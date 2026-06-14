import pandas as pd
from db.db import crear_engine

query = """
    WITH notas AS (
        SELECT alumnos.id AS id_alumno, CONCAT(alumnos.nombre, ' ', alumnos.apellidos) AS alumno, alumnos.dni, alumnos.fecha_nacimiento,
        asignaturas.nombre AS asignatura, asignaturas.curso, asignaturas.creditos, asignaturas.horas_semanales, asignaturas.profesor, asignaturas.descripcion,
        CASE 
            WHEN notas_alumnos.nota IS NULL THEN 0
            WHEN notas_alumnos.nota < 0 THEN 0
            WHEN notas_alumnos.nota > 10 THEN 10
            ELSE notas_alumnos.nota
        END AS nota
        FROM notas_alumnos
        JOIN alumnos ON notas_alumnos.id_alumno = alumnos.id
        JOIN asignaturas ON notas_alumnos.id_asignatura = asignaturas.id
        ),
    alumnos_sin_practicas AS (
        SELECT id_alumno, alumno, SUM(horas_semanales) AS horas_suspensas
        FROM notas
        WHERE nota < 5
        GROUP BY id_alumno
        HAVING SUM(horas_semanales) >= 9
    )

    SELECT DISTINCT id, nombre, apellidos, dni, fecha_nacimiento
    FROM alumnos
    WHERE id NOT IN(SELECT id_alumno FROM alumnos_sin_practicas);
"""

engine = crear_engine()

def obtener_alumnos_practicas_dataframe():
    return pd.read_sql(query, engine)
