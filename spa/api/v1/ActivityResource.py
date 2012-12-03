from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from  spa.models._Activity import _Activity


class ActivityResource(BackboneCompatibleResource):

    class Meta:
        queryset = _Activity.objects.all()
        resource_name = 'activity'
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True

    def dehydrate(self, bundle):

        return bundle