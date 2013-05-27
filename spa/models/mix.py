import os
import rfc822
from datetime import datetime
import urlparse
from sorl.thumbnail import get_thumbnail
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Count
from core.utils import url
from core.utils.audio.mp3 import mp3_length
from core.utils.url import unique_slugify
from spa.models.mixlike import MixLike
from spa.models.genre import Genre
from spa.models.mixplay import MixPlay
from spa.models.mixdownload import MixDownload
from dss import settings, localsettings
from spa.models.userprofile import UserProfile
from spa.models._basemodel import _BaseModel
from spa.models.mixfavourite import MixFavourite
from core.utils.file import generate_save_file_name


def mix_file_name(instance, filename):
    return generate_save_file_name(instance.uid, 'mixes', filename)


def mix_image_name(instance, filename):
    ret = generate_save_file_name(instance.uid, 'mix-images', filename)
    return ret


class MixManager(models.Manager):
    pass


class Mix(_BaseModel):
    class Meta:
        app_label = 'spa'

    title = models.CharField(max_length=150)
    description = models.TextField()
    upload_date = models.DateTimeField(default=datetime.now())
    mix_image = models.ImageField(blank=True, upload_to=mix_image_name)
    local_file = models.FileField(blank=True, upload_to=mix_file_name)
    download_url = models.CharField(max_length=255)
    stream_url = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, editable=False)
    waveform_generated = models.BooleanField(default=False)
    uid = models.CharField(max_length=38, blank=True, unique=True)
    download_allowed = models.BooleanField(default=False)
    duration = models.IntegerField(null=True, blank=True)
    slug = models.SlugField()

    genres = models.ManyToManyField(Genre)

    class ImmutableMeta:
        immutable = ['user']

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.slug = unique_slugify(self, self.title)

        #Check for the unlikely event that the waveform has been generated
        if os.path.isfile(self.get_waveform_path()):
            self.waveform_generated = True
            self.duration = mp3_length(self.get_absolute_path())

        super(Mix, self).save(force_insert, force_update, using, update_fields)

    def get_absolute_path(self, prefix=""):
        fileName, extension = os.path.splitext(self.local_file.name)
        if extension == "" or extension == ".":
            extension = ".mp3"
        return '%s/mixes/%s%s%s' % (settings.MEDIA_ROOT, prefix, self.uid, extension)

    def get_absolute_url(self):
        return '/mix/%s' % self.slug

    def get_full_url(self):
        return 'http://%s%s' % (Site.objects.get_current().domain, self.get_absolute_url())

    def get_download_url(self):
        return 'http://%s/audio/download/%s' % (Site.objects.get_current().domain, self.pk)

    def get_waveform_path(self):
        return os.path.join(settings.MEDIA_ROOT, "waveforms/", "%s.%s" % (self.uid, "png"))

    def get_waveform_url(self):

        if self.waveform_generated and os.path.exists(self.get_waveform_path()):

            waveform_root = localsettings.WAVEFORM_URL if hasattr(localsettings,
                                                                  'WAVEFORM_URL') else "%swaveforms" % settings.MEDIA_URL
            ret = "%s/%s.%s" % (waveform_root, self.uid, "png")
            return url.urlclean(ret)

        else:
            return urlparse.urljoin(settings.STATIC_URL, "img/waveform-processing.gif")

    def _get_social_image(self):
        if self.user:
            return self.user.get_medium_profile_image()
        return None

    def get_image_url(self):
        try:
            ret = get_thumbnail(self.mix_image, '160x160', crop='center')
            return "%s/%s" % (settings.MEDIA_URL, ret.name)
        except Exception, ex:
            self.logger.error("Mix: error getting mix image %s" % ex.message)
            social_image = self._get_social_image()
            if social_image:
                return social_image

        return super(Mix, self).get_image_url(self.mix_image, settings.STATIC_URL + 'img/default-track.png')

    def get_stream_path(self):
        #return 'media/%s/' % self.local_file.name
        return '/audio/stream/%d' % self.id

    def get_date_as_rfc822(self):
        return rfc822.formatdate(
            rfc822.mktime_tz(rfc822.parsedate_tz(self.upload_date.strftime("%a, %d %b %Y %H:%M:%S"))))

    @classmethod
    def get_for_username(cls, user, queryset=None):
        if queryset is None:
            queryset = Mix.objects

        return queryset \
            .filter(user__slug__exact=user) \
            .filter(waveform_generated=True) \
            .order_by('-id')

    @classmethod
    def get_listing(cls, listing_type, user=None, queryset=None):
        candidates = queryset or Mix.objects \
            .filter(waveform_generated=True) \
            .filter(is_featured=True) \
            .exclude(duration__isnull=True)

        if listing_type == 'latest':
            queryset = candidates.order_by('-id')
        elif listing_type == 'likes':
            queryset = candidates.annotate(karma=Count('likes')).order_by('-karma')
        elif listing_type == 'favourites':
            queryset = candidates.annotate(karma=Count('likes')).order_by('-karma')
        elif listing_type == 'toprated':
            queryset = candidates.annotate(karma=Count('likes')).order_by('-karma')
        elif listing_type == 'mostactive':
            queryset = candidates.filter(waveform_generated=True).annotate(karma=Count('comments')).order_by('-karma')
        elif listing_type == 'mostplayed':
            queryset = candidates.annotate(karma=Count('plays')).order_by('-karma')
        elif listing_type == 'recommended':
            queryset = candidates.order_by('-id')
        elif listing_type == 'favourites':
            queryset = candidates.filter(favourites__user=user).order_by('favourites__date')
        else:
            #check if we have a valid genre
            queryset = candidates.filter(genres__slug__exact=listing_type)
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

    def add_download(self, user):
        try:
            self.downloads.add(MixDownload(user=user if user.is_authenticated() else None))
        except Exception, e:
            self.logger.exception("Error adding mix download")

    def add_play(self, user):
        try:
            self.plays.add(MixPlay(user=user if user.is_authenticated() else None))
        except Exception, e:
            self.logger.exception("Unable to add mix play")

    def is_liked(self, user):
        if user is None:
            return False
        if user.is_authenticated():
            return self.likes.filter(user=user).count() != 0

        return False

    def update_favourite(self, user, value):
        try:
            if user is None:
                return
            if user.is_authenticated():
                if value:
                    if self.favourites.filter(user=user).count() == 0:
                        self.favourites.add(MixFavourite(mix=self, user=user.get_profile()))
                else:
                    self.favourites.filter(user=user).delete()
        except Exception, ex:
            self.logger.error("Exception updating favourite: %s" % ex.message)

    def update_liked(self, user, value):
        try:
            if user is None:
                return
            if user.is_authenticated():
                if value:
                    if self.likes.filter(user=user).count() == 0:
                        self.likes.add(MixLike(mix=self, user=user.get_profile()))
                else:
                    self.likes.filter(user=user).delete()
        except Exception, ex:
            self.logger.error("Exception updating like: %s" % ex.message)

    def is_favourited(self, user):
        if user is None:
            return False
        if user.is_authenticated():
            return self.favourites.filter(user=user).count() != 0
        else:
            return False
