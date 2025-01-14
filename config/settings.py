"""
Settings

Para produccion, configure los siguientes secretos en Google Cloud Secret Manager:

- pjecz_pagos_cliente_api_base_url
- pjecz_pagos_cliente_api_timeout
- pjecz_pagos_cliente_base_url
- pjecz_pagos_cliente_salt
- pjecz_pagos_cliente_secret_key
- pjecz_pagos_cliente_recaptcha_public_key
- pjecz_pagos_cliente_recaptcha_private_key

Para desarrollo, debe crear un archivo .env con las variables de entorno:

- API_BASE_URL
- API_TIMEOUT
- BASE_URL
- SALT
- SECRET_KEY
- RECAPTCHA_PUBLIC_KEY
- RECAPTCHA_PRIVATE_KEY
"""

import os
from functools import lru_cache

from dotenv import load_dotenv
from google.cloud import secretmanager
from pydantic_settings import BaseSettings

load_dotenv()

PROJECT_ID = os.getenv("PROJECT_ID", "")  # Por defecto esta vacio, esto significa estamos en modo local
SERVICE_PREFIX = os.getenv("SERVICE_PREFIX", "pjecz_hercules")


def get_secret(secret_id: str) -> str:
    """Get secret from google cloud secret manager"""

    # If not in google cloud, return environment variable
    if PROJECT_ID == "":
        return os.getenv(secret_id.upper(), "")

    # Create the secret manager client
    client = secretmanager.SecretManagerServiceClient()

    # Build the resource name of the secret version
    secret = f"{SERVICE_PREFIX}_{secret_id}"
    name = client.secret_version_path(PROJECT_ID, secret, "latest")

    # Access the secret version
    response = client.access_secret_version(name=name)

    # Return the decoded payload
    return response.payload.data.decode("UTF-8")


class Settings(BaseSettings):
    """Settings"""

    API_BASE_URL: str = get_secret("api_base_url")
    API_TIMEOUT: str = get_secret("api_timeout")
    BASE_URL: str = get_secret("base_url")
    SALT: str = get_secret("salt")
    SECRET_KEY: str = get_secret("secret_key")
    RECAPTCHA_PUBLIC_KEY: str = get_secret("recaptcha_public_key")
    RECAPTCHA_PRIVATE_KEY: str = get_secret("recaptcha_private_key")

    class Config:
        """Load configuration"""

        @classmethod
        def customise_sources(cls, init_settings, env_settings, file_secret_settings):
            """Customise sources, first environment variables, then .env file, then google cloud secret manager"""
            return env_settings, file_secret_settings, init_settings


@lru_cache()
def get_settings() -> Settings:
    """Get Settings"""
    return Settings()
