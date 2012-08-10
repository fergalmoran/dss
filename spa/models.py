from datetime import datetime
import logging
import urlparse
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.aggregates import Count
from django.db.models.signals import post_save
from django_gravatar.helpers import has_gravatar, get_gravatar_url
import os
from core.utils.file import generate_save_file_name
from dss import settings
from tasks.waveform import create_waveform_task
from tinymce import models as tinymce_models

def mix_file_name(instance, filename):
    return generate_save_file_name('mixes', filename)


def mix_image_name(instance, filename):
    return generate_save_file_name('mix-images', filename)


def venue_image_name(instance, filename):
    return generate_save_file_name('venue-images', filename)


def release_image_name(instance, filename):
    return generate_save_file_name('release-images', filename)


def release_file_name(instance, filename):
    return generate_save_file_name('release-audio', filename)

class BaseModel(models.Model):
    logger = logging.getLogger(__name__)
    class Meta:
        abstract = True

class UserProfile(BaseModel):
    class Meta:
        db_table = 'www_userprofile'

    # This field is required.
    user = models.ForeignKey(User, unique=True)
    avatar_type = models.CharField(max_length=15)
    avatar_image = models.ImageField(blank=True, upload_to='avatars/')

    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(user=instance)
    post_save.connect(create_user_profile, sender=User)

    def get_username(self):
        return self.user.username
    username = property(get_username)

    def get_email(self):
        return self.user.email
    email = property(get_email)

    def get_first_name(self):
        return self.user.first_name
    first_name = property(get_first_name)

    def get_last_name(self):
        return self.user.last_name
    last_name = property(get_last_name)

    def get_absolute_url(self):
        return reverse('user_details', kwargs={'user_name': self.user.username})

    def nice_name(self):
        return self.first_name + ' ' + self.last_name

    def get_avatar_image(self, size=150):
        avatar_type = self.avatar_type
        if avatar_type == 'gravatar':
            gravatar_exists = has_gravatar(self.email)
            if gravatar_exists:
                return get_gravatar_url(self.email, size)
        elif avatar_type == 'social':
            try:
                social_account = SocialAccount.objects.filter(user = self)[0]
                if social_account:
                    provider = social_account.get_provider_account()
                    return provider.get_avatar_url()
            except:
                pass
        elif avatar_type == 'custom':
            return self.avatar_image.url

        return urlparse.urljoin(settings.STATIC_URL, "img/default-avatar-32.png")

class Mix(BaseModel):
    class Meta:
        db_table = 'www_mix'

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
    def get_listing(cls, listing_type):
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

class Comment(BaseModel):
    class Meta:
        db_table = 'www_comment'

    user = models.ForeignKey(User, editable=False)
    mix = models.ForeignKey(Mix, editable=False, related_name='comments')
    comment = models.CharField(max_length=1024)
    date_created = models.DateTimeField(auto_now=True)
    time_index = models.IntegerField()

    def get_absolute_url(self):
        return '/comment/%i' % self.id

    def save(self, force_insert=False, force_update=False, using=None):
        super(Comment, self).save(force_insert, force_update, using)

class Label(BaseModel):
    class Meta:
        db_table = 'www_label'

    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

class Release(BaseModel):
    class Meta:
        db_table = 'www_release'

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

class ReleaseAudio(BaseModel):
    class Meta:
        db_table = 'www_releaseaudio'

    def __unicode__(self):
        return self.description

    def get_waveform_url(self):
        return settings.MEDIA_URL + 'waveforms/release/%d.%s' % (self.id, "png")

    local_file = models.FileField(upload_to=release_file_name)
    release = models.ForeignKey(Release, related_name='release_audio')
    description = models.TextField()

class __Like(BaseModel):
    date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, null=True    )

class MixLike(__Like):
    class Meta:
        db_table = 'www_like'
    mix = models.ForeignKey(Mix, related_name='likes')

class MixPlay(__Like):
    class Meta:
        db_table = 'www_play'
    mix = models.ForeignKey(Mix, related_name='plays')

class Venue(models.Model):
    user = models.ForeignKey(User)
    venue_name = models.CharField(max_length=250)
    venue_address = models.CharField(max_length=1024)
    venue_image = models.ImageField(blank=True, upload_to=venue_image_name)

    def __unicode__(self):
        return self.venue_name

class Event(models.Model):
    event_venue = models.ForeignKey(Venue)

    event_date = models.DateField(default=datetime.now())
    event_time = models.TimeField(default=datetime.now())

    date_created = models.DateField(default=datetime.now())
    event_title = models.CharField(max_length=250)
    event_description = tinymce_models.HTMLField()

    attendees = models.ManyToManyField(User, related_name='event__attendees')

    def get_absolute_url(self):
        return '/events/%i' % self.id

    def __unicode__(self):
        return self.event_title
