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

@login_required
def upload_progress(request):
    """
    Return JSON object with information about the progress of an upload.
    """
    if 'HTTP_X_PROGRESS_ID' in request.META:
        progress_id = request.META['HTTP_X_PROGRESS_ID']
        from django.utils import simplejson

        cache_key = "%s_%s" % (request.META['REMOTE_ADDR'], progress_id)
        data = cache.get(cache_key)
        json = simplejson.dumps(data)
        print >> sys.stderr, json
        return HttpResponse(json)
    else:
        logging.error("Received progress report request without X-Progress-ID header. request.META: %s" % request.META)
        return HttpResponseBadRequest('Server Error: You must provide X-Progress-ID header or query param.')
