import os
from django.core.files.storage import FileSystemStorage
from django.core.management.base import NoArgsCommand
from dss import settings

from spa.models.mix import Mix
from core.tasks import create_waveform_task


class Command(NoArgsCommand):
    help = "Generate all outstanding waveforms"

    def _generateWaveform(self, mix):
        #Check for file in mix directory
        try:
            processed_file = mix.get_absolute_path()
            if not os.path.isfile(processed_file):
                cached_file = mix.get_cache_path()
                if not os.path.isfile(cached_file):
                    print "File for %s not found tried\n\t%s\n\t%s" % (mix.title, processed_file, cached_file)
                    return

            print "File found, starting waveform task (%s)" % mix.uid
            create_waveform_task.delay(in_file=cached_file, uid=mix.uid)
            print "Task submitted"

        except Exception, ex:
            print "Error generating waveform: %s" % ex.message

    def handle(self, *args, **options):
        print "Scanning for missing waveforms"
        unprocessed = Mix.objects.filter(waveform_generated=False)
        for mix in unprocessed:
            print "Generating waveform for mix %d" % mix.id
            self._generateWaveform(mix)

    def handle_noargs(self, **options):
        print "Scanning for missing waveforms"
        unprocessed = Mix.objects.filter(waveform_generated=False)
        for mix in unprocessed:
            print "Generating waveform for mix %d" % mix.id
            self._generateWaveform(mix.uid)
