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
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  
    
    #Se eliminan las columnas 'cdSerie' y 'descripcion'
    df.drop(['cdSerie','descripcion'], axis=1, inplace=True)
    
    df = df.rename(columns={'idVariable': 'variable_id'})  # Renombro la columna de id

    #se forma una tupla con los valores de los ids de variables que no interesan al análisis.
    variables_a_eliminar = [4, 30, 31, 32, 40, 43]  
    df_transformado = df[~df['variable_id'].isin(variables_a_eliminar)]

    # Encontrar la fecha más reciente en la columna 'fecha' y se pasa a la una nueva columna 'fecha dato' con la misma fecha en todas las filas
    fecha_mas_reciente = df_transformado['fecha'].max()
    df_transformado['fecha_dato'] = fecha_mas_reciente

    return df_transformado

