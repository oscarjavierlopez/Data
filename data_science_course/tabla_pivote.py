import pandas as pd

"""
Una tabla pivote (pivot table) es una forma de reorganizar y resumir datos para analizarlos mejor.
"""

df_gdp = pd.read_csv('gdp.csv',encoding='latin1')

#Mostrar el gdp de cada país en cada año
df_gdp_pivot = df_gdp.pivot_table(index="country", values="gdppc", columns="year")
print(df_gdp_pivot)



df_supermarket_sales = pd.read_excel('supermarket_sales.xlsx')

#Sacar la cantidad de articulos y el total gastado de hombres vs mujeres
df_supermarket_sales_pivot = df_supermarket_sales.pivot_table(index="Gender", aggfunc="sum", values=["Quantity","Total"])
print(df_supermarket_sales_pivot)

#Exportar tabla pivote
df_supermarket_sales_pivot.to_excel("supermarket_sales_pivot.xlsx")