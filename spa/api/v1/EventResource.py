import humanize
from tastypie.authorization import Authorization
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models.Event import  Event

class EventResource(BackboneCompatibleResource):
    class Meta:
        queryset = Event.objects.all()
        authorization = Authorization()

    def dehydrate(self, bundle):
        bundle.data['item_url'] = 'event/%s' % bundle.obj.id
        bundle.data['event_venue'] = bundle.obj.event_venue.venue_name
        return bundle

    def dehydrate_event_date(self, bundle):
        return humanize.naturalday(bundle.obj.event_date)