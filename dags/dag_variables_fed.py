import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv

from scripts import extract_data_fed, transform_data_fed, load_to_redshift_fed, actualizar_dim_fecha

# Se cargan las variables del archivo .env
load_dotenv()

conn_params = {
    'host': os.getenv('REDSHIFT_HOST'),
    'database': os.getenv('REDSHIFT_DB'),
    'user': os.getenv('REDSHIFT_USER'),  
    'password': os.getenv('REDSHIFT_PASSWORD'),
    'port': os.getenv('REDSHIFT_PORT'),
}

# Tabla de destino
destination_table = "fact_table"  


with DAG(
    'etl_redshift_dag_variables_fed',
    default_args={
        'depends_on_past':False, 
        'email_on_failure': False,
        'email_on_retry': False,
        'retry_delay': timedelta(minutes=1),
        'retries': 1,
    },
    description='pipeline ETL para cargar principales variables FED a Redshift',
    schedule_interval='0 19 * * 2-6',
    start_date= datetime(2024, 10, 29),
    catchup=True
) as dag:
    
    # Tarea 1: Extraer data
    extract_task = PythonOperator(
        task_id='extract_data_fed_task',
        python_callable=extract_data_fed,
        provide_context=True,
    )

    # Tarea 2: Transformar data
    transform_task = PythonOperator(
        task_id='transform_data_fed_task',
        python_callable=transform_data_fed,
    )

    # Tarea 3: Cargar data
    load_task = PythonOperator(
        task_id='load_to_redshift_task',
        python_callable=load_to_redshift_fed,
        op_kwargs={
            'destination_table': destination_table,
            'conn_params': conn_params
        },
    )

    # Tarea 4: Actualizar la tabla de las fechas
    actualizar_fecha_task = PythonOperator(
        task_id='actualizar_dim_fecha',
        python_callable=actualizar_dim_fecha,
    )

    #Seteando el orden de tareas
    actualizar_fecha_task >> extract_task >> transform_task >> load_task