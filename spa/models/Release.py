from datetime import datetime
from django.db import models
from core.utils.file import generate_save_file_name
from dss import settings
from spa.models.Label import Label
from spa.models.UserProfile import UserProfile
from spa.models._BaseModel import _BaseModel

def release_image_name(instance, filename):
    return generate_save_file_name('release-images', filename)

def release_file_name(instance, filename):
    return generate_save_file_name('release-audio', filename)

class Release(_BaseModel):
    class Meta:
        app_label = 'spa'

    release_artist = models.CharField(max_length=100)
    release_title = models.CharField(max_length=100)
    release_description = models.TextField()
    release_image = models.ImageField(blank=True, upload_to=release_image_name)
    release_label = models.ForeignKey(Label)
    release_date = models.DateField(default=datetime.now())

    embed_code = models.TextField(blank=True)

    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, editable=False)

    def __unicode__(self):
        return self.release_title

    def save(self, force_insert=False, force_update=False, using=None):
        super(Release, self).save(force_insert, force_update, using)

    def get_absolute_url(self):
        return '/release/%i' % self.id

    @classmethod
    def get_view_model(cls):
        qs = cls.objects.get(is_active=True)
        return qs


class ReleaseAudio(_BaseModel):
    class Meta:
        app_label = 'spa'

    def __unicode__(self):
        return self.description

    def get_waveform_url(self):
        return settings.MEDIA_URL + 'waveforms/release/%d.%s' % (self.id, "png")

    local_file = models.FileField(upload_to=release_file_name)
    release = models.ForeignKey(Release, related_name='release_audio', null=True, blank=True)
    description = models.TextField()