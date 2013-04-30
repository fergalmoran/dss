from django.db import models
from spa.models import _BaseModel
from spa.models.userprofile import UserProfile

class ChatMessage(_BaseModel):
    message = models.TextField('Message')
    timestamp = models.DateTimeField('Timestamp', auto_now_add=True)
    user = models.ForeignKey(UserProfile, related_name='chat_messages', blank=True, null=True)