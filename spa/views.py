import logging
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render_to_response
from django.template.context import RequestContext
import sys

def app(request):
    return render_to_response("inc/app.html", context_instance=RequestContext(request))

def upload(request):
    return render_to_response("inc/upload.html", context_instance=RequestContext(request))


