import subprocess
import traceback
import uuid
import os
from dss import settings

def generate_waveform(input_file, output_file):
    print "Generating waveform"
    try:
        working_file = "%s%s.wav" % (settings.DSS_TEMP_PATH, uuid.uuid1())
        try:
            print "Starting decode : %s\nInput File: %s\nOutput File: %s" % (settings.DSS_LAME_PATH, input_file, working_file)
            p = subprocess.call([settings.DSS_LAME_PATH, "--decode", input_file, working_file])
            print "Finished decode"
            if os.path.exists(working_file):
                print "Starting waveform generation"
                #print "%s -m -l -i %s -o -b 000000 %s" % (settings.DSS_WAVE_PATH, working_file, output_file)
                #subprocess.call([settings.DSS_WAVE_PATH, "-t", "-m", "-l", "-i", working_file, "-o", output_file])
                ret = subprocess.call(["/usr/local/bin/wav2png", "-w", "800", "-h", "120", "-o", output_file, working_file], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
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

    except:
        print "Error generating waveform"
        traceback.print_exc()
