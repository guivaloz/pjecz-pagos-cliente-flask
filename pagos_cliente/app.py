"""
Flask App
"""

from flask import Flask

from pagos_cliente.blueprints.avisos.views import avisos
from pagos_cliente.blueprints.carros.views import carros
from pagos_cliente.blueprints.resultados.views import resultados
from pagos_cliente.blueprints.sistemas.views import sistemas
from pagos_cliente.extensions import csrf


def create_app():
    """Crear app"""

    # Definir app
    app = Flask(__name__)

    # Cargar la configuración
    app.config.from_object("config.settings")

    # Registrar blueprints
    app.register_blueprint(carros)
    app.register_blueprint(resultados)
    app.register_blueprint(sistemas)
    app.register_blueprint(avisos)

    # Cargar las extensiones
    extensions(app)

    # Entregar app
    return app


def extensions(app):
    """Extensiones"""

    # CSRF
    csrf.init_app(app)
