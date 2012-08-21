from datetime import datetime
from django.db import models
from django.db.models import Count
import os
from core.utils.file import generate_save_file_name
from dss import settings
from spa.models.MixLike import MixLike
from spa.models.MixPlay import MixPlay
from spa.models.UserProfile import UserProfile
from spa.models._BaseModel import _BaseModel
from tasks.waveform import create_waveform_task

def mix_file_name(instance, filename):
    return generate_save_file_name('mixes', filename)

def mix_image_name(instance, filename):
    return generate_save_file_name('mix-images', filename)

class Mix(_BaseModel):
    class Meta:
        app_label = 'spa'

    title = models.CharField(max_length=50)
    description = models.TextField()
    upload_date = models.DateTimeField(default=datetime.now())
    mix_image = models.ImageField(blank=True, upload_to=mix_image_name)
    local_file = models.FileField(upload_to=mix_file_name)
    download_url = models.CharField(max_length=255)
    stream_url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, editable=False)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        super(Mix, self).save(force_insert, force_update, using)
        if not os.path.exists(self.get_waveform_path()):
            create_waveform_task.delay(id=self.id, in_file=self.local_file.file.name)

    def get_absolute_url(self):
        return '/mix/%i' % self.id

    def get_waveform_path(self):
        return os.path.join(settings.MEDIA_ROOT, "waveforms/mix/", "%d.%s" % (self.id, "png"))

    def get_waveform_url(self):
        return settings.MEDIA_URL + 'waveforms/mix/%d.%s' % (self.id, "png")

    def get_image(self):
        try:
            if self.mix_image:
                if os.path.exists(self.mix_image.file.name):
                    return  self.mix_image.url
        except Exception as ex:
            pass

        return settings.STATIC_URL + 'img/default-track.png'

    def get_stream_path(self):
        return settings.MEDIA_URL + self.local_file.name

    @classmethod
    def get_listing(cls, listing_type, user=None):
        queryset = None
        if listing_type == 'latest':
            queryset = Mix.objects.all().order_by( 'id')
        elif listing_type == 'toprated':
            queryset = Mix.objects.all()\
                .annotate(karma=Count('likes'))\
                .order_by('-karma')
        elif listing_type == 'mostactive':
            queryset = Mix.objects.all()\
                .annotate(karma=Count('comments'))\
                .order_by('-karma')
        elif listing_type == 'mostplayed':
            queryset = Mix.objects.all()\
                .annotate(karma=Count('likes'))\
                .order_by('-karma')
        elif listing_type == 'recommended':
            queryset = Mix.objects.all().order_by( '-id')
        elif listing_type == 'favourites':
            queryset = Mix.objects.filter(favourites__user=user).order_by('favourites__date')
            debug = queryset.query
        return queryset

    @classmethod
    def get_user_mixes(cls, user_name):
        mixes = Mix.objects.filter(user__user__username=user_name)
        if mixes.count():
            return {
                "inline_play": False,
                "heading": "Some mixes from " + mixes[0].user.user.get_full_name() or mixes[0].user.user.username,
                "latest_mix_list": mixes,
                }

        return {
            "heading": "No mixes found for this user",
            "latest_mix_list": None,
            }

    def add_play(self, user):
        try:
            self.plays.add(MixPlay(user = user if user.is_authenticated() else None))
        except Exception, e:
            self.logger.exception("Error getting mix stream url")

    def is_liked(self, user):
        if user is None:
            return False
        if user.is_authenticated():
            return self.likes.filter(user=user).count() <> 0

        return False

    def is_favourited(self, user):
        if user is None:
            return False
        if user.is_authenticated():
            return self.favourites.filter(user=user).count() <> 0
        else:
            return False
