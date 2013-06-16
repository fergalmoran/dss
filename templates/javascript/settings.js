if (!com) var com = {};
if (!com.podnoms) com.podnoms = {};

com.podnoms.settings = {
    CHAT_HOST: '{{ CHAT_HOST }}',
    REALTIME_HOST: '{{ CHAT_HOST }}',
    REALTIME_PORT: '{{ CHAT_HOST }}',
    urlRoot: '{{ API_URL }}',
    liveStreamRoot: 'http://{{ LIVE_STREAM_URL }}:{{ LIVE_STREAM_PORT }}/{{ LIVE_STREAM_MOUNT }}',
    streamInfoUrl: 'http://{{ LIVE_STREAM_INFO_URL }}',
    volume: '{{ DEFAULT_AUDIO_VOLUME }}',
    smDebugMode: '{{ SM_DEBUG_MODE }}',
    isDebug: '{{ IS_DEBUG }}',
    drawTimelineOnMix: false,
    staticUrl: '{{ STATIC_URL }}',
    urlArgs: '{{ IS_DEBUG }}' ? "" : "bust="+ (new Date()).getTime(),
    currentUser: {{ CURRENT_USER_ID }},
    /** simple helper to take an api JSON object and initialise a player item */
    setupPlayerWrapper: function (id, stream_url) {
        com.podnoms.player.setupPlayer({
            id: id,
            boundingEl: $('#mix-container-' + id),
            waveFormEl: $('#waveform-' + id),
            playHeadEl: $('#playhead-player-' + id),
            loadingEl: $('#progress-player-' + id),
            seekHeadEl: $('#player-seekhead'),
            playButtonEl: $('#play-pause-button-small-' + id),
            url: stream_url || ""
        });
    }
};
