from django.db import models
from model_utils.managers import InheritanceManager
from spa.models.notification import Notification
from spa.models.userprofile import UserProfile
from spa.models._basemodel import _BaseModel
import abc

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
        return "%s" % self.get_object_name()

    def create_notification(self):
        notification = Notification()
        notification.from_user = self.user
        notification.to_user = self.get_target_user()
        notification.notification_text = "%s %s %s" % (self.user, self.get_verb_past(), self.get_object_name())
        notification.notification_url = self.get_object_url()
        notification.verb = self.get_verb_past()
        notification.target = self.get_object_name()
        notification.save()

    def get_activity_url(self):
        return '/api/v1/activity/%s' % self.id

    @abc.abstractmethod
    def get_target_user(self):
        pass

    @abc.abstractmethod
    def get_object_name(self):
        pass

    @abc.abstractmethod
    def get_object_url(self):
        pass

    @abc.abstractmethod
    def get_object_singular(self):
        pass


class ActivityFollow(Activity):
    to_user = models.ForeignKey('spa.UserProfile', related_name='follower_activity')

    def get_target_user(self):
        return self.user

    def get_object_name(self):
        return self.user.get_nice_name()

    def get_object_url(self):
        return self.user.get_profile_url()

    def get_object_singular(self):
        return "user"

    def get_verb_past(self):
        return "followed"


class ActivityFavourite(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='favourites')

    def get_target_user(self):
        return self.mix.user

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "favourited"


class ActivityPlay(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='plays')

    def get_target_user(self):
        return self.mix.user

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "played"


class ActivityLike(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='likes')

    def get_target_user(self):
        return self.mix.user

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "liked"


class ActivityDownload(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='downloads')

    def get_target_user(self):
        return self.mix.user

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "downloaded"
