from django.db import models
from spa.models.Mix import Mix
from spa.models._Activity import _Activity

class MixLike(_Activity):
    class Meta:
        app_label = 'spa'

    mix = models.ForeignKey(Mix, related_name='likes')