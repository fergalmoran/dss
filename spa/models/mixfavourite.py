from spa.models.userprofile import UserProfile
from spa.models._basemodel import _BaseModel
from django.db import models


class MixFavourite(_BaseModel):
    mix = models.ForeignKey('spa.Mix', related_name='favourites')
    user = models.ForeignKey(UserProfile, related_name='favourites')
    date = models.DateTimeField(auto_now=True)

