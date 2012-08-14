from django.db import models
from spa.models.Mix import Mix
from spa.models.__Activity import __Activity

class MixLike(__Activity):
    class Meta:
        db_table = 'www_like'
        app_label = 'spa'

    mix = models.ForeignKey(Mix, related_name='likes')