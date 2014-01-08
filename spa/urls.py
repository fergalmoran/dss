from django.conf.urls import patterns, url, include
from tastypie.api import Api
from spa.ajax import AjaxHandler
from spa.api.v1.DebugResource import DebugResource
from spa.api.v1.NotificationResource import NotificationResource
from spa.audio import AudioHandler
from spa.api.v1.ChatResource import ChatResource
from spa.api.v1.CommentResource import CommentResource
from spa.api.v1.EventResource import EventResource
from spa.api.v1.MixResource import MixResource
from spa.api.v1.ReleaseAudioResource import ReleaseAudioResource
from spa.api.v1.ReleaseResource import ReleaseResource
from spa.api.v1.UserResource import UserResource
from spa.api.v1.ActivityResource import ActivityResource

api = Api(api_name='v1')
api.register(ChatResource())
api.register(CommentResource())
api.register(MixResource())
api.register(ReleaseResource())
api.register(ReleaseAudioResource())
api.register(EventResource())
api.register(UserResource())
api.register(ActivityResource())
api.register(NotificationResource())
api.register(DebugResource())

ajax = AjaxHandler()
audio = AudioHandler()

urlpatterns = patterns(
    '',
    url(r'^$', 'spa.views.app', name='home'),
    url(r'^tpl/(?P<template_name>\w+)/$', 'spa.templates.get_template'),
    url(r'^dlg/(?P<dialog_name>\w+)/$', 'spa.templates.get_dialog'),
    url(r'^dlg/embed/(?P<slug>[\w\d_.-]+)/$', 'spa.templates.get_embed_codes_dialog'),

    url(r'^js/(?P<template_name>\w+)/$', 'spa.templates.get_javascript'),
    url(r'^tplex/(?P<template_name>\w+)/$', 'spa.templates.get_template_ex'),
    url(r'^podcast', 'spa.podcast.get_default_podcast'),
    url(r'^podcast\.xml', 'spa.podcast.get_default_podcast'),
    url(r'^social/', include('spa.social.urls')),
    url(r'^embed/', include('spa.embedding.urls')),
    url(r'_upload/', 'spa.ajax.upload', name='mix_upload'),
    url(r'^ajax/', include(ajax.urls)),
    url(r'^audio/', include(audio.urls)),
    url(r'^api/', include(api.urls)),
    url(r'^comments/', include('django.contrib.comments.urls')),
    (r'^.*/$', 'spa.views.default')
)


