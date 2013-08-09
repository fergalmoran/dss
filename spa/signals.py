import threading
from django.core.exceptions import ObjectDoesNotExist, ImproperlyConfigured
from django.db.models import get_app
from django.db.models.signals import post_save
from django.dispatch import Signal
from django.contrib.auth.models import User
from south import signals
from core.utils.audio.mp3 import mp3_length

from dss import settings
from spa.models.userprofile import UserProfile
from spa.models.mix import Mix

waveform_generated = Signal()


def waveform_generated_callback(sender, **kwargs):
    print "Updating model with waveform"
    try:
        uid = kwargs['uid']
        if uid is not None:
            mix = Mix.objects.get(uid=uid)
            if mix is not None:
                mix.waveform_generated = True
                mix.duration = mp3_length(mix.get_absolute_path())
                mix.save()
    except ObjectDoesNotExist:
        print "Mix has still not been uploaded"
        pass


waveform_generated.connect(waveform_generated_callback)


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        up = UserProfile(user=user)
        up.save()


post_save.connect(create_profile, sender=User)

"""
    Doing signals for notifications here.
    I like this method because I have a single signal
    and just check for a hook method on the sender
"""


def post_save_handler(**kwargs):
    instance = kwargs['instance']
    if hasattr(instance, 'create_notification'):
        instance.create_notification()
    if hasattr(instance, 'notify_activity'):
        instance.notify_activity()


post_save.connect(post_save_handler)
