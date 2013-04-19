from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.constants import ALL, ALL_WITH_RELATIONS
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
            'username': ALL,
            'id': ALL,
        }

    def full_dehydrate(self, bundle, for_list=False):
        return super(UserResource, self).full_dehydrate(bundle, for_list)

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(user_id=bundle.request.user.id)

    def dehydrate(self, bundle):
        bundle.data['display_name'] = bundle.obj.display_name
        bundle.data['first_name'] = bundle.obj.first_name
        bundle.data['last_name'] = bundle.obj.last_name
        bundle.data['email'] = bundle.obj.email

        if bundle.obj.activity_sharing is not None:
            bundle.data['activity_share_likes'] = \
                (bundle.obj.activity_sharing & UserProfile.ACTIVITY_SHARE_LIKES) != 0
            bundle.data['activity_share_favourites'] = \
                (bundle.obj.activity_sharing & UserProfile.ACTIVITY_SHARE_FAVOURITES) != 0
            bundle.data['activity_share_comments'] = \
                (bundle.obj.activity_sharing & UserProfile.ACTIVITY_SHARE_COMMENTS) != 0
        else:
            bundle.data['activity_share_likes'] = 0
            bundle.data['activity_share_favourites'] = 0
            bundle.data['activity_share_comments'] = 0

        if bundle.obj.activity_sharing_networks is not None:
            bundle.data['activity_share_networks_facebook'] = \
                (bundle.obj.activity_sharing_networks & UserProfile.ACTIVITY_SHARE_NETWORK_FACEBOOK) != 0
            bundle.data['activity_share_networks_twitter'] = \
                (bundle.obj.activity_sharing_networks & UserProfile.ACTIVITY_SHARE_NETWORK_TWITTER) != 0
        else:
            bundle.data['activity_share_networks_facebook'] = 0
            bundle.data['activity_share_networks_facebook'] = 0

        return bundle

    def hydrate_slug(self, bundle):
        if bundle.data['slug'] == '':
            bundle.data['slug'] = None
        return bundle

