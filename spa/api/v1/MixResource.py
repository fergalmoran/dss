from django.conf.urls import url
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator, InvalidPage
from django.db.models import Count
from django.http import Http404
from django.template.loader import render_to_string
from tastypie import fields
from tastypie.authorization import Authorization
from tastypie.constants import ALL_WITH_RELATIONS
from tastypie.fields import ToOneField
from tastypie.http import HttpGone
from tastypie.utils import trailing_slash

from core.serialisers import json
from spa.api.v1.ActivityResource import ActivityResource
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.api.v1.CommentResource import CommentResource
from spa.models.genre import Genre
from spa.models.mix import Mix


class MixResource(BackboneCompatibleResource):
    comments = fields.ToManyField('spa.api.v1.CommentResource.CommentResource', 'comments', null=True, full=True)
    favourites = fields.ToManyField('spa.api.v1.UserResource.UserResource', 'favourites',
                                    related_name='favourites', full=False, null=True)

    likes = fields.ToManyField('spa.api.v1.UserResource.UserResource', 'likes',
                               related_name='likes', full=False, null=True)

    class Meta:
        queryset = Mix.objects.filter(is_active=True)
        user = ToOneField('UserResource', 'user')
        always_return_data = True
        detail_uri_name = 'slug'
        excludes = ['is_active', 'local_file', 'upload_date', 'waveform-generated']
        post_excludes = ['comments']
        filtering = {
            'comments': ALL_WITH_RELATIONS,
            'favourites': ALL_WITH_RELATIONS,
            'likes': ALL_WITH_RELATIONS,
            'slug': ALL_WITH_RELATIONS,
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
            url(r"^(?P<resource_name>%s)/search%s$" % (self._meta.resource_name, trailing_slash()),
                self.wrap_view('get_search'),
                name="api_get_search"),
            url(r"^(?P<resource_name>%s)/(?P<id>[\d]+)/$" % self._meta.resource_name, self.wrap_view('dispatch_detail'),
                name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/random/$" % self._meta.resource_name, self.wrap_view('dispatch_random'),
                name="api_dispatch_random"),
            url(r"^(?P<resource_name>%s)/(?P<slug>[\w\d-]+)/$" % self._meta.resource_name,
                self.wrap_view('dispatch_detail'), name="api_dispatch_detail"),
            url(r"^(?P<resource_name>%s)/(?P<slug>\w[\w/-]*)/comments%s$" % (
                self._meta.resource_name, trailing_slash()), self.wrap_view('get_comments'), name="api_get_comments"),
            url(r"^(?P<resource_name>%s)/(?P<slug>\w[\w/-]*)/activity%s$" % (
                self._meta.resource_name, trailing_slash()), self.wrap_view('get_activity'), name="api_get_activity"),
        ]

    def dispatch_random(self, request, **kwargs):
        kwargs['pk'] = self._meta.queryset.values_list('pk', flat=True).order_by('?')[0]
        return self.get_detail(request, **kwargs)

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
        ret = super(MixResource, self).obj_update(bundle, bundle.request)

        bundle.obj.update_favourite(bundle.request.user, bundle.data['favourited'])
        bundle.obj.update_liked(bundle.request.user, bundle.data['liked'])

        self._unpackGenreList(ret, bundle.data['genre-list'])
        return ret

    def apply_sorting(self, obj_list, options=None):
        orderby = options.get('order_by', '')
        if orderby == 'latest':
            obj_list = obj_list.order_by('-id')
        elif orderby == 'toprated':
            obj_list = obj_list.annotate(karma=Count('activity_likes')).order_by('-karma')
        elif orderby == 'mostplayed':
            obj_list = obj_list.annotate(karma=Count('activity_plays')).order_by('-karma')
        elif orderby == 'mostactive':
            obj_list = obj_list.annotate(karma=Count('comments')).order_by('-karma')
        elif orderby == 'recommended':
            obj_list = obj_list.annotate(karma=Count('activity_likes')).order_by('-karma')

        return obj_list

    def apply_filters(self, request, applicable_filters):
        semi_filtered = super(MixResource, self) \
            .apply_filters(request, applicable_filters) \
            .filter(waveform_generated=True)

        f_user = request.GET.get('user', None)

        if f_user is not None:
            semi_filtered = semi_filtered.filter(user__slug=f_user)
        else:
            semi_filtered = semi_filtered.filter(is_featured=True)

        return semi_filtered

    def hydrate_favourited(self, bundle):
        return bundle

    def dehydrate_mix_image(self, bundle):
        return bundle.obj.get_image_url(size="160x110")

    def dehydrate(self, bundle):
        bundle.data['waveform_url'] = bundle.obj.get_waveform_url()
        bundle.data['user_name'] = bundle.obj.user.get_nice_name()
        bundle.data['user_profile_url'] = bundle.obj.user.get_absolute_url()
        bundle.data['user_profile_image'] = bundle.obj.user.get_small_profile_image()
        bundle.data['item_url'] = '/mix/%s' % bundle.obj.slug

        bundle.data['favourite_count'] = bundle.obj.favourites.count()

        bundle.data['play_count'] = bundle.obj.activity_plays.count()
        bundle.data['download_count'] = bundle.obj.activity_downloads.count()
        bundle.data['like_count'] = bundle.obj.activity_likes.count()

        bundle.data['tooltip'] = render_to_string('inc/player_tooltip.html', {'item': bundle.obj})
        bundle.data['comment_count'] = bundle.obj.comments.count()

        bundle.data['genre-list'] = json.to_ajax(bundle.obj.genres.all(), 'description', 'slug')
        bundle.data['liked'] = bundle.obj.is_liked(bundle.request.user)

        if bundle.request.user.is_authenticated():
            bundle.data['can_edit'] = bundle.request.user.is_staff or bundle.obj.user_id == bundle.request.user.id
        else:
            bundle.data['can_edit'] = False

        if bundle.request.user.is_authenticated():
            bundle.data['favourited'] = bundle.obj.favourites.filter(user=bundle.request.user).count() != 0
        else:
            bundle.data['favourited'] = False

        return bundle

    def get_search(self, request, **kwargs):
        self.method_check(request, allowed=['get'])
        self.is_authenticated(request)
        self.throttle_check(request)

        # Do the query.
        sqs = Mix.objects.filter(title__icontains=request.GET.get('q', ''))
        paginator = Paginator(sqs, 20)

        try:
            page = paginator.page(int(request.GET.get('page', 1)))
        except InvalidPage:
            raise Http404("Sorry, no results on that page.")

        objects = []

        for result in page.object_list:
            bundle = self.build_bundle(obj=result, request=request)
            bundle = self.full_dehydrate(bundle)
            objects.append(bundle)

        object_list = {
            'objects': objects,
        }

        self.log_throttled_access(request)
        return self.create_response(request, object_list)
