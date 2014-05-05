from django.db.models import Q
from schedule.models import Event

class ShowOverlapException(Exception):
    pass

class Show(Event):
    class Meta:
        app_label = 'spa'

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
            throw an exception if event overlaps with another event
        """
        import ipdb; ipdb.set_trace()
        overlaps = Show.objects.filter(
            Q(start__gte=self.start, end__lte=self.start) |
            Q(start__gte=self.end, end__lte=self.end)
        )
        if len(overlaps) != 0:
            raise ShowOverlapException()

        return super(Show, self).save(force_insert, force_update, using, update_fields)
