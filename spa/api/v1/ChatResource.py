from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models.chatmessage import ChatMessage

class CommentResource(BackboneCompatibleResource):
    class Meta:
        queryset = ChatMessage.objects.all().order_by('-timestamp')
