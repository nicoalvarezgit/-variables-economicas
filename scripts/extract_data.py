import os
import requests
import pandas as pd
from airflow.exceptions import AirflowSkipException


def extract_data():
    """
    Extrae datos de la API del BCRA y los convierte en un DataFrame de pandas.

    Raises:
        Exception: Si la solicitud a la API falla o si el resultado de la respuesta es un código de error.
        AirflowSkipException: Si el DataFrame resultante está vacío.

    Returns:
        pd.DataFrame: DataFrame con los datos extraídos de la API.
    """
    
    #Creo objeto url para guardar el https de la API del BCRA 
    url = "https://api.bcra.gob.ar/estadisticas/v2.0/principalesvariables"
    
    #Se realiza el request generando una excepción si hay error.
    try:
        response = requests.get(url, verify=False)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Error al conectar con la API  del BCRA: {e}")
    
    #Se verifica que la solicitud haya sido exitosa
    if response.status_code !=200: #200 es el código exitoso de la consulta
        raise Exception(f"Error en la solicitud a la API. Código error: {response.status_code}")
    
    #Guardo la respuesta en JSON en la variabla data
    data = response.json()

    #Convierto en data frame al objeto 'results' descartando el 'status_code' que no es importante para el análisis 
    df = pd.DataFrame(data['results'])

    #Chequeo con airflow que el data frame no este vacío (podría agregarse como test?)
    if df.empty:
        raise AirflowSkipException
   
    return df

