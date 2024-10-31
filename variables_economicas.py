import pandas as pd


df=pd.read_csv('transformed_data_fed.csv', index_col=0)


df=df.dropna(axis=0,thresh=2)

print(df.shape)

print (df)

# Tarea 5: Limpieza duplicados
#    limpieza_duplicados_task = PythonOperator(
#        task_id='limpieza_duplicados',
#        python_callable=limpieza_duplicados,
#         op_kwargs={
#            'redshift_table': REDSHIFT_TABLE,
#            'conn_params': conn_params,
#            'columns': columns
#        },
#    )

#>> limpieza_duplicados_task