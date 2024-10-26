import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv

from scripts import extract_data, transform_data, load_to_redshift, actualizar_dim_fecha

# Se cargan las variables del archivo .env
load_dotenv()

conn_params = {
    'host': os.getenv('REDSHIFT_HOST'),
    'database': os.getenv('REDSHIFT_DB'),
    'user': os.getenv('REDSHIFT_USER'),  
    'password': os.getenv('REDSHIFT_PASSWORD'),
    'port': os.getenv('REDSHIFT_PORT'),
}


#REDSHIFT_CONN_STRING = f"postgresql://{user}:{password}@{host}:{port}/{database}"
DATA_PATH=os.path.dirname(os.path.realpath(__file__)) 
REDSHIFT_TABLE = "redshift_table"

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

    #Seteando el orden de tareas
    actualizar_fecha_task >> extract_task >> transform_task >> load_task