"""
Resultados, vistas
"""

import requests
from flask import Blueprint, abort, current_app, jsonify, redirect, render_template, request, url_for

from pagos_cliente.extensions import csrf

resultados = Blueprint("resultados", __name__, template_folder="templates")


@resultados.route("/resultado", methods=["GET", "POST"])
@csrf.exempt
def procesar_lo_que_viene_del_banco():
    """Procesar lo que viene del banco"""

    # Si no viene el payload del banco por POST
    if not request.form:
        abort(400, "No se ha proporcionado el payload del banco.")
    if request.form["strResponse"] == "":
        abort(400, "No se ha proporcionado el payload del banco.")

    # Preparar el cuerpo a enviar a la API "/pag_pagos/resultado"
    request_body = {
        "xml_encriptado": request.form["strResponse"],
    }

    # Enviar al API, donde se actualizará el pago
    try:
        respuesta = requests.post(
            f"{current_app.config['API_BASE_URL']}/pag_pagos/resultado",
            json=request_body,
            timeout=current_app.config["API_TIMEOUT"],
        )
    except requests.exceptions.ConnectionError as error:
        abort(500, "No se pudo conectar con la API de pagos. " + str(error))
    except requests.exceptions.Timeout as error:
        abort(500, "Tiempo de espera agotado al conectar con la API de pagos. " + str(error))
    except requests.exceptions.HTTPError as error:
        abort(500, "Error HTTP porque la API de pagos arrojó un problema: " + str(error))
    except requests.exceptions.RequestException as error:
        abort(500, "Error desconocido con la API de pagos. " + str(error))
    datos = respuesta.json()

    # Verificar que haya tenido éxito
    if not "success" in datos:
        abort(400, "No se pudo actualizar el carro de pagos.")
    if not datos["success"]:
        if "message" in datos:
            abort(400, datos["message"])
        abort(400, "No se pudo actualizar el carro de pagos.")

    # Validar que haya recibido el estado
    if not "estado" in datos:
        abort(400, "No se pudo obtener el estado del pago.")

    # Validar que haya recibido el folio
    if not "folio" in datos:
        abort(400, "No se pudo obtener el folio del pago.")

    #
    # Comentado porque no funciona como se esperaba
    #
    # Preparar un mensaje en JSON para responder al banco con estatus 200
    # response = jsonify({"message": "Datos recibidos satisfactoriamente"})
    # response.status_code = 200
    #
    # Redirigir a la página de resultado PAGADO
    # if datos["estado"] == "PAGADO":
    #     pagado_url = url_for("resultados.resultado_pagado", folio=datos["folio"])
    #     return redirect(pagado_url), response.status_code
    #
    # De lo contrario, redirigir a la página de resultado FALLIDO
    # fallido_url = url_for("resultados.resultado_fallido", folio=datos["folio"])
    # return redirect(fallido_url), response.status_code

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


@resultados.route("/resultado/abortado", methods=["GET", "POST"])
def resultado_abortado():
    """Resultado abortado"""

    # Entregar
    return render_template("resultados/abortado.jinja2")
