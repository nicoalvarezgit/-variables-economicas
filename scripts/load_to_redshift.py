import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import psycopg2
from psycopg2 import sql
import pandas as pd
from scripts import extract_data, transform_data

# Se cargan las variables del archivo .env
load_dotenv()

# Obtener las credenciales desde las variables de entorno
user = os.getenv('REDSHIFT_USER')
password = os.getenv('REDSHIFT_PASSWORD')
host = os.getenv('REDSHIFT_HOST')
port = os.getenv('REDSHIFT_PORT')
database = os.getenv('REDSHIFT_DB') 

#Llamo al directorio actual
current_dir= os.path.dirname(os.path.realpath(__file__))
# Voy hacia la carpeta anterior
parent_dir = os.path.join(current_dir, os.pardir)

#Defino las constantes.
REDSHIFT_CONN_STRING = f"postgresql://{user}:{password}@{host}:{port}/{database}"
DATA_PATH=os.path.abspath(parent_dir)
REDSHIFT_TABLE = "redshift_table"


def load_to_redshift(transformed_csv: str, redshift_table: str, redshift_conn_string: str):
    #Cargo la data transformada del archivo parquet
    df= pd.read_csv(transformed_csv, index_col=0)

    #Se crea el engine de sqlalchemy para redshift
    engine= create_engine(redshift_conn_string)

    try:
         #Cargo la data al Redshift table
        df.to_sql(redshift_table, engine, if_exists='append', index=True, method='multi')

        with engine.begin() as connection:
            print("Conexión exitosa a Redshift")
            # Probar la conexión con una consulta
            result = connection.execute("SELECT current_date")
            for row in result:
                print(f"El día actual en Redshift es: {row[0]}")

    except Exception as e:
        print(f"Error en la conexión o carga de datos a Redshift: {e}")
    
    finally:
        engine.dispose()
    
 
def main(data_path: str, redshift_table: str, redshift_conn_string: str):
    output_path = extract_data(data_path)
    transformed_data_path = transform_data (output_path, data_path)
    load_to_redshift(transformed_data_path, redshift_table, redshift_conn_string)

#Si se llama load_to_redshift como módulo, se corre la función
if __name__ == "__main__":
    load_to_redshift(DATA_PATH, REDSHIFT_TABLE, REDSHIFT_CONN_STRING)