import environ
from .base import *

ALLOWED_HOSTS = ['223.130.134.111']




DEBUG = True



env = environ.Env()
environ.Env.read_env(BASE_DIR/'.env')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('PASSWORD'),
        'HOST': env('DB_PASSWORD'), 
        'PORT': '5432',
    }
}