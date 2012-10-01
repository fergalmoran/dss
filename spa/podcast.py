import PyRSS2Gen
from django.contrib.sites.models import Site
from django.http import HttpResponse
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime
from spa.models import Mix

def get_default_podcast(request):

    mixes = Mix.objects.all()
    items = []
    for mix in mixes:
        items += [
            PyRSS2Gen.RSSItem(
                title = mix.title,
                link = 'http://%s:%s/audio/download/%s' % (Site.objects.get_current().domain, request.META['SERVER_PORT'], mix.pk),
                description = mix.description,
                pubDate = mix.upload_date,
                categories = [PyRSS2Gen.Category("Music")],
                guid = mix.uid)
        ]

    rss = PyRSS2Gen.RSS2(
        title = "Deep South Sounds Podcast",
        link = "http://deepsouthsounds.com",
        description = "Deep house music with a Cork twist",
        lastBuildDate = datetime.datetime.now(),
        items=items)

    return HttpResponse(rss.to_xml(), mimetype="text/xml")


