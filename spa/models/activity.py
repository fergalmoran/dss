import abc

from django.db import models
from model_utils.managers import InheritanceManager
from core.utils.url import wrap_full

from spa.models.notification import Notification
from spa.models.userprofile import UserProfile
from spa.models._basemodel import _BaseModel


ACTIVITYTYPES = (
    ('p', 'played'),
    ('d', 'downloaded'),
    ('l', 'liked'),
    ('f', 'favourited'),
    ('l', 'followed')
)

class Activity(_BaseModel):
    objects = InheritanceManager()
    user = models.ForeignKey(UserProfile, null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s" % self.get_object_name()

    def create_notification(self):
        try:
            notification = Notification()
            notification.from_user = self.user
            notification.to_user = self.get_target_user()
            notification.notification_text = "%s %s %s" % (
                self.user.get_nice_name() or "Anonymouse", self.get_verb_past(), self.get_object_name_for_notification())

            notification.notification_html = "<a href='%s'>%s</a> %s <a href='%s'>%s</a>" % (
                wrap_full(self.user.get_profile_url() or "http://deepsounds.com"),
                self.user.get_nice_name() or "Anonymouse",
                self.get_verb_past(),
                wrap_full(self.get_object_url()),
                self.get_object_name_for_notification()
            )

            notification.notification_url = wrap_full(self.get_object_url())
            notification.verb = self.get_verb_past()
            notification.target = self.get_object_name()
            notification.save()
        except Exception, ex:
            print "Error creating activity notification: %s" % ex.message
            raise ex

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

    def get_object_name_for_notification(self):
        return self.get_object_name()


class ActivityFollow(Activity):
    to_user = models.ForeignKey('spa.UserProfile', related_name='activity_follow')

    def get_target_user(self):
        return self.to_user

    def get_object_name(self):
        return self.to_user.get_nice_name()

    def get_object_url(self):
        return self.to_user.get_profile_url()

    def get_object_singular(self):
        return "user"

    def get_verb_past(self):
        return "followed"

    def get_object_name_for_notification(self):
        return "You"


class ActivityFavourite(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_favourites')

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
    mix = models.ForeignKey('spa.Mix', related_name='activity_plays')

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
    mix = models.ForeignKey('spa.Mix', related_name='activity_likes')

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
    mix = models.ForeignKey('spa.Mix', related_name='activity_downloads')

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

class ActivityComment(Activity):
    mix = models.ForeignKey('spa.Mix', related_name='activity_comments')

    def get_target_user(self):
        return self.mix.user

    def get_object_name(self):
        return self.mix.title

    def get_object_url(self):
        return self.mix.get_absolute_url()

    def get_object_singular(self):
        return "mix"

    def get_verb_past(self):
        return "commented on"
