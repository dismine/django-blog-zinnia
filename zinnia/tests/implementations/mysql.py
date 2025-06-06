"""Settings for testing zinnia on MySQL"""

from zinnia.tests.implementations.settings import *  # noqa

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "zinnia",
        "USER": "root",
        "PASSWORD": "mysql",
        "HOST": "mysql",
        "TEST": {
            "CHARSET": "utf8",
            "COLLATION": "utf8_general_ci",
        },
    }
}
