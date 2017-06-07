"""
Django settings for myproject project.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
DJ_PROJECT_DIR = os.path.dirname(__file__)
BASE_DIR = os.path.dirname(DJ_PROJECT_DIR)
WSGI_DIR = os.path.dirname(BASE_DIR)
REPO_DIR = os.path.dirname(WSGI_DIR)
DATA_DIR = os.environ.get('OPENSHIFT_DATA_DIR', BASE_DIR)

import sys
sys.path.append(os.path.join(REPO_DIR, 'libs'))
import secrets
SECRETS = secrets.getter(os.path.join(DATA_DIR, 'secrets.json'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = SECRETS['secret_key']

# SECURITY WARNING: don't run with debug turned on in production!
#if os.environ.get('DEBUG') is not None:
#    DEBUG = os.environ.get('DEBUG') == 'True'
#else:
#    DEBUG = True
if 'OPENSHIFT_REPO_DIR' in os.environ:
    DEBUG = False
else:
    DEBUG = True

from socket import gethostname
ALLOWED_HOSTS = [
    gethostname(), # For internal OpenShift load balancer security purposes.
    os.environ.get('OPENSHIFT_APP_DNS'), # Dynamically map to the OpenShift gear name.
    #'example.com', # First DNS alias (set up in the app)
    #'www.example.com', # Second DNS alias (set up in the app)
]

# Email
# SMTP

email_password = os.environ.get('EMAIL_PASSWORD','password')
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'smtp.zoho.com')
EMAIL_HOST_USER = os.environ.get('EMAIL_USERNAME',"admin@rpcodes.biz")
EMAIL_HOST_PASSWORD = email_password
EMAIL_PORT = os.environ.get('EMAIL_SMTP_PORT',587)
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL_DEFAULT_FROM_USER',EMAIL_HOST_USER)

# s3 Environment variables
s3_key_id = os.environ.get('ENV_S3_KEY_ID','rundeployscript')
s3_key_secret = os.environ.get('ENV_S3_KEY_SECRET','rundeployscript')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Dependencies
    'rest_framework',
    # tokens
    'rest_framework.authtoken',
    # custom users
    'users',
    # photos uploaded to s3
    'storages', # django-storages
    'photos'
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

# GETTING-STARTED: change 'myproject' to your project name:
ROOT_URLCONF = 'myproject.urls'

LOGIN_REDIRECT_URL = '/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [ os.path.join(BASE_DIR, 'templates')
         # , os.path.join(BASE_DIR, 'templates/registration/')  # this line makes django look in our custom templates before the admin ones
          ],
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

WSGI_APPLICATION = 'myproject.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            # GETTING-STARTED: change 'db.sqlite3' to your sqlite3 database:
            'NAME': os.path.join(DATA_DIR, 'db.sqlite3'),
        }
    }
else:
    postgres_user = os.environ.get('OPENSHIFT_POSTGRESQL_DB_USERNAME','admin')
    postgres_password = os.environ.get('OPENSHIFT_POSTGRESQL_DB_PASSWORD','password')
    postgres_host = os.environ.get('OPENSHIFT_POSTGRESQL_DB_HOST','localhost')
    postgres_port = os.environ.get('OPENSHIFT_POSTGRESQL_DB_PORT','5432')
    # By default, openshift console creates database
    # named after $OPENSHIFT_APP_NAME
    postgres_db_name = os.environ.get('OPENSHIFT_APP_NAME','data')

    DATABASES = {
        'default': {
            'HOST' : postgres_host
            , 'PORT' : postgres_port
            , 'ENGINE': 'django.db.backends.postgresql_psycopg2'
            , 'NAME': postgres_db_name
            , 'USER' : postgres_user
            , 'PASSWORD' : postgres_password
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
STATIC_URL = '/static/'
# in production, static files served from here
STATIC_ROOT = os.path.join(WSGI_DIR, 'static')
# In prod., collect files from here; in dev, access from here
STATICFILES_DIRS = ( os.path.join(BASE_DIR, 'static'), )

#
# LOGGING
# Allow display of 500 errors
# TODO: Verify appears on openshift host
#
LOGGING = {
    'version': 1,
    'handlers': {
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.request': {
            'handlers':['console'],
            'propagate': True,
            'level':'DEBUG',
        }
    },
}

REST_FRAMEWORK = {
   'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.IsAuthenticated',),
   'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
   'PAGE_SIZE': 100,
   'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),


    'DEFAULT_PARSER_CLASSES': (
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.FormParser',
        'rest_framework.parsers.MultiPartParser',
    ),
    'DEFAULT_FILTER_BACKENDS': ('rest_framework.filters.DjangoFilterBackend',),

}

# Amazon (photo) storage
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'




# Your Amazon Web Services access key, as a string.
AWS_ACCESS_KEY_ID=s3_key_id

# Your Amazon Web Services secret access key, as a string.
AWS_SECRET_ACCESS_KEY= s3_key_secret

# Your Amazon Web Services storage bucket name, as a string.
AWS_STORAGE_BUCKET_NAME="rpcdata" # arn:aws:s3::: ?

AWS_S3_CUSTOM_DOMAIN = '%s.s3.amazonaws.com' % AWS_STORAGE_BUCKET_NAME

# Relates to custom storage, in case we need other i.e. staticfiles later
MEDIAFILES_LOCATION = 'media'
MEDIA_URL = "https://%s/%s/" % (AWS_S3_CUSTOM_DOMAIN, MEDIAFILES_LOCATION)
DEFAULT_FILE_STORAGE = 'photos.custom_storages.MediaStorage'


# Disable browseables when not in debug
if (DEBUG):
   REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    )
else:
   REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
        'rest_framework.renderers.JSONRenderer',
   )
