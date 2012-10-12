from django.contrib.auth.models import User
from django.db import models
from spa.models._BaseModel import _BaseModel

class _Activity(_BaseModel):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True)
    uid = models.CharField(max_length=50, blank=True, null = True)