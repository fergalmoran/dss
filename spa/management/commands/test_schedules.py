from django.core.management.base import NoArgsCommand
from datetime import datetime
from spa.models import Show
from spa.models.show import ShowOverlapException

DATE_FORMAT = '%d/%m/%Y %H:%M:%S'
START_DATE = datetime.strptime("28/04/2013 12:00:00", DATE_FORMAT)
END_DATE = datetime.strptime("28/04/2013 13:00:00", DATE_FORMAT)


class Command(NoArgsCommand):
    def handle_noargs(self, **options):
        try:
            Show.objects.all().delete()
            Show(description="Test event one", start=START_DATE, end=END_DATE).save()
            Show(description="Test event one", start=START_DATE, end=END_DATE).save()

        except Exception, ex:
            print "Debug exception: %s" % ex.message
