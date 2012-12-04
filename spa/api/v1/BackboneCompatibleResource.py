from django.conf.urls import url
from tastypie import fields
from tastypie.resources import ModelResource


class BackboneCompatibleResource(ModelResource):
    pass