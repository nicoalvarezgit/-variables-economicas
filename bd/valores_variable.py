import os
import psycopg2
from psycopg2 import sql


try:
    # Establecer la conexión
    conn = psycopg2.connect(**conn_params)
    cur = conn.cursor()

    # Ejecutar la inserción
    for dato in datos:
        cur.execute(insert_query, dato)

    # Confirmar los cambios
    conn.commit()
    print("Datos insertados correctamente en dim_variable.")

except Exception as e:
    print(f"Error al insertar datos: {e}")

finally:
    # Cerrar la conexión
    if cur:
        cur.close()
    if conn:
        conn.close()

def valores_variable():
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

    # Consulta de inserción
    insert_query = """
        INSERT INTO dim_variable (variable_id, nombre_variable, fuente, unidad, tipo_variable, frecuencia) VALUES
        (%s, %s, %s, %s, %s, %s)
    """

    # Datos para insertar
    datos = [
        ('bcra_tasa_interes', 'Tasa de Interés BCRA', 'BCRA', 'porcentaje', 'monetaria', 'diaria'),
        ('fed_m2_supply', 'M2 Money Supply', 'FED', 'billones USD', 'monetaria', 'mensual')
    ]

    #Se arma el cursor    
    cur = conn.cursor()

    # Ejecutar la inserción
    for dato in datos:
        cur.execute(insert_query, dato)

    # Confirmar los cambios
    conn.commit()
    print("Datos insertados correctamente en dim_variable.")

    conn.close()


if __name__ == "__main__":
    valores_variable()