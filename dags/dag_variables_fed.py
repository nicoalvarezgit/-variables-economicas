# Definir el DAG
default_args = {
    'owner': 'tu_nombre',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'retries': 1
}

dag = DAG('actualizar_dim_fecha', default_args=default_args, schedule_interval='@daily')

actualizar_fecha_task = PythonOperator(
    task_id='actualizar_dim_fecha',
    python_callable=actualizar_dim_fecha,
    dag=dag
)