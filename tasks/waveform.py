import os
import subprocess
import traceback
import uuid
from dss import settings
from celery.task.base import task
import spa

@task(name='www.create_waveform_task')
def create_waveform_task(in_file, id=None):
    try:
        working_file = "/tmp/%s.wav" % (uuid.uuid1())
        out_file = os.path.join(settings.MEDIA_ROOT, 'waveforms/%i.png' % id)
        try:
            print "Starting decode"
            p = subprocess.call(["/usr/bin/lame", "--decode", in_file, working_file])
            print "Finished decode"
            if os.path.exists(working_file):
                print "Starting waveform generation"
                subprocess.call(["waveformgen",  "-m", "-l", "-i", working_file, "-o", out_file])

                if os.path.isfile(out_file):
                    os.remove(working_file)
                    print "Generated waveform"
                    return out_file
                else:
                    print "Failed generating waveform: %s" % out_file
            else:
                print "Unable to find working file, did LAME succeed?"
                return ""
        except:
            print "Error generating waveform"
            traceback.print_exc()

    except:
        print "Error generating waveform"
        traceback.print_exc()


@task(name='www.gmw')
def gmw():
    objects = spa.models.mix.Mix.objects.all()

    for object in objects:
        file = os.path.join(settings.MEDIA_ROOT, 'waveforms/%i.png' % object.pk)
        if not os.path.isfile(file):
            print "Found missing waveform"
            create_waveform_task(object.pk, object.local_file.file.name)


