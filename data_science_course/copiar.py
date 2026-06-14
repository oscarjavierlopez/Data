import pandas as pd
import numpy as np

players_dataframe = pd.read_csv('players_20.csv',encoding='latin1')
players_dataframe = players_dataframe[['short_name', 'long_name', 'age', 'dob', 'height_cm', 'weight_kg', 'nationality', 'club']]
players_dataframe = players_dataframe.set_index('short_name')

"""
La copia es un objeto distinto, por lo tanto si se cambian valores en la copia solo se reflejan en la copia y si se cambian en 
el original solo se reflejan en el original

Si hicieramos players_dataframe_copy =  players_dataframe serían el mismo objeto y lo que se modifique en uno se modificará en otro
"""

players_dataframe_copy =  players_dataframe.copy()
players_dataframe_copy['age'] = 20
print(players_dataframe)
print(players_dataframe_copy)