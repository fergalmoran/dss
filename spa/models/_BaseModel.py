import logging
from django.db import models

class _BaseModel(models.Model):
    logger = logging.getLogger(__name__)
    class Meta:
        abstract = True
        app_label = 'spa'