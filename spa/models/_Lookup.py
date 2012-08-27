from django.db import models
from _BaseModel import _BaseModel

class _Lookup(_BaseModel):
    description = models.CharField(max_length=100)

    def __unicode__(self):
        return self.description
