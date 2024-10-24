from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import locale
import os
from datetime import datetime, timedelta
import redshift_connector
import awswrangler as wr
import pandas as pd

REDSHIFT_TABLE = "dim_fecha"
REDSHIFT_SCHEMA = "2024_nicolas_alvarez_julia_schema"

#Se estable el español como predeterminado especialmente por los nombres de día y mes.
locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')

conn_params = {
    'host': os.getenv('REDSHIFT_HOST'),
    'database': os.getenv('REDSHIFT_DB'),
    'user': os.getenv('REDSHIFT_USER'),  
    'password': os.getenv('REDSHIFT_PASSWORD'),
    'port': os.getenv('REDSHIFT_PORT'),
}

def actualizar_dim_fecha():
    try:
        # Obtener la fecha más reciente de la tabla dim_fecha usando awswrangler
        query = f"SELECT MAX(fecha_id) AS max_fecha FROM {REDSHIFT_SCHEMA}.{REDSHIFT_TABLE};"
        # Se establece la conexión
        conn = redshift_connector.connect(**conn_params)
        df_max_fecha = wr.redshift.read_sql_query(query, con=conn)  
        
        max_fecha = df_max_fecha['max_fecha'].iloc[0]

        # Si la fecha más reciente es anterior a hoy, agregar nuevas fechas
        hoy = datetime.now().date()
        if max_fecha < hoy:
            fechas = pd.date_range(start=max_fecha + pd.Timedelta(days=1), end=hoy).to_pydatetime().tolist()

            # Crear dataframe con descomposición de fechas
            data = []
            for fecha in fechas:
                data.append({
                    'fecha_id': fecha,
                    'año': fecha.year,
                    'mes': fecha.month,
                    'nombre_mes': fecha.strftime('%B'),
                    'dia': fecha.day,
                    'nombre_dia': fecha.strftime('%A'),
                    'trimestre': (fecha.month - 1) // 3 + 1
                })

            df_fechas = pd.DataFrame(data)

            # Insertar nuevas fechas en la tabla dim_fecha usando awswrangler
            wr.redshift.to_sql(
                df=df_fechas,
                schema=REDSHIFT_SCHEMA,
                table=REDSHIFT_TABLE,
                con=conn, 
                mode="append"
            )

            print(f"Fechas agregadas exitosamente a la tabla {REDSHIFT_SCHEMA}.{REDSHIFT_TABLE} en Redshift.")
        
    except Exception as e:
        print(f"Error en la conexión o actualización de la tabla: {e}")
        
        
if __name__ == "__main__":
    actualizar_dim_fecha()

