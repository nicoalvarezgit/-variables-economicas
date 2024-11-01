import requests
import pandas as pd
from airflow.exceptions import AirflowSkipException

def extract_data() -> pd.DataFrame:
    """
    Extrae datos de las principales variables desde la API del BCRA.

    Raises:
        Exception: Si el resultado de la request es un código de error.
        AirflowSkipException: Si el DataFrame resultante está vacío.

    Returns:
        pd.DataFrame: DataFrame con los datos extraídos de la API.
    """
    
    #Defino la url a la que le voy a hacer el request
    url = "https://api.bcra.gob.ar/estadisticas/v2.0/principalesvariables"
    
    response = requests.get(url, verify=False)

    if response.status_code != 200:
        raise Exception(f"Error en la solicitud a la API. Código error: {response.status_code}")
    
    #Guardo la respuesta en JSON en la variabla data
    data = response.json()
    
    #Convierto en data frame al objeto 'results' descartando el 'status_code' que no es importante para el análisis 
    df = pd.DataFrame(data['results'])

    #Chequeo con airflow que el data frame no este vacío (podría agregarse como test?)
    if df.empty:
        raise AirflowSkipException("No se encontraron datos para esta fecha")

    return df

