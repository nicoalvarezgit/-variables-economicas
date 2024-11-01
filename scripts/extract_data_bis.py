import requests
import pandas as pd
from airflow.exceptions import AirflowSkipException
from datetime import datetime

def extract_data(execution_date: datetime, variables_ids: list[int]) -> pd.DataFrame:
    """
    Extrae datos de la API del BCRA para múltiples variables en la fecha de ejecución.

    Args:
        execution_date (datetime): Fecha de ejecución del DAG
        variables_ids (list[int]): Lista de varibales a consultar.
    
    Raises:
        Exception: Si el resultado de la request es un código de error.
        AirflowSkipException: Si el DataFrame resultante está vacío.

    Returns:
        pd.DataFrame: DataFrame con los datos extraídos de la API.
    """
    fecha = execution_date.strftime('%Y-%m-%d')
    datos= [] # acá se van a almacenar los datos
    variables_ids=[1,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,21,22,23,24,25,26,27,28,29,34,35,41,42]

    #Creo objeto url para guardar el https de la API del BCRA 
    for id_var in variables_ids:
        url = f"https://api.bcra.gob.ar/estadisticas/v2.0/datosvariable/{id_var}/{fecha}/{fecha}"
        response = requests.get(url, verify=False)

        # Verificar la URL generada (solo para depuración)
        print(f"URL de solicitud: {url}")
    
        response = requests.get(url, verify=False)
        
        # Si el status_code es 404, pasar a la siguiente variable sin lanzar una excepción
        if response.status_code == 404:
            print(f"No se encontraron datos para idVariable {id_var} en la fecha {fecha}.")
            continue

        if response.status_code != 200:
            raise Exception(f"Error en la solicitud a la API para idVariable {id_var}. Código error: {response.status_code}")
    
        #Guardo la respuesta en JSON en la variabla data
        data = response.json().get('results',[])
        datos.extend(data) #Se suman los resultados a la lista vacía

    #Convierto en data frame al objeto 'results' descartando el 'status_code' que no es importante para el análisis 
    df = pd.DataFrame(datos)

    #Chequeo con airflow que el data frame no este vacío (podría agregarse como test?)
    if df.empty:
        raise AirflowSkipException("No se encontraron datos para esta fecha")
   
    return df


#def extract_task_callable(**kwargs):
#        execution_date=kwargs['execution_date']
#        df = extract_data(execution_date, variables_ids)
#        return df
