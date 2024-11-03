import os
import pandas as pd
import redshift_connector
import awswrangler as wr
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

# Configuración de conexión a Redshift
conn_params = {
    'host': os.getenv('REDSHIFT_HOST'),
    'database': os.getenv('REDSHIFT_DB'),
    'user': os.getenv('REDSHIFT_USER'),
    'password': os.getenv('REDSHIFT_PASSWORD'),
    'port': os.getenv('REDSHIFT_PORT'),
}

# Función para obtener nombres de variables desde dim_variable
def fetch_variable_names():
    query = """
    SELECT variable_id, nombre_variable
    FROM "2024_nicolas_alvarez_julia_schema".dim_variable
    """
    with redshift_connector.connect(
        host=conn_params['host'],
        database=conn_params['database'],
        user=conn_params['user'],
        password=conn_params['password'],
        port=int(conn_params['port'])
    ) as conn:
        df = wr.redshift.read_sql_query(query, con=conn)
    return df.set_index('variable_id')['nombre_variable'].to_dict()
# Cargar los nombres de las variables para el menú desplegable
variable_dict = fetch_variable_names()

# Función para extraer datos de Redshift según selección
def fetch_data(series_ids, start_date, end_date):
    if len(series_ids) == 1:
        series_filter = f"('{series_ids[0]}')"  # Para un único valor
    else:
        series_filter = str(tuple(series_ids))  # Para múltiples valores

    query = f"""
    SELECT fecha_dato, variable_id, valor
    FROM "2024_nicolas_alvarez_julia_schema".fact_table
    WHERE variable_id IN {series_filter}
    AND fecha BETWEEN '{start_date}' AND '{end_date}'
    ORDER BY fecha
    """
    with redshift_connector.connect(
        host=conn_params['host'],
        database=conn_params['database'],
        user=conn_params['user'],
        password=conn_params['password'],
        port=int(conn_params['port'])
    ) as conn:
        df = wr.redshift.read_sql_query(query, con=conn)
        print("Datos devueltos por la consulta:")
        print(df.head())  # Muestra las primeras filas para verificar
    return df
# Crear la Aplicación Dash
app = Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Visualización de Series de Tiempo - FED Data"),
    dcc.Dropdown(
        id="series-dropdown",
        options=[
            {"label": nombre, "value": var_id} for var_id, nombre in variable_dict.items()
        ],
        value=[list(variable_dict.keys())[0]],  # Valor por defecto (primera variable)
        multi=True,
        placeholder="Selecciona una o más variables"
    ),
    dcc.DatePickerRange(
        id="date-picker",
        start_date="2015-01-01",
        end_date="2024-11-03",
        display_format="YYYY-MM-DD"
    ),
    dcc.Graph(id="line-graph")
])

# Definir Callback para Actualizar el Gráfico
@app.callback(
    Output("line-graph", "figure"),
    [Input("series-dropdown", "value"),
     Input("date-picker", "start_date"),
     Input("date-picker", "end_date")]
)
def update_graph(selected_series, start_date, end_date):
    if not selected_series:
        return px.line()  # Gráfico vacío si no hay selección

    # Extraer datos desde Redshift
    df = fetch_data(selected_series, start_date, end_date)

    # Convertir variable_id a nombre_variable en el DataFrame
    df["nombre_variable"] = df["variable_id"].map(variable_dict)

    # Generar gráfico de líneas
    fig = px.line(df, x="fecha_dato", y="valor", color="nombre_variable",
                  title="Series de Tiempo Seleccionadas")
    fig.update_layout(xaxis_title="Fecha", yaxis_title="Valor")
    
    return fig

# Correr la aplicación
if __name__ == "__main__":
    app.run_server(debug=False)
