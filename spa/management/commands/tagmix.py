from django.core.management.base import NoArgsCommand
from spa.models.mix import Mix


class Command(NoArgsCommand):
    help = "Create tracklists for all mixes"

    def handle_noargs(self, **options):
        print "Tagging audio files"
        mixes = Mix.objects.filter(uid='3af66ac3-ff29-4b24-85a6-ae6ac774ca07')
        #mixes = Mix.objects.all()
        for mix in mixes:
            print "Tagging: %s" % mix.title
            mix.create_mp3_tags()

        print "Finished tagging"

