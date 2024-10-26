###Trabajo práctico de variables económicas

##Introducción

Este proyecto genera ingestas diarias del Banco Central de la República Argentina y la Reserva Federal de los Estados Unidos. Se conecta con las APIs públicas de dichas instituciones, extrayendo los valores diarios de las principales variables monetarias.

##Desarrollo del proyecto.

El mismo se realizó generando un entorno local de pruebas con la librería Poetry. El mismo se puede recrear utilizando el comando poetry shell. También si el usuario desea utilizar otro tipo de entorno virtual, en el documento "requirements.txt" se encuentran detallados las librerías necesarias para su utilización.

##Pipelines

El proyecto cuenta con dos pipelines, uno para cada fuente de datos. Ambos cargan sus datos en una fact_table, alojada en Redshift, parte de un esquema estrella con otras dos tablas que abarcan las dimensiones variables y fechas.


Se crearon 2 test unitarios para probar la extraccion y la transformación del pipeline de BCRA, que también se puede realizar con GitHub Actions (está codeado para que se realicen automáticamente cuando se hace un push o un pull request).


