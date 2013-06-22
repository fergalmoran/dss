import os
import logging

from django.conf.urls import url
from django.http import Http404
from sendfile import sendfile

from dss import settings
from spa.models.mix import Mix
from utils import here


logger = logging.getLogger('spa')


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
            if mix.download_allowed:
                mix.add_download(request.user)
                filename = "%s/mixes/%s.mp3" % (here(settings.MEDIA_ROOT), mix.uid)
                response = sendfile(request, filename, attachment=True, attachment_filename="Deep South Sounds - %s.mp3" % mix.title)
                return response
    except Exception, ex:
        print ex

    raise Http404("Mix not found")


def start_streaming(request, mix_id):
    logger.debug('Start streaming called: %s' % mix_id)
    try:
        mix = Mix.objects.get(pk=mix_id)
        if mix is not None:
            mix.add_play(request.user)
            #logger.debug('Found the mix (old method): %s' % mix.uid)
            #filename = mix.local_file.path
            logger.debug('Found the mix (new method) %s' % mix.uid)
            filename = "%s/mixes/%s.mp3" % (here(settings.MEDIA_ROOT), mix.uid)
            logger.debug('Serving file: %s' % filename)

            response = sendfile(request, filename)
            return response
    except Exception, ex:
        print ex

    raise Http404("Mix not found")

