"""
Carros, vistas
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for


carros = Blueprint("carros", __name__, template_folder="templates")


@carros.route("/carro", methods=["GET", "POST"])
def ingresar():
    """Ingresar datos personales"""

    # Si viene el formulario

    # Tomar por GET la clave del tramite y servicio

    # Validar que exista el tramite y servicio

    # Entregar el formulario para ingresar datos personales
    return render_template("carros/ingresar.jinja2")


@carros.route("/carro/<int:pag_pago_id>", methods=["GET", "POST"])
def revisar(pag_pago_id):
    """Revisar antes de ir al banco"""

    # Validar el pago

    # Entregar la pagina para revisar, con el boton para ir al banco
    return render_template("carros/revisar.jinja2")
