from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from tastypie.exceptions import ImmediateHttpResponse
from tastypie.http import HttpForbidden, HttpBadRequest
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import Mix
from spa.models.comment import Comment


class CommentResource(BackboneCompatibleResource):
    mix = fields.ToOneField('spa.api.v1.MixResource.MixResource', 'mix')

    class Meta:
        queryset = Comment.objects.all().order_by('-date_created')
        resource_name = 'comments'
        filtering = {
            "mix": ('exact',),
        }
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True

    def obj_create(self, bundle, **kwargs):
        bundle.data['user'] = bundle.request.user

        try:
            if 'mix_id' in bundle.data:
                mix = Mix.objects.get(pk=bundle.data['mix_id'])
                if mix is not None:
                    return super(CommentResource, self).obj_create(bundle, user=bundle.request.user, mix=mix)
        except Exception, e:
            self.logger.error("Error creating comment (%s)" % e.message)
            pass
        raise ImmediateHttpResponse(
            HttpBadRequest("Unable to hydrate comment from supplied data.")
        )

    def dehydrate(self, bundle):
        bundle.data['avatar_image'] = bundle.obj.user.get_profile().get_small_profile_image()
        bundle.data['user_url'] = bundle.obj.user.get_absolute_url()
        bundle.data['user_name'] = bundle.obj.user.get_profile().get_nice_name() or bundle.obj.user.get_profile().display_name
        return bundle
