"""
Carros, formularios
"""
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField
from wtforms import BooleanField, EmailField, HiddenField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class IngresarForm(FlaskForm):
    """Formulario para ingresar los datos personales del cliente"""

    # Campo oculto con la clave del trámite o servicio, es obligatorio
    pag_tramite_servicio_clave = HiddenField("Clave del trámite o servicio")

    # Campos ocultos, que son opcionales
    autoridad_clave = HiddenField("Clave de la autoridad")
    cantidad = HiddenField("Cantidad")
    descripcion = HiddenField("Descripción")
    distrito_clave = HiddenField("Clave del distrito")

    # Campos que debe llenar el cliente con sus datos personales
    nombres = StringField("Nombres", validators=[DataRequired(), Length(min=3, max=64)])
    apellido_primero = StringField("Primer apellido", validators=[DataRequired(), Length(min=3, max=64)])
    apellido_segundo = StringField("Segundo apellido", validators=[DataRequired(), Length(min=3, max=64)])
    curp = StringField("CURP", validators=[DataRequired(), Length(min=18, max=18)], render_kw={"placeholder": "18 caracteres"})
    email = EmailField("Email", validators=[DataRequired(), Length(min=3, max=128)])
    telefono = StringField("Telefono celular", validators=[DataRequired(), Length(min=10, max=10)], render_kw={"placeholder": "10 dígitos sin espacios ni guiones"})

    # Debe aceptar el aviso de privacidad
    aceptar = BooleanField("He leído y acepto el <a href='/aviso' class='nav-link link-aviso'>Aviso de Privacidad</a>", validators=[DataRequired()])

    # Debe cumplir el recapcha
    recaptcha = RecaptchaField()

    # Botón para continuar con la revisión de los datos antes de ir al banco
    continuar = SubmitField("Continuar")
