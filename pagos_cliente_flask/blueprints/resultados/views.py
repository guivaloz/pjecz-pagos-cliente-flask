"""
Resultados, vistas
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for


resultados = Blueprint("resultados", __name__, template_folder="templates")


@resultados.route("/resultado", methods=["GET", "POST"])
def procesar_lo_que_viene_del_banco():
    """Procesar lo que viene del banco"""

    # Si viene el formulario

    # Tomar por GET la clave del tramite y servicio

    # Validar que exista el tramite y servicio

    # Entregar la pagina donde el estado es FALLIDO

    # Entregar la pagina donde el estado es PAGADO
    return render_template("resultados/pagado.jinja2")
