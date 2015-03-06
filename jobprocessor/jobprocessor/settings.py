"""
Django settings for jobprocessor project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '9ifdm#fej!0t3zbu^1)l9pte&3xm_$75jci06*e61z=0#%5wyy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'jobmonitor',
    'jobmanager',
    'clustermanager',
    'skeleton',
    'xmp',
    'face_extraction',
    'pluginmanager',
#    'oauth2_provider',
#    'corsheaders',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
#    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'jobprocessor.urls'

WSGI_APPLICATION = 'jobprocessor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases


# TODO da cambiare in modo che faccia riferimento al db del server centrale
# in modo da gestire l'autenticazione degli utenti.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Cache manager
CACHES = {
	'default' : {
		'BACKEND' : 'django.core.cache.backends.filebased.FileBasedCache',
		'LOCATION' :  '/var/spool/active/data/cache',
	}
}
# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

# Template directory
TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/var/spool/active/jobprocessor/templates',
)


# Celery backend configuration
BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'amqp://'
CELERY_MESSAGE_COMPRESSION = 'gzip'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "Europe/Rome"
#CELERY_IGNORE_RESULT = True
CELERYD_POOL_RESTARTS = True

# Cors settings
CORS_ORIGIN_ALLOW_ALL = True
