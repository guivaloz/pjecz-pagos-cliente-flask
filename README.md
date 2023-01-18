# pjecz-pagos-cliente-flask

Cliente del Portal de Pagos hecho con Flask.

## Configuracion

Crear archivo `.env` con

    # API Citas V2 cliente
    API_BASE_URL="http://localhost:8000/v2"
    API_TIMEOUT=12

    # Flask
    FLASK_APP=pagos_cliente_flask.app
    FLASK_DEBUG=1

    # Salt sirve para cifrar el ID con HashID
    SALT=XXXXXXXXXXXXXXXXXXXXXXXX

    # Secret key sirve para CSRF
    SECRET_KEY=XXXXXXXXXXXXXXXXXXXXXXXX

    # reCAPTCHA configuration
    RECAPTCHA_PUBLIC_KEY = os.environ.get("RECAPTCHA_PUBLIC_KEY", "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")
    RECAPTCHA_PRIVATE_KEY = os.environ.get("RECAPTCHA_PRIVATE_KEY" "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx")

Crear archivo `.bashrc` que arranque el entorno virtual y cargue las variables

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
        echo "   SALT: ${SALT}"
        echo
    fi

    if [ -d venv ]
    then
        echo "-- Python Virtual Environment"
        source venv/bin/activate
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
        echo "   gcloud app deploy"
        echo
    fi
