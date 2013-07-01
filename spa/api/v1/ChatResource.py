from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models.chatmessage import ChatMessage

class ChatResource(BackboneCompatibleResource):
    class Meta:
        queryset = ChatMessage.objects.all().order_by('-timestamp')
        resource_name = 'chat'
