import pandas as pd
import numpy as np

players_dataframe = pd.read_csv('players_20.csv',encoding='latin1')
players_dataframe = players_dataframe[['short_name', 'long_name', 'age', 'dob', 'height_cm', 'weight_kg', 'nationality', 'club']]
players_dataframe = players_dataframe.set_index('short_name')

"""
dataframe.loc[indice(s), col(s)]
Selecciona elementos por el valor de su indice
"""
#Extraer todos los datos de L.Messi 
messi_data = players_dataframe.loc['L. Messi']
print(messi_data)

#extraer la edad de L.Messi
messi_age = players_dataframe.loc['L. Messi', 'age']
print(f'La edad de Messi es {messi_age} años')

#Obtener el peso de Cristiano Ronaldo 
cristiano_weight = players_dataframe.loc['Cristiano Ronaldo', 'weight_kg']
print(f'El peso de Cristiano es {cristiano_weight}kg')

#Obtener todas las filas dentro de la columna height_cm
height_cm = players_dataframe.loc[: , 'height_cm']
print(height_cm)

#Obtener los datos de Messi y Cristiano
messi_cristiano_data = players_dataframe.loc[['L. Messi', 'Cristiano Ronaldo']]
print(messi_cristiano_data)

#Obtener el tamaño de Messi y de Ronaldo
messi_cristiano_height = players_dataframe.loc[['L. Messi', 'Cristiano Ronaldo'], 'height_cm']
print(messi_cristiano_height)

#obtener el tamaño y peso de Messi
messi_height_weight = players_dataframe.loc['L. Messi', ['height_cm', 'weight_kg']]
print(messi_height_weight)

#obtener el tamaño y peso de Messi y Ronaldo
messi_ronaldo_weight_height = players_dataframe.loc[['L. Messi', 'Cristiano Ronaldo'], ['height_cm', 'weight_kg']]
print(messi_ronaldo_weight_height)

#Obtener height_cm, weight_kg, nationality, club de Messi y Ronaldo
messi_cristiano_data = players_dataframe.loc[['L. Messi', 'Cristiano Ronaldo'], 'height_cm': 'club']
print(messi_cristiano_data)

#Obtener los nombres del top 10 de jugadores
top10 = players_dataframe.index[0:10]
top10_names = players_dataframe.loc[top10, 'long_name']
print(top10_names)

#Seleccionar jugadores con height_cm > 180
tall_players = players_dataframe.loc[players_dataframe['height_cm'] > 180]
print(tall_players)

#Seleccionar jugadores con height_cm > 180 y que sean de Argentina
tall_argentina_plyers = players_dataframe.loc[(players_dataframe['height_cm'] > 180) & (players_dataframe['nationality'] == 'Argentina')]
print(tall_argentina_plyers)

#Hacer que la estatura de Messi sean 175
players_dataframe.loc['L. Messi', 'height_cm'] = 175
print(players_dataframe)

#Dar a todas las columnas del último jugador valor null
players_dataframe.iloc[-1] = np.nan
print(players_dataframe)

#Poner altura a 0 a todos los players que tengan height_cm>180
players_dataframe.loc[players_dataframe['height_cm']>180, 'height_cm'] = 0
print(players_dataframe)