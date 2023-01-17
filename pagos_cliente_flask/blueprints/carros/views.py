"""
Carros, vistas
"""
from flask import abort, Blueprint, render_template, request, flash, redirect, url_for
import requests

from config.settings import API_BASE_URL, API_TIMEOUT
from lib.safe_string import safe_clave

from .forms import IngresarForm, RevisarForm

carros = Blueprint("carros", __name__, template_folder="templates")


@carros.route("/carro", methods=["GET", "POST"])
def ingresar():
    """Ingresar datos personales"""

    # Si viene el formulario

    # Tomar por GET la clave del tramite y servicio
    clave = safe_clave(request.args.get("clave"))
    if clave == "":
        abort(400, "No se ha proporcionado la clave del trámite o servicio.")

    # Consultar tramite servicio
    try:
        respuesta = requests.get(
            f"{API_BASE_URL}/pag_tramites_servicios/{clave}",
            timeout=API_TIMEOUT,
        )
        respuesta.raise_for_status()
    except requests.exceptions.ConnectionError as error:
        abort(500, "No se pudo conectar con la API de pagos. " + str(error))
    except requests.exceptions.HTTPError as error:
        abort(500, "Error en la API de pagos. " + str(error))
    except requests.exceptions.Timeout as error:
        abort(500, "Tiempo de espera agotado al conectar con la API de pagos. " + str(error))
    except requests.exceptions.RequestException as error:
        abort(500, "Error desconocido al conectar con la API de pagos. " + str(error))
    datos = respuesta.json()

    # Entregar el formulario para ingresar datos personales
    form = IngresarForm()
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

    # Validar el pago

    # Entregar la pagina para revisar, con el boton para ir al banco
    form = RevisarForm()
    form.descripcion.data = "Descripción del trámite o servicio"
    form.email.data = "loquesea@noexiste.com"
    form.costo.data = "$ 1,000.00"
    return render_template("carros/revisar.jinja2", form=form, pag_pago_id_hasheado="abc123abc123")
