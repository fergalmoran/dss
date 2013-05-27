from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Count
from django.template.loader import render_to_string
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.http import HttpGone
from tastypie.utils import trailing_slash

from core.serialisers import json
from spa.api.v1.ActivityResource import ActivityResource
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.api.v1.CommentResource import CommentResource
from spa.models.genre import Genre
from spa.models.mix import Mix


class MixResource(BackboneCompatibleResource):
    comments = fields.ToManyField('spa.api.v1.CommentResource.CommentResource', 'comments', null=True)
    #downloads = fields.ToManyField('spa.api.v1.ActivityResource.ActivityResource', 'downloads')

    class Meta:
        queryset = Mix.objects.filter(is_active=True)
        always_return_data = True
        detail_uri_name = 'slug'
        excludes = ['download_url', 'is_active', 'local_file', 'upload_date', 'waveform-generated']
        filtering = {
            'comments': ALL_WITH_RELATIONS
        }
        authorization = Authorization()

    def _parseGenreList(self, genres):
        #for magic..
        ret = []
        for genre in genres:
            if genre['id'] == genre['text']:
                new_item = Genre(description=genre['text'])
                new_item.save()
                ret.append(new_item)
            else:
                ret.append(Genre.objects.get(pk=genre['id']))

        return ret

    def _unpackGenreList(self, bundle, genres):
        genre_list = self._parseGenreList(genres)
        bundle.obj.genres = genre_list
        bundle.obj.save()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<id>[\d]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d-]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<slug>\w[\w/-]*)/comments%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_comments'), name="api_get_comments"),
            url(r"^(?P<resource_name>%s)/(?P<slug>\w[\w/-]*)/activity%s$" % (self._meta.resource_name, trailing_slash()), self.wrap_view('get_activity'), name="api_get_activity"),
        ]

    def get_comments(self, request, **kwargs):
        try:
            basic_bundle = self.build_bundle(request=request)
            obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()

        child_resource = CommentResource()
        return child_resource.get_list(request, mix=obj)

    def get_activity(self, request, **kwargs):
        try:
            basic_bundle = self.build_bundle(request=request)
            obj = self.cached_obj_get(bundle=basic_bundle, **self.remove_api_resource_names(kwargs))
        except ObjectDoesNotExist:
            return HttpGone()

        child_resource = ActivityResource()
        return child_resource.get_list(request, mix=obj)

    def obj_create(self, bundle, **kwargs):
        file_name = "mixes/%s.%s" % (bundle.data['upload-hash'], bundle.data['upload-extension'])
        uid = bundle.data['upload-hash']
        if 'is_featured' not in bundle.data:
            bundle.data['is_featured'] = False

        bundle.data['user'] = bundle.request.user.get_profile()
        ret = super(MixResource, self).obj_create(
            bundle,
            user=bundle.request.user.get_profile(),
            local_file=file_name,
            uid=uid)

        self._unpackGenreList(ret, bundle.data['genre-list'])
        #if ret is hunky dory
        return ret

    def obj_update(self, bundle, **kwargs):
        #don't sync the mix_image, this has to be handled separately
        del bundle.data['mix_image']

        bundle.obj.update_favourite(bundle.request.user, bundle.data['favourited'])
        bundle.obj.update_liked(bundle.request.user, bundle.data['liked'])
        ret = super(MixResource, self).obj_update(bundle, bundle.request)
        self._unpackGenreList(ret, bundle.data['genre-list'])
        return ret

    def apply_sorting(self, obj_list, options=None):
        orderby = options.get('order_by', '')
        if orderby == 'latest':
            obj_list = obj_list.order_by('-id')
        elif orderby == 'toprated':
            obj_list = obj_list.annotate(karma=Count('likes')).order_by('-karma')
        elif orderby == 'mostplayed':
            obj_list = obj_list.annotate(karma=Count('plays')).order_by('-karma')
        elif orderby == 'mostactive':
            obj_list = obj_list.annotate(karma=Count('comments')).order_by('-karma')
        elif orderby == 'recommended':
            obj_list = obj_list.annotate(karma=Count('likes'))  .order_by('-karma')

        return obj_list

    def apply_filters(self, request, applicable_filters):
        semi_filtered = super(MixResource, self).apply_filters(request, applicable_filters)
        type = request.GET.get('type', None)
        if type == 'favourites':
            semi_filtered = semi_filtered.filter(favourites__mix__in=semi_filtered)

        return semi_filtered

    def hydrate_favourited(self, bundle):
        return bundle

    def dehydrate_mix_image(self, bundle):
        return bundle.obj.get_image_url()

    def dehydrate(self, bundle):
        bundle.data['waveform_url'] = bundle.obj.get_waveform_url()
        bundle.data['user_name'] = bundle.obj.user.get_nice_name()
        bundle.data['user_profile_url'] = bundle.obj.user.get_absolute_url()
        bundle.data['user_profile_image'] = bundle.obj.user.get_small_profile_image()
        bundle.data['item_url'] = '/mix/%s' % bundle.obj.slug

        bundle.data['play_count'] = bundle.obj.plays.count()
        bundle.data['download_count'] = bundle.obj.downloads.count()
        bundle.data['like_count'] = bundle.obj.likes.count()
        bundle.data['favourite_count'] = bundle.obj.favourites.count()
        bundle.data['tooltip'] = render_to_string('inc/player_tooltip.html', {'item': bundle.obj})
        bundle.data['comment_count'] = bundle.obj.comments.count()

        bundle.data['genre-list'] = json.to_ajax(bundle.obj.genres.all(), 'description', 'slug')
        bundle.data['liked'] = bundle.obj.is_liked(bundle.request.user)
        bundle.data['favourited'] = bundle.obj.is_favourited(bundle.request.user)
        return bundle


