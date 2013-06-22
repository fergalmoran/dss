from django.core.management.base import NoArgsCommand
import requests

__author__ = 'fergalm'

class Command(NoArgsCommand):

    def handle_noargs(self, **options):
        try:
            token = 'AAACMhWPn1hEBAO3jZCedwkZA194rEC2SZA0qZBMoF8V7lS8pLVcxBqd90vY87oqPJcnJ4jx3YCYqXsGJEnZC9mhCx1Qz7MPsNd2vrSBDe5AZDZD'
            uid = '456582037725172'
            proxies = {
                "http": "127.0.0.1:8888",
                "https": "127.0.0.1:8888",
                }
            url = "https://graph.facebook.com/%s?access_token=%s" % (uid, token)
            response = requests.delete(url, proxies=proxies)
            return response
        except Exception, ex:
            print "Error talking with facebook: %s" % ex.message