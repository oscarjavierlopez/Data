import pandas as pd

players_dataframe = pd.read_csv('players_20.csv',encoding='latin1')
players_dataframe = players_dataframe[['short_name', 'long_name', 'age', 'dob', 'height_cm', 'weight_kg', 'nationality', 'club']]
players_dataframe = players_dataframe.set_index('short_name')

"""
dataframe.iloc[indice(s), col(s)]
Selecciona elementos por la posición numérica de su índice o la posicion numerica de su columna
"""

#Obtener el tamaño de Messi
messi_height_cm = players_dataframe.iloc[0, 3]
print(messi_height_cm)

#Obtener toda la data de Messi y Ronaldo
messi_cristiano_data = players_dataframe.iloc[[0,1]]
print(messi_cristiano_data)

#Obtener tamaño y peso demessi y ronaldo
messi_ronaldo_weight_height = players_dataframe.iloc[[0,1], [3,4]]
print(messi_ronaldo_weight_height)

