from django.db import models
from spa.models._Activity import _Activity

class MixPlay(_Activity):
    mix = models.ForeignKey('spa.Mix', related_name='plays')