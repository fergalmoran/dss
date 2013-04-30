from spa.models import _BaseModel, UserProfile, Mix, _Activity
from django.db import models

class MixFavourite(_Activity):
    mix = models.ForeignKey(Mix, related_name='favourites')

    def get_verb_passed(self):
        return "favourited"

    def get_object_singular(self):
        return "mix"

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()