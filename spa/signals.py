from django.contrib.sessions.models import Session
from django.core import signals
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save, pre_save
from django.dispatch import Signal, receiver
from django.contrib.auth.models import User
from core.utils.audio.mp3 import mp3_length

from spa.models.userprofile import UserProfile
from spa.models.mix import Mix

waveform_generated_signal = Signal()


def _waveform_generated_callback(sender, **kwargs):
    print "Updating model with waveform"
    try:
        uid = kwargs['uid']
        if uid is not None:
            mix = Mix.objects.get(uid=uid)
            if mix is not None:
                mix.waveform_generated = True
                mix.duration = mp3_length(mix.get_absolute_path())
                mix.save(update_fields=["waveform_generated", "duration"])
    except ObjectDoesNotExist:
        print "Mix has still not been uploaded"
        pass


waveform_generated_signal.connect(_waveform_generated_callback)

update_user_geoip_signal = Signal()


def _update_user_geoip_callback(sender, **kwargs):
    try:
        user = UserProfile.objects.get(pk=kwargs['profile_id'])
        user.city = kwargs['city']
        user.country = kwargs['country']
        user.save()
    except ObjectDoesNotExist:
        pass


update_user_geoip_signal.connect(_update_user_geoip_callback)


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
    #should save generate a notification to a target user
    if hasattr(instance, 'create_notification'):
        instance.create_notification()
    #should save post to the activity feed
    if hasattr(instance, 'create_activity'):
        instance.create_activity()

    #try to get the user's geo profile
    if hasattr(instance, 'update_geo_info'):
        instance.update_geo_info()


post_save.connect(post_save_handler)

"""
    Setting up a post save handler for sessions here
    So that I can store the session id against the user
"""


@receiver(pre_save, sender=Session, dispatch_uid='session_pre_save')
def session_pre_save(sender, **kwargs):
    s = kwargs['instance']
    if s is not None:
        uid = s.get_decoded().get('_auth_user_id')
        if uid is not None:
            try:
                user = User.objects.get(pk=uid)
                p = user.get_profile()
                p.last_known_session = s.session_key
                p.save()
            except ObjectDoesNotExist:
                pass

