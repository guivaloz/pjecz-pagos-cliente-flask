"""
Configuración de la aplicación
"""
import os


# API
API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:8000/v2")
API_TIMEOUT = int(os.environ.get("API_TIMEOUT", 12))

# Salt para convertir/reconverir el id en hash
SALT = os.environ.get("SALT", "Esta es una muy mala cadena aleatoria")

# Secret key para CSRF
# SECRET_KEY = os.urandom(24)
SECRET_KEY = "MZSVRPga7z0Zbd9UuF8E16Bu"
