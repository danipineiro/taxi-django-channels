from .base import *

DEBUG = False

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

MAIL_PROVIDER_KEY = os.environ.get("MAIL_PROVIDER_KEY", "production_key")
SMS_PROVIDER_KEY = os.environ.get("SMS_PROVIDER_KEY", "production_key")
