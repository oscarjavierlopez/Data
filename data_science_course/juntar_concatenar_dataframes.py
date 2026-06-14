import pandas as pd 
df_movies = pd.read_csv("IMDb_movies.csv",encoding='latin1')[['imdb_title_id', 'title', 'year', 'genre', 'country']]
df_ratings = pd.read_csv("IMDb_ratings.csv",encoding='latin1')[['imdb_title_id', 'total_votes', 'mean_vote']]

#concatenar verticalmente dataframes
df1 = pd.DataFrame({'id': ['A', 'B', 'C', 'D'],
                    'age': [30, 23, 25, 22]})
df2 = pd.DataFrame({'id': ['E', 'F', 'G', 'F'],
                    'age': [40, 21, 19, 24]})
print(pd.concat([df1, df2], ignore_index=True))


"""
Extraer 50% del dataframe df_movies y concatenarlo verticalmente a df_movies en un
nuevo dataframe llamado df_samples
"""
print(pd.concat([df_movies, df_movies.sample(frac=0.5)]))

#Concatenar horizontalmente dataframes(Hace falta tener indices iguales)
print(pd.concat([df_movies.set_index('imdb_title_id'),df_ratings.set_index('imdb_title_id')],axis=1))

#Inner join de df_movies y df_ratings
print(df_movies.merge(df_ratings, on="imdb_title_id", how="inner"))

#Full join 
df1 = pd.DataFrame({'id': ['A', 'B', 'C', 'D'],
                    'age': [30, 23, 25, 22]})
df2 = pd.DataFrame({'id': ['C', 'D', 'E', 'F'],
                    'job': ['Doctor', 'Statistician',
                            'Accountant', 'Developer']})
print(df1.merge(df2, on="id", how="outer"))

#Full join exclusivo => muestra elementos que solo existen en un dataframe(los comunes no se muestran)
print(df1.merge(df2, on='id', how="outer", indicator=True).query('_merge != "both"')) #indicator es la columna _merge

#left join
print(df1.merge(df2, on='id', how='left'))

#left join exclusivo
print(df1.merge(df2, on='id', how='left', indicator=True).query('_merge == "left_only"'))

