import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR

# Obtener el hostname externo desde las variables de entorno, o usar uno por defecto
external_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME', 'backend-maintcheck-1.onrender.com')

# Configuración de hosts permitidos y CSRF
ALLOWED_HOSTS = [external_hostname]
CSRF_TRUSTED_ORIGINS = [f'https://{external_hostname}']

# Configuraciones de seguridad y entorno
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

# Middleware necesario para producción
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Almacenamiento de archivos estáticos
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Configuración de la base de datos para Render
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}
