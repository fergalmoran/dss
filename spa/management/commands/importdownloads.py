from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import NoArgsCommand
import csv
from spa.models import Mix, Activity, UserProfile
from spa.models.activity import ActivityDownload


class Command(NoArgsCommand):
    help = "Import activity post activity refactor"

    def handle_noargs(self, **options):
        print "Importing from downloads.txt"
        f = open("/var/www/deepsouthsounds.com/dss/downloads.txt", "rt")
        rows = csv.DictReader(f, dialect='excel-tab')
        for row in rows:
            try:
                mix = Mix.objects.get(id=row['mix_id'])
                if row['user_id'] != '' and row['user_id'] != 'NULL':
                    try:
                        user = UserProfile.objects.get(user__id=row['user_id'])
                        ActivityDownload(user=user, mix=mix).save()
                        print "Added download: %s User: %s" % (mix.title, user.get_nice_name())
                    except ObjectDoesNotExist:
                        print "Unable to find user: %s" % row['user_id']
                        ActivityDownload(user=None, mix=mix).save()
                        print "Added download: %s UnknownUser: %s" % (mix.title, row['user_id'])
                else:
                    ActivityDownload(user=None, mix=mix).save()
                    print "Added download: %s User: None" % mix.title

            except ObjectDoesNotExist:
                pass
            except Exception, e:
                print "Error: %s" % e.message



