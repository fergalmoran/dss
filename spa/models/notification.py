import threading
from django.db import models
from core.realtime.notification import post_notification
from spa.models import _BaseModel, UserProfile


class NotificationThread(threading.Thread):
    def __init__(self, instance, **kwargs):
        self.instance = instance
        super(NotificationThread, self).__init__(**kwargs)

    def run(self):
        post_notification(self.instance.get_notification_url())


class Notification(_BaseModel):
    to_user = models.ForeignKey(UserProfile, related_name='to_notications')
    from_user = models.ForeignKey(UserProfile, related_name='notifications', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    notification_text = models.CharField(max_length=1024)
    notification_url = models.URLField(null=True)

    verb = models.CharField(max_length=200, null=True)
    target = models.CharField(max_length=200, null=True)

    accepted_date = models.DateTimeField(null=True)

    def notify_activity(self):
        NotificationThread(instance=self).start()

    def get_notification_url(self):
        return '/api/v1/notification/%s' % self.id
