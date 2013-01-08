from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from spa.api.v1.BackboneCompatibleResource import BackboneCompatibleResource
from  spa.models._Activity import _Activity


class ActivityResource(BackboneCompatibleResource):

    class Meta:
        queryset = _Activity.objects.all()
        resource_name = 'activity'
        authorization = Authorization()
        authentication = Authentication()
        always_return_data = True

    def get_object_list(self, request):
        return self._meta.queryset.select_subclasses()

    def dehydrate(self, bundle):
        try:
            if bundle.obj.user is not None:
                bundle.data["message"] = "%s %s a %s on %s" %\
                    (bundle.obj.user.get_full_name(),
                     bundle.obj.get_verb_passed(),
                     bundle.obj.get_object_singular(),
                     bundle.obj.date)
                return bundle

        except AttributeError, ae:
            self.logger.debug("AttributeError: Error dehydrating activity, %s" % ae.message)
        except TypeError, te:
            self.logger.debug("TypeError: Error dehydrating activity, %s" % te.message)
        except Exception, ee:
            self.logger.debug("Exception: Error dehydrating activity, %s" % ee.message)
