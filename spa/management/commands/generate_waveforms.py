import os
from dss import settings
from core.utils.waveform import generate_waveform
from spa.models.Mix import Mix
from spa.models.Release import ReleaseAudio
from django.core.management.base import NoArgsCommand

class Command(NoArgsCommand):

    help = "Generate all outstanding waveforms"

    def _check_file(self, local_file, output_file):
        if os.path.isfile(os.path.join(settings.MEDIA_ROOT, local_file)):
            file = os.path.join(settings.MEDIA_ROOT, output_file)
            if not os.path.isfile(file):
                print "Found missing waveform"
                generate_waveform(local_file, file)

    def handle_noargs(self, **options):
        print "Generating waveforms for mix"
        objects = Mix.objects.all()
        for object in objects:
            output_file = 'waveforms/mix/%d.png' % object.pk
            self._check_file(object.local_file.file.name, output_file)
            
        print "Generating waveforms for release"
        objects = ReleaseAudio.objects.all()
        for object in objects:
            output_file = 'waveforms/release/%d.png' % object.pk
            self._check_file(object.local_file.file.name, output_file)
