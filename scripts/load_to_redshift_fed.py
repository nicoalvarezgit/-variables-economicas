import os
from dotenv import load_dotenv
import redshift_connector
import awswrangler as wr
import pandas as pd
from typing import Any, Dict

# Se cargan las variables del archivo .env
load_dotenv()

destination_table = "fact_table"
REDSHIFT_SCHEMA = "2024_nicolas_alvarez_julia_schema"

# Parámetros de conexión
conn_params = {
    'host': os.getenv('REDSHIFT_HOST'),
    'database': os.getenv('REDSHIFT_DB'),
    'user': os.getenv('REDSHIFT_USER'),  
    'password': os.getenv('REDSHIFT_PASSWORD'),
    'port': os.getenv('REDSHIFT_PORT'),
}


def load_to_redshift_fed(ti: Any, destination_table: str, conn_params: dict[str, str]) -> None: 
    """Carga los datos transformados a la fact_table de Redshift.

    Args:
        ti (Any): `TaskInstance` de Airflow para obtener el DataFrame desde xcom.
        destination_table (str): Referencia a la fact_table en Redshift.
        conn_params (Dict[str, str]): Parámetros de conexión a la base de datos Redshift.

    Raises:
        Exception: Si ocurre un error en la conexión o en la carga de datos a Redshift.
    """
    
    ## Obtener el DataFrame transformado desde xcom
    data = ti.xcom_pull(task_ids='transform_data_fed_task', key='transformed_data')
    if data is None:
        raise ValueError("No se encontró data transformada en xcom para 'transformed_data'")
    df= pd.DataFrame(data)

    numeric_columns = ['valor']  # Cambia según los nombres de las columnas numéricas en tu DataFrame
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
        
    try:
        # Se establece la conexión
        conn = redshift_connector.connect(**conn_params)

        #Cargo la data al Redshift table
        wr.redshift.to_sql(
            df=df,
            con=conn,
            table=destination_table, 
            schema=REDSHIFT_SCHEMA, 
            mode="append",
            use_column_names=True, 
            index=False, 
            lock=True
        )

        print(f"Datos cargados exitosamente en la tabla {REDSHIFT_SCHEMA}.{destination_table} en Redshift.")
        
    except Exception as e:
        raise Exception(f"Error en la conexión o carga de datos a Redshift: {e}")
    
    finally:
        if conn in locals():
            conn.close()
            print("Conexión a Redshift cerrada")
