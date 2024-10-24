import os
import psycopg2

def create_dim_variable_table():
    # Conectar a Redshift utilizando las credenciales almacenadas en variables de entorno
    conn = psycopg2.connect(
        dbname=os.getenv('REDSHIFT_DB'),
        user=os.getenv('REDSHIFT_USER'),
        password=os.getenv('REDSHIFT_PASSWORD'),
        host=os.getenv('REDSHIFT_HOST'),
        port=os.getenv('REDSHIFT_PORT')
    )

    # Especificar el esquema donde se creará la tabla
    schema = '"2024_nicolas_alvarez_julia_schema"'

    # Consulta SQL para crear la tabla en el esquema especificado
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {schema}.dim_variable (
        variable_id VARCHAR (50) PRIMARY KEY,
        nombre_variable VARCHAR (255),
        fuente VARCHAR (50),
        tipo_variable VARCHAR (50),
        frecuencia VARCHAR (50)
    );
    """

    with conn.cursor() as cur:
        cur.execute(create_table_query)
        conn.commit()

    conn.close()

if __name__ == "__main__":
    create_dim_variable_table()