import logging
import uuid
from django.contrib.auth import logout
from django.http import HttpResponseServerError, HttpResponseRedirect
from django.shortcuts import render_to_response, redirect
from django.template import loader, Context
from django.template.context import RequestContext
import sys
from core.utils.string import lreplace, rreplace
from dss import settings
from spa.social.views import social_redirect


logger = logging.getLogger('spa')


def _app(request):
    return social_redirect(request)


def app(request):
    if 'HTTP_USER_AGENT' in request.META:
        if request.META['HTTP_USER_AGENT'].startswith('facebookexternalhit'):
            logger.debug("Redirecting facebook hit")
            return social_redirect(request)

    context = {
        'is_bot': request.user_agent.is_bot,
        'socket_io': settings.SOCKET_IO_JS_URL,
        'bust': uuid.uuid1()
    }

    if request.user_agent.browser.family == '___Firefox___':
        context['ua_html'] = \
            """<div class="alert alert-block alert-warning">
                    <button type="button" class="close" data-dismiss="alert">
                        <i class="fa fa-times"></i>
                    </button>
                    <i class="fa fa-eye"></i>
                    <strong>Hello Firefox user.</strong> If you are having any problems with the site, please do a
                    <a href="#" onclick="location.reload(true);">&nbsp;full refresh</a> (CTRL-F5)<br/>
                    <i class="fa fa-ambulance"></i>
                    if you're still having problems, please clear your cache (CTRL-SHIFT-DEL).
                </div>"""

    return render_to_response(
        "inc/app.html",
        context,
        context_instance=RequestContext(request))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect("/")

def default(request):
    if 'HTTP_USER_AGENT' in request.META and request.META['HTTP_USER_AGENT'].startswith('facebookexternalhit'):
        return social_redirect(request)

    backbone_url = "http://%s/#%s" % (request.get_host(), rreplace(lreplace(request.path, '/', ''), '/', ''))
    return redirect(backbone_url)


def upload(request):
    return render_to_response("inc/upload.html", context_instance=RequestContext(request))


def debug_500(request, template_name='debug_500.html'):
    """
    500 error handler.

    Templates: `500.html`
    Context: sys.exc_info() results
     """
    t = loader.get_template(template_name)  # You need to create a 500.html template.
    ltype, lvalue, ltraceback = sys.exc_info()
    sys.exc_clear()  # for fun, and to point out I only -think- this hasn't happened at
    # this point in the process already
    return HttpResponseServerError(t.render(Context({'type': ltype, 'value': lvalue, 'traceback': ltraceback})))
