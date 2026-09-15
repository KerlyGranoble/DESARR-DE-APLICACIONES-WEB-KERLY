import os
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    """Crea y devuelve una nueva conexión a la base de datos MySQL."""
    try:
        conexion = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "tienda_virtual"),
            port=int(os.getenv("DB_PORT", 3306)),
        )
        return conexion
    except Error as e:
        print(f"Error al conectar a MySQL: {e}")
        return None
