# settings.py

"""
Django settings for bidding_conventions project.
"""

import os
from pathlib import Path

import structlog
from dotenv import load_dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
SECRET_KEY = os.getenv(
    "SECRET_KEY",
    "",
)

ALLOWED_HOSTS = ["127.0.0.1", "localhost"]


CSRF_TRUSTED_ORIGINS = [
    "https://www.python-plums.com",
]

CORS_ALLOWED_ORIGINS = [
    "https://www.python-plums.com",
    "http://localhost:8888",
]

# dev convenience
if DEBUG:
    DEV_PORTS = ["5173", "5174", "5175", "8888", "8000"]
    DEV_HOSTS = ["localhost", "127.0.0.1"]
    for port in DEV_PORTS:
        for host in DEV_HOSTS:
            host_str = f"http://{host}:{port}"
            CORS_ALLOWED_ORIGINS.append(host_str)
            CSRF_TRUSTED_ORIGINS.append(host_str)

CORS_ALLOW_CREDENTIALS = True  # Required for cookies to be sent/received

if DEBUG:
    CSRF_COOKIE_SAMESITE = "Lax"
    CSRF_COOKIE_SECURE = False
    SESSION_COOKIE_SECURE = False
else:
    CSRF_COOKIE_SAMESITE = "None"  # Not sure about this in production
    CSRF_COOKIE_SECURE = True  # True only in HTTPS


# Application definition

INSTALLED_APPS = [
    "bidding_conventions",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",  # Must be as high as possible
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [str(Path(BASE_DIR, "templates"))],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Internationalization

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/6.0/howto/static-files/

STATIC_URL = "static/"


LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "structlog_json": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.JSONRenderer(),
            "foreign_pre_chain": [
                structlog.processors.TimeStamper(fmt="iso", utc=True),
                structlog.stdlib.add_log_level,
                structlog.stdlib.add_logger_name,
            ],
        },
        "simple": {  # add this
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "file_json": {
            "class": "logging.handlers.RotatingFileHandler",
            "filename": f"{BASE_DIR}/logs/file.log",
            "maxBytes": 5_000_000,
            "backupCount": 10,
            "formatter": "structlog_json",
            "level": "INFO",
            # 'level': 'WARNING',   # or 'WARNING' if you want quieter
        },
        "console": {  # add this
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "ERROR",
        },
    },
    "loggers": {
        "": {
            "handlers": ["file_json"],
            # 'level': 'INFO',   # or 'WARNING' if you want quieter
            "level": "WARNING",  # or 'WARNING' if you want quieter
            "propagate": False,
        },
        "django": {
            "handlers": ["file_json", "console"],  # add 'console' here
            "level": "DEBUG",  # was WARNING
            "propagate": False,
        },
        "django.server": {
            "handlers": ["file_json"],
            "level": "INFO",
            "propagate": False,
        },
    },
}
