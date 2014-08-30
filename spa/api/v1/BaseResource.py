import logging
from tastypie.resources import ModelResource


class BaseResource(ModelResource):
    logger = logging.getLogger(__name__)
    pass

    def _remove_kwargs(self, *args, **kwargs):
        for arg in args:
            if arg in kwargs:
                del kwargs['activity_sharing_networks_facebook']

        return kwargs