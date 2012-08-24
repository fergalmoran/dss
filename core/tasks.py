import shutil
from celery.task import task
import os
from core.utils.waveform import generate_waveform
from dss import settings

"""
    name='core.tasks.create_waveform_task'
"""
@task()
def create_waveform_task(in_file, uid):
    out_file = os.path.join(settings.MEDIA_ROOT, 'waveforms/%s.png' % uid)
    print "Creating waveform \n\tIn: %s\n\tOut: %s" % (in_file, out_file)
    generate_waveform(in_file, out_file)
    if os.path.isfile(out_file):
        print "Waveform generated successfully"
        file, extension = os.path.splitext(in_file)
        new_file = in_file.replace('cache', 'mixes')
        print "Moving cache audio clip from %s to %s" % (in_file, new_file)
        shutil.move(in_file, new_file)
    else:
        print "Outfile is missing"
