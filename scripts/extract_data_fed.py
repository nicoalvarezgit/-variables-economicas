import os
import requests
import pandas as pd
from datetime import datetime, timedelta

##Se publica a las 16_15 (puede ser que esté una o dos horas)

#Defino la página base:
url_base="https://api.stlouisfed.org/fred/series/observations"

series_ids= [
     "DFF", "T10Y2Y", "DGS1", "DGS2", "DGS3", "DGS5", "DGS7", "DGS10", "DGS20", "DGS30", "DFII5", "DFII10", "DFII30", "DTB4WK", "DTB3", "DTB6", "DPRIME", "DPCREDIT", "DGS1MO", "DGS3MO", "DGS6MO"
]

#Llamo a la api_key para hacer la request
api_key=os.getenv('api_key')

DATA_PATH=os.path.dirname(__file__)

def request_fed_data(series_id: list):
    hoy = datetime.today().strftime('%Y-%m-%d')
    anteayer = (datetime.today() - timedelta(days=4)).strftime('%Y-%m-%d')
    ayer = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')
    params = {
        'series_id': series_id,
        'api_key': api_key,
        'file_type': 'json',
        'observation_start': anteayer,
        'observation_end': ayer,
    }
    response = requests.get(url_base, params=params)
    
    # Verificar si la respuesta fue exitosa
    if response.status_code != 200:
        raise Exception(f"Error en la solicitud a la API. Código error: {response.status_code}")
        
    data = response.json()
    
    # Imprimir las claves (keys) del JSON obtenido
    print(f"Keys for {series_id}: {data.keys()}")
    
    return data



def process_to_dataframe(data, series_id):
    # Verificar si existe el campo 'observations' en los datos
    if 'observations' not in data:
        print(f"No 'observations' field found for series {series_id}")
        return None
    
    # Extraer las observaciones de los datos JSON
    observations = data['observations']
    
    # Imprimir las primeras observaciones para revisar su estructura
    print(f"Observations for {series_id}: {observations[:5]}")
    
    # Convertir las observaciones en un DataFrame
    df = pd.DataFrame(observations)
    
    # Mostrar los nombres de las columnas del DataFrame
    print(f"Columns in DataFrame for {series_id}: {df.columns}")
    
    return df

if __name__ == "__main__":
    all_dataframes = []  # Lista para almacenar los DataFrames

    for series_id in series_ids:
        data = request_fed_data(series_id)
        
        if data is not None:
            df = process_to_dataframe(data, series_id)
            if df is not None and not df.empty:
                print(f"Data for {series_id} on {datetime.today().strftime('%Y-%m-%d')}:")
                                
                # Agregar una columna con el identificador de la serie
                df['series_id'] = series_id
                
                # Añadir el DataFrame a la lista
                all_dataframes.append(df)
            else:
                print(f"No data found for {series_id} on {datetime.today().strftime('%Y-%m-%d')}")

    # Concatenar todos los DataFrames en uno solo
    if all_dataframes:
        final_df = pd.concat(all_dataframes, ignore_index=True)
             
        final_df.to_csv(os.path.join(DATA_PATH, 'data_fed.csv'))
        print("Datos exportados a CSV exitosamente")
        print("Final concatenated DataFrame:")
        print(final_df)
        