if (!com) var com = {};
if (!com.podnoms) com.podnoms = {};

com.podnoms.settings = {
    CHAT_HOST: '{{ CHAT_HOST }}',
    REALTIME_HOST: '{{ CHAT_HOST }}',
    REALTIME_PORT: '{{ CHAT_HOST }}',
    urlRoot:'{{ API_URL }}',
    liveStreamRoot:'http://{{ LIVE_STREAM_URL }}:{{ LIVE_STREAM_PORT }}/{{ LIVE_STREAM_MOUNT }}',
    streamInfoUrl:'http://{{ LIVE_STREAM_INFO_URL }}',
    volume:'{{ DEFAULT_AUDIO_VOLUME }}',
    smDebugMode: '{{ SM_DEBUG_MODE }}',

    /** simple helper to take an api JSON object and initialise a player item */
    setupPlayer:function (data, id) {
        com.podnoms.player.setupPlayer({
            id:id,
            boundingEl:$('#mix-container-'+ id),
            waveFormEl:$('#waveform-' + id),
            playHeadEl:$('#playhead-player-' + id),
            loadingEl:$('#progress-player-' + id),
            timeLineEl:$('#player-timeline-' + id),
            seekHeadEl:$('#player-seekhead'),
            playButtonEl:$('#play-pause-button-small-' + id),
            url:data.stream_url
        });
    }
};
