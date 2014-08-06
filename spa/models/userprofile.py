import logging
import urlparse

from django.contrib.auth.models import User
from django.core.exceptions import SuspiciousOperation
from django.db import models
from django.db.models import Count
from django_gravatar.helpers import has_gravatar, get_gravatar_url
from sorl.thumbnail import get_thumbnail
from allauth.socialaccount.models import SocialAccount
from sorl import thumbnail
from sorl.thumbnail.helpers import ThumbnailError

from core.utils.file import generate_save_file_name
from core.utils.url import unique_slugify
from dss import settings
from spa.models.basemodel import BaseModel


logger = logging.getLogger(__name__)


def avatar_name(instance, filename):
    return generate_save_file_name(str(instance.id), 'avatars', filename)


class UserProfileManager(models.Manager):
    def get_query_set(self):
        return super(UserProfileManager, self).get_query_set().annotate(mix_count=Count('mixes'))


class UserProfile(BaseModel):
    class Meta:
        app_label = 'spa'

    objects = UserProfileManager()
    ACTIVITY_SHARE_LIKES = 1
    ACTIVITY_SHARE_FAVOURITES = 2
    ACTIVITY_SHARE_COMMENTS = 4

    ACTIVITY_SHARE_NETWORK_FACEBOOK = 1
    ACTIVITY_SHARE_NETWORK_TWITTER = 2

    user = models.OneToOneField(User, unique=True, related_name='userprofile')
    avatar_type = models.CharField(max_length=15, default='social')
    avatar_image = models.ImageField(max_length=1024, blank=True, upload_to=avatar_name)
    display_name = models.CharField(blank=True, max_length=35)
    description = models.CharField(blank=True, max_length=2048)

    slug = models.SlugField(max_length=50, blank=True, null=True, default=None)
    activity_sharing = models.IntegerField(default=0)
    activity_sharing_networks = models.IntegerField(default=0)

    following = models.ManyToManyField('self', null=True, blank=True, symmetrical=False, related_name='followers')

    #location properties
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    last_known_session = models.CharField(max_length=250, blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.user.get_full_name(), self.slug)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Save Photo after ensuring it is not blank.  Resize as needed.
        """
        if self.slug is None or self.slug == '':
            self.slug = unique_slugify(self, self.get_username())
            print "Slugified: %s" % self.slug

        """
        Check if follower has been added
        """
        l = self.get_dirty_fields()

        return super(UserProfile, self).save(force_insert, force_update, using, update_fields)

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

    def __create_slug(self):
        try:
            unique_slugify(self, self.get_username() or self.user.get_full_name(), slug_separator='_')
            self.save()
        except Exception, e:
            self.logger.error("Unable to create profile slug: %s", e.message)

    def toggle_favourite(self, mix, value):
        try:
            if value:
                if self.activity.filter(mix=mix).count() == 0:
                    self.activity.model.add(mix=mix, user=self)
                    self.favourites.model.save()
            else:
                self.favourites.model.delete(mix=mix)
        except Exception, ex:
            self.logger.error("Exception updating favourite: %s" % ex.message)

    def is_follower(self, user):
        try:
            return user.get_profile() in self.followers.all()
        except Exception, ex:
            logger.error(ex.message)

        return False

    def get_absolute_url(self):
        if self.slug is None or len(self.slug) == 0:
            self.__create_slug()

        return "user/%s" % self.slug

    def get_nice_name(self):
        return self.display_name or self.first_name + ' ' + self.last_name

    #TODO Refactor the below into something sane
    def get_medium_profile_image(self):
        try:
            image = self.get_avatar_image()
            if self.avatar_type == 'custom':
                image = "%s%s" % (settings.MEDIA_URL, get_thumbnail(image, "170x170", crop='center').name)
            return image
        except SuspiciousOperation, ex:
            self.logger.warn("Error getting medium profile image: %s", ex.message)
        except IOError, ex:
            self.logger.warn("Error getting medium profile image: %s", ex.message)

    def get_small_profile_image(self):
        try:
            if self.avatar_type == 'custom':
                image = self.avatar_image
                image = "%s%s" % (settings.MEDIA_URL, get_thumbnail(image, "32x32", crop='center').name)
                return image
        except SuspiciousOperation, ex:
            self.logger.exception("Error getting small profile image")
        except IOError, ex:
            self.logger.exception("Error getting small profile image")
        except ThumbnailError:
            pass

        return self.get_avatar_image()

    def get_sized_avatar_image(self, width, height):
        try:
            image = self.get_avatar_image()
            sized = thumbnail.get_thumbnail(image, "%sx%s" % (width, height), crop="center")
            return urlparse.urljoin(settings.MEDIA_URL, sized.name)
        except SuspiciousOperation:
            return UserProfile.get_default_avatar_image()
        except Exception, ex:
            return UserProfile.get_default_avatar_image()

    def get_avatar_image(self):
        avatar_type = self.avatar_type
        if avatar_type == 'gravatar':
            gravatar_exists = has_gravatar(self.email)
            if gravatar_exists:
                return get_gravatar_url(self.email)
        elif avatar_type == 'social' or avatar_type == '':
            try:
                social_account = SocialAccount.objects.filter(user=self.user)[0]
                if social_account:
                    provider = social_account.get_provider_account()
                    return provider.get_avatar_url()
            except Exception, ex:
                pass
        elif avatar_type == 'custom' or avatar_type:
            return urlparse.urljoin(settings.MEDIA_URL, self.avatar_image.name)

        return UserProfile.get_default_avatar_image()

    def get_profile_url(self):
        return '/user/%s' % (self.slug)

    def get_profile_description(self):
        try:
            if not self.description:
                social_account = SocialAccount.objects.filter(user=self.user)[0]
                if social_account is not None:
                    provider = social_account.get_provider_account()
                    if 'bio' in provider.account.extra_data:
                        return provider.account.extra_data['bio']
            else:
                return self.description
        except Exception, ex:
            pass

        return "Just another<br>DSS lover"

    @classmethod
    def get_default_avatar_image(cls):
        return urlparse.urljoin(settings.STATIC_URL, "img/default-avatar-32.png")

    @classmethod
    def get_default_moniker(cls):
        return "Anonymouse"

