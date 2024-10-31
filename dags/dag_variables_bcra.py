import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv

from scripts import extract_data, transform_data, load_to_redshift, actualizar_dim_fecha, limpieza_duplicados

# Se cargan las variables del archivo .env
load_dotenv()

conn_params = {
    'host': os.getenv('REDSHIFT_HOST'),
    'database': os.getenv('REDSHIFT_DB'),
    'user': os.getenv('REDSHIFT_USER'),  
    'password': os.getenv('REDSHIFT_PASSWORD'),
    'port': os.getenv('REDSHIFT_PORT'),
}

REDSHIFT_TABLE = "fact_table"
#columns = ["variable_id", "fecha", "valor", "fecha_dato"]

with DAG(
    'etl_redshift_dag_variables_bcra',
    default_args={
        'depends_on_past':False, 
        'email_on_failure': False,
        'email_on_retry': False,
        'retry_delay': timedelta(minutes=1),
        'retries': 1,
    },
    description='pipeline ETL para cargar principales variables BCRA a Redshift',
    schedule_interval='1 0 * * 2-6',
    start_date= datetime(2024, 10, 28),
    catchup=True
) as dag:
    
    # Tarea 1: Extraer data
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
    )

    # Tarea 2: Transformar data
    def transform_task_callable(**kwargs):
        df = kwargs['ti'].xcom_pull(task_ids='extract_data')
        return transform_data(df)

    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_task_callable,
        provide_context=True
    )

    # Tarea 3: Cargar data
    def load_task_callable(**kwargs):
        df_transformado = kwargs['ti'].xcom_pull(task_ids='transform_data')
        load_to_redshift(df_transformado, conn_params)


    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_task_callable,
        provide_context=True
    )

    # Tarea 4: Actualizar la tabla de las fechas
    actualizar_fecha_task = PythonOperator(
        task_id='actualizar_dim_fecha',
        python_callable=actualizar_dim_fecha,
    )

    
    #Seteando el orden de tareas
    actualizar_fecha_task >> extract_task >> transform_task >> load_task 