import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display,HTML
import plotly.express as px

df_population = pd.read_csv('population_total.csv', encoding='latin1')
df_population.dropna(inplace=True) #Eliminamos valores nulos

df_population_pivot = df_population.pivot_table(values="population", index="year", columns="country", aggfunc="sum")
df_population_pivot = df_population_pivot[["United States", "China", "India", "Indonesia", "Brazil"]]

#Grafico de lineas
#df_population_pivot.plot(kind="line", xlabel="Año", ylabel="Poblacion", title="Poblacion 1995-2020", figsize=(8,4))

#Grafico de lineas dinámico
# fig = px.line(
#     df_population_pivot,
#     title="Población 1995-2020",
#     labels={
#         "x": "Año",
#         "value": "Población",
#         "variable": "País"
#     }
# )

#Grafico de barras para el año 2020
# df_population_pivot_2020 = df_population_pivot[df_population_pivot.index.isin([2020])].T
# print(df_population_pivot_2020)
# df_population_pivot_2020.plot(kind="bar", xlabel="Ciudad", ylabel="Poblacion", title="Poblacion 2020")

#Grafico de barras dinamico
# df_population_pivot_2020 = df_population_pivot[df_population_pivot.index.isin([2020])].T
# fig = px.bar(df_population_pivot_2020, title="Poblacion 2020", )


#Grafico de barras para año 2019 y 2020
# df_population_pivot_2020 = df_population_pivot[df_population_pivot.index.isin([2019, 2020])].T
# print(df_population_pivot_2020)
# df_population_pivot_2020.plot(kind="bar", xlabel="Ciudad", ylabel="Poblacion", title="Poblacion 2020")

#Piechart para el año 2020
# df_population_pivot_2020 = df_population_pivot[df_population_pivot.index.isin([2020])].T
# df_population_pivot_2020.rename(columns={2020: "2020"}, inplace=True)
# print(df_population_pivot_2020)
# df_population_pivot_2020.plot(kind="pie", title="Poblacion 2020", y="2020")

#Piechart dinamico
# df_population_pivot_2020 = df_population_pivot[df_population_pivot.index.isin([2020])].T
# df_population_pivot_2020.rename(columns={2020: "2020"}, inplace=True)
# fig = px.pie(df_population_pivot_2020, title="Poblacion 2020", values="2020", names=df_population_pivot_2020.index,)

#Boxplot de united states
# df_population_pivot[["United States"]].plot(kind="box", ylabel="Poblacion", title="Poblacion en EEUU")

# #Boxplot dinamico
# fig = px.box(df_population_pivot[["United States"]], title="Poblacion en EEUU")

#Boxplot de varios paises
#df_population_pivot.plot(kind="box",xlabel="paises", ylabel="Poblacion", title="Poblacion en países")


#Boxplot dinamico de varios paises
#fig = px.box(df_population_pivot, title="Poblacion en países")

#Histograma para china y EEUU
#df_population_pivot[["China", "United States"]].plot(kind="hist" )

#Histograma dinamico
#fig = px.histogram(df_population_pivot[["China", "United States"]])

#Scaterplot del dataframe original
# df_sample = df_population.query("country=='United States' or country=='China' or country=='India' or country=='Indonesia' or country=='Brazil'")
# df_sample.plot(kind="scatter", x="year", y="population", s=80)

#Scater plot dinamico
df_sample = df_population.query("country=='United States' or country=='China' or country=='India' or country=='Indonesia' or country=='Brazil'")
fig = px.scatter(df_sample, x="year", y="population")

#guardar grafico
# df_population_pivot.plot(kind="line", xlabel="Año", ylabel="Poblacion", title="Poblacion 1995-2020", figsize=(8,4))
# plt.savefig("lineplot.png")

#plt.show()
fig.show()