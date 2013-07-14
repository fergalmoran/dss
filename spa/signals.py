import threading
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import Signal
from django.contrib.auth.models import User
from south import signals
from core.realtime.activity import post_activity
from core.utils.audio.mp3 import mp3_length

from dss import settings
from spa.models.userprofile import UserProfile
from spa.models.activity import ActivityPlay, ActivityDownload, ActivityFavourite, ActivityLike, ActivityFollow, Activity
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
        pass


waveform_generated.connect(waveform_generated_callback)


def create_profile(sender, **kw):
    user = kw["instance"]
    if kw["created"]:
        up = UserProfile(user=user)
        up.save()


post_save.connect(create_profile, sender=User)

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("new_follower", _("You have a new follower on deepsouthsounds.com"),
                                        _("You have a new follower."))

    signals.post_migrate.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"

"""
    Doing signals for notifications here.
    I like this method because I have a single signal
    and just check for a hook method on the sender
"""


def notification_post_save_handler(**kwargs):
    instance = kwargs['instance']
    if hasattr(instance, 'create_notification'):
        instance.create_notification()
    if hasattr(instance, 'notify_activity'):
        instance.notify_activity()


post_save.connect(notification_post_save_handler)
