from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import NoArgsCommand, CommandError
from spa.models import UserProfile
from core.utils.url import unique_slugify

class Command(NoArgsCommand):
    help = "Updates audio files with their durations"

    def handle(user, *args, **options):
        try:
            candidates = User.objects.all()
            for user in candidates:
                try:
                    profile = user.get_profile()
                except ObjectDoesNotExist, ce:
                    print "Creating profile for %s" % user.get_username()
                    UserProfile.objects.create(user=user)
                    profile = user.get_profile()
                          
                if profile.slug is None or profile.slug == '':
                    profile.slug = unique_slugify(profile, user.get_username())
                    print "Slugified: %s" % profile.slug
                    profile.save()

                user.save()
        except Exception, ex:
            raise CommandError(ex.message)
