import urlparse
from allauth.socialaccount.models import SocialAccount
from django import template
from django.contrib.auth.models import User
from django_gravatar.helpers import has_gravatar, get_gravatar_url
from dss import settings
from spa.models.UserProfile import UserProfile

register = template.Library()

@register.filter
def nice_name(user):
    if user == "":
        return "Anonymous"
    if user.is_authenticated():
        profile = user.get_profile()
        if profile is not None:
            if profile.display_name <> "":
                return profile.display_name
    else:
        return "Anonymous"

    return user.get_full_name() or user.username

@register.filter
def avatar_image(user, size=150):
    profile = user.get_profile()
    avatar_type = profile.avatar_type

    if avatar_type == 'gravatar':
        gravatar_exists = has_gravatar(user.email)
        if gravatar_exists:
            return get_gravatar_url(user.email, size)
    elif avatar_type == 'social' or avatar_type == '':
        try:
            social_account = SocialAccount.objects.filter(user = user)[0]
            if social_account:
                provider = social_account.get_provider_account()
                return provider.get_avatar_url()
        except:
            return urlparse.urljoin(settings.STATIC_URL, "img/default-avatar-32.png")
    elif avatar_type == 'custom':
        return profile.avatar_image.url

    return settings.STATIC_URL + "/images/default-avatar-32.png"
