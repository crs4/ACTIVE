"""
Django settings for job_processor project.

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
SECRET_KEY = '_f0*_i=fu9i4s6hsf2eu_731kdu1^m5d!)m5fm8d+2u110qtnm'

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
    'skeleton',
    'job_manager',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'job_processor.urls'

WSGI_APPLICATION = 'job_processor.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# parameters used for system logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format' : "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt' : "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'job_processor.log',
            'formatter': 'verbose'
        },
        'file2': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'face_recog.log',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        # low level system logging
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'INFO',
        },
        'job_processor': {
            'handlers': ['file'],
            'level': 'DEBUG',
        },
        'face_recog': {
            'handlers': ['file2'],
            'level': 'DEBUG',
        },
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


# Celery backend configuration
BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'amqp://'
CELERY_MESSAGE_COMPRESSION = 'gzip'
CELERY_ENABLE_UTC = True
CELERY_TIMEZONE = "Europe/Rome"
CELERYD_POOL_RESTARTS = True

# maximum number of parallel executable jobs
MAX_NUM_JOBS = 12

# python module containing plugins that will be stored and searched
PLUGIN_SCRIPT_MODULE = 'plugins_script'

# endpoint associated to the ACTIVE core instance
ACTIVE_CORE_ENDPOINT = 'http://156.148.132.79:80/'

# dictetory where all digital items are stored and shared among the cluster
MEDIA_ROOT = '/var/spool/active/data/'
