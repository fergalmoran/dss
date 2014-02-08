from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from spa.models import Recurrence
from spa.models.venue import Venue


class Event(models.Model):
    class Meta:
        app_label = 'spa'

    event_venue = models.ForeignKey(Venue)

    event_date = models.DateField(default=datetime.now())
    event_time = models.TimeField(default=datetime.now())

    date_created = models.DateField(default=datetime.now())
    event_title = models.CharField(max_length=250)
    event_description = models.TextField()
    event_recurrence = models.ForeignKey(Recurrence)

    attendees = models.ManyToManyField(User, related_name='attendees')

    def get_absolute_url(self):
        return '/event/%i' % self.id

    def __unicode__(self):
        return self.event_title