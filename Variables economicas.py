# -*- coding: utf-8 -*-
"""
Created on Wed Sep  4 16:30:24 2024

@author: L12504
"""

import requests
import pandas as pd


url = "https://api.bcra.gob.ar/estadisticas/v2.0/principalesvariables"

response = requests.get(url)
data = response.json()

results = data['results']

listado_variables = pd.DataFrame(results)

print(listado_variables.head())