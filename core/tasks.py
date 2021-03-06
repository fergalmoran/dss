import shutil
from celery.task import task
import os
from django.core.exceptions import ObjectDoesNotExist

try:
    from django.contrib.gis.geoip import GeoIP
except ImportError:
    pass

from core.utils.waveform import generate_waveform
from dss import settings
from spa.signals import waveform_generated_signal, update_user_geoip_signal


@task(time_limit=3600)
def create_waveform_task(in_file, uid):
    out_file = os.path.join(settings.MEDIA_ROOT, 'waveforms/%s.png' % uid)
    print "Creating waveform \n\tIn: %s\n\tOut: %s" % (in_file, out_file)
    generate_waveform(in_file, out_file)
    if os.path.isfile(out_file):
        print "Waveform generated successfully"
        out_file, extension = os.path.splitext(in_file)
        new_file = os.path.join(settings.MEDIA_ROOT, "mixes", "%s%s" % (uid, extension))
        print "Moving cache audio clip from %s to %s" % (in_file, new_file)
        shutil.move(in_file, new_file)
        print "Uid: %s" % uid

        waveform_generated_signal.send(sender=None, uid=uid)
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
            update_user_geoip_signal.send(sender=None, profile_id=profile_id, city=city['city'],
                                          country=country['country'])
            print "Updated user location"
    except Exception, e:
        print e.message
        pass
