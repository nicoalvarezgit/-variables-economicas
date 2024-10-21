import os
import pandas as pd

DATA_PATH=os.path.join(os.path.dirname(__file__),os.pardir)

def transform_data(input_parquet: str, output_csv: str):
    
    #Cargo la data cruda del archivo parquet
    df= pd.read_parquet(input_parquet)
    
    # Se formatean los valores de la columna 'fecha' en formato datetime y se le saca la hora
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')  
    
    #Se elimina la columna 'cdSerie' que no aporta ningún valor, mantengo el idVariable
    df.drop('cdSerie', axis=1, inplace=True)
    
    df = df.rename(columns={'idVariable': 'id', 'descripcion': 'variable'})  # Renombrar la columna de valor

    #se forma una tupla con los valores de los ids de variables que no interesan al análisis.
    variables_a_eliminar = [4, 30, 31, 32, 40, 43]  
    df = df[~df['id'].isin(variables_a_eliminar)]

    # Encontrar la fecha más reciente en la columna 'fecha' y se pasa a la una nueva columna 'fecha dato' con la misma fecha en todas las filas
    fecha_mas_reciente = df['fecha'].max()
    df['fecha_dato'] = fecha_mas_reciente

    #Se guarda el archivo transormado en formato csv
    df.to_csv(output_csv, index=False)

    print(f"Data transformada y guardada en {output_csv}")
    return output_csv

#Si se llama transform_data como módulo, se corre la función
if __name__ == "__main__":
    input_parquet= os.path.join(DATA_PATH,'data.parquet')
    output_csv=os.path.join(DATA_PATH,'transformed_data.csv')
    transform_data(input_parquet, output_csv)

