from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from tastypie import fields
from tastypie.http import HttpGone, HttpMultipleChoices
from tastypie.resources import ModelResource
from tastypie.utils import trailing_slash


class BackboneCompatibleResource(ModelResource):
    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/children%s$" %
                (self._meta.resource_name, trailing_slash()), self.wrap_view('get_children'), name="api_get_children"),
        ]
