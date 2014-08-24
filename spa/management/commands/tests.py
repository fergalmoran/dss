from unittest import TestCase
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
            user = UserProfile.objects.get(slug='fergalmoran')
            activity = ActivityDownload(user=user, mix=mix)
            activity.save()

            """
                Try to find an active session for this user
                If it exists, post to the realtime controller
            """
            sessions = user.user.session_set.all()
            for session in sessions:
                result = post_activity(session.session_key, activity.get_activity_url())

            self.assertTrue(result == "", msg=result)

        except Exception, ex:
            print "Error: test_post_activity: %s" % ex.message