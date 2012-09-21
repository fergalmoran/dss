from django.db import models
from spa.models._Activity import _Activity

class MixLike(_Activity):
    mix = models.ForeignKey('spa.Mix', related_name='likes')

    def __unicode__(self):
        return "%s on %s" % (self.user.get_full_name(), self.mix.title)
