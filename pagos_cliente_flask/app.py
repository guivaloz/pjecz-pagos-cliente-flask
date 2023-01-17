"""
Flask App
"""
from flask import Flask

from .extensions import csrf

from .blueprints.carros.views import carros
from .blueprints.resultados.views import resultados


def create_app():
    """Crear app"""

    # Definir app
    app = Flask(__name__)

    # Cargar la configuración
    app.config.from_object('config.settings')

    # Registrar blueprints
    app.register_blueprint(carros)
    app.register_blueprint(resultados)

    # Cargar las extensiones
    extensions(app)

    # Entregar app
    return app


def extensions(app):
    """Extensiones"""

    # CSRF
    csrf.init_app(app)
