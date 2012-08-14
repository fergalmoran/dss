from django.contrib.auth.models import User
from django.db import models
from spa.models.__BaseModel import __BaseModel
from spa.models.Mix import Mix

class Comment(__BaseModel):
    class Meta:
        db_table = 'www_comment'
        app_label = 'spa'

    user = models.ForeignKey(User, editable=False)
    mix = models.ForeignKey(Mix, editable=False, related_name='comments')
    comment = models.CharField(max_length=1024)
    date_created = models.DateTimeField(auto_now=True)
    time_index = models.IntegerField()

    def get_absolute_url(self):
        return '/comment/%i' % self.id

    def save(self, force_insert=False, force_update=False, using=None):
        super(Comment, self).save(force_insert, force_update, using)