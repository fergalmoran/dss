import logging

from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext

from core.utils.string import lreplace, rreplace
from spa.social import social_redirect


logger = logging.getLogger('spa')


def _app(request):
    return social_redirect(request)


def app(request):
    if 'HTTP_USER_AGENT' in request.META:
        if request.META['HTTP_USER_AGENT'].startswith('facebookexternalhit'):
            logger.debug("Redirecting facebook hit")
            return social_redirect(request)

    return render_to_response(
        "inc/app.html",
        context_instance=RequestContext(request))


def default(request):
    if 'HTTP_USER_AGENT' in request.META:
        if request.META['HTTP_USER_AGENT'].startswith('facebookexternalhit'):
            logger.debug("Redirecting facebook hit")
            return social_redirect(request)

    backbone_url = "http://%s/#%s" % (request.get_host(), rreplace(lreplace(request.path, '/', ''), '/', ''))
    return redirect(backbone_url)


def upload(request):
    return render_to_response("inc/upload.html", context_instance=RequestContext(request))
