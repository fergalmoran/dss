from django.contrib.auth.models import User
from django.db import models
from spa.models.__BaseModel import __BaseModel

class __Activity(__BaseModel):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True    )