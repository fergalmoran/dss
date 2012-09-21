if (!com) var com = {};
if (!com.podnoms) com.podnoms = {};

com.podnoms.settings = {
    urlRoot:'{{ API_URL }}',
    liveStreamRoot:'http://{{ LIVE_STREAM_URL }}:{{ LIVE_STREAM_PORT }}/{{ LIVE_STREAM_MOUNT }}',
    streamInfoUrl:'http://{{ LIVE_STREAM_INFO_URL }}',
    volume:'{{ DEFAULT_AUDIO_VOLUME }}',
    smDebugMode: false,
    setupPlayer:function (data, id) {
        com.podnoms.player.setupPlayer({
            id:id,
            waveFormEl:$('#waveform-' + id),
            playHeadEl:$('#playhead-player-' + id),
            loadingEl:$('#progress-player-' + id),
            seekHeadEl:$('#player-seekhead'),
            playButtonEl:$('#play-pause-button-small-' + id),
            url:data.stream_url
        });
    }
};
