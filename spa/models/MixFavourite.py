from spa.models import _BaseModel, UserProfile, Mix, _Activity
from django.db import models

class MixFavourite(_Activity):
    mix = models.ForeignKey(Mix, related_name='favourites')
