from django.contrib.auth.models import User
from spa.models._basemodel import _BaseModel
from django.db import models


class MixFavourite(_BaseModel):
    mix = models.ForeignKey('spa.Mix', related_name='favourites')
    user = models.ForeignKey(User, related_name='favourites')
    date = models.DateTimeField(auto_now=True)

