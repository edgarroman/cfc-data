"""
Django settings for cfc project.

Generated by 'django-admin startproject' using Django 1.9.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'ulzdg%y02jjjug(*k5ctn4pud8iz$^78$bkjsxifq%*=b%pkz='

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize', # for easy template tag helpers
    'cfc.apps.core',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'cfc.urls'

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

WSGI_APPLICATION = 'cfc.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.9/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'work_local', 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'America/New_York'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# ======================================================
LEAGUE_CFC_PAGES = [
    { 'league' : 'ODSL', 'url' : 'http://elements.demosphere.com/91918/teams/club/17029528.html'},
    { 'league' : 'NCSL', 'url' : 'http://elements.demosphere.com/80738/teams/club/15599440.html'},
]

# EDP Teams are a PITA so we have to list them individually
LEAGUE_EDP_TEAMS = []
'''
    {
        'team' : 'CAPITAL FUTBOL STRIKERS RED',
#        'team' : 'CAPITALFC STRIKERS RED',
        'url': 'http://events.gotsport.com/events/schedule.aspx?eventid=57134&FieldID=0&applicationID=3843293&action=Go'
    },
    {
        'team' : 'CAPITALFC UNITED RED 02B',
        'url' : 'http://events.gotsport.com/events/schedule.aspx?eventid=57134&FieldID=0&applicationID=3826553&action=Go'
    },
    {
        'team' : 'CAPITALFC UNITED RED 01B',
        'url' : 'http://events.gotsport.com/events/schedule.aspx?eventid=57134&FieldID=0&applicationID=3826552&action=Go'
    },
    {
        'team' : 'CAPITALFC DC COSMOS',
        'url' : 'http://events.gotsport.com/events/schedule.aspx?eventid=57134&FieldID=0&applicationID=3826505&action=Go'
    },
    {
        'team' : 'CAPITAL FUTBOL DIPLOMATS',
        'url' : 'http://events.gotsport.com/events/schedule.aspx?eventid=57134&FieldID=0&applicationID=3826507&action=Go'
    },
]
'''

FIELD_ALIAS = {
    'Watkins ES' : 'Watkins',
    'Watkins Elementary School  DC #1' : 'Watkins',
    'Watkins Elementary School   DC #1' : 'Watkins',
    'Watkins Rec Center' : 'Watkins',

    'Ridge Road Rec Center': 'Ridge Road Rec Center',
    'Ridge Road Rec Center  DC Full sided field': 'Ridge Road Rec Center',
    'Ridge Road Rec Center  DC full-sided field': 'Ridge Road Rec Center', # Warning control char included
    'Ridge Rd Recreation DC #1' : 'Ridge Road Rec Center',

    'Randall Recreation Center Randall Full sided field': 'Randall Rec Center',
    'Randall Recreation Center #1 Full': 'Randall Rec Center',
    'Randall Recreation Center Soccer Field': 'Randall Rec Center',
    'Randall Rec Center': 'Randall Rec Center',
    'Randall Junior High School #1': 'Randall Rec Center',

    'Trinidad Recreation Center Full Sided': 'Trinidad Rec Center',
    'Trinidad Rec Center': 'Trinidad Rec Center',
    'Trinidad Rec. Center': 'Trinidad Rec Center',
    'Trinidad Rec Center #1' : 'Trinidad Rec Center',

    'Jefferson Middle School' : 'Jefferson Middle School',

    'Rosedale Rec Center' : 'Rosedale Rec Center',
    'Rosedale Rec Center, DC Small sided' : 'Rosedale Rec Center',
    'Rosedale Rec Center  DC Small sided field 1' : 'Rosedale Rec Center',
    'Rosedale Rec Center, DC full sided field' : 'Rosedale Rec Center',
    'Rosedale Recreation Center Field' : 'Rosedale Rec Center',
}

# =====================================================


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'work_local','static')

# Logging
# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.

# Log rotation settings
U_LOGFILE_SIZE = 1 * 1024 * 1024
U_LOGFILE_COUNT = 2

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
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console':{
            'level':'INFO',
            'class':'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': 'application.log',
            'maxBytes' : U_LOGFILE_SIZE,
            'backupCount' : U_LOGFILE_COUNT,
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers':['file','console'],
            'level':'INFO',
            'propagate': True,
        },
        ## Todo: this must be your app
        'cfc.apps': {
            'handlers': ['file','console'],
            'level': 'INFO',
        },
    }
}


# Must be the last item in this list to override environment settings
try:
    from cfc.settings_local import *
except:
    pass
