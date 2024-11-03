import os
import pandas as pd
import awswrangler as wr
from datetime import datetime
import redshift_connector

# Define el rango de fechas
start_date = "2015-01-01"
end_date = "2024-09-30"

# Genera el DataFrame con el rango de fechas y desglosa en columnas adicionales
dates = pd.date_range(start=start_date, end=end_date, freq='D')
df_fecha = pd.DataFrame({
    'fecha_dato': dates,
    'año': dates.year,
    'mes': dates.month,
    'nombre_mes': dates.strftime('%B'),
    'dia': dates.day,
    'nombre_dia_semana': dates.strftime('%A'),
    'trimestre': dates.quarter
})

# Configura los parámetros de conexión a Redshift
conn_params = {
    'host': os.getenv('REDSHIFT_HOST'),
    'database': os.getenv('REDSHIFT_DB'),
    'user': os.getenv('REDSHIFT_USER'),
    'password': os.getenv('REDSHIFT_PASSWORD'),
    'port': os.getenv('REDSHIFT_PORT'),
}

# Cargar el DataFrame en Redshift en la tabla dim_fecha
try:
    conn = redshift_connector.connect(**conn_params)
    print("Conexión a Redshift establecida con éxito")

    wr.redshift.to_sql(
        df=df_fecha,
        con=conn,
        table='dim_fecha',
        schema='2024_nicolas_alvarez_julia_schema',  # Ajusta el esquema según corresponda
        mode="append",  # Usa "append" para agregar los datos si ya existe la tabla
        index=False,
        lock=True
    )

    print("Datos de fechas cargados exitosamente en la tabla dim_fecha en Redshift.")

except Exception as e:
    raise Exception(f"Error en la conexión o carga de datos a Redshift: {e}")

finally:
    if 'conn' is not None:
        conn.close()
        print("Conexión a Redshift cerrada")
