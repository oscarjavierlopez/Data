import pandas as pd
import numpy as np

players_dataframe = pd.read_csv('players_20.csv',encoding='latin1')
players_dataframe = players_dataframe[['short_name', 'long_name', 'age', 'dob', 'height_cm', 'weight_kg', 'nationality', 'club']]
players_dataframe = players_dataframe.set_index('short_name')

"""
axis=0 => elimina fila
axis=1 => elimina columna
"""
#eliminar fila de Messi
players_dataframe = players_dataframe.drop( 'L. Messi', axis=0)
print(players_dataframe)

#Eliminar fila de Cristiano Ronaldo
players_dataframe = players_dataframe.drop(index=['Cristiano Ronaldo'])
print(players_dataframe)

"""
inplace=True reemplaza el dataframe original en lugar de devolver uno nuevo
"""
#Eliminar filas de Neymar Jr y J. Oblak  
players_dataframe.drop(index=['Neymar Jr', 'J. Oblak'], inplace=True)  
print(players_dataframe)

#Eliminar columna long_name
players_dataframe.drop('long_name', axis=1, inplace=True)
print(players_dataframe)

#Eliminar columna age
players_dataframe.drop(columns=['age'], inplace=True)
print(players_dataframe)

#Eliminar última columna
players_dataframe.drop(columns=players_dataframe.columns[-1], inplace=True)
print(players_dataframe)
