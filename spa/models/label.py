from django.db import models
from spa.models._basemodel import _BaseModel

class Label(_BaseModel):
    class Meta:
        app_label = 'spa'

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name