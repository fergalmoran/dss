from django.db.models import Count
from tastypie.authentication import SessionAuthentication, Authentication
from tastypie.authorization import DjangoAuthorization, Authorization
from tastypie import fields
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpUnauthorized
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import Playlist, Mix


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

    def hydrate(self, bundle):
        bundle.obj.user = bundle.request.user.get_profile()
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
