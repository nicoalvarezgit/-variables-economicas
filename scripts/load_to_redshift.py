import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy import text
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


def load_to_redshift(transformed_parquet: str, redshift_table: str, redshift_conn_string: str):
    #Cargo la data transformada del archivo parquet
    df= pd.read_parquet(transformed_parquet)

    #Se crea el engine de sqlalchemy para redshift
    engine= create_engine(redshift_conn_string)

    #Cargo la data al Redshift table
    df.to_sql(redshift_table, engine, if_exists='replace', index=True, method='multi')

    try:    
        with engine.begin() as connection:
            print("Conexión exitosa a Redshift")
            #Testeo con una query la conexión
            result = connection.execute("SELECT current_date")
            for row in result:
                print("El día actual en Redshift es": row[0])
    except Exception as e:
        print(f"Error en la conexión a Redshift: {e}")
     
    
    #print(f"Data cargada en Redshift table {redshift_table}")
    
def main(data_path: str, redshift_table: str, redshift_conn_string: str):
    output_path = extract_data(data_path)
    transformed_data_path = transform_data (output_path, data_path)
    load_to_redshift(transformed_data_path, redshift_table, redshift_conn_string)

#Si se llama load_to_redshift como módulo, se corre la función
if __name__ == "__main__":
    load_to_redshift(DATA_PATH, REDSHIFT_TABLE, REDSHIFT_CONN_STRING)