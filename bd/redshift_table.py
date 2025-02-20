import os
import psycopg2

def create_redshift_table():
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
    CREATE TABLE IF NOT EXISTS {schema}.redshift_table (
        id INT,
        variable TEXT,
        fecha DATE,
        valor NUMERIC,
        fecha_dato DATE
    );
    """

    with conn.cursor() as cur:
        cur.execute(create_table_query)
        conn.commit()

    conn.close()

if __name__ == "__main__":
    create_redshift_table()
