from django.shortcuts import render_to_response
from django.template.context import RequestContext

def app(request):
    response = render_to_response("inc/app.html", context_instance=RequestContext(request))
    """
    set the fb headers, for now just do it on every response.
    <meta property="fb:app_id" content="154504534677009" />
    <meta property="og:type"   content="deepsouthsounds:mix" />
    <meta property="og:title"  content="June 2012" />
    <meta property="og:image"  content="http://www-test.deepsouthsounds.com:8000/static/img/site-logo-gr.png" />
    """

    return response
