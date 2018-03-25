"""
Django settings for cmdb project.
Overwright defautl settings for production
"""
from cmdb.settings import *
import os

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# To change with your host
ALLOWED_HOSTS = ["*"]


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'prd-db.sqlite3'),
    }
}

STATIC_ROOT = '/cmdb/static'
STATIC_URL = '/static/'
