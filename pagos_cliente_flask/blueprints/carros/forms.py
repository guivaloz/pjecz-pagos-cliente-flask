"""
Carros, formularios
"""
from flask_wtf import FlaskForm
from wtforms import BooleanField, EmailField, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class IngresarForm(FlaskForm):
    """Formulario para ingresar datos personales"""

    clave = HiddenField("Clave del trámite o servicio")
    nombres = StringField(
        "Nombres",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    apellido_primero = StringField(
        "Primer apellido",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    apellido_segundo = StringField(
        "Segundo apellido",
        validators=[DataRequired(), Length(min=3, max=64)],
    )
    curp = StringField(
        "CURP",
        validators=[DataRequired(), Length(min=18, max=18)],
        render_kw={"placeholder": "18 caracteres"},
    )
    email = EmailField(
        "Email",
        validators=[DataRequired(), Length(min=3, max=128)],
    )
    telefono = StringField(
        "Telefono celular",
        validators=[DataRequired(), Length(min=10, max=10)],
        render_kw={"placeholder": "10 dígitos sin espacios ni guiones"},
    )
    aceptar = BooleanField(
        "He leído y acepto el Aviso de Privacidad",
        validators=[DataRequired()],
    )
    continuar = SubmitField("Continuar")


class RevisarForm(FlaskForm):
    """Formulario para revisar antes de ir al banco"""

    descripcion = StringField("Trámite o servicio")
    email = EmailField("Email")
    total = StringField("Total")
    continuar = SubmitField("Continuar")
