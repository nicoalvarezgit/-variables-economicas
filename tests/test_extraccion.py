import unittest
from unittest.mock import patch, MagicMock
from scripts.extract_data import extract_data

class TestExtractData(unittest.TestCase):
    
    @patch('requests.get')
    @patch('pandas.DataFrame.to_parquet')
    def test_extract_data_status_code(self, mock_to_parquet, mock_get):
        #Se configura el mock para simular la respuesta exitosa:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'results': [{'idVariable': 1, 'descripcion': 'Variable 1', 'fecha': '2023-10-01'}]}
        mock_get.return_value = mock_response
        
        # Llamar a la función a una dirección ficticia
        output_path = 'output_path_ficticio'
        result = extract_data(output_path)

        #Verifico que la salida haya sido exitosa y no lanzó las excepciones 
        mock_get.assert_called_once_with("https://api.bcra.gob.ar/estadisticas/v2.0/principalesvariables", verify=False)
        self.assertEqual(mock_response.status_code, 200)
        self.assertEqual(result, 'output_path_ficticio/data.parquet')

        # Verificar que se intentó escribir el archivo parquet
        mock_to_parquet.assert_called_once()

if __name__ == '__main__':
    unittest.main()