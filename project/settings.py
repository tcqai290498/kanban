import os
import sys
from pathlib import Path
from urllib.parse import urlparse, ParseResult
import django
from django.utils.translation import gettext_lazy as _
from dotenv import find_dotenv, load_dotenv
from jutil.parse import parse_bool


# Load .env

dotenv_path = find_dotenv(os.path.dirname(os.path.abspath(__file__)) + "/.env")
if not dotenv_path:
    raise Exception(".env missing")
load_dotenv(dotenv_path)


# Core settings

BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ["SECRET_KEY"]
DEBUG = parse_bool(os.environ["DEBUG"])
ALLOWED_HOSTS = os.environ["ALLOWED_HOSTS"].split(",")
MEDIA_ROOT = Path(os.getenv("MEDIA_ROOT") or BASE_DIR).resolve()
LOGS_DIR = MEDIA_ROOT / "logs"


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django_extensions",
    "rest_framework.authtoken",
    "process",
    "login",
    "logout",
    "task",
    "corsheaders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]

ROOT_URLCONF = "project.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            os.path.join(BASE_DIR, "project/templates"),
            os.path.dirname(django.__file__),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "project.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DB_URL = urlparse(os.environ["DB_URL"])
assert isinstance(DB_URL, ParseResult)

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": DB_URL.path[1:],
        "USER": DB_URL.username,
        "PASSWORD": DB_URL.password,
        "HOST": DB_URL.hostname,
        "PORT": 5432,
        "CONN_MAX_AGE": 180,
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

COUNTRY_CODE = "FI"

LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("fi", _("Finnish")),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)


# Email

EMAIL_SENDGRID_API_KEY = os.getenv("EMAIL_SENDGRID_API_KEY") or ""
EMAIL_HOST = "smtp.sendgrid.net"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "apikey"
EMAIL_HOST_PASSWORD = EMAIL_SENDGRID_API_KEY
EMAIL_SENDING_ENABLED = parse_bool(os.getenv("EMAIL_SENDING_ENABLED") or "False")

DEFAULT_FROM_EMAIL = "no-reply@example.com"
SERVER_EMAIL = "no-reply@example.com"


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "static"
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]


# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# Logging

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "filters": {
        "ndebug": {
            "()": "django.utils.log.RequireDebugFalse",
        },
    },
    "formatters": {
        "verbose": {"format": "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s", "datefmt": "%Y-%m-%d %H:%M:%S"},
        "simple": {"format": "%(levelname)s %(message)s"},
    },
    "handlers": {
        "file": {"level": "DEBUG", "class": "logging.FileHandler", "filename": os.path.join(LOGS_DIR, "django.log"), "formatter": "verbose"},
        "console": {
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "django": {
            "handlers": ["file", "console"],
            "level": "WARNING",
        },
    },
}


# Security options

if not DEBUG:
    X_FRAME_OPTIONS = "DENY"
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SECURE = True
    LANGUAGE_COOKIE_HTTPONLY = True
    LANGUAGE_COOKIE_SECURE = True
    LANGUAGE_COOKIE_SAMESITE = "Lax"


AUTHENTICATION_BACKENDS = [
    "project.authentication.EmailBackend",
    "django.contrib.auth.backends.ModelBackend",
]

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": ("rest_framework.permissions.IsAdminUser",),
    "PAGE_SIZE": 10,
}

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
CORS_ALLOW_ALL_METHODS = True
CORS_ALLOW_ALL_ORIGINS = True
