from django.db import models
from spa.models import _BaseModel, UserProfile


class Notification(_BaseModel):
    to_user = models.ForeignKey(UserProfile, related_name='to_notications')
    from_user = models.ForeignKey(UserProfile, related_name='notifications', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    notification_text = models.CharField(max_length=1024)
    notification_url = models.URLField(null=True)

    verb = models.CharField(max_length=200, null=True)
    target = models.CharField(max_length=200, null=True)

    accepted_date = models.DateTimeField(null=True)