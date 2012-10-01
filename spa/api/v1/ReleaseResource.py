import datetime
import humanize
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import Label
from spa.models.Release import Release
from django.core.exceptions import ObjectDoesNotExist
class ReleaseResource(BackboneCompatibleResource):
    release_audio = fields.ToManyField('spa.api.v1.ReleaseAudioResource.ReleaseAudioResource', 'release_audio', 'release', null=True, blank=True)
    class Meta:
        queryset = Release.objects.filter(release_date__gte=datetime.date.today() - datetime.timedelta(days=7))
        filtering = {
            'release_audio' : ALL_WITH_RELATIONS
        }
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):
        bundle.data['user'] = {'pk': request.user.pk}
        return super(ReleaseResource, self).obj_create(bundle, request, user=request.user.get_profile())

    def hydrate(self, bundle):
        if 'release_label' in bundle.data:
            try:
                label = Label.objects.get(name__exact=bundle.data['release_label'])
            except ObjectDoesNotExist:
                label = Label(name=bundle.data['release_label'])
                label.save()

            bundle.obj.release_label = label
        return bundle

    def dehydrate(self, bundle):
        bundle.data['release_label'] = bundle.obj.release_label.name
        bundle.data['item_url'] = 'release/%s' % bundle.obj.id
        bundle.data['mode'] = 'release'
        return bundle

    def dehydrate_release_date(self, bundle):
        return humanize.naturalday(bundle.obj.release_date)