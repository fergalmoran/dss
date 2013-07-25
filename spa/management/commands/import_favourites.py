from django.core.management.base import NoArgsCommand
from spa.models.activity import ActivityFavourite


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            l = ActivityFavourite.objects.all()
            for item in l:
                m = item.mix
                m.favourites.add(item.user)
                m.save()

        except Exception, ex:
            print "Debug exception: %s" % ex.message