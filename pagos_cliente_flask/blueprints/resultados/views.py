"""
Resultados, vistas
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for


resultados = Blueprint("resultados", __name__, template_folder="templates")


@resultados.route("/resultado", methods=["GET", "POST"])
def procesar_lo_que_viene_del_banco():
    """Procesar lo que viene del banco"""
    # pendiente

    # Tomar el PAYLOAD del banco

    # Validar el ID del pago

    # Entregar
    return render_template("resultados/pagado.jinja2")


@resultados.route("/resultado/pagado", methods=["GET", "POST"])
def resultado_pagado():
    """Resultado pagado"""

    # Entregar
    return render_template("resultados/pagado.jinja2")


@resultados.route("/resultado/fallido", methods=["GET", "POST"])
def resultado_fallido():
    """Resultado fallido"""

    # Entregar
    return render_template("resultados/fallido.jinja2")
