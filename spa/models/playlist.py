from django.db import models
from spa.models import BaseModel, UserProfile, Mix


class Playlist(BaseModel):
    name = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(UserProfile, related_name='playlists')
    mixes = models.ManyToManyField(Mix)
    public = models.BooleanField(default=True)