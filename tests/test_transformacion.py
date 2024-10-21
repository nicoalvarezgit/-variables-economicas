import unittest
from unittest.mock import patch
import os
import pandas as pd
from scripts.transform_data import transform_data

class TestTransformData(unittest.TestCase):

    @patch('pandas.DataFrame.to_csv')  # Mock para evitar escribir el archivo
    @patch('pandas.read_parquet')  # Mock para simular la carga de datos
    def test_transform_data_call(self, mock_read_parquet, mock_to_csv):
        # Simular DATA_PATH como lo tienes en tu entorno
        DATA_PATH = os.path.join(os.path.dirname(__file__), os.pardir)

        # Crear un Mock DataFrame simulado
        mock_df = mock_read_parquet.return_value = pd.DataFrame({
            'idVariable': [4, 30, 31, 32, 40, 43] + [i for i in range(6, 35)],  # 35 filas
            'descripcion': ['Var 1', 'Var 2', 'Var 3', 'Var 4', 'Var 5'] * 7,
            'fecha': ['2024-10-01', '2024-10-02', '2024-10-03', '2024-10-04', '2024-10-05'] * 7,
            'cdSerie': ['A', 'B', 'C', 'D', 'E'] * 7,
            'valor': [100, 200, 300, 400, 500] * 7
        })

        # Definir rutas reales
        input_parquet = os.path.join(DATA_PATH, 'data.parquet')
        output_csv = os.path.join(DATA_PATH, 'transformed_data.csv')

        # Llamar a la función de transformación
        transform_data(input_parquet, output_csv)

        # Verificar que se llamó a to_csv con el path correcto
        mock_to_csv.assert_called_once_with(output_csv, index=False)

if __name__ == '__main__':
    unittest.main()
