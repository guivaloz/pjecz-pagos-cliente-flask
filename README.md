# pjecz-pagos-cliente-flask

Cliente del Portal de Pagos hecho con Flask.

## Configurar

Genere el `SECRET_KEY` con este comando

```bash
openssl rand -hex 32
```

Crear archivo `.env` con

```ini
# API Citas V3 cliente: el cual usa success y message
API_BASE_URL="http://localhost:8000/v3"
API_TIMEOUT=12

# Base URL sirve para elaborar el vinculo al comprobante del pago
BASE_URL="http://localhost:5000"

# Flask
FLASK_APP=pagos_cliente.app
FLASK_DEBUG=1

# Salt sirve para cifrar el ID con HashID
SALT=XXXXXXXXXXXXXXXXXXXXXXXX

# Secret key sirve para CSRF
SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXX

# reCAPTCHA configuration
RECAPTCHA_PUBLIC_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
RECAPTCHA_PRIVATE_KEY=XXXXXXXXXXXXXXXXXXXXXXXX
```

Crear archivo `.bashrc` que arranque el entorno virtual y cargue las variables

```bash
if [ -f ~/.bashrc ]
then
    . ~/.bashrc
fi

if command -v figlet &> /dev/null
then
    figlet PJECZ Pagos Cliente Flask
else
    echo "== PJECZ Pagos Cliente Flask"
fi
echo

if [ -f .env ]
then
    echo "-- Variables de entorno"
    export $(grep -v '^#' .env | xargs)
    echo "   API_BASE_URL: ${API_BASE_URL}"
    echo "   API_TIMEOUT: ${API_TIMEOUT}"
    echo "   FLASK_APP: ${FLASK_APP}"
    echo "   FLASK_DEBUG: ${FLASK_DEBUG}"
    echo "   RECAPTCHA_PUBLIC_KEY: ${RECAPTCHA_PUBLIC_KEY}"
    echo "   RECAPTCHA_PRIVATE_KEY: ${RECAPTCHA_PRIVATE_KEY}"
    echo "   SALT: ${SALT}"
    echo "   SECRET_KEY: ${SECRET_KEY}"
    echo
fi

if [ -d .venv ]
then
    echo "-- Python Virtual Environment"
    source .venv/bin/activate
    echo "   $(python3 --version)"
    export PYTHONPATH=$(pwd)
    echo "   PYTHONPATH: ${PYTHONPATH}"
    echo
    echo "-- Ejecutar Flask"
    alias arrancar="flask run --port=5000"
    echo "   arrancar = flask run --port=5000"
    echo
fi

if [ -f app.yaml ]
then
    echo "-- Subir a Google Cloud"
    echo "   poetry export -f requirements.txt --output requirements.txt --without-hashes"
    echo "   gcloud app deploy"
    echo
fi
```

## Configurar Poetry

Por defecto, el entorno se guarda en un directorio unico en `~/.cache/pypoetry/virtualenvs`

Modifique para que el entorno se guarde en el mismo directorio que el proyecto

```bash
poetry config --list
poetry config virtualenvs.in-project true
```

Verifique que este en True

```bash
poetry config virtualenvs.in-project
```

## Instalar

Crear entorno virtual con Python 3.11

```bash
python3.11 -m venv .venv
```

Activar entorno virtual

```bash
source .venv/bin/activate
```

Actualizar pip de ser necesario

```bash
pip install --upgrade pip
```

Instalar Poetry para manejar dependencias

```bash
pip install poetry
```

Instalar dependencias

```bash
poetry install
```

## Arrancar

Cargar el `.bashrc`

```bash
source .bashrc
```

Ejecutar Flask con el alias arrancar

```bash
arrancar
```
