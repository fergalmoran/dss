import os
import logging

from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import get_model
from django.http import HttpResponse
from annoying.decorators import render_to
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

from core.utils import live
from dss import localsettings, settings
from spa import social
from spa.models import UserProfile, mixfavourite, Release
from spa.models.mix import Mix
from spa.models.comment import Comment
from spa.models.mixlike import MixLike
from core.serialisers import json
from core.tasks import create_waveform_task


logger = logging.getLogger(__name__)


class AjaxHandler(object):
    # Get an instance of a logger

    def __init__(self, api_name="v1"):
        self.api_name = api_name

    @property
    def urls(self):
        pattern_list = [
            url(r'^mix-description/(?P<mix_id>\d+)/$', 'spa.ajax.get_mix_description', name='ajax_mix-description'),
            url(r'^mix/add_comment/$', 'spa.ajax.mix_add_comment', name='mix_add_comment'),
            url(r'^mix/comments/(?P<mix_id>\d+)/$', 'spa.ajax.mix_comments', name='ajax_mix_comments'),
            url(r'^header/$', 'spa.ajax.header', name='header'),
            url(r'^session_play_count/$', 'spa.ajax.session_play_count'),
            url(r'^mix_stream_url/(?P<mix_id>\d+)/$', 'spa.ajax.get_mix_stream_url'),
            url(r'^release_player/(?P<release_id>\d+)/$', 'spa.ajax.release_player'),
            url(r'^live_now_playing/$', 'spa.ajax.live_now_playing'),
            url(r'^like/$', 'spa.ajax.like', name='ajax_mix_like'),
            url(r'^favourite/$', 'spa.ajax.favourite', name='ajax_mix_favourite'),
            url(r'^toggle_follow/$', 'spa.ajax.toggle_follow', name='ajax_toggle_follow'),
            url(r'^facebook_post_likes_allowed/$', 'spa.ajax.facebook_post_likes_allowed',
                name='ajax_facebook_post_likes_allowed'),
            url(r'^upload_image/(?P<mix_id>\d+)/$', 'spa.ajax.upload_image', name='ajax_upload_image'),
            url(r'^upload_release_image/(?P<release_id>\d+)/$', 'spa.ajax.upload_release_image',
                name='ajax_upload_release_image'),
            url(r'^upload_avatar_image/$', 'spa.ajax.upload_avatar_image', name='ajax_upload_avatar_image'),
            url(r'^upload_mix_file_handler/$', 'spa.ajax.upload_mix_file_handler', name='ajax_upload_mix_file_handler'),
            url(r'^lookup/(?P<source>\w+)/$', 'spa.ajax.lookup', name='ajax_lookup'),
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
    return simplejson.dumps(data)


def get_mix_description(request, mix_id):
    return HttpResponse(_get_json('ArgleBargle'), mimetype="application/json")


@render_to('inc/header.html')
def header(request):
    return HttpResponse(render_to_response('inc/header.html'))


def session_play_count(request):
    if 'play_count' in request.session:
        result = simplejson.dumps({
            'play_count': request.session['play_count']
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
        data = {
            'stream_url': mix.get_stream_path(),
            'description': mix.description,
            'item_url': mix.get_absolute_url(),
            'title': mix.title
        }
        return HttpResponse(simplejson.dumps(data), mimetype="application/json")
    except Exception, e:
        logger.exception("Error getting mix stream url")


def live_now_playing(request):
    return HttpResponse(
        simplejson.dumps({
            'stream_url': "radio.deepsouthsounds.com",
            'description': 'Description',
            'title': live.get_now_playing(
                localsettings.JS_SETTINGS['LIVE_STREAM_URL'],
                localsettings.JS_SETTINGS['LIVE_STREAM_PORT'],
                localsettings.JS_SETTINGS['LIVE_STREAM_MOUNT'])
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

        return HttpResponse(_get_json('Comment posted', 'description'))
    else:
        return HttpResponse(_get_json('Error posting', 'description'))


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
                mix = Mix.objects.get(pk=request.POST['dataId'])
                if mix is not None:
                    if mix.likes.count() == 0:
                        uid = social.post_like(request, mix)
                        mix.likes.add(MixLike(mix=mix, user=request.user, uid=uid))
                        response = _get_json('Liked')
                    else:
                        for like in mix.likes.all():
                            uid = like.uid
                            if uid is not None and uid <> '':
                                social.delete_like(request, uid)

                        mix.likes.all().delete()
                        response = _get_json('Unliked')
                    mix.save()
                    return HttpResponse(response)


@login_required()
def toggle_follow(request):
    response = _get_json('Invalid request')
    try:
        if request.is_ajax() and request.method == 'POST' and 'userId' in request.POST:
            profile = request.user.get_profile()
            following = UserProfile.objects.get(user__id=request.POST['userId'])
            if following is not None:
                if profile.followers is None or (following not in profile.followers.all()):
                    profile.add_follower(following)
                    response = _get_json('Followed')
                else:
                    profile.followers.remove(following)
                    response = _get_json('Unfollowed')
                profile.save()
    except Exception, ex:
        if settings.DEBUG:
            response = _get_json(ex.message)
        else:
            response = _get_json('Error')

    return HttpResponse(response)

@login_required()
def favourite(request):
    if request.is_ajax():
        if request.method == 'POST':
            if request.POST['dataMode'] == 'mix':
                mix = Mix.objects.get(pk=request.POST['dataId'])
                if mix is not None:
                    if mix.favourites.count() == 0:
                        mix.favourites.add(mixfavourite(mix=mix, user=request.user))
                        response = _get_json('Favourited')
                    else:
                        mix.favourites.all().delete()
                        response = _get_json('Unfavourited')
                    mix.save()
                    return HttpResponse(response)


@login_required()
def facebook_post_likes_allowed(request):
    profile = request.user.get_profile();
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


@csrf_exempt
def upload_mix_file_handler(request):
    try:
        if 'Filedata' in request.FILES and 'upload-hash' in request.POST:
            f = request.FILES['Filedata']
            fileName, extension = os.path.splitext(f.name)
            uid = request.POST['upload-hash']
            in_file = os.path.join(settings.CACHE_ROOT, "mixes", "%s%s" % (uid, extension))
            with open(in_file, 'wb+') as destination:
                for chunk in f.chunks():
                    destination.write(chunk)
            try:
                create_waveform_task.delay(in_file=in_file, mix_uid=uid)
            except Exception, ex:
                logger.exception("Error starting waveform generation task: %s" % ex.message)
        return HttpResponse(_get_json("Success"), mimetype='application/json')
    except Exception, ex:
        logger.exception("Error uploading mix")
    return HttpResponse(_get_json("Failed"), mimetype='application/json')


@csrf_exempt
def lookup(request, source):
    query = request.GET['query'] if 'query' in request.GET else request.GET['q'] if 'q' in request.GET else ''
    if query <> '':
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
