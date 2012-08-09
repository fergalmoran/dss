from tastypie import fields
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import ReleaseAudio

class ReleaseAudioResource(BackboneCompatibleResource):
    release = fields.ToOneField('spa.api.v1.ReleaseResource.ReleaseResource', 'release')

    class Meta:
        queryset = ReleaseAudio.objects.all()
        resource_name = 'audio'
        filtering = {
            "release": ('exact',),
            }

    def dehydrate(self, bundle):
        bundle.data['waveform_url'] = bundle.obj.get_waveform_url()
        return bundle