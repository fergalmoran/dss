from django.conf.urls import url
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import UserProfile

class UserResource(BackboneCompatibleResource):
    class Meta:
        queryset = UserProfile.objects.all()
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True
        filtering = {
            'user': ALL_WITH_RELATIONS,
            }

    def dehydrate(self, bundle):
        bundle.data['display_name'] = bundle.obj.display_name
        bundle.data['first_name'] = bundle.obj.first_name
        bundle.data['last_name'] = bundle.obj.last_name
        bundle.data['email'] = bundle.obj.email
        return bundle

    def apply_authorization_limits(self, request, object_list):
        if request.user is not None:
            return object_list.filter(user=request.user)