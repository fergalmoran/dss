#e Django settings for dss project.
from datetime import timedelta
import os

from django.core.urlresolvers import reverse_lazy
import djcelery
from django.conf import global_settings
import sys

from dss import localsettings
from dss import logsettings
from utils import here


DEBUG = localsettings.DEBUG
DEVELOPMENT = localsettings.DEBUG

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Fergal Moran', 'fergal.moran@gmail.com'),
)

MANAGERS = ADMINS
AUTH_PROFILE_MODULE = 'spa.UserProfile'

ALLOWED_HOSTS = ['*']  #localsettings.ALLOWED_HOSTS if hasattr(localsettings, 'ALLOWED_HOSTS') else []
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'deepsouthsounds',
        'ADMINUSER': 'postgres',
        'USER': localsettings.DATABASE_USER if hasattr(localsettings, 'DATABASE_USER') else 'deepsouthsounds',
        'PASSWORD': localsettings.DATABASE_PASSWORD if hasattr(localsettings, 'DATABASE_PASSWORD') else '',
        'HOST': localsettings.DATABASE_HOST if hasattr(localsettings, 'DATABASE_HOST') else 'localhost',
    }
}

ROOT_URLCONF = 'dss.urls'
TIME_ZONE = 'Europe/Dublin'
LANGUAGE_CODE = 'en-ie'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
USE_TZ = True

SITE_ROOT = here('')
MEDIA_ROOT = localsettings.MEDIA_ROOT
STATIC_ROOT = localsettings.STATIC_ROOT
CACHE_ROOT = localsettings.CACHE_ROOT

STATIC_URL = localsettings.STATIC_URL if hasattr(localsettings, 'STATIC_URL') else '/static/'

if DEBUG:
    MEDIA_URL = '/media/'
else:
    MEDIA_URL = localsettings.MEDIA_URL if hasattr(localsettings, 'MEDIA_URL') else '/static/'

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

TINYMCE_JS_URL = os.path.join(STATIC_ROOT, "js/libs/tiny_mce/tiny_mce.js")
TINYMCE_DEFAULT_CONFIG = {
    'cleanup_on_startup': True,
    'custom_undo_redo_levels': 10,
    #'mode': "textareas",
    'theme': "advanced",
    'theme_advanced_toolbar_location': "top",
    'theme_advanced_toolbar_align': "left",
    'theme_advanced_buttons1': "fullscreen,separator,preview,separator,bold,italic,underline,strikethrough,separator,bullist,numlist,outdent,indent,separator,undo,redo,separator,link,unlink,anchor,separator,image,cleanup,help,separator,code"
    ,
    'theme_advanced_buttons2': "",
    'theme_advanced_buttons3': "",
    'auto_cleanup_word': True,
    'plugins': "table,save,advhr,advimage,advlink,emotions,iespell,insertdatetime,print,contextmenu,fullscreen,preview,searchreplace"
    ,
    'plugin_insertdate_dateFormat': "%m/%d/%Y",
    'plugin_insertdate_timeFormat': "%H:%M:%S",
    'extended_valid_elements': "a[name|href|target=_blank|title|onclick],img[class|src|border=0|alt|title|hspace|vspace|width|height|align|onmouseover|onmouseout|name],hr[class|width|size|noshade],font[face|size|color|style],span[class|align|style]"
    ,
    'fullscreen_settings': {
        'theme_advanced_path_location': "top",
        'theme_advanced_buttons1': "fullscreen,separator,preview,separator,cut,copy,paste,separator,undo,redo,separator,search,replace,separator,code,separator,cleanup,separator,bold,italic,underline,strikethrough,separator,forecolor,backcolor,separator,justifyleft,justifycenter,justifyright,justifyfull,separator,help"
        ,
        'theme_advanced_buttons2': "removeformat,styleselect,formatselect,fontselect,fontsizeselect,separator,bullist,numlist,outdent,indent,separator,link,unlink,anchor"
        ,
        'theme_advanced_buttons3': "sub,sup,separator,image,insertdate,inserttime,separator,tablecontrols,separator,hr,advhr,visualaid,separator,charmap,emotions,iespell,flash,separator,print"
    }
}
TINYMCE_SPELLCHECKER = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)
STATICFILES_STORAGE = 'require.storage.OptimizedStaticFilesStorage'
STATICFILES_DIRS = (
    here('static'),
)

SECRET_KEY = localsettings.SECRET_KEY

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
    #'django.template.loaders.app_directories.load_template_source',
)
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django_facebook.context_processors.facebook',
    'django.core.context_processors.request',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.contrib.auth.context_processors.auth',
    "allauth.socialaccount.context_processors.socialaccount",
    "allauth.account.context_processors.account",
    "spa.context_processors.debug"
)

AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + (
    "allauth.account.auth_backends.AuthenticationBackend",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'spa.middleware.cors.XsSharingMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    #'spa.middleware.uploadify.SWFUploadMiddleware',
    #'spa.middleware.sqlprinter.SqlPrintingMiddleware' if DEBUG else None,
    #'debug_toolbar.middleware.DebugToolbarMiddleware',
)

WSGI_APPLICATION = 'dss.wsgi.application'
TEMPLATE_DIRS = (here('templates'),)
INSTALLED_APPS = (
    'grappelli',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django_facebook',
    'django_extensions',
    'django_gravatar',
    'compressor',
    'notification',
    'djcelery',
    'sorl.thumbnail',
    'south',
    'avatar',
    'spa',
    'spa.signals',
    'core',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.google',
    'debug_toolbar',
    'django_jenkins',
    'dbbackup',
    'jfu',
    #'backbone_tastypie',
)

# where to redirect users to after logging in
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_URL = reverse_lazy('home')

LOGGING = logsettings.LOGGING

FACEBOOK_APP_ID = '154504534677009'
FACEBOOK_APP_SECRET = localsettings.FACEBOOK_APP_SECRET

from celery_settings import *
djcelery.setup_loader()

SOCIALACCOUNT_AVATAR_SUPPORT = True
SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'SCOPE': ['email', 'publish_stream', 'publish_actions'],
        'METHOD': 'oauth2',
        'LOCALE_FUNC': lambda request: 'en_IE'
    },
    'google': {
        'SCOPE': ['https://www.googleapis.com/auth/userinfo.profile'],
        'AUTH_PARAMS': {'access_type': 'online'}
    }
}
AVATAR_STORAGE_DIR = MEDIA_ROOT + '/avatars/'
ACCOUNT_LOGOUT_REDIRECT_URL = '/'
LOGIN_REDIRECT_URL = '/'

DSS_TEMP_PATH = localsettings.DSS_TEMP_PATH
DSS_LAME_PATH = localsettings.DSS_LAME_PATH
DSS_WAVE_PATH = localsettings.DSS_WAVE_PATH

PIPELINE_YUI_BINARY = localsettings.PIPELINE_YUI_BINARY
PIPELINE = False
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
INTERNAL_IPS = ('127.0.0.1', '86.44.166.21', '192.168.1.111')

GOOGLE_ANALYTICS_CODE = localsettings.GOOGLE_ANALYTICS_CODE
TASTYPIE_DATETIME_FORMATTING = 'rfc-2822'

SENDFILE_BACKEND = localsettings.SENDFILE_BACKEND
SENDFILE_ROOT = os.path.join(MEDIA_ROOT, 'mixes')
SENDFILE_URL = '/media/mixes'

import mimetypes

mimetypes.add_type("text/xml", ".plist", False)

HTML_MINIFY = not localsettings.DEBUG

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = localsettings.EMAIL_HOST
EMAIL_PORT = localsettings.EMAIL_PORT
DEFAULT_FROM_EMAIL = 'DSS ChatBot <chatbot@deepsouthsounds.com>'
DEFAULT_HTTP_PROTOCOL = 'http'

if DEBUG:
    import mimetypes

    mimetypes.add_type("image/png", ".png", True)
    mimetypes.add_type("image/png", ".png", True)
    mimetypes.add_type("application/x-font-woff", ".woff", True)
    mimetypes.add_type("application/vnd.ms-fontobject", ".eot", True)
    mimetypes.add_type("font/ttf", ".ttf", True)
    mimetypes.add_type("font/otf", ".otf", True)

# TODO(fergal.moran@gmail.com): #import localsettings - so all localsettings are part of import settings

REALTIME_HEADERS = {
    'content-type': 'application/json'
}

DBBACKUP_STORAGE = localsettings.DBBACKUP_STORAGE
DBBACKUP_TOKENS_FILEPATH = localsettings.DBBACKUP_TOKENS_FILEPATH
DBBACKUP_DROPBOX_APP_KEY = localsettings.DBBACKUP_DROPBOX_APP_KEY
DBBACKUP_DROPBOX_APP_SECRET = localsettings.DBBACKUP_DROPBOX_APP_SECRET
DBBACKUP_CLEANUP_KEEP = 5

if 'test' in sys.argv:
    try:
        from test_settings import *
    except ImportError:
        pass

GEOIP_PATH = localsettings.GEOIP_PATH
from pipelinesettings import *


