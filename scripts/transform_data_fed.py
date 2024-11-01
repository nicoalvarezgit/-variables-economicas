import pandas as pd
from typing import Any

def transform_data_fed(ti: Any) -> None:
    """Transforma los datos extraídos de la API de la FED y los envía a xcom.

    Esta función realiza varias operaciones como eliminar columnas innecesarias, renombra y reorganizar el 
    orden de las columnas, elimina duplicados y luego envía el DataFrame transformado de vuelta a xcom.

    Args:
        ti (Any): `TaskInstance` de Airflow utilizado para el manejo de xcom.

    Raises:
        ValueError: Si no se encuentra data en xcom para la clave 'extracted_data'.
        Exception: Si ocurre un error al enviar los datos transformados a xcom.
    """
    
    #Cargo la data frame con Xcom
    data=ti.xcom_pull(task_ids='extract_data_fed_task', key='extracted_data')
    if data is None:
        raise ValueError("No se encontró data en XCom para 'extracted_data'")
    df= pd.DataFrame(data)
    
    #Se elimina la columna 'realtime_start'
    df.drop(['realtime_start'], axis=1, inplace=True)

    #Se renombran las columnas para que coincidan con las tables
    df = df.rename(columns={'series_id': 'variable_id', 'realtime_end': 'fecha', 'date': 'fecha_dato', 'value': 'valor'})  # Renombro las columnas

    #Se reorganizan las columnas 
    orden_df=['variable_id','fecha','valor','fecha_dato']
    df_transformado= df[orden_df]

    # Eliminar duplicados
    df_transformado.drop_duplicates(subset=['fecha_dato', 'variable_id'], inplace=True)


    # Se envía el df por xcom 
    try:
        ti.xcom_push(key='transformed_data', value=df_transformado.to_dict())
        print("Datos transformados y enviados por XCom")
    except Exception as e:
        raise Exception(f"Error al enviar los datos transformados a xcom: {e}")
