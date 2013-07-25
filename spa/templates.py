from django.contrib.sites.models import Site
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from htmlmin.decorators import not_minified_response
from dss import localsettings
from spa.forms import UserForm

__author__ = 'fergalm'


@not_minified_response
def get_template(request, template_name):
    return render_to_response(
        'views/%s.html' % template_name,
        context_instance=RequestContext(request))


@not_minified_response
def get_template_ex(request, template_name):
    html = render_to_response(
        'views/%s.html' % template_name,
        context_instance=RequestContext(request, {'form': UserForm()}))
    return html


@not_minified_response
def get_embed_codes_dialog(request, slug):
    payload = {
        'embed_code': 'http://%s/embed/%s' % (Site.objects.get_current().domain, slug)
    }
    return render_to_response(
        'views/dlg/EmbedCodes.html',
        payload,
        context_instance=RequestContext(request))


@not_minified_response
def get_dialog(request, dialog_name, **kwargs):
    return render_to_response(
        'views/dlg/%s.html' % dialog_name,
        context_instance=RequestContext(request))


def get_javascript(request, template_name):
    localsettings.JS_SETTINGS.update({
        'CURRENT_USER_ID': request.user.id or -1
    })
    return render_to_response(
        'javascript/%s.js' % template_name,
        localsettings.JS_SETTINGS,
        context_instance=RequestContext(request),
        mimetype="text/javascript")
