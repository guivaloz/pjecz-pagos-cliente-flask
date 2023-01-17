"""
Configuración de la aplicación
"""
import os


# Secret key para CSRF
SECRET_KEY = os.urandom(24)

# Requests
API_BASE_URL = "http://localhost:8006/v2"
API_TIMEOUT = 12
