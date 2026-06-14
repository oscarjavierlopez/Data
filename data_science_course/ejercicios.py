import pandas as pd

df_car_sales = pd.read_csv('Car_sales.csv', encoding='latin1')

"""
Calcula tanto la suma como el promedio de todas las columnas numéricas pasando una lista 
de funciones
"""
print(df_car_sales.select_dtypes(include='float64').agg(['sum', 'mean']))

"""
Ejercicio 2: Agregaciones específicas por columna
Usa un diccionario dentro del método .agg() para aplicar funciones distintas a columnas específicas
:
A la columna sales_in_thousands, calcúlale la suma y el promedio.
A la columna price_in_thousands, obtén el valor máximo.
"""
print(df_car_sales.agg({'Sales_in_thousands':['sum', 'mean'], 'Price_in_thousands':['max']}))


"""
Ejercicio 1: Filtrado previo a la agrupación
Reto: Filtra el DataFrame para quedarte solo con los vehículos cuyo precio (price_in_thousands) sea mayor a 25.
Luego, agrupa por manufacturer y calcula el promedio de caballos de fuerza (horsepower)
"""
print(df_car_sales.query('Price_in_thousands > 25').groupby('Manufacturer').agg({"Horsepower": "mean"}))


"""
Reto: Agrupa los datos por vehicle_type. Utiliza el método .agg() para obtener la mediana y 
la desviación estándar (std) de la columna fuel_capacity
"""
print(df_car_sales.agg({"Fuel_capacity": ["median", "std"]}))


"""
Reto: Agrupa por manufacturer y calcula el valor máximo de la columna engine_size.
Ordena el resultado de forma descendente para identificar qué fabricante ofrece el motor más grande en su catálogo
"""
print(df_car_sales.groupby('Manufacturer').agg({"Engine_size": "max"}).sort_values(by="Engine_size", ascending=False))

"""
Reto: Agrupa por manufacturer y utiliza una función para contar cuántos valores nulos hay
en la columna price_in_thousands por cada marca 
"""
print(df_car_sales.groupby('Manufacturer').apply(lambda x: x.isnull().sum())["Price_in_thousands"])

"""
Reto: Agrupa por vehicle_type. Crea un DataFrame resumen con tres columnas nuevas:
ventas_totales: La suma de sales_in_thousands.
precio_promedio: El promedio de price_in_thousands.
modelo_mas_potente: El máximo de horsepower. (Recuerda usar el formato: NombreNuevaColumna = ('ColumnaOriginal', 'funcion') dentro de agg)
"""
df_car_sales_summary = df_car_sales.groupby('Vehicle_type').agg(ventas_totales=('Sales_in_thousands', 'sum'),
                                                                precio_promedio=('Price_in_thousands', 'mean'),
                                                                modelo_mas_potente=('Horsepower', 'max'))[['ventas_totales', 'precio_promedio', 'modelo_mas_potente']]
print(df_car_sales_summary)

"""
Reto: Agrupa por vehicle_type. Para cada grupo, calcula la diferencia entre el precio de cada coche individual
y el precio máximo de su categoría
"""
print(df_car_sales.groupby('Vehicle_type')['Price_in_thousands'].apply(lambda x: x.max() - x))

"""
Reto: Identifica qué columnas tienen valores nulos y calcula el porcentaje de datos faltantes para cada una
.
Imputación: En lugar de eliminar filas, reemplaza los valores nulos de la columna rating utilizando la moda (el valor más frecuente)
de esa misma columna.
Recuerda convertir el resultado de la moda en un string antes de usar fillna
"""
df_netflix_titles = pd.read_csv('netflix_titles.csv', encoding='latin1')
for column in df_netflix_titles.columns:
    print(f'{column}: {df_netflix_titles[column].isnull().mean() * 100}')

df_netflix_titles['rating'] = df_netflix_titles['rating'].fillna(df_netflix_titles['rating'].mode()[0])
print(df_netflix_titles.loc[5989, 'rating'])


