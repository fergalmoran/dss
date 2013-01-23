from django.db import models
from spa.models._Activity import _Activity

class MixDownload(_Activity):
    mix = models.ForeignKey('spa.Mix', related_name='downloads')

    def get_verb_passed(self):
        return "downloaded"

    def get_object_singular(self):
        return "mix"
