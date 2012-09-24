from wsgiref.util import FileWrapper
from django.conf.urls import url
from django.http import HttpResponse, Http404
import os
from sendfile import sendfile
from spa.models.Mix import Mix

class AudioHandler(object):
    @property
    def urls(self):
        pattern_list = [
            url(r'^stream/(?P<mix_id>\d+)/$', 'spa.audio.start_streaming', name='audio_start_streaming'),
            url(r'^download/(?P<mix_id>\d+)/$', 'spa.audio.download', name='audio_download'),
        ]
        return pattern_list

def download(request, mix_id):
    try:
        mix = Mix.objects.get(pk=mix_id)
        if mix is not None:
            filename = mix.local_file.path   # Select your file here.
            file, ext = os.path.splitext(filename)
            response = sendfile(request, filename, attachment=True, attachment_filename="%s.%s" % (mix.title, ext))
            return response
    except Exception, ex:
        print ex

    raise Http404("Mix not found")

def start_streaming(request, mix_id):
    try:
        mix = Mix.objects.get(pk=mix_id)
        if mix is not None:
            filename = mix.local_file.path   # Select your file here.
            response = sendfile(request, filename)
            """
            #wrapper = FixedFileWrapper(open(filename, 'rb'))
            response = HttpResponse(FileIterWrapper(open(filename)), content_type='audio/mpeg')
            response['Content-Length'] = os.path.getsize(filename)
            response['Content-Type'] = "audio/mpeg"
            response['Content-Transfer-Encoding'] = "binary"
            response['Cache-Control'] = "no-cache"
            """
            return response
    except Exception, ex:
        print ex

    raise Http404("Mix not found")