from django.db import models

from spa.models.UserProfile import UserProfile
from spa.models._BaseModel import _BaseModel


class UserFollows(_BaseModel):
    follower = models.ManyToManyField(UserProfile, related_name='followers')
    following = models.ManyToManyField(UserProfile, related_name='following')
