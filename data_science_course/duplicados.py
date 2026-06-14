import pandas as pd

laptop_dataframe = pd.read_csv('laptop_price.csv',encoding='latin1')

#Ver si hay duplicados en la columna Company
print(laptop_dataframe.duplicated('Company'))

#Mostrar filas duplicadas en la columna company(si aparece vacío es que no hay duplicados)
print(laptop_dataframe[laptop_dataframe.duplicated('Company')])

#Mostrar filas duplicadas en las columnas Company, Product y TypeName
print(laptop_dataframe[laptop_dataframe.duplicated(['Company', 'Product', 'TypeName'])])

"""
Keep=first => se salva(false) la primera fila que cumpla la coincidencia
Keep=last => se salva(false) la primera última que cumpla la coincidencia
Keep=false => se salvan solo las filas que no estén duplicadas
"""

#Mostrar filas no duplicadas en las columnas Company, Product y TypeName
print(laptop_dataframe[~laptop_dataframe.duplicated(['Company', 'Product', 'TypeName'])])

#Eliminar duplicados de la columna company 
print(laptop_dataframe.drop_duplicates(['Company']))

#Obtener valores unicos en la columna Company
print(laptop_dataframe['Company'].unique())