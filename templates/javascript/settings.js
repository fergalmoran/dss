if (!window.appSettings) {
    window.appSettings = {};
    appSettings.urlRoot = '{{ API_URL }}';
    appSettings.liveStreamRoot = 'http://{{ LIVE_STREAM_URL }}:{{ LIVE_STREAM_PORT }}/{{ LIVE_STREAM_MOUNT }}';
    appSettings.streamInfoUrl = 'http://{{ LIVE_STREAM_INFO_URL }}';
}