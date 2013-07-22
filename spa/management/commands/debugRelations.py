from django.core.management.base import NoArgsCommand
from spa.models import Mix


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            list = Mix.objects.filter(slug='dss-on-deepvibes-radio-17th-july-jamie-o-sullivan')[0]
            for fav in list.favourites.all():
                print fav.slug
            pass
        except Exception, ex:
            print "Debug exception: %s" % ex.message