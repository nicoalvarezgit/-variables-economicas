from unittest.mock import patch, MagicMock
import pandas as pd
from scripts.load_to_redshift import load_to_redshift

def test_load_to_redshift():
    # DataFrame simulado para la carga
    df_transformado = pd.DataFrame({
        'variable_id': [1, 2],
        'fecha': ['2024-10-01', '2024-10-02'],
        'valor': [100, 200],
        'fecha_dato': ['2024-10-01', '2024-10-02']
    })

    conn_params = {
        'host': 'localhost',
        'database': 'database',
        'user': 'my_user',
        'password': 'password',
        'port': 5439
    }
    
    # Patch de wr.redshift.to_sql para evitar la conexión real y verificar los argumentos
    with patch("awswrangler.redshift.to_sql") as mock_to_sql, patch("redshift_connector.connect") as mock_connect:
        mock_connect.return_value = MagicMock()
        mock_to_sql.return_value = None  

        # Ejecutar la función de carga
        load_to_redshift(df_transformado, conn_params)

        # Verificar que to_sql fue llamado una vez con los parámetros correctos
        mock_to_sql.assert_called_once_with(
            df=df_transformado,
            con=MagicMock(),  # la conexión es un mock
            table="fact_table",  
            schema="2024_nicolas_alvarez_julia_schema",  
            mode="append",
            use_column_names=True,
            index=False,
            lock=True
        )
