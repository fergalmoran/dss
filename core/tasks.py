import shutil
from celery.task import task
import os
from django.contrib.gis.geoip import GeoIP
from core.utils.waveform import generate_waveform
from dss import settings
from spa.signals import waveform_generated
from spa.models.userprofile import UserProfile

@task(time_limit=3600)
def create_waveform_task(in_file, uid):
    out_file = os.path.join(settings.MEDIA_ROOT, 'waveforms/%s.png' % uid)
    print "Creating waveform \n\tIn: %s\n\tOut: %s" % (in_file, out_file)
    generate_waveform(in_file, out_file)
    if os.path.isfile(out_file):
        print "Waveform generated successfully"
        file, extension = os.path.splitext(in_file)
        new_file = os.path.join(settings.MEDIA_ROOT, "mixes", "%s%s" % (uid, extension))
        print "Moving cache audio clip from %s to %s" % (in_file, new_file)
        shutil.move(in_file, new_file)
        print "Uid: %s" % uid
        waveform_generated.send(sender=None, uid=uid)
    else:
        print "Outfile is missing"

@task
def update_geo_info_task(ip_address, profile_id):
    try:
        ip = '188.141.70.110' if ip_address == '127.0.0.1' else ip_address
        if ip:
            g = GeoIP()
            city = g.city(ip)
            country = g.country(ip)
            try:
                user = UserProfile.objects.get(pk=profile_id)
                user.city = city['city']
                user.country = country['country_name']
                user.save()
            except ObjectDoesNotExist:
                pass
            print "Updated user location"
    except Exception, e:
        print e.message
        pass
