from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import pre_save
from django.dispatch import receiver, Signal
from django.db.models import signals
from django.contrib.auth.management import create_superuser
from django.contrib.auth import models as auth_app
from spa.models import _BaseModel, Release
from spa.models.Mix import Mix

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

"""
def handle_image_updating(sender, field, instance, **kwargs):
    #Don't over
    if instance.id:
        if instance[field] == 'DONOTSEND':
            old_item = Mix.objects.get(pk=instance.id)
            instance[field] = old_item[field]
            instance.post.save()
"""

"""
signals.post_syncdb.disconnect(
    create_superuser,
    sender=auth_app,
    dispatch_uid = "django.contrib.auth.management.create_superuser")
"""