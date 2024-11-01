import pytest
from airflow.exceptions import AirflowSkipException
from scripts import extract_data

def test_extract_data_empty_dataframe(monkeypatch):
    # Simulamos la respuesta de requests.get para que devuelva una respuesta con un 'results' vacío
    class MockResponse:
        status_code = 200
        def json(self):
            return {"results": []}  # Datos vacíos

    # Usamos monkeypatch para reemplazar requests.get por MockResponse
    monkeypatch.setattr("requests.get", lambda *args, **kwargs: MockResponse())

    # Validamos que extract_data arroje AirflowSkipException con datos vacíos
    with pytest.raises(AirflowSkipException):
        extract_data("/some/path")  # No importa el path aquí
