from rest_framework import serializers
from spa.models.comment import Comment


class CommentSerialiser(serializers.HyperlinkedModelSerializer):
    user = serializers.RelatedField(many=False)

    class Meta:
        model = Comment
        fields = ('comment', 'date_created', 'user')