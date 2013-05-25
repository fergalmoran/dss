from django.contrib.auth.models import User
from django.db import models
from spa.models._basemodel import _BaseModel


class MixLike(_BaseModel):
    mix = models.ForeignKey('spa.Mix', related_name='likes')
    user = models.ForeignKey(User, related_name='likes')
    date = models.DateTimeField(auto_now=True)
