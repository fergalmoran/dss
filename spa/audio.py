from wsgiref.util import FileWrapper
from django.conf.urls import url
from django.http import HttpResponse, Http404
import os
from spa.models.Mix import Mix

class FixedFileWrapper(FileWrapper):
    def __iter__(self):
        self.filelike.seek(0)
        return self

class AudioHandler(object):
    @property
    def urls(self):
        pattern_list = [
            url(r'^stream/(?P<mix_id>\d+)/$', 'spa.audio.start_streaming', name='audio_start_streaming'),
        ]
        return pattern_list

def start_streaming(request, mix_id):
    try:
        mix = Mix.objects.get(pk=mix_id)
        if mix is not None:
            filename = mix.local_file.file.name   # Select your file here.
            wrapper = FixedFileWrapper(open(filename, 'rb'))
            response = HttpResponse(wrapper, content_type='audio/mpeg')
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Type'] = "audio/mpeg"
            response['Content-Disposition'] = "inline; filename=stream.mp3"
            response['Cache-Control'] = "no-cache"
            response['Content-Transfer-Encoding'] = "binary"
            return response
    except Exception, ex:
        print ex

    raise Http404("Mix not found")