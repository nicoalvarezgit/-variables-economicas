import pytest

if __name__ == "__main__":
    # Ejecuta todos los tests en la carpeta `tests` usando `pytest`
    pytest.main(["-q", "--tb=short", "tests"])