import urlparse
from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django_gravatar.helpers import has_gravatar, get_gravatar_url
import os
from core.utils.file import generate_save_file_name
from dss import settings
from spa.models._BaseModel import _BaseModel
def avatar_name(instance, filename):
    return generate_save_file_name(str(instance.id), 'avatars', filename)

class UserProfile(_BaseModel):
    class Meta:
        app_label = 'spa'

    ACTIVITY_SHARE_LIKES = 1
    ACTIVITY_SHARE_FAVOURITES = 2
    ACTIVITY_SHARE_COMMENTS = 4

    ACTIVITY_SHARE_NETWORK_FACEBOOK = 1
    ACTIVITY_SHARE_NETWORK_TWITTER = 2

    # This field is required.
    user = models.ForeignKey(User, unique=True)
    avatar_type = models.CharField(max_length=15, default='social')
    avatar_image = models.ImageField(blank=True, upload_to=avatar_name)
    display_name = models.CharField(blank=True, max_length=35)
    description = models.CharField(blank=True, max_length=2048)

    profile_slug = models.CharField(max_length=35, blank=True, null=True, default=None)
    activity_sharing = models.IntegerField(default=0)
    activity_sharing_networks = models.IntegerField(default=0)
    def save(self, size=(260, 180)):
        """
        Save Photo after ensuring it is not blank.  Resize as needed.
        """
        from PIL import Image
        if not self.id and not self.source:
            return

        if self.profile_slug == '':
            self.profile_slug = None

        super(UserProfile, self).save()

        filename = self.get_source_filename()
        image = Image.open(filename)

        image.thumbnail(size, Image.ANTIALIAS)
        image.save(filename)

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
        return self.display_name or self.first_name + ' ' + self.last_name

    def get_avatar_image(self, size=150):
        avatar_type = self.avatar_type
        if avatar_type == 'gravatar':
            gravatar_exists = has_gravatar(self.email)
            if gravatar_exists:
                return get_gravatar_url(self.email, size)
        elif avatar_type == 'social' or avatar_type == '':
            try:
                social_account = SocialAccount.objects.filter(user = self)[0]
                if social_account:
                    provider = social_account.get_provider_account()
                    return provider.get_avatar_url()
            except:
                pass
        elif avatar_type == 'custom' or avatar_type:
            return self.avatar_image.url

        return urlparse.urljoin(settings.STATIC_URL, "img/default-avatar-32.png")

    def get_profile_url(self):
        return 'http://%s/user/%s' % (Site.objects.get_current().domain, self.profile_slug)

    def save(self, force_insert=False, force_update=False, using=None):
        return super(UserProfile, self).save(force_insert, force_update, using)

