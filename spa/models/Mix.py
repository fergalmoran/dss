from django.contrib.sites.models import Site
from django.db.models.signals import post_save
from django.dispatch import Signal, receiver
import os
from core.utils import url
from datetime import datetime
from django.db import models
from django.db.models import Count
from spa.models.MixPlay import MixPlay
from dss import settings, localsettings
from spa.models.UserProfile import UserProfile
from spa.models._BaseModel import _BaseModel
from core.utils.file import generate_save_file_name

def mix_file_name(instance, filename):
    return generate_save_file_name(instance.uid, 'mixes', filename)

def mix_image_name(instance, filename):
    ret =  generate_save_file_name(instance.uid, 'mix-images', filename)
    return ret

class Mix(_BaseModel):
    class Meta:
        app_label = 'spa'

    title = models.CharField(max_length=50)
    description = models.TextField()
    upload_date = models.DateTimeField(default=datetime.now())
    mix_image = models.ImageField(blank=True, upload_to=mix_image_name)
    local_file = models.FileField(blank=True, upload_to=mix_file_name)
    download_url = models.CharField(max_length=255)
    stream_url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, editable=False)
    waveform_generated = models.BooleanField(default=False)
    uid = models.CharField(max_length=38, blank=True, unique=True)
    download_allowed = models.BooleanField(default=False)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None):
        #turn away now - horrid hack to strip media root url
        #from image - will sort when I've figured backbone out better
        if self.mix_image.name.startswith(settings.MEDIA_URL):
            self.mix_image.name = self.mix_image.name[len(settings.MEDIA_URL):len(self.mix_image.name)]

        #Check for the unlikely event that the waveform has been generated
        if os.path.isfile(self.get_waveform_path()):
            self.waveform_generated = True

        super(Mix, self).save(force_insert, force_update, using)

    def get_absolute_url(self):
        return '/mix/%i' % self.id

    def get_download_url(self):
        return 'http://%s/audio/download/%s' % (Site.objects.get_current().domain, self.pk)

    def get_waveform_path(self):
        return os.path.join(settings.MEDIA_ROOT, "waveforms/", "%s.%s" % (self.uid, "png"))

    def get_waveform_url(self):
        waveform_root = localsettings.WAVEFORM_URL if hasattr(localsettings, 'WAVEFORM_URL') else "%s/waveforms/" % settings.MEDIA_URL
        ret = "%s/%s.%s" % (waveform_root, self.uid, "png")
        return url.urlclean(ret)

    def get_image_url(self):
        return super(Mix, self).get_image_url(self.mix_image, settings.STATIC_URL + 'img/default-track.png')

    def get_stream_path(self):
        #return 'media/%s/' % self.local_file.name
        return '/audio/stream/%d' % self.id

    @classmethod
    def get_listing(cls, listing_type, user=None):
        queryset = None
        if listing_type == 'latest':
            queryset = Mix.objects.filter(waveform_generated=True).order_by( '-id')
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
                .annotate(karma=Count('plays'))\
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
