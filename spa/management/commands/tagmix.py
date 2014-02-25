from django.core.management.base import NoArgsCommand
from spa.models.mix import Mix


class Command(NoArgsCommand):
    help = "Create tracklists for all mixes"

    def handle_noargs(self, **options):
        print "Tagging audio files"
        mixes = Mix.objects.filter(uid='1fb5bd5d-e32a-4e0d-9321-014587d53327')
        #mixes = Mix.objects.all()
        for mix in mixes:
            print "Tagging: %s" % mix.title
            mix.create_mp3_tags()

        print "Finished tagging"

