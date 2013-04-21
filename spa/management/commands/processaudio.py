import os
from django.core.management.base import NoArgsCommand, CommandError
from core.utils.audio import Mp3FileNotFoundException
from core.utils.audio.mp3 import mp3_length
from dss import settings
from spa.models import Mix


class Command(NoArgsCommand):
    help = "Updates audio files with their durations"

    def handle(self, *args, **options):
        try:
            candidates = Mix.objects.filter(duration__isnull=True)
            for mix in candidates:
                try:
                    print "Finding duration for: %s" % mix.title
                    length = mp3_length(mix.get_absolute_path())
                    print "\tLength: %d" % length
                    mix.duration = length
                    mix.save()
                except Mp3FileNotFoundException, me:
                    mix.delete()
                    print me.message
        except Exception, ex:
            raise CommandError(ex.message)