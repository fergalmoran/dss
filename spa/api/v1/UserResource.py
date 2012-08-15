from django.conf.urls import url
from tastypie.authorization import Authorization
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import UserProfile

class UserResource(BackboneCompatibleResource):
    class Meta:
        queryset = UserProfile.objects.all()
        authorization = Authorization()

    def dehydrate(self, bundle):
        bundle.data['display_name'] = bundle.obj.display_name
        bundle.data['first_name'] = bundle.obj.first_name
        bundle.data['last_name'] = bundle.obj.last_name
        bundle.data['email'] = bundle.obj.email
        return bundle

    def override_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<username>[\w\d_.-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            ]