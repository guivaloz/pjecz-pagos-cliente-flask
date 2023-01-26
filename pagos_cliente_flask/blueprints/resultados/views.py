"""
Resultados, vistas
"""
import logging  # Imports Python standard library logging

from flask import abort, Blueprint, render_template, request, redirect, url_for
import google.cloud.logging  # Imports the Cloud Logging client library
import requests

from pagos_cliente_flask.extensions import csrf
from config.settings import API_BASE_URL, API_TIMEOUT

# Instantiates a client
client = google.cloud.logging.Client()

# Retrieves a Cloud Logging handler based on the environment
# you're running in and integrates the handler with the
# Python logging module. By default this captures all logs
# at INFO level and higher
client.setup_logging()

resultados = Blueprint("resultados", __name__, template_folder="templates")


@resultados.route("/resultado", methods=["GET", "POST"])
@csrf.exempt
def procesar_lo_que_viene_del_banco():
    """Procesar lo que viene del banco"""

    # Si no viene el payload del banco por POST
    if not request.form:
        mensaje_error = "No se recibió el payload del banco."
        logging.warning(mensaje_error)
        abort(400, mensaje_error)
    if request.form["strResponse"] == "":
        mensaje_error = "Es una cadena de texto vacia el payload del banco."
        logging.warning(mensaje_error)
        abort(400, mensaje_error)

    # Preparar el cuerpo a enviar a la API "/pag_pagos/resultado"
    request_body = {
        "xml_encriptado": request.form["strResponse"],
    }

    # Enviar al API, donde se actualizará el pago
    try:
        respuesta = requests.post(
            f"{API_BASE_URL}/pag_pagos/resultado",
            json=request_body,
            timeout=API_TIMEOUT,
        )
    except requests.exceptions.ConnectionError as error:
        mensaje_error = "No se pudo conectar con la API de pagos. " + str(error)
        logging.error(mensaje_error)
        abort(500, mensaje_error)
    except requests.exceptions.Timeout as error:
        mensaje_error = "Tiempo de espera agotado al conectar con la API de pagos. " + str(error)
        logging.error(mensaje_error)
        abort(500, mensaje_error)
    except requests.exceptions.HTTPError as error:
        mensaje_error = "Error HTTP porque la API de pagos arrojó un problema: " + str(error)
        logging.error(mensaje_error)
        abort(500, mensaje_error)
    except requests.exceptions.RequestException as error:
        mensaje_error = "Error desconocido con la API de pagos. " + str(error)
        logging.error(mensaje_error)
        abort(500, mensaje_error)
    datos = respuesta.json()

    # Verificar que haya tenido exito
    mensaje_error = "No se pudo actualizar el carro de pagos."
    if not "success" in datos:
        logging.error(mensaje_error)
        abort(400, mensaje_error)
    if not datos["success"]:
        if "message" in datos:
            logging.error(datos["message"])
            return redirect(url_for("resultados.resultado_fallido", mensaje=datos["message"]))
        logging.error(mensaje_error)
        return redirect(url_for("resultados.resultado_fallido", mensaje=mensaje_error))

    # Validar que haya recibido el estado
    mensaje_error = "No se pudo obtener el estado del pago."
    if not "estado" in datos:
        logging.error(mensaje_error)
        return redirect(url_for("resultados.resultado_fallido", mensaje=mensaje_error))

    # Validar que haya recibido el folio
    mensaje_error = "No se pudo obtener el folio del pago."
    if not "folio" in datos:
        logging.error(mensaje_error)
        return redirect(url_for("resultados.resultado_fallido", mensaje=mensaje_error))

    # Redirigir a la página de resultado PAGADO
    if datos["estado"] == "PAGADO":
        return redirect(url_for("resultados.resultado_pagado", folio=datos["folio"]))

    # De lo contrario, el reultado es FALLIDO
    return redirect(url_for("resultados.resultado_fallido", folio=datos["folio"]))


@resultados.route("/resultado/pagado", methods=["GET", "POST"])
def resultado_pagado():
    """Resultado pagado"""

    # Si viene el folio
    folio = request.args.get("folio")
    if folio is None:
        folio = ""

    # Entregar
    return render_template("resultados/pagado.jinja2", folio=folio)


@resultados.route("/resultado/fallido", methods=["GET", "POST"])
def resultado_fallido():
    """Resultado fallido"""

    # Si viene el folio
    folio = request.args.get("folio")
    if folio is None:
        folio = ""

    # Entregar
    return render_template("resultados/fallido.jinja2", folio=folio)
