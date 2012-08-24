import os
from dss import settings
from core.utils.waveform import generate_waveform
from django.core.management.base import NoArgsCommand
from spa.models.Mix import Mix

class Command(NoArgsCommand):
    help = "Generate all outstanding waveforms"
    def _check_file(self, local_file, output_file):
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, local_file)):
            file = os.path.join(settings.MEDIA_ROOT, output_file)
            if not os.path.isfile(file):
                print "Found missing waveform"
                generate_waveform(local_file, file)

    def handle(self, *args, **options):
        for guid in args:
            output_file = 'waveforms/%s.png' % guid
            local_file =  '%s/%s' % (self.CACHE_ROOT, guid)
            if os.path.isfile(local_file):
                self._check_file(local_file, output_file)

    def handle_noargs(self, **options):
        print "Generating waveforms for mix"
        unprocessed = Mix.objects.filter(waveform_generated=False)
        for mix in unprocessed:
            pass