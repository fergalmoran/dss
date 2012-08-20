from spa.models import _BaseModel, Tracklist
from django.db import models

class PurchaseLink(_BaseModel):
    track = models.ForeignKey(Tracklist, related_name='purchase_link')
    url = models.URLField()
    provider = models.CharField(max_length=255)