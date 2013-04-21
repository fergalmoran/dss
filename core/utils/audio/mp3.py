from mutagen.mp3 import MP3
from core.utils.audio import Mp3FileNotFoundException


def mp3_length(source_file):
    try:
        audio = MP3(source_file)
        return audio.info.length
    except IOError:
        raise Mp3FileNotFoundException("Audio file not found: %s" % source_file)