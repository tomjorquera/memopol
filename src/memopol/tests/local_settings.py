"""
Memopol local settings example.
Edit and rename to local_settings.py to use.
"""

import os
from socket import gethostname


DATA_DIR = 'data'
LOG_DIR = 'log'
PUBLIC_DIR = 'wsgi/static'


DATABASES = {
    'default': {
        'NAME': 'test',
        'USER': 'memopol_test',
        'PASSWORD': 'memopol_test',
        'HOST': 'localhost',
        'PORT': '5432',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
    }
}


ALLOWED_HOSTS = [
    gethostname(),
]


SITE_ID = 1
SITE_NAME = 'Memopol'
SITE_DOMAIN = gethostname()

ORGANIZATION_NAME = 'Memopol'
