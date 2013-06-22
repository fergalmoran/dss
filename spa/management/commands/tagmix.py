from django.core.management.base import NoArgsCommand
from spa.models.mix import Mix


class Command(NoArgsCommand):
    help = "Create tracklists for all mixes"

    def handle_noargs(self, **options):
        print "Tagging audio files"
        mixes = Mix.objects.filter(uid='6e2576bc-aba9-4717-9f9f-dede31fc2eaa')
        for mix in mixes:
            print "Tagging: %s" % mix.title
            mix.create_mp3_tags()

        print "Finished tagging"

