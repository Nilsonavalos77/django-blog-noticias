from pathlib import Path

# BASE_DIR apunta a la raíz de tu proyecto (carpeta que contiene manage.py)
BASE_DIR = Path(__file__).resolve().parent.parent

# Seguridad y debugging
SECRET_KEY = 'django-insecure-!=z3l=x3z39e0v7#d%z9h*$-#u@p95kbhk#qt5=ojy$x*d)9aj'
DEBUG = True
ALLOWED_HOSTS = ['julianamarighetti.pythonanywhere.com']

# Aplicaciones instaladas (tu app blog incluida)
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog',              # Tu app principal
    'widget_tweaks',     # Para personalizar formularios en templates
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Rutas y plantillas
ROOT_URLCONF = 'info.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Directorios globales para templates si los agregas
        'APP_DIRS': True,  # Busca templates en carpetas /templates de cada app
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',  # importante para request en templates
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'info.wsgi.application'

# Base de datos (SQLite por defecto)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Validadores de contraseña
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',},
]

# Internacionalización
LANGUAGE_CODE = 'es'
TIME_ZONE = 'America/Argentina/Buenos_Aires'
USE_I18N = True
USE_TZ = True

# Archivos estáticos (CSS, JS, imágenes)

# URL base para acceder a archivos estáticos (ej: http://tusitio.com/static/)
STATIC_URL = '/static/'

# Directorios donde Django buscará archivos estáticos durante desarrollo
STATICFILES_DIRS = [
    BASE_DIR / 'static',           # Carpeta global static en la raíz del proyecto (ej: info/static)
    BASE_DIR / 'blog' / 'static',  # Carpeta static dentro de la app blog (info/blog/static)
]

# Carpeta destino para archivos estáticos cuando ejecutes collectstatic (producción)
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Archivos multimedia subidos por usuarios
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'  # Carpeta donde se almacenan los archivos subidos

# URL para redirigir después del login
LOGIN_REDIRECT_URL = '/'

# Tipo por defecto de clave primaria
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
