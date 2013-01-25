import logging
from django.db import models
from django.utils import simplejson
import os
from core.utils import url
from dss import localsettings, settings

class _BaseModel(models.Model):
    logger = logging.getLogger(__name__)

    class Meta:
        abstract = True
        app_label = 'spa'

    def tosimplejson(self):
        ret = simplejson.dump(self)

    @classmethod
    def get_lookup(cls, filter_field, transform=None, filter=None):
        if filter is not None:
            filter_dict = {'%s__startswith' % filter_field: filter}
            return cls.objects.all().filter(filter_dict).extra(select=transform)
        else:
            return cls.objects.all()

    def get_image_url(self, image, default):
        try:
            if os.path.isfile(image.path):
                images_root = localsettings.IMAGE_URL if hasattr(localsettings, 'IMAGE_URL') else "%s" % settings.MEDIA_URL
                ret = "%s/%s" % (images_root, image)
                return url.urlclean(ret)

        except Exception, ex:
            pass

        return default

    @classmethod
    def get_lookup_filter_field(cls):
        field_list = cls._meta.get_all_field_names()
        for field in field_list:
            if field.endswith("name") or field.endswith("description"):
                return field
        return "description"

    def base_pre_save(self, sender, instance, created, **kwargs):
        pass

    def clean_image(self, image_field, sender):
        if self.__dict__[image_field] == "DONOTSEND":
            try:
                old_instance = sender.objects.get(pk=self.pk)
                if old_instance is not None:
                    self.__dict__[image_field] = old_instance.__dict__[image_field]
            except Exception, ex:
                pass
