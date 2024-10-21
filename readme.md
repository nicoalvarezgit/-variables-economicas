Este es el readme del trabajo de variables económicas.

El objetivo es armar un set de datos con variables ecónomicas para interpretar la realidad nacional.

Se trata de una conexión a la API (pública) del BCRA y sus prinicipales variables (monetarias principalmente)

Con poetry se generó un entorno local con los requerimientos necesarios, detallados en el pyproyect y exportados al requirements.txt 

Se genero un DAG para extraer la información diaria, transformarla y cargarla a una tabla de resdhift.

Se crearon 2 test unitarios para probar la extraccion y la transformación de la misma, que también se puede realizar con GitHub Actions

