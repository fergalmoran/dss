from django.db import models

from spa.models.UserProfile import UserProfile
from spa.models._BaseModel import _BaseModel


class UserFollows(_BaseModel):
    user_from = models.OneToOneField(UserProfile)
    user_to = models.OneToOneField(UserProfile)
