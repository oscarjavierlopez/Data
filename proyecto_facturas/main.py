from ETL.extract import crear_dataframe

def main():
    df_facturas = crear_dataframe("Data/bronze")
    print(df_facturas)

if __name__ == "__main__":
    main()