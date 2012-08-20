import logging
import urllib
from django.core.management.base import NoArgsCommand
from django.utils import simplejson
from spa.models import Tracklist

class Command(NoArgsCommand):

    help = "Create purchase links for tracks"

    def generate_purchase_link(self, track):
        print "Looking for beatport link for %s" % track.description
        url = "http://api.beatport.com/catalog/3/search?query=%s&facets[]=trackName:%s" % (track.description, track.description)
        result = simplejson.load(urllib.urlopen(url))

        if 'Error' in result:
            print "Failed"
            return ""
        else:
            for entry in result['results']:
                print entry['name']

    def handle_noargs(self, **options):
        try:
            tracks = Tracklist.objects.all()
            for track in tracks:
                link = self.generate_purchase_link(track)
        except Exception, ex:
            print "Error generating purchase link: %s" % ex.message
