from rest_framework import serializers
from spa.models.comment import Comment


class CommentSerialiser(serializers.HyperlinkedModelSerializer):
    user = serializers.RelatedField(many=False)
    avatar_image = serializers.Field(source='avatar_image')

    class Meta:
        model = Comment
        fields = ('comment', 'date_created', 'user', 'avatar_image')