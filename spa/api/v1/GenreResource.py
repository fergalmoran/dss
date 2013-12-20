from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpBadRequest, HttpMethodNotAllowed, HttpUnauthorized, HttpApplicationError, HttpNotImplemented
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import Mix, UserProfile, Genre
from spa.models.comment import Comment


class GenreResource(BackboneCompatibleResource):
    class Meta:
        queryset = Genre.objects.all().order_by('text')
        resource_name = 'genres'

        excludes = ['id', 'resource_uri']
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True
