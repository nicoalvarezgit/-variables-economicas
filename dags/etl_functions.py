import os
from datetime import datetime

from sqlalchemy import create_engine
import requests
import pandas as pd
from airflow import 

REDSHIFT_CONN_STRING = f"postgresql://{user}:{password}@{host}:{port}/{database}"

def extract_data(output_parquet: str):
    #Pongo la data sobre la API
    url = "https://api.bcra.gob.ar/estadisticas/v2.0/principalesvariables"
    response = requests.get(url, verify=False)
    data = response.json()

    #Lo convierto en data frame
    df = pd.DataFrame(data)

    path = os.path.join(output_parquet, 'data.parquet')
    #Guardo el archivo parquet
    df.to_parquet(path)
    if df.empty:
        raise AirflowSkipException
    print(f"Data extraída y guardada en {path}")
    return path

def transform_data(input_parquet: str, output_parquet: str):
    #Cargo la data cruda del archivo parquet
    df= pd.read_parquet(input_parquet)

    #Acá le realizo las transformaciones que quiero al df
    df_transformed = df[df[''] > 5] #Ejemplo de transofrmación

    path = os.path.join(output_parquet, 'transformed_data.parquet')
    #Se guarda el archivo transormado en formato parquet
    df_transformed.to_parquet(path, index=True)

    print(f"Data transformada y guardada en {path}")
    return path

def load_to_redshift(transformed_parquet: str, redshift_table: str, redshift_conn_string: str):
    #Cargo la data transformada del archivo parquet
    df= pd.read_parquet(transformed_parquet)

    #Se crea el engine de sqlalchemy para redshift
    engine= create_engine(redshift_conn_string)

    #Cargo la data al Redshift table
    df.to_sql(redshift_table, engine, if_exists='replace', index=True, method='multi')

    print(f"Data cargada en Redshift table {redshift_table}")
    
def main(data_path: str, redshift_table: str, redshift_conn_string: str):
    output_path = extract_data(data_path)
    transformed_data_path = transform_data (output_path, data_path)
    load_to_redshift(transformed_data_path, redshift_table, redshift_conn_string)