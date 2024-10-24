import os
import pandas as pd

DATA_PATH=os.path.dirname(__file__)
#os.path.join(,os.pardir)

def transform_data_fed(input_csv: str, output_csv: str):
    
    #Cargo la data cruda del archivo csv
    df= pd.read_csv(input_csv)
    
    # Se reorganiza el DataFrame en función de la fecha del dato
    df_pivot = df.pivot_table(
        index='date',  
        columns='series_id',  
        values='value',  
        aggfunc='first'  
    )

    df_pivot.reset_index(inplace=True)
    print(df_pivot)

    #Hay una variable (DFF) que tiene datos de más de un día, mientras del resto toma un solo día. Se elimina la fila adelantada.
    df_pivot=df_pivot.dropna(axis=0,thresh=2)

    #Se guarda el archivo transormado en formato csv
    df_pivot.to_csv(output_csv, index=False)

    print(f"Data transformada y guardada en {output_csv}")
    return output_csv

#Si se llama transform_data como módulo, se corre la función
if __name__ == "__main__":
    input_csv= os.path.join(DATA_PATH,'data_fed.csv')
    output_csv=os.path.join(DATA_PATH,'transformed_data_fed.csv')
    transform_data_fed(input_csv, output_csv)

