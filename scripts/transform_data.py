import os
import pandas as pd


def transform_data(input_parquet: str, output_csv: str):
    
    #Cargo la data cruda del archivo parquet
    df= pd.read_parquet(input_parquet)
    
    # Se formatean los valores de la columna 'fecha' en formato datetime y se le saca la hora
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  
    
    #Se elimina la columna 'cdSerie' que no aporta ningún valor, mantengo el idVariable
    df.drop('cdSerie', axis=1, inplace=True)
    
    #df.set_index('fecha', inplace=True)  # Usar la fecha como índice
    
    df = df.rename(columns={'idVariable': 'id', 'descripcion': 'variable'})  # Renombrar la columna de valor

    #se forma una tupla con los valores de los ids de variables que no interesan al análisis.
    variables_a_eliminar = [4, 30, 31, 32, 40, 43]  
    df = df[~df['id'].isin(variables_a_eliminar)]

    # Encontrar la fecha más reciente en la columna 'fecha' y se pasa a la una nueva columna 'fecha dato' con la misma fecha en todas las filas
    fecha_mas_reciente = df['fecha'].max()
    df['fecha dato'] = fecha_mas_reciente

    #Se crea el path nuevamente para guardar el dataframe transformado
    path = os.path.join(output_csv, 'transformed_data.csv')
    
    #Se guarda el archivo transormado en formato parquet
    df.to_csv(path, index=False)

    print(f"Data transformada y guardada en {path}")
    return path

#Si se llama transform_data como módulo, se corre la función
if __name__ == "__main__":
    transform_data('data.parquet', '.')

