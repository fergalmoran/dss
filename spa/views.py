from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
import re
from spa.social import social_redirect

def _app(request):
    return social_redirect(request)

def app(request):
    if request.META['HTTP_USER_AGENT'].startswith('facebookexternalhit'):
        return social_redirect(request)
    else:
        return render_to_response(
            "inc/app.html",
            context_instance=RequestContext(request))

def default(request):
    backbone_url = "http://%s/#%s" % (request.get_host(), re.sub('/$', '', request.path))
    return redirect(backbone_url)

def upload(request):
    return render_to_response("inc/upload.html", context_instance=RequestContext(request))
