import uuid
from django.core.urlresolvers import reverse
from django.test.client import Client
import unittest
from utils import here


class TestPostMix(unittest.TestCase):
    fixtures = ['full.json']

    def testPost(self):
        print "Running TestPostMix"
        try:
            c = Client()
            uid = uuid.uuid1()
            with open(here('spa/tests/data/test.mp3')) as fp:

                response = c.post(reverse('jfu_upload'), {'upload-hash': uid, 'files[]': [fp]}, HTTP_ACCEPT_ENCODING="application/json")
                self.assertEquals(response.status_code, 200)
        except Exception, ex:
            self.fail(ex.message)