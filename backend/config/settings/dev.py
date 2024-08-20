from datetime import timedelta

from .base import *

MIDDLEWARE += [
    "common.middleware.QueryCountMiddleware",
]

AUTH_PASSWORD_VALIDATORS = []

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=3600),
}

MAIL_PROVIDER_KEY = os.environ.get("MAIL_PROVIDER_KEY", None)
SMS_PROVIDER_KEY = os.environ.get("SMS_PROVIDER_KEY", None)
