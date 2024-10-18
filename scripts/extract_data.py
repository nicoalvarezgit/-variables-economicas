import os
import requests
import psycopg2
import pandas as pd
import pyarrow
from airflow.exceptions import AirflowSkipException

def extract_data(output_parquet: str):
    
    #Creo objeto url para guardar el https de la API del BCRA y realizo un request.
    url = "https://api.bcra.gob.ar/estadisticas/v2.0/principalesvariables"
    response = requests.get(url, verify=False)
    
    #Se verifica que la solicitud haya sido exitosa
    if response.status_code !=200: #200 es el código exitoso de la consulta
        raise Exception(f"Error en la solicitud a la API. Código error: {response.status_code}")
    
    #Guardo la respuesta en JSON en la variabla data
    data = response.json()

    #Lo convierto en data frame
    df = pd.DataFrame(data)

    #Armo la ruta llamando al directorio
    path = os.path.join(output_parquet, 'data.parquet')
    
    #Guardo el archivo parquet
    df.to_parquet(path)
   
   #Chequeo con airflow que el data frame no este vacío (podría agregarse como test?)
    if df.empty:
        raise AirflowSkipException
   
   #Realizo una impresión para ver el path y cierro la función de extracción pidiendole que me devuelva el path
    print(f"Data extraída y guardada en {path}")
   
    return path

#Ejecutable
#extract_data('.')

