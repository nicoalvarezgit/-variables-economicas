import os
import pandas as pd
from datetime import datetime, timedelta


def transform_data(input_parquet: str, output_parquet: str):
    
    #Cargo la data cruda del archivo parquet
    df= pd.read_parquet(input_parquet)
    
    # Se formatean los valores de la columna 'fecha' en formato datetime y se le saca la hora
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  
    
    #Se elimina la columna 'cdSerie' que no aporta ningún valor, mantengo el idVariable
    df.drop('cdSerie', axis=1, inplace=True)
    
    #df.set_index('fecha', inplace=True)  # Usar la fecha como índice
    
    df = df.rename(columns={'idVariable': 'id', 'descripcion': 'variable'})  # Renombrar la columna de valor

    variables_a_eliminar = [4, 30, 31, 32, 40, 43] #se forma una tupla con los valores de los ids de variables que no interesan al análisis. 
    df = df[~df['id'].isin(variables_a_eliminar)]

    #Se crea el path nuevamente para guardar el dataframe transformado
    path = os.path.join(output_parquet, 'transformed_data.parquet')
    
    #Se guarda el archivo transormado en formato parquet
    df.to_parquet(path, index=True)

    print(f"Data transformada y guardada en {path}")
    return path

#Si se llama transform_data como módulo, se corre la función
if __name__ == "__main__":
    transform_data('data.parquet', '.')

