from django.contrib.auth.models import User
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import UserProfile


class UserProfileResource(BackboneCompatibleResource):
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'profile'
        include_resource_uri = False
        include_absolute_url = False
        always_return_data = True
        authorization = DjangoAuthorization()
        authentication = Authentication()

    def _hydrateBitmapOption(self, source, comparator):
        return "checked" if (source & comparator) != 0 else ""


    def hydrate(self, bundle):
        if 'activity_sharing_likes' in bundle.data:
            likes = UserProfile.ACTIVITY_SHARE_LIKES if bundle.data['activity_sharing_likes'] else 0
            favourites = UserProfile.ACTIVITY_SHARE_FAVOURITES if bundle.data['activity_sharing_favourites'] else 0
            comments = UserProfile.ACTIVITY_SHARE_COMMENTS if bundle.data['activity_sharing_comments'] else 0
            bundle.data['activity_sharing'] = (likes | favourites | comments)
            del bundle.data['activity_sharing_likes']
            del bundle.data['activity_sharing_favourites']
            del bundle.data['activity_sharing_comments']

        if 'activity_sharing_networks_facebook' in bundle.data:
            facebook = UserProfile.ACTIVITY_SHARE_NETWORK_FACEBOOK if bundle.data['activity_sharing_networks_facebook'] else 0
            twitter = UserProfile.ACTIVITY_SHARE_NETWORK_TWITTER if bundle.data['activity_sharing_networks_twitter'] else 0
            bundle.data['activity_sharing_networks'] = (facebook | twitter)
            del bundle.data['activity_sharing_networks_facebook']
            del bundle.data['activity_sharing_networks_twitter']

        return bundle

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        """
            This feels extremely hacky - but for some reason, deleting from the bundle
            in hydrate is not preventing the fields from being serialized at the ORM
        """
        if 'activity_sharing_networks_facebook' in kwargs: del kwargs['activity_sharing_networks_facebook']
        if 'activity_sharing_networks_twitter' in kwargs: del kwargs['activity_sharing_networks_twitter']
        if 'activity_sharing_likes' in kwargs: del kwargs['activity_sharing_likes']
        if 'activity_sharing_favourites' in kwargs: del kwargs['activity_sharing_favourites']
        if 'activity_sharing_comments' in kwargs: del kwargs['activity_sharing_comments']

        return super(UserProfileResource, self).obj_update(bundle, skip_errors, **kwargs)

    def dehydrate(self, bundle):
        del bundle.data['activity_sharing']
        del bundle.data['activity_sharing_networks']
        if bundle.obj.user.id == bundle.request.user.id:
            bundle.data['activity_sharing_likes'] = \
                self._hydrateBitmapOption(bundle.obj.activity_sharing, UserProfile.ACTIVITY_SHARE_LIKES)
            bundle.data['activity_sharing_favourites'] = \
                self._hydrateBitmapOption(bundle.obj.activity_sharing, UserProfile.ACTIVITY_SHARE_FAVOURITES)
            bundle.data['activity_sharing_comments'] = \
                self._hydrateBitmapOption(bundle.obj.activity_sharing, UserProfile.ACTIVITY_SHARE_COMMENTS)

            bundle.data['activity_sharing_networks_facebook'] = \
                self._hydrateBitmapOption(bundle.obj.activity_sharing_networks, UserProfile.ACTIVITY_SHARE_NETWORK_FACEBOOK)
            bundle.data['activity_sharing_networks_twitter'] = \
                self._hydrateBitmapOption(bundle.obj.activity_sharing_networks, UserProfile.ACTIVITY_SHARE_NETWORK_TWITTER)

        return bundle

class UserResource(BackboneCompatibleResource):
    profile = fields.ToOneField(UserProfileResource, attribute='userprofile', related_name='user', full=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['is_active', 'is_staff', 'is_superuser', 'password']
        authorization = DjangoAuthorization()
        authentication = Authentication()

    def dehydrate(self, bundle):
        if bundle.obj.id != bundle.request.user.id:
            del bundle.data['email']
            del bundle.data['username']

        return bundle
