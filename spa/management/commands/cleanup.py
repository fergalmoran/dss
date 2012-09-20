from shutil import copyfile
from django.core.management.base import NoArgsCommand
import os
from spa.models import Mix

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        mixes = Mix.objects.all()
        for mix in mixes:
            filename = mix.mix_image.file.name
            if os.path.isfile(filename):
                filename, extension = os.path.splitext(filename)
                new_file = "%s/%s%s" % (os.path.dirname(mix.mix_image.file.name), mix.uid, extension)
                print "Moving %s to %s" % (mix.mix_image.file.name, new_file)
                mix.mix_image = extension
                mix.save()
                copyfile(filename, new_file)

