# -*- coding: utf-8 -*-
"""
Django settings for ITCG.ua project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""
import os
import sys
import re

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_NAME = os.path.basename(BASE_DIR)

sys.path.append("/home/www/etc/python-lib/")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

if not re.search("/sites-itcg/", BASE_DIR):
    DEBUG = True
    TEMPLATE_DEBUG = True
else:
    DEBUG = False
    TEMPLATE_DEBUG = False

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'glutenfree_shop',                      # Or path to database file if using sqlite3.
        'USER': 'www',                      # Not used with sqlite3.
        'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '127.0.0.1',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.4/ref/settings/#allowed-hosts
ALLOWED_HOSTS = ["*",]

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Europe/Kiev'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'ru'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

MEDIA_ROOT = os.path.join(BASE_DIR, PROJECT_NAME, 'media')
MEDIA_URL = '/media/'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = os.path.join(BASE_DIR, '../static_content/', 'static')

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/
STATIC_URL = '/static/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'i$@t0kc)rug^#$a&amp;nx=71eg=c0h5+^s_=nhg1_6_ytrrobi)an'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

SITE_ID = 1
ROOT_URLCONF = '%s.urls' % PROJECT_NAME

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = '%s.wsgi.application' % PROJECT_NAME

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'apps'),
    os.path.join(BASE_DIR, PROJECT_NAME, 'templates'),
)

INSTALLED_APPS = (
    # External apps that need to go before django's
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    # 'apps.itcg_admin',

    # Django modules
    'django.contrib.sites',
    'django.contrib.flatpages',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'import_export',
    'daterange_filter',

    # External apps
    'bootstrap3',
    'gunicorn',
    'south',
    'sorl.thumbnail',
    'social_auth',

    # Local apps
    'apps.product',
    'apps.cart',
    'apps.userprofile',
    'apps.general'
)

# SOCIAL_AUTH
FACEBOOK_APP_ID = '797990966926683'
FACEBOOK_API_SECRET = '70e20d170258df36114c052b291f6734'
FACEBOOK_EXTENDED_PERMISSIONS = ['email']

AUTHENTICATION_BACKENDS = (
    'social_auth.backends.facebook.FacebookBackend',
    'django.contrib.auth.backends.ModelBackend',
)

# Разрешаем создавать пользователей через social_auth
SOCIAL_AUTH_CREATE_USERS = True
# Перечислим pipeline, которые последовательно буду обрабатывать респонс
SOCIAL_AUTH_PIPELINE = (
    # Получает по backend и uid инстансы social_user и user
    'social_auth.backends.pipeline.social.social_auth_user',
    # Получает по user.email инстанс пользователя и заменяет собой тот, который получили выше.
    # Кстати, email выдает только Facebook и GitHub, а Vkontakte и Twitter не выдают
    'social_auth.backends.pipeline.associate.associate_by_email',
    # Пытается собрать правильный username, на основе уже имеющихся данных
    'social_auth.backends.pipeline.user.get_username',
    # Создает нового пользователя, если такого еще нет
    'social_auth.backends.pipeline.user.create_user',
    # Пытается связать аккаунты
    'social_auth.backends.pipeline.social.associate_user',
    # Получает и обновляет social_user.extra_data
    'social_auth.backends.pipeline.social.load_extra_data',
    # Обновляет инстанс user дополнительными данными с бекенда
    'social_auth.backends.pipeline.user.update_user_details'
)

SOCIAL_AUTH_PROVIDERS = [
    {'id': p[0], 'name': p[1], 'position': {'width': p[2][0], 'height': p[2][1], }}
    for p in (
        ('facebook', u'Login via Facebook', (0, -210)),
    )
]


SESSION_SERIALIZER='django.contrib.sessions.serializers.PickleSerializer'

# LOGIN_URL          = '/login-form/'
LOGIN_REDIRECT_URL = '/'
# LOGIN_ERROR_URL    = '/login-error/'

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    PROJECT_NAME+'.context_processors.cart',
    PROJECT_NAME+'.context_processors.top_menu',
    PROJECT_NAME+'.context_processors.left_recipes',
)

def get_static_dir(apps):
    l = [os.path.join(BASE_DIR, PROJECT_NAME, 'static')]
    for app in apps:
        try:
            app_static_path = os.path.join(BASE_DIR, 'apps', app.split('apps.')[1], 'static')
            if os.path.isdir(app_static_path):
                l.append(app_static_path)
        except:
            pass
    return tuple(l)

# Additional locations of static files
STATICFILES_DIRS = get_static_dir(INSTALLED_APPS)


# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'default': {
        'level':'DEBUG',
        'class':'logging.handlers.RotatingFileHandler',
        'filename': os.path.join(BASE_DIR, '../logs/django.log'),
        'maxBytes': 1024*1024*5, # 5 MB
        'backupCount': 5,
        'formatter':'simple',
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': os.path.join(BASE_DIR, '../logs/django.log'),
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'django': {
            'handlers': ['logfile'],
            'level': 'ERROR',
            'propagate': False,
        },
       'samsungtabs': {
            'handlers': ['logfile'],
            'level': 'WARNING', # Or maybe INFO or DEBUG
            'propagate': False
       },
    }
}

# import logging
#
# logging.basicConfig(
#     level=logging.DEBUG,
#     format='%(asctime)s %(levelname)s %(message)s',
#     filename= os.path.join(BASE_DIR, '../logs/django.log'),
#     filemode='w'
# )

# insert for printing log in views, context_processors etc...
# import logging
# logging.debug('logging menu')

try:
    from local_settings import *
except ImportError:
    pass
