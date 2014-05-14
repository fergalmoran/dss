from django.conf import settings


def dss_context(context):
    return {
        'DEBUG': settings.DEBUG,
        'live_enabled': settings.LIVE_ENABLED
    }
