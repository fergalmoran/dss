window.HeaderView = Backbone.View.extend({
    events:{
        "click #header-play-pause-button":"togglePlayState",
        "click #header-live-button":"playLive"
    },
    initialize:function () {
        this.render();
        _.bindAll(this, "trackChanged");
        _.bindAll(this, "trackPlaying");
        _.bindAll(this, "trackPaused");
        _eventAggregator.bind("track_changed", this.trackChanged);
        _eventAggregator.bind("track_playing", this.trackPlaying);
        _eventAggregator.bind("track_paused", this.trackPaused);
    },
    trackChanged:function (data) {
        $(this.el).find('#track-description').text(data.title);
        $(this.el).find('#track-description').attr("href", "#" + data.item_url);
    },
    trackPlaying:function (data) {
        $(this.el).find('#header-play-button-icon').removeClass('icon-play');
        $(this.el).find('#header-play-button-icon').addClass('icon-pause');
    },
    trackPaused:function (data) {
        $(this.el).find('#header-play-button-icon').removeClass('icon-pause');
        $(this.el).find('#header-play-button-icon').addClass('icon-play');
    },
    render:function () {
        $(this.el).html(this.template());
        return this;
    },
    playLive:function () {
        dssSoundHandler.playLive();
        _eventAggregator.trigger("track_playing")
        var button = $(this.el).find('#header-play-pause-button');
        button.data("mode", "pause");
        $.getJSON(
            'ajax/live_now_playing/',
            function (data) {
                _eventAggregator.trigger("track_changed", data);
            });
    },
    togglePlayState:function () {
        var button = $(this.el).find('#header-play-pause-button');
        var mode = button.data("mode");
        if (mode == "play") {
            dssSoundHandler.resumeSound();
            _eventAggregator.trigger("track_playing");
            button.data("mode", "pause");
        } else {
            dssSoundHandler.pauseSound();
            _eventAggregator.trigger("track_paused");
            button.data("mode", "play");
        }
    }
});