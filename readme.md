# Trabajo práctico de variables económicas

Este es un repositorio que genera ingestas diarias del Banco Central de la República Argentina y la Reserva Federal de los Estados Unidos, mediante pipelines extraen, transforman y cargan los datos en una tabla de Redshift. Cuenta con herramientas de visualización de los datos para otorgar una herramienta de comprensión a la realidad económica. 

## Contenidos del proyecto

1. [Introducción](##Introducción)
2. [Instalación](#Instalación)
3. [Utilización](#Utilización)
4. [Estructura del Proyecto](#estructura-del-proyecto)

## Introducción

El objetivo de este repositorio es poder seguir diariamente las principales variables económicas. Para hacerlo se arma un pipeline de ETL por cada fuente de datos (por ahora disponibles solo BCRA y FED). Los mismos extraen los datos diarios de sus respectivas API, se transforman y son cargados a una tabla de Redshift donde se encuentran alojados. 

## Instalación
El trabajó se desarrolló generando un entorno local de pruebas con la librería Poetry, la misma se puede instalar mediante el código: pip install poetry.
El proyecto cuenta con los archivos pyproyect y .lock que permiten levantar los requerimientos necesarios, con el comando poetry shell se activa el entorno local con las dependencias requeridas. 
Así mismo, si el usuario desea utilizar otro tipo de entorno virtual, en el documento "requirements.txt" se encuentran detallados las librerías necesarias correrlo de otra manera.

### Requisitos Previos
- Docker
- Git
- Crear archivo .env con la información necesaria.

### Paso a Paso (con los comandos para una terminal de bash)

*Clonar el repositorio*
git clone https://github.com/nicoalvarezgit/variables-economicas.git

*Ir a la carpeta del proyecto*
cd variables-economicas

*Construir y correr los contenedores*
docker-compose up 

## Utilización
Una vez desplegado el proyecto, el usuario puede accerder a la interfaz de Airflow, accediendo a http://localhost:8080. En la carpeta dags se encuentran los códigos de los dags, en caso de que el usuario quiera cambiar alguna de las configuraciones de los mismos.

Los datos son volcados en un esquema estrella con fact_table como tabla principal donde son injertados los datos diariamente, mientras que cuenta con dos tablas de dimensiones (dim_fecha y dim_variables). Todas estas tablas pueden ser creadas con los scripts en la carpeta bd (Aclaración: para que las tablas al crearse guarden su adecuada relación, deben crearse en primer lugar la tabla de dimensiones y luego la fact_table). 

Cuenta con una herramienta de visualización de las tasas de interés de la FED, con datos desde enero de 2015. El usuario va a poder elegir que variables quiere visualizar y el rango.
Para esto debe correr el script "app_dash.py" (con poetry se corre con el comando "poetry run python fed_dash.py"). La salida será un link a ttp://127.0.0.1:8050, donde accediendo el usuario podrá hacer uso de esta herramienta de visualización. 

El proyecto cuenta con una serie de tests unitarios en derredor de los scripts del ETL del BCRA. Los mismos se corren con el comando "poetry run python tests_etl_bcra.py"

## Estructura del Proyecto

variables-economicas/
├── dags/                 # DAGs de Airflow
├── logs/                 # Logs de ejecución
├── bd/                   # Carpetas con códigos para creación de tablas. 
├── scripts/              # Scripts de extracción, transformación y carga.
├── docker-compose.yaml   # Configuración de Docker Compose
├── .env                  # Ejemplo de variables de entorno
├── README.md             # Actual archivo, con la descripción del proyecto.
├── tests_etl_bcra.py     # Script para correr los tests
└── fed_dash.py           # Script para correr el dash de visualicón de la FED
