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


DATA_PATH=os.path.dirname(os.path.realpath(__file__)) 
REDSHIFT_TABLE = "fact_table"
columns = ["variable_id", "fecha", "valor", "fecha_dato"]


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
    start_date= datetime(2024, 10, 17),
    catchup=True
) as dag:
    
    # Tarea 1: Extraer data
    extract_task = PythonOperator(
        task_id='extract_data',
        python_callable=extract_data,
        op_kwargs={'output_parquet': DATA_PATH}
    )

    # Tarea 2: Transformar data
    transform_task = PythonOperator(
        task_id='transform_data',
        python_callable=transform_data,
        op_kwargs={'input_parquet': os.path.join(DATA_PATH,'data.parquet'),
                   'output_csv': os.path.join(DATA_PATH, 'transfomed_data.csv')}
    )

    # Tarea 3: Cargar data
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_to_redshift,
        op_kwargs={
            'transformed_csv': os.path.join(DATA_PATH, 'transfomed_data.csv'),
            'redshift_table': REDSHIFT_TABLE,
            'conn_params': conn_params
        },
    )

    # Tarea 4: Actualizar la tabla de las fechas
    actualizar_fecha_task = PythonOperator(
        task_id='actualizar_dim_fecha',
        python_callable=actualizar_dim_fecha,
    )

    # Tarea 5: Limpieza duplicados
    limpieza_duplicados_task = PythonOperator(
        task_id='limpieza_duplicados',
        python_callable=limpieza_duplicados,
         op_kwargs={
            'redshift_table': REDSHIFT_TABLE,
            'conn_params': conn_params,
            'columns': columns
        },
    )

    #Seteando el orden de tareas
    actualizar_fecha_task >> extract_task >> transform_task >> load_task >> limpieza_duplicados_task