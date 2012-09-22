import shutil
from celery.task import task
import os
from core.utils.waveform import generate_waveform
from dss import settings
from spa.signals import waveform_generated

@task()
def create_waveform_task(in_file, mix_uid):
    out_file = os.path.join(settings.MEDIA_ROOT, 'waveforms/%s.png' % mix_uid)
    print "Creating waveform \n\tIn: %s\n\tOut: %s" % (in_file, out_file)
    generate_waveform(in_file, out_file)
    if os.path.isfile(out_file):
        print "Waveform generated successfully"
        file, extension = os.path.splitext(in_file)
        new_file = in_file.replace('cache', 'mixes')
        print "Moving cache audio clip from %s to %s" % (in_file, new_file)
        shutil.move(in_file, new_file)
        print "Uid: %s" % mix_uid
        waveform_generated.send(sender=None, uid=mix_uid)
    else:
        print "Outfile is missing"
