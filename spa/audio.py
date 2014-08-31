import mimetypes
import os
import logging
import urlparse

from django.conf.urls import url
import json
from django.http import Http404, HttpResponse, HttpResponseForbidden, HttpResponseNotFound, HttpResponseRedirect
from django.core.servers.basehttp import FileWrapper
from django.shortcuts import redirect
from django.utils import simplejson
from django.utils.encoding import smart_str
from nginx_signing.signing import UriSigner
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
        if not request.user.is_authenticated():
            return HttpResponseForbidden("Get tae fuck!!!")

        mix = Mix.objects.get(pk=mix_id)
        if mix is not None:
            if mix.download_allowed:
                response = {
                    'url': '',
                    'filename': smart_str('Deep South Sounds - %s.%s' % (mix.title, mix.filetype)),
                    'mime_type': 'application/octet-stream'
                }
                if mix.archive_path in [None, '']:
                    audio_file = mix.get_absolute_path()
                    if os.path.exists(audio_file):
                        response['url'] = audio_file.name
                else:
                    response['url'] = mix.archive_path

                return HttpResponse(json.dumps(response))
            else:
                return HttpResponse('Downloads not allowed for this mix', status=401)

    except Exception, ex:
        print ex

    raise Http404("Mix not found")


def start_streaming(request, mix_id):
    logger.debug('Start streaming called: %s' % mix_id)
    try:
        mix = Mix.objects.get(pk=mix_id)
        if mix is not None:
            mix.add_play(request.user)
            # logger.debug('Found the mix (old method): %s' % mix.uid)
            logger.debug('Found the mix (new method) %s' % mix.uid)
            filename = "%s/mixes/%s.mp3" % (here(settings.MEDIA_ROOT), mix.uid)
            logger.debug('Serving file: %s' % filename)

            response = sendfile(request, filename)
            return response
    except Exception, ex:
        print ex

    raise Http404("Mix not found")

