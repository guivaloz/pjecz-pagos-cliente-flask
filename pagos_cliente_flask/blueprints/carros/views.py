"""
Carros, vistas
"""
from flask import abort, Blueprint, render_template, request, redirect, url_for
import requests

from config.settings import API_BASE_URL, API_TIMEOUT
from lib.safe_string import safe_clave, safe_email, safe_string
from lib.hashids import cifrar_id

from .forms import IngresarForm, RevisarForm

carros = Blueprint("carros", __name__, template_folder="templates")


@carros.route("/carro", methods=["GET", "POST"])
def ingresar():
    """Ingresar datos personales"""

    # Si viene el formulario
    form = IngresarForm()
    if form.validate_on_submit():

        # Preparar el cuerpo a enviar a la API "/pag_pagos/carro"
        request_body = {
            "nombres": safe_string(form.nombres.data, save_enie=True),
            "apellido_primero": safe_string(form.apellido_primero.data, save_enie=True),
            "apellido_segundo": safe_string(form.apellido_segundo.data, save_enie=True),
            "curp": safe_string(form.curp.data),
            "email": safe_email(form.email.data),
            "telefono": safe_string(form.telefono.data),
            "pag_tramite_servicio_clave": safe_clave(form.clave.data),
        }

        # Enviar al API, donde se creará el cliente de no existir y el pago
        try:
            respuesta = requests.post(
                f"{API_BASE_URL}/pag_pagos/carro",
                json=request_body,
                timeout=API_TIMEOUT,
            )
            respuesta.raise_for_status()
        except requests.exceptions.ConnectionError as error:
            abort(500, "No se pudo conectar con la API de pagos. " + str(error))
        except requests.exceptions.Timeout as error:
            abort(500, "Tiempo de espera agotado al conectar con la API de pagos. " + str(error))
        except requests.exceptions.RequestException as error:
            abort(500, "Error desconocido con la API de pagos. " + str(error))
        datos = respuesta.json()
        if not "pag_pago_id" in datos:
            abort(500, "No se pudo agregar el trámite o servicio al carro.")

        # Redirigir a la página de revisión
        return redirect(url_for("carros.revisar", pag_pago_id_hasheado=cifrar_id(int(datos["pag_pago_id"]))))

    # Tomar por GET la clave del tramite y servicio
    clave = safe_clave(request.args.get("clave"))
    if clave == "":
        abort(400, "No se ha proporcionado la clave del trámite o servicio.")

    # Consultar tramite-servicio por su clave
    try:
        respuesta = requests.get(
            f"{API_BASE_URL}/pag_tramites_servicios/{clave}",
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        abort(500, "No se pudo conectar con la API de pagos. " + str(error))
    except requests.exceptions.Timeout as error:
        abort(500, "Tiempo de espera agotado al conectar con la API de pagos. " + str(error))
    except requests.exceptions.RequestException as error:
        abort(500, "Error desconocido con la API de pagos. " + str(error))
    datos = respuesta.json()
    if not "descripcion" in datos or not "costo" in datos:
        abort(500, "No se pudo consultar el trámite o servicio.")

    # Entregar el formulario para ingresar datos personales
    form.clave.data = clave
    return render_template(
        "carros/ingresar.jinja2",
        form=form,
        descripcion=datos["descripcion"],
        costo=datos["costo"],
    )


@carros.route("/carro/<string:pag_pago_id_hasheado>", methods=["GET", "POST"])
def revisar(pag_pago_id_hasheado):
    """Revisar antes de ir al banco"""

    # Consultar el pago
    try:
        respuesta = requests.get(
            f"{API_BASE_URL}/pag_pagos/{pag_pago_id_hasheado}",
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        abort(500, "No se pudo conectar con la API de pagos. " + str(error))
    except requests.exceptions.Timeout as error:
        abort(500, "Tiempo de espera agotado al conectar con la API de pagos. " + str(error))
    except requests.exceptions.RequestException as error:
        abort(500, "Error desconocido con la API de pagos. " + str(error))
    datos = respuesta.json()
    if not "pag_tramite_servicio_descripcion" in datos or not "email" in datos or not "total" in datos:
        abort(500, "No se pudo consultar el pago.")

    # Entregar la pagina para revisar, con el boton para ir al banco
    form = RevisarForm()
    form.descripcion.data = datos["pag_tramite_servicio_descripcion"]
    form.email.data = datos["email"]
    form.total.data = datos["total"]
    return render_template(
        "carros/revisar.jinja2",
        form=form,
        pag_pago_id_hasheado=pag_pago_id_hasheado,
    )
