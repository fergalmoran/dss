import os
import shutil
from django.core.management.base import NoArgsCommand
from spa.models import Mix


class Command(NoArgsCommand):
    def handle(self, *args, **options):
        candidates = Mix.objects.all()
        for mix in candidates:
            file = mix.get_absolute_path(prefix="expired/")
            if os.path.exists(file):
                new = mix.get_absolute_path()
                shutil.move(file, new)
