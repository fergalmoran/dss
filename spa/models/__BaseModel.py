import logging
from django.db import models

class __BaseModel(models.Model):
    logger = logging.getLogger(__name__)
    class Meta:
        abstract = True
        app_label = 'spa'