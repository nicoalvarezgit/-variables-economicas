import pandas as pd
from datetime import datetime
from scripts.transform_data import transform_data

def test_transform_data():
    # Simulamos un DataFrame inicial con datos
    df_inicial = pd.DataFrame({
        'idVariable': [4, 6, 30, 7, 40],  # Valores para filtrar y mantener
        'descripcion': ['Desc1', 'Desc2', 'Desc3', 'Desc4', 'Desc5'],
        'fecha': ['2024-10-01', '2024-10-02', '2024-10-03', '2024-10-04', '2024-10-05'],
        'cdSerie': ['A', 'B', 'C', 'D', 'E'],
        'valor': [100, 200, 300, 400, 500]
    })
    
    # Ejecutar la función de transformación
    df_transformado = transform_data(df_inicial)

    # Verificar que las columnas 'cdSerie' y 'descripcion' fueron eliminadas
    assert 'cdSerie' not in df_transformado.columns
    assert 'descripcion' not in df_transformado.columns

    # Se verifica que se borraron las 'variable_id' que no son de interés
    assert not df_transformado['variable_id'].isin([4, 30, 40]).any()

    
