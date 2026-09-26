import os
import psycopg2
from psycopg2 import OperationalError
from dotenv import load_dotenv

load_dotenv()


def obtener_conexion():
    """Crea y devuelve una nueva conexión a la base de datos PostgreSQL."""
    try:
        database_url = os.getenv("DATABASE_URL")
        if database_url:
            # Render (y otros hosts) entregan la conexión completa en DATABASE_URL
            conexion = psycopg2.connect(database_url, sslmode="require")
        else:
            # Conexión local usando variables sueltas (desarrollo)
            conexion = psycopg2.connect(
                host=os.getenv("DB_HOST", "localhost"),
                user=os.getenv("DB_USER", "postgres"),
                password=os.getenv("DB_PASSWORD", ""),
                dbname=os.getenv("DB_NAME", "tienda_virtual"),
                port=int(os.getenv("DB_PORT", 5432)),
            )
        return conexion
    except OperationalError as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None
