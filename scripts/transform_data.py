import pandas as pd


def transform_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Realiza transformaciones sobre el DataFrame obtenido de la extracción.

    Args:
        df (pd.DataFrame): DataFrame crudo extraído de la API.

    Returns:
        pd.DataFrame: DataFrame transformado listo para la carga.
    """
    # Se formatean los valores de la columna 'fecha' en formato datetime y se le saca la hora
    df['fecha_dato'] = pd.to_datetime(df['fecha'], errors='coerce')  
    
    #Se eliminan las columnas 'cdSerie' y 'descripcion'
    df.drop(['cdSerie','descripcion'], axis=1, inplace=True)
    
    df = df.rename(columns={'idVariable': 'variable_id'})  # Renombro la columna de id

    #se forma una tupla con los valores de los ids de variables que no interesan al análisis.
    variables_a_eliminar = [4, 30, 31, 32, 40, 43]  
    df_transformado = df.loc[~df['variable_id'].isin(variables_a_eliminar)].copy()

    # Encontrar la fecha más reciente en la columna 'fecha' y se pasa a la una nueva columna 'fecha dato' con la misma fecha en todas las filas
    fecha_mas_reciente = df_transformado['fecha_dato'].max()
    df_transformado['fecha'] = fecha_mas_reciente

    #Se reordenan las columnas para coincidir con la fact_table
    orden_df=['variable_id','fecha','valor','fecha_dato']
    df_transformado= df_transformado[orden_df]

    return df_transformado

