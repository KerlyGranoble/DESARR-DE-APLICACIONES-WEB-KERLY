import os
from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

import models
from forms.login_form import LoginForm
from forms.usuario_form import RegistroForm
from forms.producto_form import ProductoForm
from forms.cliente_form import ClienteForm
from forms.proveedor_form import ProveedorForm
from forms.facturacion_form import FacturacionForm

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "clave-por-defecto-cambiar")

# ------------------------------------------------------------------
# Configuración de Flask-Login
# ------------------------------------------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Debes iniciar sesión para acceder a esta página."


@login_manager.user_loader
def load_user(user_id):
    return models.obtener_usuario_por_id(user_id)


# ------------------------------------------------------------------
# Rutas públicas
# ------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/registro", methods=["GET", "POST"])
def registro():
    form = RegistroForm()
    if form.validate_on_submit():
        existente = models.obtener_usuario_por_nombre(form.usuario.data)
        if existente:
            flash("Ese nombre de usuario ya está registrado.", "danger")
            return render_template("registro.html", form=form)

        password_hash = generate_password_hash(form.password.data)
        models.crear_usuario(form.usuario.data, password_hash)
        flash("Registro exitoso. Ahora puedes iniciar sesión.", "success")
        return redirect(url_for("login"))

    return render_template("registro.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = models.obtener_usuario_por_nombre(form.usuario.data)
        if usuario and check_password_hash(usuario.password, form.password.data):
            login_user(usuario)
            siguiente = request.args.get("next")
            return redirect(siguiente or url_for("dashboard"))
        else:
            flash("Usuario o contraseña incorrectos.", "danger")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Sesión cerrada correctamente.", "info")
    return redirect(url_for("login"))


# ------------------------------------------------------------------
# Rutas protegidas
# ------------------------------------------------------------------
@app.route("/dashboard")
@login_required
def dashboard():
    total_productos = len(models.listar_productos())
    total_clientes = len(models.listar_clientes())
    total_proveedores = len(models.listar_proveedores())
    total_facturas = len(models.listar_facturas())
    return render_template(
        "dashboard.html",
        total_productos=total_productos,
        total_clientes=total_clientes,
        total_proveedores=total_proveedores,
        total_facturas=total_facturas,
    )


# ---------------- PRODUCTOS ----------------
@app.route("/productos")
@login_required
def productos():
    lista = models.listar_productos()
    return render_template("productos.html", productos=lista)


@app.route("/productos/nuevo", methods=["GET", "POST"])
@login_required
def nuevo_producto():
    form = ProductoForm()
    proveedores = models.listar_proveedores()
    form.proveedor_id.choices = [(0, "-- Sin proveedor --")] + [
        (p["id"], p["nombre"]) for p in proveedores
    ]

    if form.validate_on_submit():
        proveedor_id = form.proveedor_id.data if form.proveedor_id.data != 0 else None
        models.crear_producto(
            form.nombre.data,
            form.descripcion.data,
            float(form.precio.data),
            form.stock.data,
            proveedor_id,
        )
        flash("Producto creado correctamente.", "success")
        return redirect(url_for("productos"))

    return render_template("formulario_producto.html", form=form, titulo="Nuevo producto")


@app.route("/productos/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar_producto(id):
    producto = models.obtener_producto(id)
    if not producto:
        flash("Producto no encontrado.", "danger")
        return redirect(url_for("productos"))

    form = ProductoForm()
    proveedores = models.listar_proveedores()
    form.proveedor_id.choices = [(0, "-- Sin proveedor --")] + [
        (p["id"], p["nombre"]) for p in proveedores
    ]

    if form.validate_on_submit():
        proveedor_id = form.proveedor_id.data if form.proveedor_id.data != 0 else None
        models.actualizar_producto(
            id,
            form.nombre.data,
            form.descripcion.data,
            float(form.precio.data),
            form.stock.data,
            proveedor_id,
        )
        flash("Producto actualizado correctamente.", "success")
        return redirect(url_for("productos"))

    if request.method == "GET":
        form.nombre.data = producto["nombre"]
        form.descripcion.data = producto["descripcion"]
        form.precio.data = producto["precio"]
        form.stock.data = producto["stock"]
        form.proveedor_id.data = producto["proveedor_id"] or 0

    return render_template("formulario_producto.html", form=form, titulo="Editar producto")


@app.route("/productos/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_producto(id):
    models.eliminar_producto(id)
    flash("Producto eliminado.", "info")
    return redirect(url_for("productos"))


# ---------------- CLIENTES ----------------
@app.route("/clientes")
@login_required
def clientes():
    lista = models.listar_clientes()
    form = ClienteForm()
    return render_template("clientes.html", clientes=lista, form=form)


@app.route("/clientes/nuevo", methods=["POST"])
@login_required
def nuevo_cliente():
    form = ClienteForm()
    if form.validate_on_submit():
        models.crear_cliente(
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.email.data,
            form.direccion.data,
        )
        flash("Cliente creado correctamente.", "success")
    else:
        flash("Revisa los datos del cliente.", "danger")
    return redirect(url_for("clientes"))


@app.route("/clientes/editar/<int:id>", methods=["POST"])
@login_required
def editar_cliente(id):
    form = ClienteForm()
    if form.validate_on_submit():
        models.actualizar_cliente(
            id,
            form.nombre.data,
            form.cedula.data,
            form.telefono.data,
            form.email.data,
            form.direccion.data,
        )
        flash("Cliente actualizado correctamente.", "success")
    else:
        flash("Revisa los datos del cliente.", "danger")
    return redirect(url_for("clientes"))


@app.route("/clientes/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_cliente(id):
    models.eliminar_cliente(id)
    flash("Cliente eliminado.", "info")
    return redirect(url_for("clientes"))


# ---------------- PROVEEDORES ----------------
@app.route("/proveedores")
@login_required
def proveedores():
    lista = models.listar_proveedores()
    form = ProveedorForm()
    return render_template("proveedores.html", proveedores=lista, form=form)


@app.route("/proveedores/nuevo", methods=["POST"])
@login_required
def nuevo_proveedor():
    form = ProveedorForm()
    if form.validate_on_submit():
        models.crear_proveedor(
            form.nombre.data, form.telefono.data, form.email.data, form.direccion.data
        )
        flash("Proveedor creado correctamente.", "success")
    else:
        flash("Revisa los datos del proveedor.", "danger")
    return redirect(url_for("proveedores"))


@app.route("/proveedores/editar/<int:id>", methods=["POST"])
@login_required
def editar_proveedor(id):
    form = ProveedorForm()
    if form.validate_on_submit():
        models.actualizar_proveedor(
            id, form.nombre.data, form.telefono.data, form.email.data, form.direccion.data
        )
        flash("Proveedor actualizado correctamente.", "success")
    else:
        flash("Revisa los datos del proveedor.", "danger")
    return redirect(url_for("proveedores"))


@app.route("/proveedores/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_proveedor(id):
    models.eliminar_proveedor(id)
    flash("Proveedor eliminado.", "info")
    return redirect(url_for("proveedores"))


# ---------------- FACTURACIÓN ----------------
@app.route("/facturacion")
@login_required
def facturacion():
    lista = models.listar_facturas()
    form = FacturacionForm()
    form.cliente_id.choices = [(c["id"], c["nombre"]) for c in models.listar_clientes()]
    form.producto_id.choices = [
        (p["id"], f"{p['nombre']} (${p['precio']})") for p in models.listar_productos()
    ]
    return render_template("facturacion.html", facturas=lista, form=form)


@app.route("/facturacion/nueva", methods=["POST"])
@login_required
def nueva_factura():
    form = FacturacionForm()
    form.cliente_id.choices = [(c["id"], c["nombre"]) for c in models.listar_clientes()]
    form.producto_id.choices = [
        (p["id"], f"{p['nombre']} (${p['precio']})") for p in models.listar_productos()
    ]

    if form.validate_on_submit():
        producto = models.obtener_producto(form.producto_id.data)
        total = float(producto["precio"]) * form.cantidad.data
        models.crear_factura(form.cliente_id.data, form.producto_id.data, form.cantidad.data, total)
        flash("Factura registrada correctamente.", "success")
    else:
        flash("Revisa los datos de la factura.", "danger")
    return redirect(url_for("facturacion"))


@app.route("/facturacion/eliminar/<int:id>", methods=["POST"])
@login_required
def eliminar_factura(id):
    models.eliminar_factura(id)
    flash("Factura eliminada.", "info")
    return redirect(url_for("facturacion"))


if __name__ == "__main__":
    app.run(debug=True)
