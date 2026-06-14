import pandas as pd

players_dataframe = pd.read_csv('players_20.csv',encoding='latin1')
players_dataframe = players_dataframe[['short_name', 'long_name', 'age', 'dob', 'height_cm', 'weight_kg', 'nationality', 'club']]
players_dataframe = players_dataframe.set_index('short_name')

#Extraer 10 jugadores aleatorios
print(players_dataframe.sample(10))

"""
Con random_state>0 los jugadores serán seleccionados aleatoriamente pero serán siempre los mismos 10 jugadores en todo el script
"""
#Extraer las nacionalidades de 10 jugadores aleatorios y que sean en todo el script los mismos jugadores
print(players_dataframe['nationality'].sample(10, random_state=1))

#Mostrar un 20% del dataframe(aleatorio)
print(players_dataframe.sample(frac=0.2))

#Incrementar el dataframe con filas aleatorias del mismo
print(players_dataframe.sample(frac=2, replace=True))



"""
El metodo apply se utiliza para aplicar una función y transformar datos
"""

#Obtener IMC de los jugadores
def calcular_imc(row):
    return row['weight_kg'] / (row['height_cm']/100)**2

print(players_dataframe.apply(calcular_imc, axis=1))

#Transformar height a cm
players_dataframe['height_cm'] = players_dataframe['height_cm'] / 100
print(players_dataframe)