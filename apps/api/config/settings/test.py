from .base import *  # noqa

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'kommercehub_test',
        'USER': 'kommerce',
        'PASSWORD': 'kommerce',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

PASSWORD_HASHERS = ['django.contrib.auth.hashers.MD5PasswordHasher']
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'