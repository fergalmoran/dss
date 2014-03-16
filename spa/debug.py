from django.conf.urls import url, patterns, include
from django.shortcuts import render_to_response
from django.template import RequestContext

urls = patterns(
    '',
    url(r'^typeahead/', 'spa.debug.typeahead'),
)

def typeahead(request):
    return render_to_response(
    'views/debug/typeahead.html',
    context_instance=RequestContext(request))
