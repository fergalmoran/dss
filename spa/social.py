from django.conf.urls import url
from django.contrib.sites.models import Site
from django.core.urlresolvers import resolve
from django.http import  Http404
from django.shortcuts import render_to_response, redirect
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
            url(r'^$', 'spa.social.index', name='social_index'),
        ]
        return pattern_list

def _getPayload(request):
    return {
        "app_id"        : settings.FACEBOOK_APP_ID,
        "site_url"      : 'http://%s:%s' % (Site.objects.get_current().domain, request.META['SERVER_PORT']),
        "site_image_url": '%s/img/dss-large.png' % settings.STATIC_URL,
    }

def redirect_mix(request, mix_id):
    try:
        mix = Mix.objects.get(pk=mix_id)
    except Mix.DoesNotExist:
        raise Http404

    image = mix.get_image_url()
    audio_url = mix.get_stream_path()
    redirect_url = mix.get_absolute_url()
    response = render_to_response(
        'inc/fb_like.html',
        _getPayload(request) + {
            "description"   : mix.title,
            "audio_url"     : 'http://%s:%s%s' % (Site.objects.get_current().domain, request.META['SERVER_PORT'], audio_url),
            "redirect"      : 'http://%s:%s#%s' % (Site.objects.get_current().domain, request.META['SERVER_PORT'], redirect_url)
        },
        context_instance = RequestContext(request)
    )
    return response

def index(request):
    response =  render_to_response(
        "inc/facebook/index.html",
        _getPayload(request),
        context_instance=RequestContext(request))
    return response

def social_redirect(request):
    try:
        resolver = resolve('/social' + request.path)
        if resolver is not None:
            return resolver.func(request)
    except Http404:
        return index(request)
