from tastypie import fields
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models.Comment import Comment


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

    def obj_create(self, bundle, request=None, **kwargs):
        bundle.data['user'] = {'pk': request.user.pk}
        return super(CommentResource, self).obj_create(bundle, request, user=request.user)

    """
    def dehydrate_date_created(self, bundle):
        return self.humanize_date(bundle.obj.date_created)
    """

    def dehydrate(self, bundle):
        bundle.data['avatar_image'] = bundle.obj.user.get_profile().get_small_profile_image()
        bundle.data['user_url'] = bundle.obj.user.get_absolute_url()
        bundle.data['user_name'] = bundle.obj.user.get_profile().get_nice_name() or bundle.obj.user.get_profile().display_name
        return bundle
