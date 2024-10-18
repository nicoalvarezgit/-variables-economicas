import os
import pandas as pd
import pyarrow
from datetime import datetime, timedelta


def transform_data(input_parquet: str, output_parquet: str):
    
    #Cargo la data cruda del archivo parquet
    df= pd.read_parquet(input_parquet)
    
    # Se formatean los valores de la columna 'fecha' en formato datetime y se le saca la hora
    df['fecha'] = pd.to_datetime(df['fecha'])  
    df['fecha'] = (df['fecha']).dt.date
    
    #Se elimina la columna 'cdSerie' que no aporta ningún valor, mantengo el idVariable
    df.drop('cdSerie', axis=1, inplace=True)
    
    #df.set_index('fecha', inplace=True)  # Usar la fecha como índice
    
    df = df.rename(columns={'idVariable': 'id', 'descripcion': 'variable'})  # Renombrar la columna de valor
        
    path = os.path.join(output_parquet, 'transformed_data.parquet')
    
    #Se guarda el archivo transormado en formato parquet
    df.to_parquet(path, index=True)

    print(f"Data transformada y guardada en {path}")
    return path

#Si se llama transform_data como módulo, se corre la función
if __name__ == "__main__":
    transform_data('data.parquet', '.')