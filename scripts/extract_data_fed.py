import os
import requests
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

#Pagina para hacer el request:
url_base="https://api.stlouisfed.org/fred/series/observations"

series_ids= [
     "DFF", "T10Y2Y", "DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30", "DFII5", "DFII10", "DFII30", "DTB4WK", "DTB3", "DTB6", "DPRIME", "DPCREDIT", "DGS1MO", "DGS3MO", "DGS6MO"
]

#Llamo a la api_key para hacer la request
api_key=os.getenv('api_key')


def request_fed_data(series_id: list, inicio_observacion: str, fin_observacion: str) -> Dict[str, Any]:
    """Solicita datos de las series de interés de la API de la FED.

    Args:
        series_id (str): Identificador de la serie de la FED a requerir.

    Returns:
        Dict[str, Any]: Respuesta de la API en formato JSON.

    Raises:
        Exception: Avisa si el código de respuesta no es exitoso.
    """
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': inicio_observacion,
        'observation_end': fin_observacion,
    }
    response = requests.get(url_base, params=params)
    
    # Verificar si la respuesta fue exitosa
    if response.status_code != 200:
        raise Exception(f"Error en la solicitud a la API. Código error: {response.status_code}")
    
    return response.json()


def process_to_dataframe(data: Dict[str, Any], series_id: str) -> Optional[pd.DataFrame]:
    """Convierte los datos de la API en un DataFrame de pandas.

    Args:
        data (Dict[str, Any]): Datos obtenidos de la API en formato JSON.
        series_id (str): Identificador de la serie de la FED.

    Returns:
        Optional[pd.DataFrame]: DataFrame con las observaciones de la serie, o None si no hay observaciones.
    """
    # Verificar que exista el campo 'observations' en los datos
    if 'observations' not in data:
        return None
    
    # Convierto las observaciones en un DataFrame
    df = pd.DataFrame(data['observations'])
    
    # Asegurar que la columna 'value' se interprete como decimal
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    
    df['series_id']=series_id
    
    return df


def extract_data_fed(**context) -> None:
    """Extrae datos de la API de la FED para las series requeridas y envía el resultado a xcom.

    Args:
        **kwargs: Argumentos adicionales, principalmente `ti` de Airflow para manejar xcom.

    Raises:
        ValueError: Si no se obtuvo ningún dato de la API.
    """
    
    ds=context['ds']
    execution_date=datetime.strptime(ds, '%Y-%m-%d')
    inicio_observacion= (execution_date - timedelta(days=1)).strftime('%Y-%m-%d')
    fin_observacion= (execution_date - timedelta(days=1)).strftime('%Y-%m-%d')
    
    all_dataframes = []  # Lista para almacenar los DataFrames
    for series_id in series_ids:
        data = request_fed_data(series_id,inicio_observacion, fin_observacion)
        df= process_to_dataframe(data, series_id)
        
        if df is not None and not df.empty:
            all_dataframes.append(df)
    if all_dataframes:
        final_df = pd.concat(all_dataframes, ignore_index=True)
        context['ti'].xcom_push(key='extracted_data', value=final_df.to_dict())
    else:
        raise ValueError("No se extrajo data de la API")
        