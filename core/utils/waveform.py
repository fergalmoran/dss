import subprocess
import traceback
import uuid
import os
from dss import settings


def generate_waveform(input_file, output_file):
    try:
        print "Starting decode : %s\n\tIn: %s\n\tOut: %s" % \
              (settings.DSS_LAME_PATH, input_file, output_file)
        #sox f679a81a-ea14-4385-a677-c663559d1e4b.mp3 -c 1 -t wav -
        #| /srv/dss/bin/wav2png -w 800 -h 120 -o song.png /dev/stdin
        convert_command = "%s %s -c 1 -t wav - | %s -w 800 -h 120 -o %s /dev/stdin" % \
                          (settings.DSS_LAME_PATH, input_file, settings.DSS_WAVE_PATH, output_file)
        print "Convert command: %s" % convert_command
        result = os.system(convert_command)
        print result

        if os.path.exists(output_file):
            return output_file
        else:
            print "Unable to find working file, did LAME succeed?"
            return ""

    except Exception, ex:
        print "Error generating waveform %s" % (ex)

