"""
Django settings for active_system project.

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
SECRET_KEY = 'q!fl232-rzbql)pife1#ys%8b-91s7=qgtdu6svy*=!)+j=6nn'

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
    'rest_framework',
    'oauth2_provider',
    'corsheaders',
    'core',
    'core.plugins.apps.PluginConfig', # collect plugin data
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
)

ROOT_URLCONF = 'active_system.urls'

WSGI_APPLICATION = 'active_system.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
	'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#        'ENGINE': 'django.db.backends.mysql',
#        'NAME': 'active',
#	'USER': 'active',
#	'PASSWORD': 'evitca',
#	'HOST': '156.148.132.223',
#	'PORT': '3306'
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
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/te$
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    '/var/spool/active/active_system/templates',
)

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_METHODS = (
	'GET',
	'POST',
	'PUT',
	'PATCH',
	'DELETE',
	'OPTIONS'
)

CORS_ALLOW_HEADERS = (
	'x-requested-with',
	'content-type',
	'accept',
	'origin',
	'authorization',
	'x-csrftoken',
	'cache-control'
)

# directory where uploaded files will be saved
MEDIA_ROOT = '/var/spool/active/data/items'

# directory where must be saved all plugin manifest files
PLUGIN_MANIFEST_PATH = '/var/spool/active/active_system/plugin_manifest'

# endpoint where will be executed a job processor
JOB_PROCESSOR_ENDPOINT = "http://156.148.132.79:9000/"

# current version of the ACTIVE core
ACTIVE_VERSION = '0.1.1'
