from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from spa.models import UserProfile
from  spa.models._Activity import _Activity
import pdb


class ActivityResource(BackboneCompatibleResource):
    class Meta:
        queryset = _Activity.objects.all().order_by('-date')
        resource_name = 'activity'
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True

    def get_object_list(self, request):
        return self._meta.queryset.select_subclasses()

    def dehydrate(self, bundle):
        try:
            pdb.set_trace()
            if bundle.obj.user is not None and bundle.obj.user.get_profile() is not None:
                user_name = bundle.obj.user.get_profile().nice_name()
                user_image = bundle.obj.user.get_profile().get_small_profile_image()
                user_profile = bundle.obj.user.get_profile().get_profile_url()
            else:
                user_name = "Anonymous user"
                user_image = UserProfile.get_default_avatar_image()
                user_profile = ""

            bundle.data["verb"] = bundle.obj.get_verb_passed(),
            bundle.data["object"] = bundle.obj.get_object_singular(),
            bundle.data["item_name"] = bundle.obj.get_object_name(),
            bundle.data["item_url"] = bundle.obj.get_object_url(),
            bundle.data["user_name"] = user_name,
            bundle.data["user_profile"] = user_profile,
            bundle.data["user_image"] = user_image
            return bundle

        except AttributeError, ae:
            self.logger.debug("AttributeError: Error dehydrating activity, %s" % ae.message)
        except TypeError, te:
            self.logger.debug("TypeError: Error dehydrating activity, %s" % te.message)
        except Exception, ee:
            self.logger.debug("Exception: Error dehydrating activity, %s" % ee.message)
        return None

    """"
    def alter_list_data_to_serialize(self, request, data):
        return [i for i in data['objects'] if i is not None and i.obj.user is not None and i.obj.get_object_name is not None and i.obj.get_object_url is not None]
    """

    def dehydrate_date(self, bundle):
        return self.humanize_date(bundle.obj.date)
