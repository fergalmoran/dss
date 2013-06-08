from django.core.exceptions import ObjectDoesNotExist
from django.core.management.base import NoArgsCommand
import csv
from spa.models import Mix, Activity, UserProfile
from spa.models.activity import ActivityPlay


class Command(NoArgsCommand):
    help = "Import activity post activity refactor"

    def handle_noargs(self, **options):
        print "Importing from plays.txt"
        f = open("/home/fergalm/Dropbox/Private/deepsouthsounds.com/dss/plays.txt", "rt")
        rows = csv.DictReader(f, dialect='excel-tab')
        for row in rows:
            try:
                mix = Mix.objects.get(id=row['mix_id'])
                if row['user_id'] != '' and row['user_id'] != 'NULL':
                    try:
                        user = UserProfile.objects.get(user__id=row['user_id'])
                        ActivityPlay(user=user, mix=mix).save()
                        print "Added play: %s user: %s" % (mix.title, user.get_nice_name())
                    except ObjectDoesNotExist:
                        print "Could not find user: %s" % row['user_id']
                else:
                    ActivityPlay(user=None, mix=mix).save()
                    print "Added play: %s user: None" % mix.title

            except ObjectDoesNotExist:
                print "Could not find mix: %s" % row['mix_id']
            except Exception, e:
                print "Error: %s" % e.message



