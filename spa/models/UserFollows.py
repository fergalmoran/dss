from django.db import models

from spa.models._basemodel import _BaseModel


class __UserFollows(_BaseModel):
    follower = models.OneToOneField('UserProfile', related_name='followers')
    following = models.OneToOneField('UserProfile', related_name='following')
