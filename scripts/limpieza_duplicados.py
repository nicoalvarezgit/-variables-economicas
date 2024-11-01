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

        # Paso 1: Crear la tabla temporal
        create_temp_table_query = f"""
        CREATE TEMP TABLE temp_table AS
        SELECT *, ROW_NUMBER() OVER(
            PARTITION BY {", ".join(columns)} ORDER BY {columns[0]}
        ) AS row_num
        FROM "{REDSHIFT_SCHEMA}"."{redshift_table}";
        """

        # Paso 2: Eliminar duplicados usando la tabla temporal
        delete_duplicates_query = f"""
        DELETE FROM "{REDSHIFT_SCHEMA}"."{redshift_table}"
        USING temp_table
        WHERE "{REDSHIFT_SCHEMA}"."{redshift_table}".{columns[0]} = temp_table.{columns[0]}
        AND temp_table.row_num > 1;
        """

        # Paso 3: Eliminar la tabla temporal
        drop_temp_table_query = "DROP TABLE temp_table;"

        # Ejecutar los comandos de forma secuencial
        cursor = conn.cursor()
        cursor.execute(create_temp_table_query)
        cursor.execute(delete_duplicates_query)
        cursor.execute(drop_temp_table_query)
        conn.commit()
        cursor.close()
    except Exception as e:
        raise Exception(f"Error en la limpieza de duplicados en Redshift: {e}")
    
    finally:
        if conn is not None:
            conn.close()

# Ejemplo de ejecución
if __name__ == "__main__":
    columns = ["variable_id", "fecha", "valor", "fecha_dato"]  # Lista completa de columnas
    limpieza_duplicados(REDSHIFT_TABLE, conn_params, columns)
