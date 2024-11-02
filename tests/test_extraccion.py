import pytest
from airflow.exceptions import AirflowSkipException
from scripts.extract_data import extract_data

def test_extract_data_df_vacio(monkeypatch):
    # Se mockea la respuesta con la llave 'results' vacío
    class MockResponse:
        status_code = 200
        def json(self):
            return {"results": []}  
        
    # Se utiliza monkeypatch para reemplazar requests.get por MockResponse
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

    # Validamos que extract_data arroje AirflowSkipException cuando el DataFrame está vacío
    with pytest.raises(AirflowSkipException):
        extract_data()  