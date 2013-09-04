from django.contrib.auth.models import User
from django.db import models
from spa.models._basemodel import _BaseModel
from spa.models.mix import Mix


class Comment(_BaseModel):
    class Meta:
        app_label = 'spa'

    user = models.ForeignKey(User, editable=False)
    mix = models.ForeignKey(Mix, editable=False, null=True, blank=True, related_name='comments')
    comment = models.CharField(max_length=1024)
    date_created = models.DateTimeField(auto_now=True)
    time_index = models.IntegerField(default=0)

    def get_absolute_url(self):
        return '/comment/%i' % self.id

