"""
Carros, vistas
"""
from flask import abort, Blueprint, render_template, redirect, request, url_for
import requests

from config.settings import API_BASE_URL, API_TIMEOUT, BASE_URL
from lib.safe_string import safe_clave, safe_email, safe_integer, safe_string
from lib.hashids import cifrar_id, descifrar_id

from .forms import IngresarForm

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
            "cantidad": safe_integer(form.cantidad.data, default="1"),
            "pag_tramite_servicio_clave": safe_clave(form.pag_tramite_servicio_clave.data),
            "autoridad_clave": safe_clave(form.autoridad_clave.data),
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
        except requests.exceptions.HTTPError as error:
            abort(500, "Error HTTP porque la API de pagos arrojó un problema: " + str(error))
        except requests.exceptions.RequestException as error:
            abort(500, "Error desconocido con la API de pagos. " + str(error))
        datos = respuesta.json()

        # Verificar que haya tenido exito
        if not "success" in datos:
            abort(400, "No se pudo crear el carro para pagar.")
        if not datos["success"]:
            if "message" in datos:
                abort(400, datos["message"])
            abort(400, "No se pudo crear el carro para pagar.")

        # Validar que haya recibido el id del pago
        if not "pag_pago_id" in datos:
            abort(400, "No se pudo obtener el id del pago.")

        # Redireccionar a la página de revisión
        return redirect(url_for("carros.revisar", pag_pago_id_hasheado=cifrar_id(int(datos["pag_pago_id"])), banco_url=datos["url"]))

    # Tomar por GET la cantidad
    cantidad = safe_integer(request.args.get("cantidad"), default="1")

    # Tomar por GET la clave del tramite y servicio
    pag_tramite_servicio_clave = safe_clave(request.args.get("clave"))
    if pag_tramite_servicio_clave == "":
        abort(400, "No se ha proporcionado la clave del trámite o servicio.")

    # Tomar por GET la clave de la autoridad
    autoridad_clave = safe_clave(request.args.get("autoridad_clave"))

    # Consultar tramite-servicio por su clave
    try:
        respuesta = requests.get(
            f"{API_BASE_URL}/pag_tramites_servicios/{pag_tramite_servicio_clave}",
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        abort(500, "No se pudo conectar con la API de pagos. " + str(error))
    except requests.exceptions.Timeout as error:
        abort(500, "Tiempo de espera agotado al conectar con la API de pagos. " + str(error))
    except requests.exceptions.HTTPError as error:
        abort(500, "Error HTTP porque la API de pagos arrojó un problema: " + str(error))
    except requests.exceptions.RequestException as error:
        abort(500, "Error desconocido con la API de pagos. " + str(error))
    datos = respuesta.json()

    # Verificar que haya tenido exito
    if not "success" in datos:
        abort(400, "No se pudo consultar el trámite o servicio.")
    if not datos["success"]:
        if "message" in datos:
            abort(400, datos["message"])
        abort(400, "No se pudo consultar el trámite o servicio.")

    # Si viene la clave de la autoridad
    autoridad_descripcion = ""
    if autoridad_clave != "":
        # Consultar la autoridad por su clave
        try:
            respuesta = requests.get(
                f"{API_BASE_URL}/autoridades/{autoridad_clave}",
                timeout=API_TIMEOUT,
            )
        except requests.exceptions.ConnectionError as error:
            abort(500, "No se pudo conectar con la API de autoridades. " + str(error))
        except requests.exceptions.Timeout as error:
            abort(500, "Tiempo de espera agotado al conectar con la API de autoridades. " + str(error))
        except requests.exceptions.HTTPError as error:
            abort(500, "Error HTTP porque la API de autoridades arrojó un problema: " + str(error))
        except requests.exceptions.RequestException as error:
            abort(500, "Error desconocido con la API de autoridades. " + str(error))
        autoridad_datos = respuesta.json()
        # Verificar que haya tenido exito
        if not "success" in autoridad_datos:
            abort(400, "No se pudo consultar la autoridad.")
        if not autoridad_datos["success"]:
            if "message" in autoridad_datos:
                abort(400, autoridad_datos["message"])
            abort(400, "No se pudo consultar la autoridad.")
        autoridad_descripcion = autoridad_datos["descripcion"]

    # Validar que haya recibido la descripcion
    if not "descripcion" in datos:
        abort(400, "No se pudo obtener la descripción del trámite o servicio.")

    # Validar que haya recibido el costo
    if not "costo" in datos:
        abort(400, "No se pudo obtener el costo del trámite o servicio.")

    # Entregar el formulario para ingresar datos personales
    form.cantidad.data = cantidad
    form.pag_tramite_servicio_clave.data = pag_tramite_servicio_clave
    form.autoridad_clave.data = autoridad_clave
    return render_template(
        "carros/ingresar.jinja2",
        form=form,
        autoridad_descripcion=autoridad_descripcion,
        descripcion=datos["descripcion"],
        costo=datos["costo"],
    )


@carros.route("/carro/<string:pag_pago_id_hasheado>", methods=["GET", "POST"])
def revisar(pag_pago_id_hasheado):
    """Revisar antes de ir al banco"""

    # Si viene el url del banco
    url = request.args.get(key="banco_url", default="")

    # Valiar el ID cifrado
    pag_pago_id = descifrar_id(pag_pago_id_hasheado)
    if pag_pago_id is None:
        abort(400, "No es válido el ID del pago.")

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
    except requests.exceptions.HTTPError as error:
        abort(500, "Error HTTP porque la API de pagos arrojó un problema: " + str(error))
    except requests.exceptions.RequestException as error:
        abort(500, "Error desconocido con la API de pagos. " + str(error))
    datos = respuesta.json()

    # Verificar que haya tenido exito
    if not "success" in datos:
        abort(400, "No se pudo consultar el carro de pagos.")
    if not datos["success"]:
        if "message" in datos:
            abort(400, datos["message"])
        abort(400, "No se pudo consultar el carro de pagos.")

    # Validar que se haya recibido el email
    if not "cit_cliente_nombre" in datos:
        abort(400, "No se recibió el nombre.")

    # Validar que se haya recibido el email
    if not "email" in datos:
        abort(400, "No se recibió el email.")

    # Validar que se haya recibido el total
    if not "estado" in datos:
        abort(400, "No se recibió el estado del pago.")

    # Validar que se haya recibido la descripcion
    if not "folio" in datos:
        abort(400, "No se recibió el folio.")

    # Validar que se haya recibido la descripcion
    if not "pag_tramite_servicio_descripcion" in datos:
        abort(400, "No se recibió la descripción del trámite o servicio.")

    # Validar que se haya recibido el total
    if not "total" in datos:
        abort(400, "No se recibió el total.")

    # Validar que se haya recibido la resultado_tiempo
    if not "resultado_tiempo" in datos:
        abort(400, "No se recibió la fecha y hora del resultado de la operación bancaria.")

    # Si NO hay URL y el estado es SOLICITADO
    if url == "" and datos["estado"] == "SOLICITADO":
        return redirect(url_for("resultados.resultado_abortado"))

    # Si el estado es PAGADO, mostrar el comprobante del pago
    if datos["estado"] == "PAGADO":
        return render_template(
            "carros/comprobante.jinja2",
            nombre=datos["cit_cliente_nombre"],
            email=datos["email"],
            folio=datos["folio"],
            descripcion=datos["pag_tramite_servicio_descripcion"],
            total=datos["total"],
            resultado_tiempo=datos["resultado_tiempo"],
            comprobante_url=BASE_URL + url_for("carros.revisar", pag_pago_id_hasheado=pag_pago_id_hasheado),
        )

    # Si el estado es FALLIDO o CANCELADO, redireccionar a la página de pago fallido
    if datos["estado"] == "FALLIDO" or datos["estado"] == "CANCELADO":
        return redirect(url_for("resultados.resultado_fallido", folio=datos["folio"]))

    # Como se tiene el URL, entregar la pagina para revisar, con el boton para ir al banco
    return render_template(
        "carros/revisar.jinja2",
        descripcion=datos["pag_tramite_servicio_descripcion"],
        email=datos["email"],
        total=datos["total"],
        pag_pago_id_hasheado=pag_pago_id_hasheado,
        url=url,
    )
