import logging
import datetime
import humanize
from tastypie.resources import ModelResource


class BackboneCompatibleResource(ModelResource):
    logger = logging.getLogger(__name__)
    pass

    def humanize_date(self, date):
        if (datetime.datetime.now() - date) <= datetime.timedelta(days=1):
            return humanize.naturaltime(date)
        else:
            return humanize.naturalday(date)