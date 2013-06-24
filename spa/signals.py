import threading
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import Signal
from django.contrib.auth.models import User
from south import signals
from core.realtime.activity import post_activity
from core.utils.audio.mp3 import mp3_length

from dss import settings
from spa.models import UserProfile
from spa.models.activity import ActivityPlay
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


class ActivityThread(threading.Thread):
    def __init__(self, instance, **kwargs):
        self.instance = instance
        super(ActivityThread, self).__init__(**kwargs)

    def run(self):
        post_activity(self.instance.get_activity_url())


def send_activity_to_realtime(sender, instance, created, **kwargs):
    ActivityThread(instance=instance).start()


post_save.connect(send_activity_to_realtime, sender=ActivityPlay, dispatch_uid="activity-realtime-play")


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


post_save.connect(create_user_profile, sender=User, dispatch_uid="users-profilecreation")

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("new_follower", _("You have a new follower on deepsouthsounds.com"),
                                        _("You have a new follower."))

    signals.post_migrate.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"