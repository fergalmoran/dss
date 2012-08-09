from allauth.socialaccount.models import SocialAccount
from django import template
from django.contrib.auth.models import User
from django_gravatar.helpers import has_gravatar, get_gravatar_url
from dss import settings
from spa.models import UserProfile

register = template.Library()

@register.filter
def nice_name(user):
    if user == "":
        return "Unknown User"

    if type(user) is UserProfile:
        return user.user.get_full_name() or user.user.username
    elif type(user) is User:
        return user.get_full_name() or user.username

@register.filter
def avatar_image(user, size=150):
    profile = user.get_profile()
    avatar_type = profile.avatar_type

    if avatar_type == 'gravatar':
        gravatar_exists = has_gravatar(user.email)
        if gravatar_exists:
            return get_gravatar_url(user.email, size)
    elif avatar_type == 'social':
        try:
            social_account = SocialAccount.objects.filter(user = user)[0]
            if social_account:
                provider = social_account.get_provider_account()
                return provider.get_avatar_url()
        except:
            pass
    elif avatar_type == 'custom':
        return profile.avatar_image.url

    return settings.STATIC_URL + "/images/default-avatar-32.png"
