from django.core.management.base import NoArgsCommand

from spa.models import Tracklist
from spa.models.mix import Mix


class Command(NoArgsCommand):
    help = "Create tracklists for all mixes"

    def handle_noargs(self, **options):
        mixes = Mix.objects.all()
        for mix in mixes:
            lines = mix.description.strip().split('\n')
            index = 0
            for line in lines:
                mix.tracklist.add(Tracklist(index=index, description=line))
                mix.save()
                print "%d: %s" % (index, line)
                index += 1