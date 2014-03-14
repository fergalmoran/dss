import subprocess
import traceback
import uuid
import os
from dss import settings


def generate_waveform(input_file, output_file):
    working_file = "%s%s.png" % (settings.DSS_TEMP_PATH, uuid.uuid1())
    try:
        print "Starting decode : %s\n\tIn: %s\n\tOut: %s" % \
              (settings.DSS_LAME_PATH, input_file, working_file)
        #sox f679a81a-ea14-4385-a677-c663559d1e4b.mp3 -c 1 -t wav -
        #| /srv/dss/bin/wav2png -w 800 -h 120 -o song.png /dev/stdin
        convert_command = "%s %s -c 1 -t wav -" % (settings.DSS_LAME_PATH, input_file)
        print "Convert command: %s" % convert_command
        command_split = convert_command.split()
        convert = subprocess.Popen(command_split,
                                   stdout=subprocess.PIPE)

        waveform_command = "%s -w 800 -h 120 -o %s" % (settings.DSS_WAVE_PATH, working_file)
        waveform = subprocess.Popen(waveform_command,
                                    stdin=convert.stdout, stdout=subprocess.PIPE)

        convert.stdout.close()
        output = waveform.communicate()[0]

        print "Finished decode\n%s" % output

        if os.path.exists(working_file):
            print "Starting waveform generation"
            ret = subprocess.call([
                                      settings.DSS_WAVE_PATH, "-w", "800", "-h", "120", "-o",
                                      output_file,
                                      working_file], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            if os.path.isfile(output_file):
                os.remove(working_file)
                print "Generated waveform"
                return output_file
            else:
                print "Failed generating waveform: %s" % output_file
                print "Subprocess returned: %s" % ret
        else:
            print "Unable to find working file, did LAME succeed?"
            return ""
    except Exception, ex:
        print "Error generating waveform %s" % (ex)

