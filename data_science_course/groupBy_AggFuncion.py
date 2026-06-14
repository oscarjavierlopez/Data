import pandas as pd

df_car_sales = pd.read_csv('Car_sales.csv', encoding='latin1')[['Manufacturer', 'Sales_in_thousands', 'Vehicle_type', 
                                                                'Price_in_thousands', 'Engine_size', 'Horsepower', 'Fuel_capacity']]
#nunique permite ver cuántos tipos diferentes hay de cada columna
print(df_car_sales.nunique())

#Funciones agregadas operando por columnas
print(df_car_sales.agg('sum'))
print(df_car_sales[['Sales_in_thousands','Price_in_thousands', 'Engine_size', 'Horsepower', 'Fuel_capacity']].agg('mean'))
print(df_car_sales[['Sales_in_thousands','Price_in_thousands', 'Engine_size', 'Horsepower', 'Fuel_capacity']].agg(['sum', 'mean']))

#Seleccionar diferentes columnas y hacer diferentes operaciones con ellas
print(df_car_sales.agg({'Sales_in_thousands':['sum', 'mean'], 'Price_in_thousands':['sum', 'max']}))

#sumar valores Sales_in_thousands y Price_in_thousands de cada fila
print(df_car_sales[['Sales_in_thousands','Price_in_thousands']].agg('sum', axis=1))

#Dar alias a las columnas con funcion de agregacion
print(df_car_sales[['Sales_in_thousands','Price_in_thousands']].agg(x=('Sales_in_thousands', 'sum'), y=('Price_in_thousands', 'sum')))

#Sacar el promedio de Sales_in_thousands y Price_in_thousands de cada categoría de coches
print(df_car_sales[['Vehicle_type', 'Sales_in_thousands','Price_in_thousands']].groupby('Vehicle_type', as_index=False).agg('mean'))

#Obtener las diferentes Manufacturer del datframe
print(df_car_sales.groupby('Manufacturer').groups.keys())

#Obtener un dataframe con los datos de aquellos coches de la Manufacturer 'Ford'
print(df_car_sales.groupby('Manufacturer').get_group('Ford'))

#Obtener el max y min de cada col agrupando por Vehicle_type
print(df_car_sales.groupby('Vehicle_type').agg(['min', 'max'])[['Sales_in_thousands','Price_in_thousands', 'Engine_size', 'Horsepower', 'Fuel_capacity']])

#Obtener min_Engine_size y max_Horsepower agrupado por Vehicle_type
print(df_car_sales.groupby('Vehicle_type').agg(min_Engine_size=('Engine_size', 'min'), max_Horsepower=('Horsepower', 'max')))

#Obtener la suma de la col Sales_in_thousands agrupadas por Manufacturer y el resultado que no esté en miles
print(df_car_sales.groupby('Manufacturer').sum().apply(lambda x: x*1000)[['Sales_in_thousands', 'Price_in_thousands']])

#Obtener las Sales_in_thousands por encima o debajo de la media de ventas agrupadas por Manufacturer
print(df_car_sales[['Manufacturer', 'Sales_in_thousands']].groupby('Manufacturer').apply(lambda x: x - x.mean()))