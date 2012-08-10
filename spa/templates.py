from django.shortcuts import render_to_response
from django.template.context import RequestContext

__author__ = 'fergalm'

def get_template(request, template_name):
    return render_to_response(
        'views/%s.html' % template_name,
        context_instance=RequestContext(request))