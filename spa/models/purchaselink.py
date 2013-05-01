from spa.models._basemodel import _BaseModel
from spa.models.tracklist import Tracklist

from django.db import models

class PurchaseLink(_BaseModel):
    track = models.ForeignKey(Tracklist, related_name='purchase_link')
    url = models.URLField()
    provider = models.CharField(max_length=255)