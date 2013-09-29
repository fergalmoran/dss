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
            in_file = mix.get_absolute_path()
            if not os.path.isfile(in_file):
                in_file = mix.get_cache_path()
                if not os.path.isfile(in_file):
                    print "File %s not found" % in_file
                    return

            create_waveform_task.delay(in_file=in_file, uid=mix.uid)

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
