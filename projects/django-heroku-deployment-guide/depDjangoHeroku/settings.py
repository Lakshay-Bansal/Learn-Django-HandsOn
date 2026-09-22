"""
Django settings for depDjangoHeroku project.

This settings file is specifically configured for deployment on the Heroku platform.
Key deployment aspects covered:
1. Environment variables via python-decouple (SECRET_KEY, DEBUG, ALLOWED_HOSTS)
2. Database configuration via dj-database-url (SQLite locally, Heroku Postgres in production)
3. Static files handling via WhiteNoise and STATIC_ROOT
4. Heroku integration via django_heroku (or standalone WhiteNoise/dj-database-url)
"""

from pathlib import Path
import os
from decouple import config
import dj_database_url
import django_heroku

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ── Security & Environment Variables ─────────────────────────────────────────
# Read from .env file locally, or from Heroku Config Vars in production.
# On Heroku, set these with: heroku config:set SECRET_KEY=... DEBUG=False ALLOWED_HOST=...

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default = '') 

# SECURITY WARNING: don't run with debug turned on in production!
# Defaults to True for local development, set to False in Heroku Config Vars
DEBUG = config('DEBUG', cast=bool, default=True)

# Comma-separated list of host/domain names that this Django site can serve.
# Example on Heroku: your-app-name.herokuapp.com
ALLOWED_HOSTS = [
    host.strip()
    for host in config('ALLOWED_HOST', default='localhost,127.0.0.1').split(',')
    if host.strip()
]


# ── Application Definition ───────────────────────────────────────────────────

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    # WhiteNoise Middleware: Must be placed directly after SecurityMiddleware.
    # Serves static files directly from Gunicorn on Heroku without needing Nginx.
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'depDjangoHeroku.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'depDjangoHeroku.wsgi.application'


# ── Database Configuration ───────────────────────────────────────────────────
# Heroku uses PostgreSQL. When you attach 'heroku-postgresql', Heroku automatically
# injects the DATABASE_URL environment variable into your application dyno.
#
# Logic below:
# - If running locally with DEBUG=True and no DATABASE_URL: use SQLite.
# - If DATABASE_URL is set (production on Heroku): parse it with dj_database_url.

database_url = config('DATABASE_URL', default='')

if DEBUG and not database_url:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': dj_database_url.config(
            default=database_url,
            conn_max_age=600,
            ssl_require=True
        )
    }


# ── Password Validation ───────────────────────────────────────────────────────

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


# ── Internationalization ─────────────────────────────────────────────────────

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# ── Static Files (CSS, JavaScript, Images) ───────────────────────────────────
# On Heroku, `python manage.py collectstatic` runs automatically during deployment.
# All static files are collected into `STATIC_ROOT`.
# WhiteNoise then serves them with compression and long-term cache headers.

STATIC_URL = '/static/'

# Absolute filesystem path where `collectstatic` gathers static files for deployment
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Additional directories where Django looks for static assets during development
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
] if os.path.exists(os.path.join(BASE_DIR, 'static')) else []

# WhiteNoise storage: compresses files and gives unique cache-busting hashes
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# ── Media Files (User-uploaded files) ─────────────────────────────────────────
# Note: Heroku dynos have an EPHEMERAL filesystem! Any uploaded file saved locally
# will be deleted whenever a dyno restarts or redeploys.
# For persistent media files on Heroku, use AWS S3, Cloudinary, or Google Cloud Storage.
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')


# ── Default Primary Key Field Type ───────────────────────────────────────────

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ── Heroku Automatic Configuration ───────────────────────────────────────────
# django_heroku automatically configures:
# - Database (from DATABASE_URL)
# - Logging to stdout
# - Allowed hosts
# - Staticfiles settings
# Note: django_heroku is invoked at the very end using locals().
try:
    django_heroku.settings(locals())
except Exception:
    pass