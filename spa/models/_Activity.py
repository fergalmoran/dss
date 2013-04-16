import abc

from django.contrib.auth.models import User
from django.db import models

from model_utils.managers import InheritanceManager

from spa.models._BaseModel import _BaseModel
from spa.models.managers.QueuedActivityModelManager import QueuedActivityModelManager


class _Activity(_BaseModel):
    user = models.ForeignKey(User, null=True)
    uid = models.CharField(max_length=50, blank=True, null=True)
    date = models.DateTimeField(auto_now=True)
    objects = InheritanceManager()

    message_manager = QueuedActivityModelManager()

    class Meta:
        app_label = 'spa'

    def __unicode__(self):
        return "%s" % self.date

    @abc.abstractmethod
    def get_verb_passed(self):
        return

    @abc.abstractmethod
    def get_verb_present(self):
        return

    @abc.abstractmethod
    def get_object_singular(self):
        return

    @abc.abstractmethod
    def get_object_plural(self):
        return

    @abc.abstractmethod
    def get_object_name(self):
        return

    @abc.abstractmethod
    def get_object_url(self):
        return

