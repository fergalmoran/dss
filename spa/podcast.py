from django.shortcuts import render_to_response, render
from django.template import RequestContext, Context
from spa.models import Mix

def get_default_podcast(request):
    mixes = Mix.objects.filter(download_allowed=True)
    return render(
        request,
        'inc/xml/podcast.xml',
        {'items': mixes},
        content_type='text/xml; charset=utf-8'
    )


