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
from spa.models.activity import ActivityFollow
from spa.models.userprofile import UserProfile
from spa.models.mix import Mix


class UserResource(BackboneCompatibleResource):
    class Meta:
        queryset = UserProfile.objects.all().annotate(mix_count=Count('mixes')).order_by('-mix_count')
        resource_name = 'user'
        excludes = ['is_active', 'is_staff', 'is_superuser', 'password']
        ordering = ['mix_count']
        authorization = DjangoAuthorization()
        authentication = Authentication()
        favourites = fields.ToManyField(MixResource, 'favourites')

    def _hydrateBitmapOption(self, source, comparator):
        return True if (source & comparator) != 0 else False

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d_.-]+)/favourites%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_user_favourites'), name="api_get_user_favourites"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d_.-]+)/activity%s$" % (
                self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_user_activity'), name="api_get_user_activity"),
            url(r"^(?P<resource_name>%s)/(?P<pk>\d+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d_.-]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    """
    Stub method, not actually needed just yet
    but take heed of note below when implementing in the future
        def apply_sorting(self, obj_list, options=None):
            #apply the sort to the obj_list, not the super call
    """

    def apply_filters(self, request, applicable_filters):
        semi_filtered = super(UserResource, self).apply_filters(request, applicable_filters)
        q = request.GET.get('q', None)
        if q is not None:
            semi_filtered = semi_filtered.filter(
                Q(user__first_name__icontains=q) |
                Q(user__last_name__icontains=q) |
                Q(display_name__icontains=q)
            )

        return semi_filtered

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

    def _patch_resource(self, bundle):
        #Handle the patched items from backbone
        if bundle.data['following']:
            bundle.obj.add_follower(bundle.request.user.get_profile())
            activity = ActivityFollow()
            activity.user = bundle.request.user.get_profile()
            activity.to_user = bundle.obj
            activity.save()
        else:
            bundle.obj.remove_follower(bundle.request.user.get_profile())

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

        self._patch_resource(bundle)

        return super(UserResource, self).obj_update(bundle, skip_errors, **kwargs)

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
        bundle.data['date_joined'] = bundle.obj.user.date_joined
        bundle.data['last_login'] = bundle.obj.user.last_login
        bundle.data['mix_count'] = bundle.obj.mix_count

        return bundle

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
