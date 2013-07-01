from mutagen.easyid3 import EasyID3, mutagen
from mutagen.id3 import ID3, TPE1, TIT2, TALB, TCON, COMM, TDRC
from mutagen.mp3 import MP3
from core.utils.audio import Mp3FileNotFoundException


def mp3_length(source_file):
    try:
        audio = MP3(source_file)
        return audio.info.length
    except IOError:
        raise Mp3FileNotFoundException("Audio file not found: %s" % source_file)


def tag_mp3(source_file, artist, title, url="", album="", year="", comment="", image_file="", genre=[]):
    #mp3Object.tags.add(APIC(encoding=3, mime=image[1], type=3, desc=u'Cover', data=open(image[0]).read()))

    try:
        audio = ID3(source_file)
    except mutagen.id3.error:
        audio = ID3()

    audio.add(TPE1(encoding=3, text=unicode(artist)))
    audio.add(TIT2(encoding=3, text=unicode(title)))
    audio.add(TALB(encoding=3, text=unicode(album)))
    audio.add(TCON(encoding=3, text=unicode("Deep House")))
    audio.add(TPE1(encoding=3, text=unicode(artist)))
    audio.add(COMM(encoding=3, lang="eng", desc="", text=unicode(comment)))
    audio.add(TDRC(encoding=3, text=unicode(year)))

    image = mutagen.id3.APIC(
        encoding=3,
        mime='image/jpeg',
        type=2,
        desc=u'Cover',
        data=open(image_file, 'rb').read()
    )
    audio.add(image)
    audio.save(source_file)

