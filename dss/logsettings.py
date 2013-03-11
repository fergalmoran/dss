import os

if os.name == 'posix':
    LOG_FILE = '/tmp/dss.log'
else:
    LOG_FILE = 'c:\\temp\\dss.log'

LOGGING = {
    'version': 1,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_FILE,
            'formatter': 'simple'
        },
    },
    'loggers': {
        'spa': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'core': {
            'handlers': ['file', 'console'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

