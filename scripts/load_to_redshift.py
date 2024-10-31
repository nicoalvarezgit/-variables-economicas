import os
from dotenv import load_dotenv
import redshift_connector
import awswrangler as wr
import pandas as pd


# Se cargan las variables del archivo .env
load_dotenv()

REDSHIFT_TABLE = "fact_table"
REDSHIFT_SCHEMA = "2024_nicolas_alvarez_julia_schema"

# Parámetros de conexión
conn_params = {
    'host': os.getenv('REDSHIFT_HOST'),
    'database': os.getenv('REDSHIFT_DB'),
    'user': os.getenv('REDSHIFT_USER'),  
    'password': os.getenv('REDSHIFT_PASSWORD'),
    'port': os.getenv('REDSHIFT_PORT'),
}


def load_to_redshift(df_transformado: pd.DataFrame, conn_params: dict): 
    """
    Carga el DataFrame transformado a la tabla fact_table en Redshift.

    Args:
        df_transformado (pd.DataFrame): DataFrame transformado.
        conn_params (dict): Parámetros personales de conexión a Redshift.

    Raises:
        Exception: Si ocurre un error de conexión o carga de datos.
    """

    try:
        # Se establece la conexión
        conn = redshift_connector.connect(**conn_params)

        #Cargo la data al Redshift table
        wr.redshift.to_sql(
            df=df_transformado,
            con=conn,
            table=REDSHIFT_TABLE, 
            schema=REDSHIFT_SCHEMA, 
            mode="append",
            use_column_names=True, 
            index=False, 
            lock=True
        )

        print(f"Datos cargados exitosamente en la tabla {REDSHIFT_SCHEMA}.{REDSHIFT_TABLE} en Redshift.")
        
    except Exception as e:
        raise Exception(f"Error en la conexión o carga de datos a Redshift: {e}")
    
    finally:
        if conn is not None:
            conn.close()
    
 
