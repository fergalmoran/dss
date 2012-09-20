import uuid
import os

def generate_save_file_name(prefix, filename):
    filename, extension = os.path.splitext(filename)
    ret = "%s%s" % ('/'.join([prefix, str(uuid.uuid1())]), extension)
    return ret
