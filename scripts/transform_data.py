import os
import pandas as pd
import pyarrow

def transform_data(input_parquet: str, output_parquet: str):
    #Cargo la data cruda del archivo parquet
    df= pd.read_parquet(input_parquet)

   # Expandimos la columna con el diccionario de variables principales
    df_normalizado = pd.json_normalize(df['variables'])

# Agregar la columna de fecha al nuevo DataFrame normalizado
    df_transformado = pd.concat([df[['fecha']], df_normalizado], axis=1)

    path = os.path.join(output_parquet, 'transformed_data.parquet')
    
    #Se guarda el archivo transormado en formato parquet
    df_transformado.to_parquet(path, index=True)

    print(f"Data transformada y guardada en {path}")
    return path

#Ejecutable
transform_data('data.parquet','transformed_data.parquet')
