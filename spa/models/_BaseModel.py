import logging
from django.db import models
from django.db.models import get_model
from django.utils import simplejson

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
            return cls.objects.all()#.extra(transform)

    @classmethod
    def get_lookup_filter_field(cls):
        field_list = cls._meta.get_all_field_names();
        for field in field_list:
            if field.endswith("_name"):
                return field
        return "description"