from rest_framework import viewsets
from api.serialisers import CommentSerialiser
from spa.models.comment import Comment


class CommentViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerialiser