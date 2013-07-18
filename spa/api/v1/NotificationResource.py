from tastypie.authentication import SessionAuthentication
from tastypie.authorization import DjangoAuthorization
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models.notification import Notification
from spa.models.userprofile import UserProfile


class NotificationResource(BackboneCompatibleResource):
    class Meta:
        queryset = Notification.objects.order_by('-id')
        resource_name = 'notification'
        authentication = SessionAuthentication()
        authorization = DjangoAuthorization()
        always_return_data = True
        excludes = ['accepted_date']

    def authorized_read_list(self, object_list, bundle):
        return object_list.filter(to_user=bundle.request.user)

    def dehydrate(self, bundle):
        if bundle.obj.from_user is not None:
            bundle.data['user_image'] = bundle.obj.from_user.get_small_profile_image()
            bundle.data['user_name'] = bundle.obj.from_user.get_nice_name()
        else:
            bundle.data['user_image'] = UserProfile.get_default_avatar_image()
            bundle.data['user_name'] = UserProfile.get_default_moniker()
        return bundle

    def alter_list_data_to_serialize(self, request, data):
        data['meta']['is_new'] = Notification.objects.filter(to_user=request.user, accepted_date__isnull=True).count()
        return data