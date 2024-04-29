"""
Django settings for manual project.

Generated by 'django-admin startproject' using Django 4.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os

import dj_database_url

db_from_env = dj_database_url.config()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-gt%#%(&0s$fg-3#=s-)s2rqu4mi#=(e*5f2zq07lu&cr04n_5+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
#DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'manual-marketing.onrender.com',]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'guide',
    'django_cleanup',
    'widget_tweaks',
    'crispy_forms',
    'crispy_bootstrap4',
    'rest_framework',
    'cloudinary_storage',
    'cloudinary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware'
]

ROOT_URLCONF = 'manual.urls'

TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
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

WSGI_APPLICATION = 'manual.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    #'default': {
    #    'ENGINE': 'django.db.backends.sqlite3',
    #    'NAME': BASE_DIR / 'db.sqlite3',
    #}

    #'default': {
    #    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #    'NAME': 'manual',
    #    'USER' : 'customer',
    #    'PASSWORD' : 'customer',
    #    'HOST' : '127.0.0.1',
    #    'PORT' : '5432',
    #}

    'default': {
	    'ENGINE': 'django.db.backends.postgresql_psycopg2',
	    'NAME': 'manual_h1l5',
	    'USER' : 'manual_admin',
	    'PASSWORD' : 'a5mw2AnOsZuaoBxckNcxkxWrTLrDfzro',
	    'HOST' : 'dpg-cons0nocmk4c73ac9sug-a.frankfurt-postgres.render.com',
	    'PORT' : '5432',
    }

}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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


# ���������� Bootstrap 4 � �������� ��������� ������ �� ��������� ��� django-crispy-forms:
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-Ru'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True 

LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

LANGUAGES = (
    ('kk', 'Kazakh'),
    ('ru', 'Russian'),    
)


#STATICFILES_DIRS = [
#    os.path.join(BASE_DIR, "static"),
#]

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
#STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ��� ������ � ������������
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')
MEDIA_URL = '/media/'

# ���������� �����������
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'do8p2p1ph',
    'API_KEY': '291791316125479',
    'API_SECRET': 'OGNQjuoJlCBaygeddDCOkVvPdI8',
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ����� ������ �� E-Mail
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.mail.ru'
EMAIL_HOST_USER = 'manua140322@mail.ru' 
EMAIL_HOST_PASSWORD = 'BXesJKuTrDz60V9RXcBh'
DEFAULT_FROM_EMAIL  = 'manua140322@mail.ru'
EMAIL_PORT = 25
EMAIL_USE_TLS = True

# Redirect to home URL after login (Default redirects to /accounts/profile/)
# ������, ��� ����� � �������, �� �� ��������� ������ ���������������� �� �������� �������� ����� � �� �� /accounts/profile/
LOGIN_REDIRECT_URL = '/'
LOGIN_URL = '/login/'
LOGOUT_URL = '/logout/'