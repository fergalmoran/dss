from celery.task import task
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.signals import post_save
from django.dispatch import Signal
from kombu import Connection
from kombu.entity import Exchange

from dss import localsettings
from spa.models import _Activity
from spa.models.Mix import Mix
import pika

waveform_generated = Signal()


def waveform_generated_callback(sender, **kwargs):
    print "Updating model with waveform"
    try:
        uid = kwargs['uid']
        if uid is not None:
            mix = Mix.objects.get(uid=uid)
            if mix is not None:
                mix.waveform_generated = True
                mix.save()
    except ObjectDoesNotExist:
        pass


waveform_generated.connect(waveform_generated_callback)


@task
def async_send_activity_to_message_queue(instance):
    # do something with the instance.
    pass


def send_activity_to_message_queue(sender, *args, **kwargs):
    try:

        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_bind(queue='activity', exchange='amq.topic')
        channel.basic_publish(exchange='amq.topic',
                              routing_key='hello',
                              body='Hello World!')
        connection.close()

        """
        activity_exchange = Exchange('activity', 'direct', durable=True)
        broker = "amqp://%s:%s@%s:%s//" % (localsettings.BROKER_USER,
                                          localsettings.BROKER_PASSWORD,
                                          localsettings.BROKER_HOST,
                                          localsettings.BROKER_PORT)
        if issubclass(sender, _Activity):
            with Connection(broker) as conn:
                with conn.Producer(serializer='json') as producer:
                    producer.publish(
                        {'name': 'Hello', 'size': 1301013},
                        exchange=activity_exchange, routing_key='video'
                    )
                    print "Message sent successfully"
        """
    except Exception, ex:
        print "Error reporting activity to message queue: %s" % ex.message


post_save.connect(send_activity_to_message_queue, sender=None)
