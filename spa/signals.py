from celery.task import task
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import Signal
from kombu import Connection
from kombu.entity import Exchange
from django.contrib.auth.models import User

from dss import localsettings
from spa.models import _Activity
from spa.models import UserProfile
from spa.models.mix import Mix
import pika

waveform_generated = Signal()


def waveform_generated_callback(sender, **kwargs):
    print "Updating model with waveform"
    try:
        uid = kwargs['uid']
        if uid is not None:
            mix = Mix.objects.get(uid=uid)
            if mix is not None:
                mix.waveform_generated = True
                mix.save()
    except ObjectDoesNotExist:
        pass


waveform_generated.connect(waveform_generated_callback)


@task
def async_send_activity_to_message_queue(instance):
    # do something with the instance.
    pass


def send_activity_to_message_queue(sender, *args, **kwargs):
    try:
        pass
    except Exception, ex:
        print "Error reporting activity to message queue: %s" % ex.message


post_save.connect(send_activity_to_message_queue, sender=None)


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User, dispatch_uid="users-profilecreation")
