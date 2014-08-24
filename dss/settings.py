#e Django settings for dss project.
import os
import mimetypes
from django.core.urlresolvers import reverse_lazy
import djcelery
from django.conf import global_settings

from dss import logsettings
from utils import here

from localsettings import *
from pipelinesettings import *
from paymentsettings import *

DEVELOPMENT = DEBUG

TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Fergal Moran', 'fergal.moran@gmail.com'),
)

MANAGERS = ADMINS
AUTH_PROFILE_MODULE = 'spa.UserProfile'

ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'deepsouthsounds',
        'ADMINUSER': 'postgres',
        'USER': DATABASE_USER,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
    }
}
import sys
if 'test' in sys.argv or 'test_coverage' in sys.argv: #Covers regular testing and django-coverage
    print "Testing"
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

ROOT_URLCONF = 'dss.urls'
TIME_ZONE = 'Europe/Dublin'
LANGUAGE_CODE = 'en-ie'
SITE_ID = 1
USE_I18N = False
USE_L10N = True
s = True

SITE_ROOT = here('')

ADMIN_MEDIA_PREFIX = STATIC_URL + "grappelli/"

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
    'pipeline.finders.PipelineFinder',
    'pipeline.finders.CachedFileFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'
STATICFILES_DIRS = (
    here('static'),
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
    "spa.context_processors.dss_context"
)

AUTHENTICATION_BACKENDS = global_settings.AUTHENTICATION_BACKENDS + (
    "allauth.account.auth_backends.AuthenticationBackend",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'user_sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'spa.middleware.cors.XsSharingMiddleware',
    #'htmlmin.middleware.HtmlMinifyMiddleware',
    #'htmlmin.middleware.MarkRequestMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'pipeline.middleware.MinifyHTMLMiddleware',
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
    'user_sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admindocs',
    'django_facebook',
    'django_extensions',
    'django_gravatar',
    'notification',
    'djcelery',
    'django_nose',
    'sorl.thumbnail',
    'south',
    'pipeline',
    'avatar',
    'spa',
    'spa.signals',
    'core',
    'dirtyfields',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.twitter',
    'allauth.socialaccount.providers.google',
    'debug_toolbar',
    'django_jenkins',
    'dbbackup',
    'schedule',
    'djrill',
    'paypal.standard.ipn',
    'django_user_agents',
     'storages',
    #'backbone_tastypie',
)

# where to redirect users to after logging in
LOGIN_REDIRECT_URL = reverse_lazy('home')
LOGOUT_URL = reverse_lazy('home')

LOGGING = logsettings.LOGGING

FACEBOOK_APP_ID = '154504534677009'

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

INTERNAL_IPS = ('127.0.0.1', '86.44.166.21', '192.168.1.111')

TASTYPIE_DATETIME_FORMATTING = 'rfc-2822'
TASTYPIE_ALLOW_MISSING_SLASH = True

SENDFILE_ROOT = os.path.join(MEDIA_ROOT, 'mixes')
SENDFILE_URL = '/media/mixes'

SESSION_ENGINE = 'user_sessions.backends.db'

mimetypes.add_type("text/xml", ".plist", False)

HTML_MINIFY = not DEBUG


DEFAULT_FROM_EMAIL = 'DSS ChatBot <chatbot@deepsouthsounds.com>'
DEFAULT_HTTP_PROTOCOL = 'http'


EMAIL_BACKEND = 'djrill.mail.backends.djrill.DjrillBackend'

if DEBUG:
    import mimetypes

    mimetypes.add_type("image/png", ".png", True)
    mimetypes.add_type("image/png", ".png", True)
    mimetypes.add_type("application/x-font-woff", ".woff", True)
    mimetypes.add_type("application/vnd.ms-fontobject", ".eot", True)
    mimetypes.add_type("font/ttf", ".ttf", True)
    mimetypes.add_type("font/otf", ".otf", True)

REALTIME_HEADERS = {
    'content-type': 'application/json'
}
TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
if 'test' in sys.argv:
    try:
        from test_settings import *
    except ImportError:
        pass

