"""
Django settings for test_site project.

Generated by 'django-admin startproject' using Django 1.8.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

from django.conf.global_settings import *

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^^bm-^5r^06@k8*k&!7e9m^b74=$n4b!p#-^2$w-!t52z0!aan'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTHENTICATION_BACKENDS = (
    'webtzite.backends.CustomModelBackend',
    #'webtzite.backends.CustomBrowserIDBackend',
    'nopassword.backends.email.EmailBackend'
)

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    #'django_browserid',
    'nopassword',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'require',
    'webtzite',
    'mpcontribs.portal',
    'mpcontribs.rest',
    'mpcontribs.explorer',
    'test_site.apps.UWSI2ExplorerConfig',
    'test_site.apps.MnO2PhaseSelectionExplorerConfig',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'webtzite.middleware.APIKeyMiddleware',
)

ROOT_URLCONF = 'test_site.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'test_site.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASE_ENGINE = 'django.db.backends.sqlite3',
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

JPY_USER = os.environ.get('JPY_USER')
PROXY_URL_PREFIX = '/flaskproxy/{}'.format(JPY_USER) if JPY_USER else ''
ROOT_PROJECT_DIR = os.path.dirname(os.path.dirname(__file__))
STATIC_ROOT = ROOT_PROJECT_DIR + '/webtzite/static'
STATIC_URL = PROXY_URL_PREFIX + '/static/'

STATIC_ROOT_URLS = {
    STATIC_URL: STATIC_ROOT,
    STATIC_URL[:-1] + '_rest': ROOT_PROJECT_DIR + '/mpcontribs/rest/static'
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/mpappkit.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'webtzite': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'localhost'
EMAIL_PORT = 25
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
DEFAULT_FROM_EMAIL = 'Test Site <test_site@matgen8.lbl.gov>'

REQUIRE_JS = 'components/requirejs/require.js'
REQUIRE_DEBUG = True

if os.environ.get('DEPLOYMENT') == 'MATGEN':
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
