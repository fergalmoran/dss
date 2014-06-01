import urllib2
import logging

from django.conf.urls import url
from django.contrib.sites.models import Site
from django.core.urlresolvers import resolve
from django.http import Http404
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import requests
from allauth.socialaccount.models import SocialToken

from dss import settings
from spa.models.mix import Mix
from spa.models.userprofile import UserProfile


logger = logging.getLogger(__name__)

"""
    Handles callbacks from facebook and twitter
"""

def _getPayload(request):
    return {
        "app_id": settings.FACEBOOK_APP_ID,
        "site_url": 'http://%s' % Site.objects.get_current().domain,
        "site_image_url": '%s/img/dss-large.png' % settings.STATIC_URL,
    }


def mix(request, args):
    try:
        if 'mix_id' in args:
            mix = Mix.objects.get(pk=args['mix_id'])
        else:
            mix = Mix.objects.get(slug=args['slug'])
    except Mix.DoesNotExist:
        raise Http404

    image = mix.get_image_url('400x400')
    audio_url = mix.get_stream_path()
    mix_url = mix.get_absolute_url()
    default = _getPayload(request)
    extras = {
        "description": mix.description.replace('<br />', '\n'),
        "title": mix.title,
        "image_url": image,
        "audio_url": audio_url,
        "mix_url": 'http://%s%s' % (Site.objects.get_current().domain, mix_url)
    }
    payload = dict(default.items() + extras.items())
    response = render_to_response(
        'inc/facebook/mix.html',
        payload,
        context_instance=RequestContext(request)
    )
    return response


def user(request, args):
    try:
        user = UserProfile.objects.get(slug=args['user_id'])
    except UserProfile.DoesNotExist:
        raise Http404

    image = user.get_avatar_image()
    profile_url = user.get_profile_url()
    default = _getPayload(request)
    extras = {
        "description": user.get_nice_name,
        "profile_url": profile_url,
        "image_url": image,
    }
    payload = dict(default.items() + extras.items())
    response = render_to_response(
        'inc/facebook/user.html',
        payload,
        context_instance=RequestContext(request)
    )
    return response


def index(request):
    response = render_to_response(
        "inc/facebook/index.html",
        _getPayload(request),
        context_instance=RequestContext(request))
    return response


def social_redirect(request):
    try:
        resolver = resolve('/social' + request.path)
        if resolver is not None:
            logger.debug("Resolver successfully resolved")
            return resolver.func(request, resolver.kwargs)
        else:
            logger.debug("No resolver found for: $%s" % request.path)
    except Http404:
        logger.debug("404 on resolver: $%s" % request.path)
        return index(request)
    except Exception, ex:
        logger.debug("Unhandled exception in social_redirect: $%s" % ex)
        return index(request)


def post_like(request, mix):
    try:
        tokens = SocialToken.objects.filter(
            account__user=request.user,
            account__provider='facebook')
        for token in tokens:
            url = 'https://graph.facebook.com/%s/og.likes' % token.account.uid
            values = {
                'access_token': token.token,
                'object': mix.get_full_url(),
            }
            response = requests.post(url, data=values)
            if response.status_code == 200:
                print "Returned %s" % response.json
                return response.json['id']
            else:
                print "Returned status code of %s" % response.status_code
    except urllib2.HTTPError, httpEx:
        print httpEx.message
    except Exception, ex:
        print ex.message
    return ""


def delete_like(request, uid):
    try:
        tokens = SocialToken.objects.filter(account__user=request.user, account__provider='facebook')
        for token in tokens:
            url = "https://graph.facebook.com/%s" % uid
            values = {
                'access_token': token.token,
            }
            response = requests.delete(url, data=values)
            return response
    except Exception, ex:
        print "Error talking with facebook: %s" % ex.message

