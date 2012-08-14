from django.db import models
from spa.models.__BaseModel import __BaseModel

class Label(__BaseModel):
    class Meta:
        db_table = 'www_label'
        app_label = 'spa'

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name