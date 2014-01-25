import threading
import mandrill

from django.db import models
from django.template import loader, Context

from core.realtime.notification import post_notification
from dss import localsettings
from spa.models import _BaseModel


class NotificationThread(threading.Thread):
    def __init__(self, instance, **kwargs):
        self._instance = instance
        super(NotificationThread, self).__init__(**kwargs)

    def run(self):
        #Check if target of notification has an active session
        session = self._instance.last_known_session
        if session:
            post_notification(notification_url=self._instance.get_notification_url(), session=session)


class Notification(_BaseModel):
    to_user = models.ForeignKey('spa.UserProfile', related_name='to_notications')
    from_user = models.ForeignKey('spa.UserProfile', related_name='notifications', null=True, blank=True)
    date = models.DateTimeField(auto_now=True)

    notification_text = models.CharField(max_length=1024)
    notification_html = models.CharField(max_length=1024)
    notification_url = models.URLField(null=True)

    verb = models.CharField(max_length=200, null=True)
    target = models.CharField(max_length=200, null=True)

    accepted_date = models.DateTimeField(null=True)

    def get_notification_url(self):
        return '/api/v1/notification/%s' % self.id

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):

        self.send_notification_email()
        return super(Notification, self).save(force_insert, force_update, using, update_fields)

    def send_notification_email(self):
        try:
            t = loader.get_template('email/notification/new.html')
            c = Context({
                'user_name': self.to_user.get_nice_name(),
                'notification_html': self.notification_html,
                'title': self.notification_html
            })
            rendered = t.render(c)

            mandrill_client = mandrill.Mandrill(localsettings.MANDRILL_API_KEY)
            message = {
                'inline_css': True,
                'from_email': 'chatbot@deepsouthsounds.com',
                'from_name': 'DSS ChatBot',
                'headers': {'Reply-To': 'chatbot@deepsouthsounds.com'},
                'metadata': {'website': 'www.deepsouthsounds.com'},
                'subject': self.notification_text,
                'to': [{'email': self.to_user.email,
                        'name': self.to_user.get_nice_name(),
                        'type': 'to'}],
                'html': rendered,
                'text': 'Get yourself some HTML man!',
            }

            result = mandrill_client.messages.send(message=message, async=False)
            print result

        except mandrill.Error, e:  # Mandrill errors are thrown as exceptions
            print 'A mandrill error occurred: %s - %s' % (e.__class__, e)
