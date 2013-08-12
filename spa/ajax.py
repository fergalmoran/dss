from datetime import datetime
import os
import logging

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage, FileSystemStorage
from django.db.models import get_model
from django.http import HttpResponse, HttpResponseNotFound
from annoying.decorators import render_to
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from core.utils import live
from dss import localsettings, settings
from spa.models import UserProfile, Release
from spa.models.mix import Mix
from spa.models.comment import Comment
from core.serialisers import json
from core.tasks import create_waveform_task
from core.utils.audio.mp3 import mp3_length
from spa.models.notification import Notification
from jfu.http import upload_receive, UploadResponse, JFUResponse

logger = logging.getLogger(__name__)


class AjaxHandler(object):
    # Get an instance of a logger

    def __init__(self, api_name="v1"):
        self.api_name = api_name

    @property
    def urls(self):
        pattern_list = [
            url(r'^mix/add_comment/$', 'spa.ajax.mix_add_comment', name='mix_add_comment'),
            url(r'^mix/comments/(?P<mix_id>\d+)/$', 'spa.ajax.mix_comments', name='ajax_mix_comments'),
            url(r'^header/$', 'spa.ajax.header', name='header'),
            url(r'^session_play_count/$', 'spa.ajax.session_play_count'),
            url(r'^mix_stream_url/(?P<mix_id>\d+)/$', 'spa.ajax.get_mix_stream_url'),
            url(r'^release_player/(?P<release_id>\d+)/$', 'spa.ajax.release_player'),
            url(r'^live_now_playing/$', 'spa.ajax.live_now_playing'),
            url(r'^mark_read/$', 'spa.ajax.mark_read'),
            url(r'^facebook_post_likes_allowed/$', 'spa.ajax.facebook_post_likes_allowed',
                name='ajax_facebook_post_likes_allowed'),
            url(r'^upload_image/(?P<mix_id>\d+)/$', 'spa.ajax.upload_image', name='ajax_upload_image'),
            url(r'^upload_release_image/(?P<release_id>\d+)/$', 'spa.ajax.upload_release_image',
                name='ajax_upload_release_image'),
            url(r'^upload_avatar_image/$', 'spa.ajax.upload_avatar_image', name='ajax_upload_avatar_image'),
            url(r'^lookup/search/$', 'spa.ajax.lookup_search', name='ajax_lookup'),
            url(r'^lookup/(?P<source>\w+)/$', 'spa.ajax.lookup', name='ajax_lookup'),
        ]
        return pattern_list


def _get_json(payload, key='value'):
    data = {
        key: payload
    }
    return simplejson.dumps(data)


@render_to('inc/header.html')
def header(request):
    return HttpResponse(render_to_response('inc/header.html'))


def session_play_count(request):
    """

    :param request:
    :return: Number of tracks played in this session
    """
    if not request.user.is_authenticated():
        if 'play_count' in request.session:
            result = simplejson.dumps({
                'play_count': request.session['play_count']
            })
        else:
            result = simplejson.dumps({
                'play_count': '0'
            })
    else:
        result = simplejson.dumps({
            'play_count': '0'
        })
    return HttpResponse(result, mimetype='application/json')


def get_mix_stream_url(request, mix_id):
    try:
        if not request.user.is_authenticated():
            if 'play_count' in request.session:
                request.session['play_count'] += 1
            else:
                request.session['play_count'] = 1

        mix = Mix.objects.get(pk=mix_id)
        mix.add_play(request.user)
        data = {
            'stream_url': mix.get_stream_path(),
            'description': mix.description,
            'item_url': mix.get_absolute_url(),
            'title': mix.title
        }
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    except Exception, e:
        logger.exception("Error getting mix stream url")
        return HttpResponse("Error getting mix stream url", status=401)


def live_now_playing(request):
    now_playing_info = live.get_now_playing(
        localsettings.JS_SETTINGS['LIVE_STREAM_URL'],
        localsettings.JS_SETTINGS['LIVE_STREAM_PORT'],
        localsettings.JS_SETTINGS['LIVE_STREAM_MOUNT'])
    try:
        if now_playing_info is not None:
            return HttpResponse(
                simplejson.dumps({
                    'stream_url': 'http://%s:%s/%s' % (
                        localsettings.JS_SETTINGS['LIVE_STREAM_URL'],
                        localsettings.JS_SETTINGS['LIVE_STREAM_PORT'],
                        localsettings.JS_SETTINGS['LIVE_STREAM_MOUNT']),
                    'description': now_playing_info['stream_description'],
                    'title': now_playing_info['current_song']
                }), mimetype="application/json")
    except:
        return HttpResponseNotFound(now_playing_info)

    return None


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

        return HttpResponse(_get_json('Comment posted', 'description'))
    else:
        return HttpResponse(_get_json('Error posting', 'description'))


