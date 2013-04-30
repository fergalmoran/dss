from django.db import models
from spa.models.activity import _Activity

class MixDownload(_Activity):
    mix = models.ForeignKey('spa.Mix', related_name='downloads')

    def get_verb_passed(self):
        return "downloaded"

    def get_object_singular(self):
        return "mix"

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()