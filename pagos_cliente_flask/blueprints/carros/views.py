"""
Carros, vistas
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for

from .forms import IngresarForm, RevisarForm

carros = Blueprint("carros", __name__, template_folder="templates")


@carros.route("/carro", methods=["GET", "POST"])
def ingresar():
    """Ingresar datos personales"""

    # Si viene el formulario

    # Tomar por GET la clave del tramite y servicio

    # Validar el tramite servicio

    # Entregar el formulario para ingresar datos personales
    form = IngresarForm()
    return render_template("carros/ingresar.jinja2", form=form)


@carros.route("/carro/<string:pag_pago_id_hasheado>", methods=["GET", "POST"])
def revisar(pag_pago_id_hasheado):
    """Revisar antes de ir al banco"""

    # Validar el pago

    # Entregar la pagina para revisar, con el boton para ir al banco
    form = RevisarForm()
    form.descripcion.data = "Descripción del trámite o servicio"
    form.email.data = "loquesea@noexiste.com"
    form.costo.data = "$ 1,000.00"
    return render_template("carros/revisar.jinja2", form=form, pag_pago_id_hasheado="abc123abc123")
