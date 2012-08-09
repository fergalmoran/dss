import uuid

__author__ = 'fergalm'
def generate_save_file_name(prefix, filename):
    return '/'.join([prefix, str(uuid.uuid1()), filename])