@render_to('inc/comment_list.html')
def mix_comments(request, mix_id):
    return {
        "results": Comment.objects.filter(mix_id=mix_id),
    }


@login_required
def mark_read(request):
    profile = request.user.get_profile()
    if profile is not None:
        Notification.objects.filter(to_user=profile).update(accepted_date=datetime.now())
        return HttpResponse('Success', status=200)
        pass

    return HttpResponse('Unauthorized', status=401)


@login_required()
def facebook_post_likes_allowed(request):
    profile = request.user.get_profile()
    if profile is not None:
        likes_allowed = profile.activity_sharing & UserProfile.ACTIVITY_SHARE_LIKES
        facebook_allowed = profile.activity_sharing_networks & UserProfile.ACTIVITY_SHARE_NETWORK_FACEBOOK

        return HttpResponse(_get_json(bool(likes_allowed & facebook_allowed)), mimetype="application/json")

    return HttpResponse(_get_json(False), mimetype="application/json")


@csrf_exempt
def upload_release_image(request, release_id):
    try:
        if 'release_image' in request.FILES and release_id is not None:
            release = Release.objects.get(pk=release_id)
            if release is not None:
                release.release_image = request.FILES['release_image']
                release.save()
                return HttpResponse(_get_json("Success"))
    except Exception, ex:
        logger.exception("Error uploading release image")
    return HttpResponse(_get_json("Failed"))


@csrf_exempt
def upload_image(request, mix_id):
    try:
        if 'mix_image' in request.FILES and mix_id is not None:
            mix = Mix.objects.get(pk=mix_id)
            if mix is not None:
                mix.mix_image = request.FILES['mix_image']
                mix.save()
                return HttpResponse(_get_json("Success"))
    except Exception, ex:
        logger.exception("Error uploading image")
    return HttpResponse(_get_json("Failed"))


@csrf_exempt
def upload_avatar_image(request):
    try:
        if 'avatar_image' in request.FILES:
            profile = request.user.get_profile()
            if profile:
                profile.avatar_image = request.FILES['avatar_image']
                profile.save()
                return HttpResponse(_get_json("Success"))
    except Exception, ex:
        logger.exception("Error uploading avatar")
    return HttpResponse(_get_json("Failed"))


@require_POST
@login_required
def upload(request):
    # The assumption here is that jQuery File Upload
    # has been configured to send files one at a time.
    # If multiple files can be uploaded simultaneously,
    # 'file' may be a list of files.
    try:
        uid = request.POST['upload-hash']
        in_file = upload_receive(request)
        fileName, extension = os.path.splitext(in_file.name)

        file_storage = FileSystemStorage(location=os.path.join(settings.CACHE_ROOT, "mixes"))
        cache_file = file_storage.save("%s%s" % (uid, extension), ContentFile(in_file.read()))

        try:
            mix = Mix.objects.get(uid=uid)
            mix.duration = mp3_length(mix.get_absolute_path())
            mix.save()
        except ObjectDoesNotExist:
            #Form hasn't been posted yet
            pass

        create_waveform_task.delay(in_file=os.path.join(file_storage.base_location, cache_file), mix_uid=uid)

        file_dict = {
            'size': in_file.size,
            'uid': uid
        }

        return UploadResponse(request, file_dict)
    except Exception, ex:
        logger.exception(ex.message)
        return HttpResponse(content="Error occurred uploading file", status=503)


@csrf_exempt
def lookup_search(request):
    query = request.GET['query'] if 'query' in request.GET else request.GET['q'] if 'q' in request.GET else ''
    if query != '':
        filter_field = Mix.get_lookup_filter_field()
        kwargs = {
            '{0}__{1}'.format(filter_field, 'icontains'): query,
        }
        rows = Mix.objects.values("title").filter(**kwargs)
        #results = serializers.serialize("json", rows, fields="title",)
        results = json.dumps(rows)
        return HttpResponse(results, mimetype='application/json')


@csrf_exempt
def lookup(request, source):
    query = request.GET['query'] if 'query' in request.GET else request.GET['q'] if 'q' in request.GET else ''
    if query != '':
        model = get_model('spa', source)
        if model is not None:
            filter_field = model.get_lookup_filter_field()
            kwargs = {
                '{0}__{1}'.format(filter_field, 'icontains'): query,
            }
            rows = model.objects.filter(**kwargs)
            results = json.to_ajax(rows, filter_field)
            return HttpResponse(simplejson.dumps(results), mimetype='application/json')
    return HttpResponse(_get_json("Key failure in lookup"), mimetype='application/json')
