"""
Django              3.2.8
djangorestframework 3.12.4

Django settings for GradesApp project.

Generated by 'django-admin startproject' using Django 3.2.8.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import sys
from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get(
    'SECRET_KEY', 'django-insecure-ma)s(1%2si759f*@a_09+oi2)k$7na_hr6zxpg&8ii017mg@t%')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = str(os.environ.get('DEBUG')) == '1'

ALLOWED_HOSTS = []
if not DEBUG:
    ALLOWED_HOSTS += os.environ.get('ALLOWED_HOSTS').split(" ")


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    'django_filters',
    'accounts',
    'grades',
]

AUTH_USER_MODEL = 'accounts.User'

AUTHENTICATION_BACKENDS = ['accounts.jwt.CustomBackend']

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema'}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'GradesApp.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'GradesApp.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'cloud': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('DB_CLOUD_NAME'),
        'USER': os.environ.get('DB_CLOUD_USER'),
        'PASSWORD': os.environ.get('DB_CLOUD_PASSWORD'),
        'HOST': os.environ.get('DB_CLOUD_HOST'),
        'PORT': os.environ.get('DB_CLOUD_PORT'),
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server", },
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'gradesappdbtest.sqlite'
    },
    'local': {
        'ENGINE': 'mssql',
        'NAME': os.environ.get('DB_LOCAL_NAME'),
        'USER': os.environ.get('DB_LOCAL_USER'),
        'PASSWORD': os.environ.get('DB_LOCAL_PASSWORD'),
        'HOST': os.environ.get('DB_LOCAL_HOST'),
        'PORT': os.environ.get('DB_LOCAL_PORT'),
        "OPTIONS": {"driver": "ODBC Driver 17 for SQL Server", }
    },
}


if 'test' in sys.argv:
    DATABASES['default'] = DATABASES['test']
elif not DEBUG:
    DATABASES['default'] = DATABASES['cloud']
else:
    DATABASES['default'] = DATABASES['local']

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Settings
# https://docs.djangoproject.com/en/4.0/topics/email/

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = os.environ.get('PAULSOFT_EMAIL_USER')
DEFAULT_FROM_EMAIL = os.environ.get('PAULSOFT_EMAIL_USER')
EMAIL_HOST_PASSWORD = os.environ.get('PAULSOFT_EMAIL_PASSWORD')
EMAIL_VERIFICATION_URL = os.environ.get('EMAIL_VERIFICATION_URL')

# Django Rest Framework settings
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'accounts.jwt.JWTAuthentication',
    ],
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
}

# Django Swagger (drf-yasg) settings
# https://drf-yasg.readthedocs.io/en/stable/settings.html

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Auth Token | example: Bearer (Token) |': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
    'USE_SESSION_AUTH': False,
    'JSON_EDITOR': True,
}

# Django CORS settings
# https://github.com/adamchainz/django-cors-headers

CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS').split(" ")
