from django.shortcuts import render
from spa.models import Mix
from spa.models.playlist import Playlist


def render_podcast(mixes, request):
    return render(
        request,
        'inc/xml/podcast.xml',
        {'items': mixes},
        content_type='text/xml; charset=utf-8'
    )


def get_default_podcast(request):
    podcast_type = request.GET.get('type', '')
    if podcast_type == 'playlist':
        try:
            playlist = Playlist.objects.get(slug=request.GET['name'])
            return render_podcast(playlist.mixes.all(), request)
        except Playlist.DoesNotExist:
            pass

    mixes = Mix.objects.filter(download_allowed=True, waveform_generated=True).order_by('-upload_date')[0:50]
    return render_podcast(mixes, request)

