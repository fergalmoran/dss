# Django settings for dss project.
from datetime import timedelta
from django.core.urlresolvers import reverse_lazy
import djcelery
import os
from dss import localsettings
from utils import here
from django.conf import global_settings

DEBUG = localsettings.DEBUG
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Fergal Moran', 'fergal.moran@gmail.com'),
)

MANAGERS = ADMINS
AUTH_PROFILE_MODULE = 'spa.UserProfile'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'deepsouthsounds',
        'USER': 'deepsouthsounds',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
        }
}
ROOT_URLCONF = 'dss.urls'
TIME_ZONE = 'Europe/Dublin'
LANGUAGE_CODE = 'en-ie'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
USE_TZ = False

SITE_ROOT = here('')
MEDIA_ROOT = here('media')
MEDIA_URL = '/media/'

STATIC_ROOT = localsettings.STATIC_ROOT or ''
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

STATICFILES_DIRS = (
    here('static'),
    )
STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    )

SECRET_KEY = '8*&amp;j)j4lnq*ft*=jhajvc7&amp;upaifb2f2s5(v6i($$+3p(4^bvd'

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
    #'django.template.loaders.app_directories.load_template_source',
    )
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
    'django.contrib.auth.context_processors.auth',
    "allauth.socialaccount.context_processors.socialaccount",
    "allauth.account.context_processors.account"
    )
AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + (
    "allauth.account.auth_backends.AuthenticationBackend",
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware'
)

WSGI_APPLICATION = 'dss.wsgi.application'
TEMPLATE_DIRS = (here('templates'),)
INSTALLED_APPS = (
    'grappelli',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'djcelery',
    'pipeline',
    'avatar',
    'notification',
    'spa',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.github',
    'allauth.socialaccount.providers.linkedin',
    'allauth.socialaccount.providers.openid',
    'allauth.socialaccount.providers.twitter',
    'emailconfirmation',
    'backbone_tastypie',
    )

# where to redirect users to after logging in
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_URL = reverse_lazy('home')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
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
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
            },
        }
}

BROKER_HOST = "127.0.0.1"
BROKER_PORT = 5672
BROKER_VHOST = "/"
BROKER_USER = "guest"
BROKER_PASSWORD = "guest"
CELERYBEAT_SCHEDULE = {
    "runs-every-30-seconds": {
        "task": "dss.generate_missing_waveforms_task",
        "schedule": timedelta(seconds=30),
        },
    }
djcelery.setup_loader()

SOCIALACCOUNT_AVATAR_SUPPORT  = True
AVATAR_STORAGE_DIR = MEDIA_ROOT + 'avatars/'

DSS_TEMP_PATH = localsettings.DSS_TEMP_PATH
DSS_LAME_PATH = localsettings.DSS_LAME_PATH
DSS_WAVE_PATH = localsettings.DSS_WAVE_PATH
PIPELINE_YUI_BINARY = localsettings.PIPELINE_YUI_BINARY
PIPELINE = True
PIPELINE_CSS = {
    'defaults': {
        'source_filenames': (
            'static/css/*.css',
            ),
        'output_filename': 'css/dss.css',
        'extra_context': {
            'media': 'screen,projection',
            },
        },
    }
