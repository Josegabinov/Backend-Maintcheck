import os
import dj_database_url
from .settings import *
from .settings import BASE_DIR

# Seguridad
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY')

# Host confiable
external_hostname = os.environ.get('RENDER_EXTERNAL_HOSTNAME')
if external_hostname:
    ALLOWED_HOSTS = ['backend-maintcheck-1.onrender.com', 'localhost', '127.0.0.1']
    CSRF_TRUSTED_ORIGINS = [f'https://{external_hostname}']
else:
    raise RuntimeError("RENDER_EXTERNAL_HOSTNAME is not set in environment variables")

# Middleware (incluye whitenoise)
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

# Archivos estáticos
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedStaticFilesStorage",
    },
}

# Base de datos
DATABASES = {
    'default': dj_database_url.config(
        default=os.environ.get('DATABASE_URL'),
        conn_max_age=600
    )
}
