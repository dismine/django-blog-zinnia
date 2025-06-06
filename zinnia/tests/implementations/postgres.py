"""Settings for testing zinnia on Postgres"""

from zinnia.tests.implementations.settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "zinnia",
        "USER": "postgres",
        "HOST": "localhost",
    }
}
