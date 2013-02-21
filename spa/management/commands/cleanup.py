from shutil import copyfile
from django.core.management.base import NoArgsCommand
import os
from spa.models import Mix

class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        mixes = Mix.objects.all()

