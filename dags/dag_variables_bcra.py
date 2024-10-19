import os
import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from dotenv import load_dotenv
from scripts import extract_data, transform_data, load_to_redshift

# Se cargan las variables del archivo .env
load_dotenv()

# Obtener las credenciales desde las variables de entorno
user = os.getenv('REDSHIFT_USER')
password = os.getenv('REDSHIFT_PASSWORD')
host = os.getenv('REDSHIFT_HOST')
port = os.getenv('REDSHIFT_PORT')
database = os.getenv('REDSHIFT_DB') 

REDSHIFT_CONN_STRING = f"postgresql://{user}:{password}@{host}:{port}/{database}"
DATA_PATH=os.path.dirname(os.path.realpath(__file__)) # el path que aparece es este 'C:\\Users\\Nicolas\\OneDrive - BCRA\\Cursos\\Python Data Application (ITBA)\\variables-economicas\\dags'
REDSHIFT_TABLE = "redshift_table"

with DAG(
    'etl_redshift_dag_variables_bcra',
    default_args={
        'depends_on_past':False, 
        'email_on_failure': False,
        'email_on_retry': False,
        'retry_delay': datetime.timedelta(minutes=2),
        'retries': 1,
    },
    description='pipeline ETL para cargar principales variables BCRA a Redshift',
    schedule_interval='1 0 * * 2-6',
    start_date= datetime(2024, 10, 1),
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
        op_kwargs={'output_parquet': DATA_PATH}
    )

    # Tarea 3: Cargar data
    load_task = PythonOperator(
        task_id='load_data',
        python_callable=load_to_redshift,
        op_kwargs={
            'redshift_table': REDSHIFT_TABLE,
            'redshift_conn_string': REDSHIFT_CONN_STRING,
        },
    )

    #Seteando el orden de tareas
    extract_task >> transform_task >> load_task