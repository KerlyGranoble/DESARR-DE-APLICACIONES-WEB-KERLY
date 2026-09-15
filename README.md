# Tienda Virtual Online — Proyecto Integrador

Sitio web para la venta de productos por Internet. Desarrollado con Flask, MySQL,
Flask-Login y Flask-WTF. Incluye gestión de Productos, Clientes, Proveedores,
Facturación y un sistema de autenticación de usuarios.

## 1. Requisitos

- Python 3.10+
- MySQL Server (local o remoto)

## 2. Instalación

```bash
# Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

## 3. Base de datos

1. Abre tu cliente de MySQL (MySQL Workbench, phpMyAdmin, consola, etc.).
2. Ejecuta el script `sql/esquema.sql`. Esto crea la base `tienda_virtual`
   y todas las tablas (usuarios, productos, clientes, proveedores, facturacion).

## 4. Variables de entorno

Copia `.env.example` a `.env` y coloca tus credenciales reales:

```bash
cp .env.example .env
```

Edita `.env`:

```
SECRET_KEY=una-clave-larga-y-aleatoria
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=tu_password
DB_NAME=tienda_virtual
DB_PORT=3306
```

**Nunca subas el archivo `.env` real a GitHub** (ya está en `.gitignore`).

## 5. Ejecutar la aplicación

```bash
python app.py
```

Abre tu navegador en `http://127.0.0.1:5000`.

## 6. Prueba completa obligatoria antes de entregar

1. Regístrate en `/registro` con un usuario y contraseña nuevos.
2. Verifica en MySQL que el usuario se guardó y que el campo `password` es un
   hash (no texto plano).
3. Intenta iniciar sesión con una contraseña incorrecta → debe rechazarse.
4. Inicia sesión con las credenciales correctas.
5. Verifica que puedes acceder a `/dashboard`, `/productos`, `/clientes`,
   `/proveedores`, `/facturacion`.
6. Cierra sesión desde el botón "Cerrar sesión".
7. Intenta acceder directamente a `/dashboard` sin sesión → debe redirigirte
   a `/login`.

## 7. Subir a GitHub

```bash
git add .
git commit -m "Semana 13-14: CRUD completo + sistema de login funcional"
git push origin main
```

> **Importante:** GitHub Pages solo mostrará el `index.html` estático de la
> raíz del repositorio (frontend). El sistema de login, Flask-Login, las
> sesiones y la conexión a MySQL solo se pueden comprobar ejecutando la
> aplicación Flask de forma local, tal como pide la guía de la tarea.
