from spa.models import _BaseModel, UserProfile, Mix
from django.db import models

class UserFavourite(_BaseModel):
    mix = models.ForeignKey(Mix, related_name='favourite_mix')
    user = models.ForeignKey(UserProfile, related_name='favourite_user')
    date = models.DateTimeField(auto_now=True)