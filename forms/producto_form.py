from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DecimalField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Length, Optional


class ProductoForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField("Descripción", validators=[Optional(), Length(max=255)])
    precio = DecimalField("Precio", validators=[DataRequired(), NumberRange(min=0)])
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=0)])
    proveedor_id = SelectField("Proveedor", coerce=int, validators=[Optional()])
    submit = SubmitField("Guardar")
