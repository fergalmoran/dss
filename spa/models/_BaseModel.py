import logging
from django.db import models
from django.utils import simplejson

class _BaseModel(models.Model):
    logger = logging.getLogger(__name__)
    class Meta:
        abstract = True
        app_label = 'spa'

    def tosimplejson(self):
        ret = simplejson.dump(self)
