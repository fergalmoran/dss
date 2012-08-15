from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from annoying.decorators import render_to
from django.shortcuts import render_to_response
import json
from django.utils import simplejson
from core.utils import live
from spa.models.Mix import Mix
from spa.models.Comment import Comment
from spa.models.MixLike import MixLike


class AjaxHandler(object):
    import logging

    # Get an instance of a logger
    logger = logging.getLogger(__name__)

    def __init__(self, api_name="v1"):
        self.api_name = api_name

    @property
    def urls(self):
        pattern_list = [
            url(r'^mix-description/(?P<mix_id>\d+)/$', 'spa.ajax.get_mix_description', name='ajax_mix-description'),
            url(r'^mix/add_comment/$', 'spa.ajax.mix_add_comment', name='mix_add_comment'),
            url(r'^mix/comments/(?P<mix_id>\d+)/$', 'spa.ajax.mix_comments', name='ajax_mix_comments'),
            url(r'^header/$', 'spa.ajax.header', name='header'),
            url(r'^mix_stream_url/(?P<mix_id>\d+)/$', 'spa.ajax.get_mix_stream_url'),
            url(r'^release_player/(?P<release_id>\d+)/$', 'spa.ajax.release_player'),
            url(r'^live_now_playing/$', 'spa.ajax.live_now_playing'),
            url(r'^like/$', 'spa.ajax.like', name='ajax_mix-description'),
            ]
        return pattern_list

    def wrap_view(self, view):
        def wrapper(request, *args, **kwargs):
            return getattr(self, view)(request, *args, **kwargs)

        return wrapper


def _get_json(payload, key='value'):
    data = {
        key: payload
    }
    return data


def get_mix_description(request, mix_id):
    return HttpResponse(json.dumps(_get_json('ArgleBargle')), mimetype="application/json")


@render_to('inc/header.html')
def header(request):
    return HttpResponse(render_to_response('inc/header.html'))


def get_mix_stream_url(request, mix_id):
    try:
        mix = Mix.objects.get(pk=mix_id)
        mix.add_play(request.user)
        data = {
            'stream_url': mix.get_stream_path(),
            'description': mix.description,
            'item_url': mix.get_absolute_url(),
            'title': mix.title
        }
        return HttpResponse(json.dumps(data), mimetype="application/json")
    except Exception, e:
        self.logger.exception("Error getting mix stream url")

def live_now_playing(request):
    return HttpResponse(
        json.dumps({
            'stream_url': "radio.deepsouthsounds.com",
            'description': 'Description',
            'title': live.get_now_playing("radio.deepsouthsounds.com", "8000", "live")
        }), mimetype="application/json")


@render_to('inc/release_player.html')
def release_player(request, release_id):
    return HttpResponse('Hello Sailor')

def mix_add_comment(request):
    if request.POST:
        comment = Comment()
        comment.mix_id = request.POST['mixid']
        comment.user = request.user
        comment.comment = request.POST['comment']
        comment.time_index = request.POST['position']
        comment.save()

        return HttpResponse(simplejson.dumps({'description': 'Hello Sailor'}))
    else:
        return HttpResponse(simplejson.dumps({'description': 'Error posting'}))

@render_to('inc/comment_list.html')
def mix_comments(request, mix_id):
    return {
        "results": Comment.objects.filter(mix_id=mix_id),
        }

@login_required()
def like(request):
    if request.is_ajax():
        if request.method == 'POST':
            if request.POST['dataMode'] == 'mix':
                mix = Mix.objects.get(pk = request.POST['dataId'])
                if mix is not None:
                    mix.likes.add(MixLike(mix = mix, user = request.user))
                    mix.save()
                    return HttpResponse(simplejson.dumps(request.raw_post_data))
