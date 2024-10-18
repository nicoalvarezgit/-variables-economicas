import os
from datetime import datetime

from dotenv import load_dotenv
from sqlalchemy import create_engine
import requests
import pandas as pd

# Se cargan las variables del archivo .env
load_dotenv()

# Obtener las credenciales desde las variables de entorno
user = os.getenv('REDSHIFT_USER')
password = os.getenv('REDSHIFT_PASSWORD')
host = os.getenv('REDSHIFT_HOST')
port = os.getenv('REDSHIFT_PORT')
database = os.getenv('REDSHIFT_DB') 


REDSHIFT_CONN_STRING = f"postgresql://{user}:{password}@{host}:{port}/{database}"
DATA_PATH=os.path.dirname(os.path.realpath(__file__))
REDSHIFT_TABLE = "redshift_table"


REDSHIFT_CONN_STRING = f"postgresql://{user}:{password}@{host}:{port}/{database}"

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