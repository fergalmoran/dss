from unittest import TestCase
from django.contrib.auth.models import User
from django.core.management.base import NoArgsCommand
from django.utils import unittest
from core.realtime.activity import post_activity
from spa.models.userprofile import UserProfile
from spa.models.activity import ActivityDownload
from spa.models.mix import Mix


class Command(NoArgsCommand):
    help = """
    If you need Arguments, please check other modules in
    django/core/management/commands.
    """

    def handle_noargs(self, **options):
        suite = unittest.TestLoader().loadTestsFromTestCase(TestRealtime)
        unittest.TextTestRunner().run(suite)


class TestRealtime(TestCase):
    def test_post_activity(self):
        try:
            mix = Mix.objects.order_by('?')[0]
            user = User.objects.get(pk=1)
            activity = ActivityDownload(user=user.get_profile(), mix=mix)
            activity.save()
            result = post_activity(activity.get_activity_url())
            self.assertTrue(result == "", msg=result)

        except Exception, ex:
            print "Error: test_post_activity: %s" % ex.message