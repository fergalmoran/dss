from django.conf.urls import patterns, url, include
import django.conf.urls
from tastypie.api import Api
from spa.ajax import AjaxHandler
from spa.audio import AudioHandler

from spa.api.v1.CommentResource import CommentResource
from spa.api.v1.EventResource import EventResource
from spa.api.v1.MixResource import MixResource
from spa.api.v1.ReleaseAudioResource import ReleaseAudioResource
from spa.api.v1.ReleaseResource import ReleaseResource
from spa.api.v1.UserResource import UserResource
from spa.social import SocialHandler

v1_api = Api(api_name='v1')
v1_api.register(MixResource())
v1_api.register(CommentResource())
v1_api.register(ReleaseResource())
v1_api.register(ReleaseAudioResource())
v1_api.register(EventResource())
v1_api.register(UserResource())
ajax = AjaxHandler()
audio = AudioHandler()
social = SocialHandler()

urlpatterns = django.conf.urls.patterns(
    '',
    url(r'^$', 'spa.views.app', name='home'),
    url(r'^upload', 'spa.views.app', name='home'),
    url(r'^tpl/(?P<template_name>\w+)/$', 'spa.templates.get_template'),
    url(r'^js/(?P<template_name>\w+)/$', 'spa.templates.get_javascript'),
    url(r'^tplex/(?P<template_name>\w+)/$', 'spa.templates.get_template_ex'),
    (r'^social/', include(social.urls)),
    (r'^ajax/', include(ajax.urls)),
    (r'^audio/', include(audio.urls)),
    (r'^api/', include(v1_api.urls)),
    (r'^.*/$', 'spa.views.default')
)