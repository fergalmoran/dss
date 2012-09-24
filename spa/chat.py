import logging
import urllib2
from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.core.serializers import json
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from dss import settings
from spa.models.ChatMessage import ChatMessage

class ChatHandler():

    logger = logging.getLogger(__name__)

    def __init__(self, api_name="v1"):
        self.api_name = api_name

    @property
    def urls(self):
        pattern_list = [
            url(r'^show_messages/$', 'spa.chat.show_messages'),
            url(r'^post_message/$', 'spa.chat.post_message'),
        ]
        return  pattern_list

@csrf_exempt
def show_messages(request):
    messages = ChatMessage.objects.all()
    return render_to_response('inc/messages.html', {'messages': messages})

@csrf_exempt
@login_required
def post_message(request):
    new_msg = ChatMessage(message = request.POST['message'], user = request.user.get_profile())
    new_msg.save()
    # Again, we're just going to assume this always works
    cmd = [{'cmd': 'inlinepush',
            'params': {
                'password': settings.APE_PASSWORD,
                'raw': 'postmsg',
                'channel': 'messages',
                'data': {
                    'msg': new_msg.msg,
                    'posted_by': new_msg.posted_by,
                    'timestamp': new_msg.timestamp
                }
            }
           }]
    url = settings.APE_SERVER + urllib2.quote(json.dumps(cmd))
    response = urllib2.urlopen(url)
    # Updating the message is handled by APE, so just return an empty 200
    return HttpResponse()
    """
    jsonified_msg = serializers.serialize("json", [new_msg])
    # Again, we're just going to assume this always works
    return HttpResponse(jsonified_msg, mimetype='application/javascript')
    """