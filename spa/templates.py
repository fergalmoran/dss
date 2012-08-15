from django.shortcuts import render_to_response
from django.template.context import RequestContext
from spa.forms import UserForm

__author__ = 'fergalm'

def get_template(request, template_name):
    return render_to_response(
        'views/%s.html' % template_name,
        context_instance=RequestContext(request))

def get_template_ex(request, template_name):
    html = render_to_response(
        'views/%s.html' % template_name,
        context_instance=RequestContext(request, {'form': UserForm() }))
    return html