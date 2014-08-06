from datetime import datetime
from django.contrib.auth.models import User
from django.db import models
from spa.models import Recurrence
from spa.models.venue import Venue

"""
class Event(views.Model):
    class Meta:
        app_label = 'spa'

    event_venue = views.ForeignKey(Venue)

    event_date = views.DateField(default=datetime.now())
    event_time = views.TimeField(default=datetime.now())

    date_created = views.DateField(default=datetime.now())
    event_title = views.CharField(max_length=250)
    event_description = views.TextField()
    event_recurrence = views.ForeignKey(Recurrence)

    attendees = views.ManyToManyField(User, related_name='attendees')

    def get_absolute_url(self):
        return '/event/%i' % self.id

    def __unicode__(self):
        return self.event_title
"""
