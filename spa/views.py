import logging
from django.shortcuts import render_to_response, redirect
from django.template.context import RequestContext
from core.utils.string import lreplace, rreplace
from spa.social.views import social_redirect


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
    t = loader.get_template(template_name) # You need to create a 500.html template.
    ltype,lvalue,ltraceback = sys.exc_info()
    sys.exc_clear() #for fun, and to point out I only -think- this hasn't happened at 
                    #this point in the process already
    return http.HttpResponseServerError(t.render(Context({'type':ltype,'value':lvalue,'traceback':ltraceback})))
