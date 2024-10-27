import os
import psycopg2
from psycopg2 import sql

def valores_variable():
    # Conectar a Redshift utilizando las credenciales almacenadas en variables de entorno
    conn = psycopg2.connect(
        dbname=os.getenv('REDSHIFT_DB'),
        user=os.getenv('REDSHIFT_USER'),
        password=os.getenv('REDSHIFT_PASSWORD'),
        host=os.getenv('REDSHIFT_HOST'),
        port=os.getenv('REDSHIFT_PORT')
    )

    # Especificar el esquema donde se creará la tabla
    schema = "2024_nicolas_alvarez_julia_schema"

    # Consulta de inserción
    insert_query = sql.SQL("""
        INSERT INTO {}.dim_variable (variable_id, nombre_variable, fuente, unidad, tipo_variable, frecuencia) VALUES
        (%s, %s, %s, %s, %s, %s)
    """).format(sql.Identifier(schema))

    # Datos para insertar
    datos = [
        ('1', 'Reservas Internacionales del BCRA (en millones de dólares)', 'BCRA', 'valor', 'variable fundamental', 'diaria'),
        ('5', 'Tipo de Cambio Mayorista ($ por USD) Comunicación A 3500', 'BCRA', 'valor', 'variable fundamental', 'diaria'),
        ('6', 'Tasa de Política Monetaria (en % n.a.)', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('7', 'BADLAR en pesos de bancos privados (en % n.a.)', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('8', 'TM20 en pesos de bancos privados (en % n.a.)', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('9', 'Tasas de interés de las operaciones de pase activas para el BCRA, a 1 día de plazo (en % n.a.)', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('10', 'Tasas de interés de las operaciones de pase pasivas para el BCRA, a 1 día de plazo (en % n.a.)', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('11', 'Tasas de interés por préstamos entre entidades financiera privadas (BAIBAR) (en % n.a.)', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('12', 'Tasas de interés por depósitos a 30 días de plazo en entidades financieras (en % n.a.)', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('13', 'Tasa de interés de préstamos por adelantos en cuenta corriente', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('14', 'Tasa de interés de préstamos personales', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('15', 'Base monetaria - Total (en millones de pesos)', 'BCRA', 'valor', 'agregado monetario', 'diaria'),
        ('16', 'Circulación monetaria (en millones de pesos)', 'BCRA', 'valor', 'agregado monetario', 'diaria'),
        ('17', 'Circulación monetaria (en millones de pesos)', 'BCRA', 'valor', 'agregado monetario', 'diaria'),
        ('18', 'Efectivo en entidades financieras (en millones de pesos)', 'BCRA', 'valor', 'agregado monetario', 'diaria'),
        ('19', 'Depósitos de los bancos en cta. cte. en pesos en el BCRA (en millones de pesos)', 'BCRA', 'valor', 'agregado monetario', 'diaria'),
        ('21', 'Depósitos en efectivo en las entidades financieras - Total (en millones de pesos)', 'BCRA', 'valor', 'agregado monetario', 'diaria'),
        ('22', 'En cuentas corrientes (neto de utilización FUCO) (en millones de pesos)', 'BCRA', 'valor', 'agregado monetario', 'diaria'),
        ('23', 'En Caja de ahorros (en millones de pesos)', 'BCRA', 'valor', 'agregado monetario', 'diaria'),
        ('24', 'A plazo (incluye inversiones y excluye CEDROS) (en millones de pesos)', 'BCRA', 'valor', 'agregado monetario', 'diaria'),
        ('25', 'M2 privado, promedio móvil de 30 días, variación interanual (en %)', 'BCRA', 'porcentaje', 'agregado monetario', 'anual'),
        ('26', 'Préstamos de las entidades financieras al sector privado (en millones de pesos)', 'BCRA', 'valor', 'agregado monetario', 'diaria'),
        ('27', 'Inflación mensual (variación en %)', 'BCRA', 'porcentaje', 'variable fundamental', 'mensual'),
        ('28', 'Inflación interanual (variación en % i.a.)', 'BCRA', 'porcentaje', 'variable fundamental', 'anual'),
        ('29', 'Inflación esperada - REM próximos 12 meses - MEDIANA (variación en % i.a)', 'BCRA', 'porcentaje', 'variable fundamental', 'anual'),
        ('34', 'Tasa de Política Monetaria (en % e.a.)', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('35', 'BADLAR en pesos de bancos privados (en % e.a.)', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('41', 'Tasas de interés de las operaciones de pase pasivas para el BCRA, a 1 día de plazo (en % e.a.)', 'BCRA', 'porcentaje', 'tasa', 'anual'),
        ('42', 'Pases pasivos para el BCRA - Saldos (en millones de pesos)', 'BCRA', 'valor', 'agregado monetario', 'diaria'),
        ('DFF', 'Tasa Efectiva de Fondos Federales', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('T10Y2Y', 'Diferencia entre el Rendimiento del Tesoro a 10 años y a 2 años', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DGS1', 'Rendimiento a 1 año del Tesoro de EE.UU. a Madurez Constante', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DGS2', 'Rendimiento a 2 años del Tesoro de EE.UU. a Madurez Constante', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DGS3', 'Rendimiento a 3 años del Tesoro de EE.UU. a Madurez Constante', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DGS5', 'Rendimiento a 5 años del Tesoro de EE.UU. a Madurez Constante', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DGS7', 'Rendimiento a 7 años del Tesoro de EE.UU. a Madurez Constante', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DGS10', 'Rendimiento a 10 años del Tesoro de EE.UU. a Madurez Constante', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DGS20', 'Rendimiento a 20 años del Tesoro de EE.UU. a Madurez Constante', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DGS30', 'Rendimiento a 30 años del Tesoro de EE.UU. a Madurez Constante', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DFII5', 'Rendimiento a 5 años del Tesoro de EE.UU. Indexado a la Inflación', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DFII10', 'Rendimiento a 10 años del Tesoro de EE.UU. Indexado a la Inflación', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DFII30', 'Rendimiento a 30 años del Tesoro de EE.UU. Indexado a la Inflación', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DTB4WK', 'Tasa del Tesoro a 4 semanas en el Mercado Secundario, Base de Descuento', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DTB3', 'Tasa del Tesoro a 3 meses en el Mercado Secundario, Base de Descuento', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DTB6', 'Tasa del Tesoro a 6 meses en el Mercado Secundario, Base de Descuento', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DPRIME', 'Tasa de Préstamo Preferencial Bancaria', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DPCREDIT', 'Crédito de Bancos Comerciales', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DGS1MO', 'Rendimiento a 1 mes del Tesoro de EE.UU. a Madurez Constante', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DGS3MO', 'Rendimiento a 3 meses del Tesoro de EE.UU. a Madurez Constante', 'FED', 'porcentaje', 'tasa', 'anual'),
        ('DGS6MO', 'Rendimiento a 6 meses del Tesoro de EE.UU. a Madurez Constante', 'FED', 'porcentaje', 'tasa', 'anual')
    ]

    # Crear el cursor
    cur = conn.cursor()

    try:
        # Ejecutar la inserción
        for dato in datos:
            cur.execute(insert_query, dato)

        # Confirmar los cambios
        conn.commit()
        print("Datos insertados correctamente en dim_variable.")

    except Exception as e:
        print(f"Error al insertar datos: {e}")
        conn.rollback()

    finally:
        # Cerrar el cursor y la conexión
        cur.close()
        conn.close()

if __name__ == "__main__":
    valores_variable()