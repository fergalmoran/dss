from django.db.models import Count
from django.conf.urls import url
from tastypie.authentication import SessionAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpUnauthorized
from tastypie.utils import trailing_slash
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import Playlist, Mix, UserProfile


class PlaylistResource(BackboneCompatibleResource):
    user = fields.ToOneField('spa.api.v1.UserResource.UserResource', 'user')
    mixes = fields.ManyToManyField('spa.api.v1.MixResource.MixResource', 'mixes', full=True, null=True)

    class Meta:
        queryset = Playlist.objects.all().annotate(mix_count=Count('mixes')).order_by('-mix_count')
        always_return_data = True

        excludes = ['public']

        authentication = Authentication()
        authorization = DjangoAuthorization()

    def authorized_read_list(self, object_list, bundle):
        if bundle.request.user.is_authenticated():
            return object_list.filter(user=bundle.request.user)

        raise ImmediateHttpResponse(
            HttpUnauthorized("Git tae fuck")
        )

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<id>[\d]+)%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d-]+)%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
        ]

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user.get_profile()
        return bundle

    def dehydrate(self, bundle):
        try:
            bundle.data['playlist_image'] = bundle.obj.mixes.objects.all()[0].get_image_url()
        except:
            bundle.data['playlist_image'] = UserProfile.get_default_avatar_image()

        bundle.data['item_url'] = '/playlist/%s' % bundle.obj.slug
        return bundle

    def obj_update(self, bundle, skip_errors=False, **kwargs):
        mixes = bundle.data['mixes']
        bundle.data.pop('mixes')
        result = super(PlaylistResource, self).obj_update(bundle, **kwargs)
        if mixes:
            for mix_item in mixes:
                result.obj.mixes.add(Mix.objects.get(pk=mix_item['id']))

        result.obj.save()

        return result

    def obj_create(self, bundle, **kwargs):
        mixes = bundle.data['mixes']
        bundle.data.pop('mixes')
        result = super(PlaylistResource, self).obj_create(bundle, **kwargs)

        if mixes:
            for mix_item in mixes:
                result.obj.mixes.add(Mix.objects.get(pk=mix_item['id']))

        result.obj.save()

        return result
