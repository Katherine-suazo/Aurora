from pathlib import Path
import os
import environ

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Inicializar environ
env = environ.Env(
    DEBUG=(bool, False)
)
# Leer el archivo .env
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Reemplaza tus variables existentes por la lectura del .env:
SECRET_KEY = env('AWS_SECRET_ACCESS_KEY')
DEBUG = env('DEBUG')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure--+18!(q09o0u9-p!$3xcll&y^7z0lu+qca2%asi7*ob#9zev1m'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'appWeb',
    'storages',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',      
    'django.contrib.sessions.middleware.SessionMiddleware',            
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'api.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'api.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = 'static/'


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# SERVIDORES QUE SE PUEDEN CONECTAR A DJANGO
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173", # react
]


# CONECTARSE A S3
STORAGES = {
    "default": {
        "BACKEND": "storages.backends.s3boto3.S3Boto3Storage",  # para guardar los archivos de usuario
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage", # para guardar los archivos estaticos
    },
}

# --- CONFIGURACIÓN DE STORAGE CON AWS S3 ---
# en .env se encuentran las credenciales para acceder a aws s3

# Leer credenciales desde el archivo .env
AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = env('AWS_S3_REGION_NAME')

# Requerido obligatoriamente para cuentas institucionales/AWS Academy
AWS_SESSION_TOKEN = env('AWS_SESSION_TOKEN')

# Seguridad y comportamiento de archivos
AWS_S3_FILE_OVERWRITE = False  # Si se sube un archivo con el mismo nombre, Django le añade un sufijo aleatorio
AWS_DEFAULT_ACL = None         # Mantiene la privacidad heredada del bucket

# Definir S3 como el almacenamiento por defecto para archivos multimedia (Media)
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'

# URL para acceder a los archivos multimedia (Django la generará automáticamente firmada)
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'
