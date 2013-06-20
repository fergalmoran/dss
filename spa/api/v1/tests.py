import datetime
from django.contrib.auth.models import User
from tastypie.test import ResourceTestCase


class UserProfileResourceTest(ResourceTestCase):
    fixtures = ['test_entries.json']

    def setUp(self):
        self.deteail_url = '/api/v1/user/'

    def test_put_detail(self):
        # Grab the current data & modify it slightly.
        original_data = self.deserialize(self.api_client.get(self.detail_url, format='json', authentication=self.get_credentials()))
        new_data = original_data.copy()
        new_data['title'] = 'Updated: First Post'
        new_data['created'] = '2012-05-01T20:06:12'

