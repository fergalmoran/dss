from spa.models import _BaseModel, Mix
from django.db import models

class Tracklist(_BaseModel):
    mix = models.ForeignKey(Mix, related_name='tracklist')
    index = models.SmallIntegerField()
    timeindex = models.TimeField(null=True)
    description = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    remixer = models.CharField(max_length=255)
    label = models.CharField(max_length=255)
