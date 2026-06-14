import pandas as pd
import numpy as np

laptop_dataframe = pd.read_csv('laptop_price.csv',encoding='latin1')

#Crear columna price_categoria que sea 'Caro' o 'Barato' según si el PC cuesta mas o menos de 2000€
laptop_dataframe['Price_categoria'] = np.where(laptop_dataframe['Price_euros'] > 2000, 'Caro', 'Barato')
print(laptop_dataframe)


#Crear columna Screen_size que sea 'Grande' si es mas de 15inches y 'Pequeña' en caso contrario y mostrar los 5 primeros valores del dataframe
laptop_dataframe['Screen_size'] = np.where(laptop_dataframe['Inches'] > 15, 'Grande', 'Pequeña')
print(laptop_dataframe.head(5))

#contar valores en Screen_size
print(laptop_dataframe.value_counts('Screen_size'))

#Crear columna price_categoria que sea Barato(<800), Caro(entre 800 y 2000) o Muy caro(>2000) con np.select
conditions = [laptop_dataframe['Price_euros'] <= 800, (laptop_dataframe['Price_euros'] > 800) & (laptop_dataframe['Price_euros'] < 2000), laptop_dataframe['Price_euros'] >= 2000]
values = ['Barato', 'Caro', 'Muy caro']
laptop_dataframe['Price_categoria'] = np.select(conditions, values, default='Sin categoria')
print(laptop_dataframe)
print(laptop_dataframe.value_counts('Price_categoria'))