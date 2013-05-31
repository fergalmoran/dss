from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import NoArgsCommand
import csv
from spa.models import Mix, Activity, UserProfile


class Command(NoArgsCommand):
    help = "Import activity post activity refactor"

    def handle_noargs(self, **options):
        print "Importing from plays.txt"
        f = open("D:\\Working\\Dropbox\\Private\\deepsouthsounds.com\\dss\\spa\\management\\commands\\plays.txt", "rt")
        rows = csv.DictReader(f, dialect='excel-tab')
        for row in rows:
            try:
                mix = Mix.objects.get(id=row['mix_id'])
                user = None

                if row['user_id'] != '':
                    try:
                        user = UserProfile.objects.get(user__id=row['user_id'])
                    except ObjectDoesNotExist:
                        pass
                activity = Activity(user=user, date=row['date'], activity_type='p')
                activity.save()

                mix.plays.add(activity)
                mix.save()
                print "Added play: %s" % mix.title
            except ObjectDoesNotExist:
                pass
            except Exception, e:
                print "Error: %s" % e.message



