from django.db import models
from spa.models._Activity import _Activity

class MixPlay(_Activity):
    mix = models.ForeignKey('spa.Mix', related_name='plays')

    def get_verb_passed(self):
        return "played"

    def get_object_singular(self):
        return "mix"

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()