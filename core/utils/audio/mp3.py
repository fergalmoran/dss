from mutagen.easyid3 import EasyID3, mutagen
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

    info = EasyID3(source_file)
    info['artist'] = unicode(artist)
    info['title'] = unicode(title)
    info['album'] = unicode(album)
    info['genre'] = unicode("Deep House")
    info['copyright'] = url
    #info['year'] = unicode(year)
    info.save()

    id3 = mutagen.id3.ID3(source_file)
    frame = mutagen.id3.COMM(encoding=3, lang='XXX', desc=u'', text=[unicode(comment)])
    id3.add(frame)

    image = mutagen.id3.APIC(
        encoding=3,
        mime='image/jpeg',
        type=2,
        desc=u'Cover',
        data=open(image_file, 'rb').read()
    )
    id3.add(image)
    id3.save()

