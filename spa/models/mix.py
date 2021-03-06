import os
import rfc822
import urlparse

from sorl.thumbnail import get_thumbnail
from django.contrib.sites.models import Site
from django.db import models

from core.utils import url
from core.utils.audio import Mp3FileNotFoundException
from core.utils.audio.mp3 import mp3_length, tag_mp3
from core.utils.url import unique_slugify, url_path_join
from spa.models.activity import ActivityDownload, ActivityPlay, ActivityFavourite, ActivityLike
from spa.models.genre import Genre
from dss import settings, localsettings
from spa.models.userprofile import UserProfile
from spa.models.basemodel import BaseModel
from core.utils.file import generate_save_file_name


def mix_file_name(instance, filename):
    return generate_save_file_name(instance.uid, 'mixes', filename)


def mix_image_name(instance, filename):
    ret = generate_save_file_name(instance.uid, 'mix-images', filename)
    return ret


class MixManager(models.Manager):
    pass

    def get_by_id_or_slug(self, id_or_slug):
        """
            Tries to get a mix using the slug first
            If this fails then try getting by id
        """
        try:
            return super(MixManager, self).get(slug=id_or_slug)
        except Mix.DoesNotExist:
            return super(MixManager, self).get(id=id_or_slug)


class Mix(BaseModel):
    class Meta:
        app_label = 'spa'

        permissions = (
            ("mix_add_homepage", "Can add a mix to the homepage"),
            ("mix_allow_download", "Can allow downloads on a mix"),
        )

    objects = MixManager()

    title = models.CharField(max_length=150)
    description = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)
    mix_image = models.ImageField(max_length=1024, blank=True, upload_to=mix_image_name)
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=True)
    user = models.ForeignKey(UserProfile, editable=False, related_name='mixes')
    waveform_generated = models.BooleanField(default=False)
    mp3tags_updated = models.BooleanField(default=False)
    uid = models.CharField(max_length=38, blank=True, unique=True)
    filetype = models.CharField(max_length=10, blank=False, default="mp3")
    download_allowed = models.BooleanField(default=False)
    duration = models.IntegerField(null=True, blank=True)
    archive_path = models.CharField(max_length=2048, null=True, blank=True)
    archive_updated = models.BooleanField(default=False)
    slug = models.SlugField()

    genres = models.ManyToManyField(Genre)

    # activity based stuff
    favourites = models.ManyToManyField(UserProfile, related_name='favourites', blank=True, null=True)
    likes = models.ManyToManyField(UserProfile, related_name='likes', blank=True, null=True)

    def __unicode__(self):
        return self.title

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.id:
            self.slug = unique_slugify(self, self.title)

        self.clean_image('mix_image', Mix)
        #Check for the unlikely event that the waveform has been generated
        if os.path.isfile(self.get_waveform_path()):
            self.waveform_generated = True
            try:
                self.duration = mp3_length(self.get_absolute_path())
            except Mp3FileNotFoundException:
                #Not really bothered about this in save as it can be called before we have an mp3
                pass

        super(Mix, self).save(force_insert, force_update, using, update_fields)

    def create_mp3_tags(self, prefix=""):
        try:
            tag_mp3(
                self.get_absolute_path(),
                artist=self.user.get_nice_name(),
                title=self.title,
                url=self.get_full_url(),
                album="Deep South Sounds Mixes",
                year=self.upload_date.year,
                comment=self.description,
                genres=self.get_nice_genres())
        except Exception, ex:
            self.logger.exception("Mix: error creating tags: %s" % ex.message)
            pass

        return '%s/mixes/%s%s.%s' % (settings.MEDIA_ROOT, prefix, self.uid, self.filetype)

    def get_nice_genres(self):
        return ", ".join(list(self.genres.all().values_list("description", flat=True)))

    def get_cache_path(self, prefix=""):
        return '%s/mixes/%s%s.%s' % (settings.CACHE_ROOT, prefix, self.uid, self.filetype)

    def get_absolute_path(self, prefix=""):
        return '%s/mixes/%s%s.%s' % (settings.MEDIA_ROOT, prefix, self.uid, self.filetype)

    def get_absolute_url(self):
        return '/mix/%s' % self.slug

    def get_full_url(self):
        return 'http://%s%s' % (Site.objects.get_current().domain, self.get_absolute_url())

    def get_download_url(self):
        return 'http://%s/audio/download/%s' % (Site.objects.get_current().domain, self.pk)

    def get_waveform_path(self):
        return os.path.join(settings.MEDIA_ROOT, "waveforms/", "%s.%s" % (self.uid, "png"))

    def get_waveform_url(self):
        if self.waveform_generated:
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

    def get_image_absolute_path(self):
        name, extension = os.path.splitext(self.mix_image.file.name)
        return os.path.join(settings.MEDIA_ROOT, 'mix-images', "%s.%s", (self.uid, extension))

    def get_image_url(self, size='160x160', default=''):
        try:
            ret = get_thumbnail(self.mix_image, size, crop='center')
            return "%s/%s" % (settings.MEDIA_URL, ret.name)
        except Exception, ex:
            self.logger.error("Mix: error getting mix image %s" % ex.message)
            social_image = self._get_social_image()
            if social_image:
                return social_image

        return super(Mix, self).get_image_url(self.mix_image, settings.STATIC_URL + 'img/default-track.png')

    def get_stream_path(self):
        if self.archive_path in [None, '']:
            ret = url_path_join(localsettings.STREAM_URL, "%s.mp3" % self.uid)
        else:
            ret = self.archive_path
        return ret

    #used for podcast xml
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

    def add_download(self, user):
        try:
            if user.is_authenticated():
                ActivityDownload(user=user.get_profile(), mix=self).save()
        except Exception, e:
            self.logger.exception("Error adding mix download: %s" % e.message)

    def add_play(self, user):
        try:
            if user.is_authenticated():
                ActivityPlay(user=user.get_profile(), mix=self).save()
            else:
                ActivityPlay(user=None, mix=self).save()

        except Exception, e:
            self.logger.exception("Unable to add mix play: %s" % e.message)

    def update_favourite(self, user, value):
        try:
            if user is None:
                return
            if user.is_authenticated():
                if value:
                    if self.favourites.filter(user=user).count() == 0:
                        ActivityFavourite(user=user.get_profile(), mix=self).save()
                        self.favourites.add(user.get_profile())
                        self.save()
                else:
                    self.favourites.remove(user.get_profile())
                self.save()

        except Exception, ex:
            self.logger.error("Exception updating favourite: %s" % ex.message)

    def update_liked(self, user, value):
        try:
            if user is None:
                return
            if user.is_authenticated():
                if value:
                    if self.likes.filter(user=user).count() == 0:
                        ActivityLike(user=user.get_profile(), mix=self).save()
                        self.likes.add(user.get_profile())
                        self.save()
                else:
                    self.likes.remove(user.get_profile())
                self.save()
        except Exception, ex:
            self.logger.error("Exception updating like: %s" % ex.message)

    def is_favourited(self, user):
        if user is None:
            return False
        if user.is_authenticated():
            return self.favourites.filter(user=user).count() != 0
        else:
            return False

    def is_liked(self, user):
        if user is None:
            return False
        if user.is_authenticated():
            return self.likes.filter(user=user).count() != 0

        return False

