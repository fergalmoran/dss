from optparse import make_option
from django.core.management.base import NoArgsCommand, BaseCommand
from core.radio.live import LiveRadioPlayer
from dss import localsettings
from spa.models import Mix


class Command(NoArgsCommand):
    option_list = BaseCommand.option_list + (
        make_option('--play',
                    action='store',
                    dest='play',
                    help='Slug or id of file to play'),
    )

    def handle(self, *args, **options):
        if options['play']:
            print "Playing %s" % options['play']
            play_mix(options['play'])
        else:
            print "Must supply an action"


def play_mix(param):
    try:
        mix = Mix.objects.get(slug=param)
        LiveRadioPlayer(
            host=localsettings.RADIO_HOST,
            port=localsettings.RADIO_PORT,
            password=localsettings.RADIO_PASSWORD,
            mount=localsettings.RADIO_MOUNT
        ).play_track(song_name=mix.title, song_file=mix.get_absolute_path())

        print "Mix %s located, proceeding to play" % param
    except Mix.DoesNotExist:
        print "Mix %s not found" % param