from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length, Optional, Email


class ProveedorForm(FlaskForm):
    nombre = StringField("Nombre", validators=[DataRequired(), Length(max=100)])
    telefono = StringField("Teléfono", validators=[Optional(), Length(max=20)])
    email = StringField("Email", validators=[Optional(), Email(), Length(max=100)])
    direccion = StringField("Dirección", validators=[Optional(), Length(max=150)])
    submit = SubmitField("Guardar")
