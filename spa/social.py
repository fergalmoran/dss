from django.conf.urls import url
from django.contrib.sites.models import Site
from django.http import  Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from dss import  settings
from spa.models.Mix import Mix

class SocialHandler(object):
    import logging
    logger = logging.getLogger(__name__)

    def __init__(self, api_name="v1"):
        self.api_name = api_name

    @property
    def urls(self):
        pattern_list = [
            url(r'^redirect/mix/(?P<mix_id>\d+)/$', 'spa.social.redirect_mix', name='social_redirect'),
            #url(r'^redirect/mix/(?P<mix_id>\d+)/$', 'spa.social.redirect_mix', name='social_redirect-mix'),
            ]
        return pattern_list


def redirect_mix(request, mix_id):
    try:
        mix = Mix.objects.get(pk=mix_id)
    except Mix.DoesNotExist:
        raise Http404
    response = render_to_response(
        'inc/fb_like.html',
        {
            "app_id"        : settings.FACEBOOK_APP_ID,
            "description"   : mix.title,
            "audio_url"     : 'http://www.%s:%s%s' % (Site.objects.get_current().domain, request.META['SERVER_PORT'], mix.get_stream_path()),
            "image_url"     : 'http://www.%s:%s%s' % (Site.objects.get_current().domain, request.META['SERVER_PORT'], mix.get_image()),
            "redirect"      : 'http://www.%s:%s#%s' % (Site.objects.get_current().domain, request.META['SERVER_PORT'], mix.get_absolute_url())
        },
        context_instance = RequestContext(request)
    )
    return response
