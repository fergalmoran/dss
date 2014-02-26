import logging
import os
from django.core.management.base import NoArgsCommand
from spa.models.mix import Mix
from datetime import datetime
import time


class Command(NoArgsCommand):
    help = "Change file modified date to mix upload date (easier sorting in airtime)"
    logger = logging.getLogger(__name__)

    def handle_noargs(self, **options):
        self.logger.debug("Updating file times")
        mixes = Mix.objects.all()
        try:
            for mix in mixes:
                self.logger.debug("Setting file time: %s" % mix.title)
                mix_file = mix.get_absolute_path()
                if os.path.isfile(mix_file):
                    os.utime(mix_file,
                             (time.mktime(datetime.now().timetuple()), time.mktime(mix.upload_date.timetuple())))
        except Exception:
            self.logger.exception("Error changing create date: %s" % mix.uid)

        print "Finished tagging"
