from django.conf.urls import url
from tastypie import fields
from tastypie.resources import ModelResource

__author__ = 'fergalm'

class BackboneCompatibleResource(ModelResource):
    def override_urls(self):
        urls = []
        for name, field in self.fields.items():
            if isinstance(field, fields.ToManyField):
                resource = r"^(?P<resource_name>{resource_name})/(?P<{related_name}>.+)/{related_resource}/$".format(
                    resource_name=self._meta.resource_name,
                    related_name=field.related_name,
                    related_resource=field.attribute,
                )
                resource = url(resource, field.to_class().wrap_view('get_list'), name="api_dispatch_detail")
                urls.append(resource)
        return urls