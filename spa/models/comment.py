from django.contrib.auth.models import User
from django.db import models
from spa.models import _BaseModel, UserProfile
from spa.models.notification import Notification
from spa.models.mix import Mix


class Comment(_BaseModel):
    class Meta:
        app_label = 'spa'

    user = models.ForeignKey(User, editable=False, null=True, blank=True)
    mix = models.ForeignKey(Mix, editable=False, null=True, blank=True, related_name='comments')
    comment = models.CharField(max_length=1024)
    date_created = models.DateTimeField(auto_now=True)
    time_index = models.IntegerField(default=0)

    def get_absolute_url(self):
        return '/comment/%i' % self.id

    def create_notification(self):
        notification = Notification()
        notification.to_user = self.mix.user
        notification.notification_url = self.mix.get_absolute_url()
        notification.verb = "Commented on"
        notification.target = self.mix.title

        if self.user is not None:
            notification.from_user = self.user.get_profile()
            notification.notification_text = "%s %s %s" % (
                self.user.get_profile().get_nice_name(), notification.verb, self.mix.title)
        else:
            notification.notification_text = "%s %s %s" % (
                "Anonymouse", notification.verb, self.mix.title
            )

        notification.save()

    def create_activity(self):
        pass
