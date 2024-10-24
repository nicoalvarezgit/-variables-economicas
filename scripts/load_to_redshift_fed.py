import os
from dotenv import load_dotenv
import redshift_connector
import awswrangler as wr
import pandas as pd
from scripts import extract_data, transform_data

# Se cargan las variables del archivo .env
load_dotenv()

DATA_PATH=os.path.join(os.path.dirname(__file__), 'transformed_data_fed.csv')
REDSHIFT_TABLE = "redshift_table"
REDSHIFT_SCHEMA = "2024_nicolas_alvarez_julia_schema"

# Parámetros de conexión
conn_params = {
    'host': os.getenv('REDSHIFT_HOST'),
    'database': os.getenv('REDSHIFT_DB'),
    'user': os.getenv('REDSHIFT_USER'),  
    'password': os.getenv('REDSHIFT_PASSWORD'),
    'port': os.getenv('REDSHIFT_PORT'),
}


def load_to_redshift(transformed_csv: str, redshift_table: str, conn_params: dict): 
    #Cargo la data transformada del archivo parquet
    df= pd.read_csv(transformed_csv)

    try:
        # Se establece la conexión
        conn = redshift_connector.connect(**conn_params)

        #Cargo la data al Redshift table
        wr.redshift.to_sql(
            df=df,
            con=conn,
            table=redshift_table, 
            schema=REDSHIFT_SCHEMA, 
            mode="append",
            use_column_names=True, 
            index=False, 
            lock=True
        )

        print(f"Datos cargados exitosamente en la tabla {REDSHIFT_SCHEMA}.{redshift_table} en Redshift.")
        
    except Exception as e:
        print(f"Error en la conexión o carga de datos a Redshift: {e}")
    
    finally:
        if conn is not None:
            conn.close()
    
 
def main(data_path: str, redshift_table: str, conn_params: dict): #redshift_conn_string: str
    output_path = extract_data(data_path)
    transformed_csv = transform_data(output_path, data_path)
    load_to_redshift(transformed_csv, redshift_table, conn_params)

#Si se llama load_to_redshift como módulo, se corre la función
if __name__ == "__main__":
    load_to_redshift(DATA_PATH, REDSHIFT_TABLE, conn_params)