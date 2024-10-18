import os
import pandas as pd
import pyarrow
from datetime import datetime, timedelta


def transform_data(input_parquet: str, output_parquet: str):
    #Cargo la data cruda del archivo parquet
    df= pd.read_parquet(input_parquet)

    df['fecha'] = pd.to_datetime(df['fecha'])  # Asegurarse de que 'fecha' esté en formato de fecha
    df.set_index('fecha', inplace=True)  # Usar la fecha como índice
    df_transformado = df[['valor']].rename(columns={'valor': f'variable_{id_variable}'})  # Renombrar la columna de valor
        
    path = os.path.join(output_parquet, 'transformed_data.parquet')
    
    #Se guarda el archivo transormado en formato parquet
    df_transformado.to_parquet(path, index=True)

    print(f"Data transformada y guardada en {path}")
    return path

#Ejecutable
transform_data('data.parquet','transformed_data.parquet')
