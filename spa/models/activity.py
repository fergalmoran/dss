from django.db import models
from model_utils.managers import InheritanceManager
from spa.models.userprofile import UserProfile
from spa.models._basemodel import _BaseModel

ACTIVITYTYPES = (
    ('p', 'played'),
    ('d', 'downloaded'),
    ('l', 'liked'),
    ('f', 'favourited'),
)


class Activity(_BaseModel):
    objects = InheritanceManager()
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.date

    def get_activity_url(self):
        return '/api/v1/activity/%s' % self.id


class ActivityMix(Activity):
    objects = InheritanceManager()

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"


class ActivityFavourite(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='favourites')

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_passed(self):
        return "favourited"


class ActivityPlay(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='plays')

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_passed(self):
        return "played"


class ActivityLike(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='likes')

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_passed(self):
        return "liked"


class ActivityDownload(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='downloads')

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_passed(self):
        return "downloaded"
