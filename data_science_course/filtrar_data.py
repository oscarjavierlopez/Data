import pandas as pd

laptop_dataframe = pd.read_csv('laptop_price.csv',encoding='latin1')

#Filtrar laptops con precio > 2000
print(laptop_dataframe[laptop_dataframe['Price_euros'] > 2000])

#Obtener cantidad de ordenadores por cada precio
print(laptop_dataframe[laptop_dataframe['Price_euros'] > 2000].value_counts('Price_euros'))

"""
and -> &
or -> |
"""
#Filtrar laptops con precio>2000€ y cuya compañía sea 'Apple'
print(laptop_dataframe[(laptop_dataframe['Price_euros'] > 2000) & (laptop_dataframe['Company'] == 'Apple')])

#Filtrar laptops de la marca 'Apple' o de la marca 'HP'
print(laptop_dataframe[(laptop_dataframe['Company'] == 'HP') |  (laptop_dataframe['Company'] == 'Apple')])

#Filtrar laptops de la marca 'Apple' o de la marca 'HP' con isin
print(laptop_dataframe[laptop_dataframe['Company'].isin(['Apple', 'HP'])])

#Filtrar laptops de la marca 'Apple' o de la marca 'HP' con isin cuyo TypeName sea 'Book' o 'Ultrabook'
print(laptop_dataframe[laptop_dataframe['Company'].isin(['Apple', 'HP']) & laptop_dataframe['TypeName'].isin(['Book', 'Ultrabook'])])



players_dataframe = pd.read_csv('players_20.csv',encoding='latin1')
players_dataframe = players_dataframe[['short_name', 'long_name', 'age', 'dob', 'height_cm', 'weight_kg', 'nationality', 'club']]
players_dataframe = players_dataframe.set_index('short_name')

#Filtrar jugadores mayores de 34 años cuya nacionalidad sea Italia
print(players_dataframe.query('age>34 and nationality=="Italy"'))

#Seleccionar los jugadores con altura > 1.8m
players_dataframe['height_cm'] = players_dataframe['height_cm'] / 100
print(players_dataframe.query('height_cm>1.80'))

#Seleccionar jugadores que nacieron antes de 1990
players_dataframe['yob'] = players_dataframe['dob'].str[:4].astype(int)
old_players_dataframe = players_dataframe.query('yob<1990')
old_players_dataframe.drop(columns=['yob'], inplace=True)
print(old_players_dataframe)

#Extraer el año de nacimiento de los jugadores
players_dataframe['yob'] =  pd.to_datetime(players_dataframe['dob']).dt.year
print(players_dataframe)

