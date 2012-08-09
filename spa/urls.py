from django.conf.urls import patterns, url, include
import django.conf.urls
from tastypie.api import Api
from spa.ajax import AjaxHandler
from spa.api.v1.CommentResource import CommentResource
from spa.api.v1.MixResource import MixResource
from spa.api.v1.ReleaseAudioResource import ReleaseAudioResource
from spa.api.v1.ReleaseResource import ReleaseResource
import spa

v1_api = Api(api_name='v1')
v1_api.register(MixResource())
v1_api.register(CommentResource())
v1_api.register(ReleaseResource())
v1_api.register(ReleaseAudioResource())

ajax = AjaxHandler()

urlpatterns = django.conf.urls.patterns(
    '',
    url(r'^$', 'spa.views.app', name='home'),
    url(r'^tpl/(?P<template_name>\w+)/$', 'spa.templates.get_template'),
    (r'^ajax/', include(ajax.urls)),
    (r'^api/', include(v1_api.urls)),
)