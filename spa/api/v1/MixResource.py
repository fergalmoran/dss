from django.template.loader import render_to_string
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource

from spa.models.Mix import Mix

class MixResource(BackboneCompatibleResource):
    comments = fields.ToManyField('spa.api.v1.CommentResource.CommentResource', 'comments', 'mix', null=True)

    class Meta:
        queryset = Mix.objects.filter(is_active=True)
        excludes = ['download_url', 'is_active', 'local_file', 'upload_date']
        filtering = {
            'comments': ALL_WITH_RELATIONS
        }
        authorization = Authorization()

    def obj_create(self, bundle, request=None, **kwargs):
        file_name = "mixes/%s.%s" % (bundle.data['upload-hash'], bundle.data['upload-extension'])
        uid = bundle.data['upload-hash']
        if 'is_featured' not in bundle.data:
            bundle.data['is_featured'] = False

        bundle.data['user'] = request.user.get_profile()
        return super(MixResource, self).obj_create(bundle, request, user=request.user.get_profile(), local_file=file_name, uid=uid)

    def obj_get_list(self, request=None, **kwargs):
        if 'user' in request.GET and request.GET['user']:
            user = request.GET['user']
            return Mix.get_for_username(user)
        elif 'sort' in request.GET and request.GET['sort']:
            sort = request.GET['sort']
            return Mix.get_listing(sort, request.user)

        return Mix.get_listing('latest', request.user)

    def dehydrate_mix_image(self, bundle):
        return bundle.obj.get_image_url()

    def dehydrate(self, bundle):
        bundle.data['waveform_url'] = bundle.obj.get_waveform_url()
        bundle.data['user_name'] = bundle.obj.user.nice_name()
        bundle.data['item_url'] = 'mix/%s' % bundle.obj.id

        bundle.data['play_count'] = bundle.obj.plays.count()
        bundle.data['like_count'] = bundle.obj.likes.count()
        bundle.data['mode'] = 'mix'
        bundle.data['tooltip'] = render_to_string('inc/player_tooltip.html', {'item': bundle.obj})
        bundle.data['comment_count'] = bundle.obj.comments.count()

        bundle.data['liked'] = bundle.obj.is_liked(bundle.request.user)
        bundle.data['favourited'] = bundle.obj.is_favourited(bundle.request.user)
        return bundle
