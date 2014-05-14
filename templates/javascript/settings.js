if (!com) var com = {};
if (!com.podnoms) com.podnoms = {};

com.podnoms.settings = {
    REALTIME_HOST: "{{ REALTIME_HOST }}",
    SOCKET_IO_JS_URL: "{{ SOCKET_IO_JS_URL }}",
    urlRoot: '{{ API_URL }}',
    liveEnabled: {{ LIVE_ENABLED }},
    liveStreamRoot: 'http://{{ LIVE_STREAM_URL }}:{{ LIVE_STREAM_PORT }}/{{ LIVE_STREAM_MOUNT }}',
    streamInfoUrl: 'http://{{ LIVE_STREAM_INFO_URL }}',
    volume: '{{ DEFAULT_AUDIO_VOLUME }}',
    nag_count: {{ NAG_COUNT }},
    smDebugMode: {{ SM_DEBUG_MODE }},
    isDebug: {{ IS_DEBUG }},
    drawTimelineOnMix: false,
    staticUrl: '{{ STATIC_URL }}',
    urlArgs: {{ IS_DEBUG }} ? "" : "bust="+ (new Date()).getTime(),
    currentUser: {{ CURRENT_USER_ID }},
    userName: "{{ CURRENT_USER_NAME }}",
    userUrl: "{{ CURRENT_USER_URL }}",
    avatarImage: "{{ AVATAR_IMAGE }}"
};
