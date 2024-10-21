Este es el readme del trabajo de variables económicas.

El objetivo es armar un set de datos con variables ecónomicas para interpretar la realidad nacional.

Lo primero que se realiza es la creación de un entorno virtual, utilizando la librería poetry. Con ella se crea el pyproyect.toml donde quedan especificados las librerías que se van a utilizar en el script de Python.
En principio se arranca con las librerías pandas, requests y pytest. También el archivo poetry.lock, junto con el anterior necesarios para que cualquiera pueda recrear el entorno virtual.

Se creó el archivo .env para llamar a las credenciales desde el script de Python. El mismo es incorporado al .gitignore para no exponer las claves. Para ello también se agrega al entorno virtual la librería python-dotenv.

