import pandas as pd

df_netflix_titles = pd.read_csv('netflix_titles.csv', encoding='latin1')


#Obtener el número de elementos nulos del dataframe
print(df_netflix_titles.isnull().sum())

#Obtener porcentaje de filas faltantes en cada columna
for column in df_netflix_titles.columns:
    print(f'{column}: {df_netflix_titles[column].isnull().mean()}')

#Eliminar filas que tengan la columna director nula
#df_netflix_titles.drop(index=df_netflix_titles[df_netflix_titles['director'].isnull()].index ,inplace=True, axis=0)
df_netflix_titles_without_null = df_netflix_titles.dropna(axis=0, subset='director')
print(df_netflix_titles_without_null)

"""
Con el método fillna NO USAR inplace=True
"""

#Reemplazar valores nulos de rating con la moda
print(df_netflix_titles[df_netflix_titles['rating'].isnull()])
df_netflix_titles['rating'] = df_netflix_titles['rating'].fillna(df_netflix_titles['rating'].mode()[0])#El valor con el que reemplazamos debe ser un numero o cadena
print(df_netflix_titles.loc[5989, 'rating'])


#Reemplazar valores nulos de duration con numeros arbitrarios
df_netflix_titles['duration'] = df_netflix_titles['duration'].fillna('0')
print(df_netflix_titles)

#forward y backward: Reemplazan valores nulos con el que tenga la fila anterior o posterior
#df_netflix_titles['director'] = df_netflix_titles['director'].ffill()
df_netflix_titles['director'] = df_netflix_titles['director'].bfill()
print(df_netflix_titles['director'])

#extraer datos de una columna con split y extract
df_movies = df_netflix_titles.query('type == "Movie"')
df_movies['minutes'] = df_movies['duration'].str.split(' ', expand=True)[0].astype(int) #expand convierte el resultado en un dataframe(sino sería una serie y acceder a los valores sería más difícil)
print(df_movies)

df_movies['year_added'] = df_movies['date_added'].str.extract('(\d{4})')
print(df_movies)

#Encontrar valores atípicos en la duraicion(minutes): <30 o mayor a 200
df_movies.query('minutes>30 and minutes<200',inplace=True)
print(df_movies)


#Pasar la columna title a minusculas, mayusculas y capitalizado
print(df_movies['title'].str.lower())
print(df_movies['title'].str.upper())
print(df_movies['title'].str.title())

#Eliminar espacios en blanco de inicio y final de la columna title
df_movies['title'] = df_movies['title'].str.strip()
print(df_movies['title'])

#Eliminar signos de puntuación en la columna title
df_movies['title'] = df_movies['title'].str.replace('[.,;:¡!¿?()\[\]{}"-]', '', regex=True)
print(df_movies['title'])

