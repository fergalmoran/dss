from django.db import models
from spa.models.activity import _Activity

class MixLike(_Activity):
    mix = models.ForeignKey('spa.Mix', related_name='likes')

    def __unicode__(self):
        return "%s on %s" % (self.user.get_full_name(), self.mix.title)

    def get_verb_passed(self):
        return "liked"

    def get_object_singular(self):
        return "mix"

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()