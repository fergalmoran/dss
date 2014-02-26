import logging
import os
from django.core.management.base import NoArgsCommand
from spa.models.mix import Mix
from utils import query_yes_no


class Command(NoArgsCommand):
    help = "Create tracklists for all mixes"
    logger = logging.getLogger(__name__)

    def handle_noargs(self, **options):
        self.logger.debug("Tagging audio files")
        #mixes = Mix.objects.filter(uid='1348680a-507d-4a1e-a828-dffc90191c5b')
        mixes = Mix.objects.filter(mp3tags_updated=False)
        try:
            for mix in mixes:
                self.logger.debug("Tagging: %s" % mix.title)
                mix_file = mix.get_absolute_path()
                if not os.path.isfile(mix_file):
                    result = query_yes_no("Mix file %s\n\t(%s - %s)\ndoes not exist, delete mix entry?" % (
                                            mix_file, mix.title, mix.slug))
                    if result:
                        mix.delete()
                else:
                    mix.create_mp3_tags()
                    mix.mp3tags_updated = True
                    mix.save()
        except Exception:
            self.logger.exception("Error tagging mix: %s" % mix.uid)

        print "Finished tagging"
