
from sqlalchemy import text
from database import engine

try:
    with engine.connect() as conexion:
        resultado = conexion.execute(
            text("SELECT current_database();")
        )

        nombre_bd = resultado.scalar()

        print("Conexión exitosa con PostgreSQL")
        print("Base de datos:", nombre_bd)

except Exception as error:
    print("Error al conectar con PostgreSQL:")
    print(error)
