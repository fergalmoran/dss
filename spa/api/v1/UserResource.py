from django.conf.urls import url
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import UserProfile

class UserResource(BackboneCompatibleResource):
    class Meta:
        queryset = UserProfile.objects.all()
        excludes = []
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

        if bundle.obj.activity_sharing is not None:
            bundle.data['activity_share_likes'] = (bundle.obj.activity_sharing & UserProfile.ACTIVITY_SHARE_LIKES) != 0;
            bundle.data['activity_share_favourites'] = (bundle.obj.activity_sharing & UserProfile.ACTIVITY_SHARE_FAVOURITES) != 0;
            bundle.data['activity_share_comments'] = (bundle.obj.activity_sharing & UserProfile.ACTIVITY_SHARE_COMMENTS) != 0;
        else:
            bundle.data['activity_share_likes'] =0
            bundle.data['activity_share_favourites'] =0
            bundle.data['activity_share_comments'] =0

        if bundle.obj.activity_sharing_networks is not None:
            bundle.data['activity_share_networks_facebook'] = (bundle.obj.activity_sharing_networks & UserProfile.ACTIVITY_SHARE_NETWORK_FACEBOOK) != 0;
            bundle.data['activity_share_networks_twitter'] = (bundle.obj.activity_sharing_networks& UserProfile.ACTIVITY_SHARE_NETWORK_TWITTER) != 0;
        else:
            bundle.data['activity_share_networks_facebook'] = 0
            bundle.data['activity_share_networks_facebook'] = 0
        return bundle

    def apply_authorization_limits(self, request, object_list):
        if request.user is not None:
            return object_list.filter(user=request.user)

    def hydrate_profile_slug(self, bundle):
        if bundle.data['profile_slug'] == '':
            bundle.data['profile_slug'] = None
        return bundle

