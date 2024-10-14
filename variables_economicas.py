# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 16:30:24 2024

@author: L12504
"""
import os
from dotenv import load_dotenv
import requests
import pandas as pd

# Se cargan las variables del archivo .env
load_dotenv()

# Obtener las credenciales desde las variables de entorno
user = os.getenv('REDSHIFT_USER')
password = os.getenv('REDSHIFT_PASSWORD')
host = os.getenv('REDSHIFT_HOST')
port = os.getenv('REDSHIFT_PORT')
database = os.getenv('REDSHIFT_DB')

url = "https://api.bcra.gob.ar/estadisticas/v2.0/principalesvariables"

response = requests.get(url, verify=False)
data = response.json()

results = data['results']

listado_variables = pd.DataFrame(results)

print(listado_variables.head())