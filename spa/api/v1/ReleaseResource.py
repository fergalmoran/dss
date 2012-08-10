import datetime
import humanize
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import Release

class ReleaseResource(BackboneCompatibleResource):
    release_audio = fields.ToManyField('spa.api.v1.ReleaseAudioResource.ReleaseAudioResource', 'release_audio', 'release')
    class Meta:
        queryset = Release.objects.all()
        filtering = {
            'release_audio' : ALL_WITH_RELATIONS
        }
        authorization = Authorization()

    def dehydrate(self, bundle):
        bundle.data['label'] = bundle.obj.release_label.name
        bundle.data['item_url'] = 'release/%s' % bundle.obj.id
        bundle.data['mode'] = 'release'
        return bundle

    def dehydrate_release_date(self, bundle):
        return humanize.naturalday(bundle.obj.release_date)