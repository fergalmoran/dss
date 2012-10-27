from django.template.loader import render_to_string
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from core.serialisers import json
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import Genre

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

    def _parseGenreList(self, genres):
        #for magic..
        ret = []
        for genre in genres:
            if genre['id'] == genre['text']:
                new_item = Genre(description = genre['text'])
                new_item.save()
                ret.append(new_item)
            else:
                ret.append(Genre.objects.get(pk=genre['id']))

        return ret

    def _unpackGenreList(self, bundle, genres):
        genre_list = self._parseGenreList(genres)
        bundle.obj.genres = genre_list
        bundle.obj.save()

    def obj_create(self, bundle, request=None, **kwargs):
        file_name = "mixes/%s.%s" % (bundle.data['upload-hash'], bundle.data['upload-extension'])
        uid = bundle.data['upload-hash']
        if 'is_featured' not in bundle.data:
            bundle.data['is_featured'] = False

        bundle.data['user'] = request.user.get_profile()
        ret = super(MixResource, self).obj_create(bundle, request, user=request.user.get_profile(), local_file=file_name, uid=uid)
        self._unpackGenreList(ret, bundle.data['genre-list'])
        #if ret is hunky dory
        return ret

    def obj_update(self, bundle, request=None, **kwargs):
        ret = super(MixResource, self).obj_update(bundle, request)
        self._unpackGenreList(ret, bundle.data['genre-list'])
        return ret

    def obj_get_list(self, request=None, **kwargs):
        if 'user' in request.GET and request.GET['user']:
            user = request.GET['user']
            return Mix.get_for_username(user)
        elif 'type' in request.GET and request.GET['type']:
            type = request.GET['type']
            return Mix.get_listing(type, request.user)

        return Mix.get_listing('latest', request.user)

    def dehydrate_mix_image(self, bundle):
        return bundle.obj.get_image_url()

    def dehydrate(self, bundle):
        bundle.data['waveform_url'] = bundle.obj.get_waveform_url()
        bundle.data['user_name'] = bundle.obj.user.nice_name()
        bundle.data['item_url'] = 'mix/%s' % bundle.obj.id

        bundle.data['play_count'] = bundle.obj.plays.count()
        bundle.data['download_count'] = bundle.obj.downloads.count()
        bundle.data['like_count'] = bundle.obj.likes.count()
        bundle.data['mode'] = 'mix'
        bundle.data['tooltip'] = render_to_string('inc/player_tooltip.html', {'item': bundle.obj})
        bundle.data['comment_count'] = bundle.obj.comments.count()

        bundle.data['genre-list'] = json.to_ajax(bundle.obj.genres.all(), 'description', 'slug')
        bundle.data['liked'] = bundle.obj.is_liked(bundle.request.user)
        bundle.data['favourited'] = bundle.obj.is_favourited(bundle.request.user)
        return bundle
