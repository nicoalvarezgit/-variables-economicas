import pandas as pd
from scripts.transform_data import transform_data

def test_transform_data():
    df_inicial = pd.DataFrame({
        'idVariable': [4, 6, 30, 7, 40],
        'descripcion': ['Desc1', 'Desc2', 'Desc3', 'Desc4', 'Desc5'],
        'fecha': ['2024-10-01', '2024-10-02', '2024-10-03', '2024-10-04', '2024-10-05'],
        'cdSerie': ['A', 'B', 'C', 'D', 'E'],
        'valor': [100, 200, 300, 400, 500]
    })

    df_transformado = transform_data(df_inicial)

    # Verificar que las columnas 'cdSerie' y 'descripcion' fueron eliminadas
    assert 'cdSerie' not in df_transformado.columns
    assert 'descripcion' not in df_transformado.columns

    # Verificar que se aplicó el filtro de 'variable_id'
    assert not df_transformado['variable_id'].isin([4, 30, 40]).any()

    # Verificar el formato datetime de 'fecha_dato'
    assert pd.api.types.is_datetime64_any_dtype(df_transformado['fecha_dato'])

    # Verificar el orden de las columnas
    assert list(df_transformado.columns) == ['variable_id', 'fecha', 'valor', 'fecha_dato']
