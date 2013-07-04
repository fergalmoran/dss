from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db.models import Count, Q
from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import DjangoAuthorization
from django.conf.urls import url
from tastypie.http import HttpMultipleChoices, HttpGone
from tastypie.utils import trailing_slash

from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.api.v1.MixResource import MixResource
from spa.models.userprofile import UserProfile
from spa.models.mix import Mix


class UserProfileResource(BackboneCompatibleResource):
    mix_count = fields.IntegerField(readonly=True)

    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'profile'
        include_resource_uri = False
        include_absolute_url = False
        always_return_data = True
        authorization = DjangoAuthorization()
        authentication = Authentication()

    def get_object_list(self, request):
        return super(UserProfileResource, self).get_object_list(request).annotate(mix_count=Count('mixes'))

    def _hydrateBitmapOption(self, source, comparator):
        return True if (source & comparator) != 0 else False

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
            facebook = UserProfile.ACTIVITY_SHARE_NETWORK_FACEBOOK if bundle.data[
                'activity_sharing_networks_facebook'] else 0
            twitter = UserProfile.ACTIVITY_SHARE_NETWORK_TWITTER if bundle.data[
                'activity_sharing_networks_twitter'] else 0
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
        bundle.data['display_name'] = bundle.obj.get_nice_name()
        bundle.data['avatar_image'] = bundle.obj.get_avatar_image()
        if bundle.obj.user.id == bundle.request.user.id:
            bundle.data['activity_sharing_likes'] = \
                self._hydrateBitmapOption(bundle.obj.activity_sharing, UserProfile.ACTIVITY_SHARE_LIKES)
            bundle.data['activity_sharing_favourites'] = \
                self._hydrateBitmapOption(bundle.obj.activity_sharing, UserProfile.ACTIVITY_SHARE_FAVOURITES)
            bundle.data['activity_sharing_comments'] = \
                self._hydrateBitmapOption(bundle.obj.activity_sharing, UserProfile.ACTIVITY_SHARE_COMMENTS)

            bundle.data['activity_sharing_networks_facebook'] = \
                self._hydrateBitmapOption(bundle.obj.activity_sharing_networks,
                                          UserProfile.ACTIVITY_SHARE_NETWORK_FACEBOOK)
            bundle.data['activity_sharing_networks_twitter'] = \
                self._hydrateBitmapOption(bundle.obj.activity_sharing_networks,
                                          UserProfile.ACTIVITY_SHARE_NETWORK_TWITTER)

        bundle.data['like_count'] = Mix.objects.filter(likes__user=bundle.obj).count()
        bundle.data['favourite_count'] = Mix.objects.filter(favourites__user=bundle.obj).count()
        bundle.data['follower_count'] = bundle.obj.followers.count()
        bundle.data['following_count'] = bundle.obj.following.count()
        bundle.data['following'] = bundle.obj.is_follower(bundle.request.user)
        bundle.data['url'] = bundle.obj.get_profile_url()
        return bundle

    def dehydrate_mix_count(self, bundle):
        return bundle.obj.mixes.count()


class UserResource(BackboneCompatibleResource):
    profile = fields.ToOneField(UserProfileResource, attribute='userprofile', related_name='user', full=True)

    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['is_active', 'is_staff', 'is_superuser', 'password']
        ordering = ['mix_count']
        authorization = DjangoAuthorization()
        authentication = Authentication()
        favourites = fields.ToManyField(MixResource, 'favourites')

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<userprofile__slug>[\w\d_.-]+)/favourites%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_user_favourites'), name="api_get_user_favourites"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<userprofile__slug>[\w\d_.-]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def apply_filters(self, request, applicable_filters):
        semi_filtered = super(UserResource, self).apply_filters(request, applicable_filters)
        q = request.GET.get('q', None)
        if q is not None:
            semi_filtered = semi_filtered.filter(
                Q(first_name__icontains=q) |
                Q(last_name__icontains=q)
            )

        return semi_filtered

    def apply_sorting(self, obj_list, options=None):
        return super(UserResource, self).apply_sorting(obj_list, options)

    def get_object_list(self, request):
        return super(UserResource, self).get_object_list(request)

    def get_user_favourites(self, request, **kwargs):
        try:
            obj = self.cached_obj_get(bundle=self.build_bundle(request=request),
                                      **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()
        except MultipleObjectsReturned:
            return HttpMultipleChoices("More than one resource is found at this URI.")

        mixes = MixResource()
        return mixes.get_list(request, favourites__user=obj.get_profile())

    def dehydrate(self, bundle):
        if bundle.obj.id != bundle.request.user.id:
            del bundle.data['email']
            del bundle.data['username']
        return bundle

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        #Handle the patched items from backbone
        if bundle.data['following']:
            bundle.obj.get_profile().add_follower(bundle.request.user.get_profile())
        else:
            bundle.obj.get_profile().remove_follower(bundle.request.user.get_profile())

        return super(UserResource, self).obj_update(bundle, skip_errors, **kwargs)
