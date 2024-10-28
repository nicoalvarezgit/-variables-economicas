import os
from dotenv import load_dotenv
import redshift_connector
import awswrangler as wr

# Cargar las variables del archivo .env
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

def limpieza_duplicados(redshift_table: str, conn_params: dict, columns: list):
    """
    Limpia duplicados en Redshift eliminando filas con duplicados en todas las columnas especificadas.
    """
    try:
        # Conectar a Redshift
        conn = redshift_connector.connect(**conn_params)

        # Ejecutar el comando DELETE para eliminar duplicados en todas las columnas
        delete_query = f"""
        DELETE FROM {REDSHIFT_SCHEMA}.{redshift_table}
        USING (
            SELECT {", ".join(columns)}, MIN(ctid) as min_ctid
            FROM {REDSHIFT_SCHEMA}.{redshift_table}
            GROUP BY {", ".join(columns)}
            HAVING COUNT(*) > 1
        ) AS duplicates
        WHERE {REDSHIFT_SCHEMA}.{redshift_table}.ctid != duplicates.min_ctid
        AND {" AND ".join([f"{REDSHIFT_SCHEMA}.{redshift_table}.{col} = duplicates.{col}" for col in columns])};
        """
        wr.redshift.execute_sql(delete_query, con=conn)
        print(f"Duplicados eliminados exitosamente en {REDSHIFT_SCHEMA}.{redshift_table}.")

    except Exception as e:
        raise Exception(f"Error en la limpieza de duplicados en Redshift: {e}")
    
    finally:
        if conn is not None:
            conn.close()

# Ejemplo de ejecución
if __name__ == "__main__":
    columns = ["variable_id", "fecha", "valor", "fecha_dato"]  # Lista completa de columnas
    limpieza_duplicados(REDSHIFT_TABLE, conn_params, columns)
