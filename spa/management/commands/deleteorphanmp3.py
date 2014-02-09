from dircache import listdir
import logging
import os
import shutil
from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import NoArgsCommand
from os.path import isfile, join
from dss import settings
from spa.models import Mix

logger = logging.getLogger('spa')


class Command(NoArgsCommand):
    def handle(self, *args, **options):
        try:
            mixes_path = join(settings.MEDIA_ROOT, "mixes")
            expired_path = join(settings.MEDIA_ROOT, "mixes/expired")
            files = [f for f in listdir(mixes_path) if isfile(join(mixes_path, f))]

            for f in files:
                uid = os.path.splitext(f)[0]
                try:
                    Mix.objects.get(uid=uid)
                except Mix.DoesNotExist:
                    new_file = os.path.join(expired_path, os.path.basename(f))
                    os.rename(f, new_file)
                    print "Moved %s to %s" % (f, new_file)
        except Exception, ex:
            logger.log(logger.WARNING, "Error: %s" % ex.message)

