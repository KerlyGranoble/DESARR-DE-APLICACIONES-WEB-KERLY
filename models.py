from flask_login import UserMixin
from conexion.conexion import obtener_conexion


# ------------------------------------------------------------------
# USUARIO (Flask-Login)
# ------------------------------------------------------------------
class Usuario(UserMixin):
    def __init__(self, id, usuario, password):
        self.id = id
        self.usuario = usuario
        self.password = password


def obtener_usuario_por_id(user_id):
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (user_id,))
    fila = cursor.fetchone()
    cursor.close()
    conexion.close()
    if fila:
        return Usuario(fila["id"], fila["usuario"], fila["password"])
    return None


def obtener_usuario_por_nombre(usuario):
    conexion = obtener_conexion()
    if not conexion:
        return None
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM usuarios WHERE usuario = %s", (usuario,))
    fila = cursor.fetchone()
    cursor.close()
    conexion.close()
    if fila:
        return Usuario(fila["id"], fila["usuario"], fila["password"])
    return None


def crear_usuario(usuario, password_hash):
    conexion = obtener_conexion()
    if not conexion:
        return False
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO usuarios (usuario, password) VALUES (%s, %s)",
        (usuario, password_hash),
    )
    conexion.commit()
    cursor.close()
    conexion.close()
    return True


# ------------------------------------------------------------------
# PROVEEDORES
# ------------------------------------------------------------------
def listar_proveedores():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM proveedores ORDER BY id DESC")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos


def obtener_proveedor(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM proveedores WHERE id = %s", (id,))
    dato = cursor.fetchone()
    cursor.close()
    conexion.close()
    return dato


def crear_proveedor(nombre, telefono, email, direccion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "INSERT INTO proveedores (nombre, telefono, email, direccion) VALUES (%s, %s, %s, %s)",
        (nombre, telefono, email, direccion),
    )
    conexion.commit()
    cursor.close()
    conexion.close()


def actualizar_proveedor(id, nombre, telefono, email, direccion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        "UPDATE proveedores SET nombre=%s, telefono=%s, email=%s, direccion=%s WHERE id=%s",
        (nombre, telefono, email, direccion, id),
    )
    conexion.commit()
    cursor.close()
    conexion.close()


def eliminar_proveedor(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM proveedores WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()


# ------------------------------------------------------------------
# PRODUCTOS
# ------------------------------------------------------------------
def listar_productos():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        """SELECT p.*, pr.nombre AS proveedor_nombre
           FROM productos p
           LEFT JOIN proveedores pr ON p.proveedor_id = pr.id
           ORDER BY p.id DESC"""
    )
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos


def obtener_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM productos WHERE id = %s", (id,))
    dato = cursor.fetchone()
    cursor.close()
    conexion.close()
    return dato


def crear_producto(nombre, descripcion, precio, stock, proveedor_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """INSERT INTO productos (nombre, descripcion, precio, stock, proveedor_id)
           VALUES (%s, %s, %s, %s, %s)""",
        (nombre, descripcion, precio, stock, proveedor_id),
    )
    conexion.commit()
    cursor.close()
    conexion.close()


def actualizar_producto(id, nombre, descripcion, precio, stock, proveedor_id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """UPDATE productos SET nombre=%s, descripcion=%s, precio=%s, stock=%s, proveedor_id=%s
           WHERE id=%s""",
        (nombre, descripcion, precio, stock, proveedor_id, id),
    )
    conexion.commit()
    cursor.close()
    conexion.close()


def eliminar_producto(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM productos WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()


# ------------------------------------------------------------------
# CLIENTES
# ------------------------------------------------------------------
def listar_clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes ORDER BY id DESC")
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos


def obtener_cliente(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute("SELECT * FROM clientes WHERE id = %s", (id,))
    dato = cursor.fetchone()
    cursor.close()
    conexion.close()
    return dato


def crear_cliente(nombre, cedula, telefono, email, direccion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """INSERT INTO clientes (nombre, cedula, telefono, email, direccion)
           VALUES (%s, %s, %s, %s, %s)""",
        (nombre, cedula, telefono, email, direccion),
    )
    conexion.commit()
    cursor.close()
    conexion.close()


def actualizar_cliente(id, nombre, cedula, telefono, email, direccion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """UPDATE clientes SET nombre=%s, cedula=%s, telefono=%s, email=%s, direccion=%s
           WHERE id=%s""",
        (nombre, cedula, telefono, email, direccion, id),
    )
    conexion.commit()
    cursor.close()
    conexion.close()


def eliminar_cliente(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()


# ------------------------------------------------------------------
# FACTURACIÓN
# ------------------------------------------------------------------
def listar_facturas():
    conexion = obtener_conexion()
    cursor = conexion.cursor(dictionary=True)
    cursor.execute(
        """SELECT f.*, c.nombre AS cliente_nombre, p.nombre AS producto_nombre
           FROM facturacion f
           JOIN clientes c ON f.cliente_id = c.id
           JOIN productos p ON f.producto_id = p.id
           ORDER BY f.id DESC"""
    )
    datos = cursor.fetchall()
    cursor.close()
    conexion.close()
    return datos


def crear_factura(cliente_id, producto_id, cantidad, total):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute(
        """INSERT INTO facturacion (cliente_id, producto_id, cantidad, total)
           VALUES (%s, %s, %s, %s)""",
        (cliente_id, producto_id, cantidad, total),
    )
    conexion.commit()
    cursor.close()
    conexion.close()


def eliminar_factura(id):
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("DELETE FROM facturacion WHERE id = %s", (id,))
    conexion.commit()
    cursor.close()
    conexion.close()
