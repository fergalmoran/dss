from django.core.management.base import NoArgsCommand
from spa.models.activity import ActivityFavourite, ActivityLike


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            l = ActivityLike.objects.all()
            for item in l:
                m = item.mix
                m.favourites.add(item.user)
                m.save()

        except Exception, ex:
            print "Debug exception: %s" % ex.message