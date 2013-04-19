import os

from django.core.management.base import NoArgsCommand

from dss import settings

from spa.models.Mix import Mix
from core.tasks import create_waveform_task


class Command(NoArgsCommand):
    help = "Generate all outstanding waveforms"

    def _generateWaveform(self, mix):
        fileName, extension = os.path.splitext(mix.local_file.name)
        if extension == "" or extension == ".":
            extension = ".mp3"
        in_file = '%s/%s%s' % (settings.CACHE_ROOT, mix.uid, extension)
        try:
            if os.path.isfile(in_file):
                create_waveform_task.delay(in_file=in_file, mix_uid=mix.uid)
            else:
                print "File %s not found" % in_file

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
