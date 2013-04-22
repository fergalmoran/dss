/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */
window.HeaderView = Backbone.View.extend({
    events:{
        "click #header-play-pause-button":"togglePlayState",
        "click #header-login-button":"login",
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
    login: function () {
        com.podnoms.utils.modal('tpl/LoginView');
        return;
        $.colorbox({
            href: "/tpl/LoginView/",
            onClosed: function () {
                Backbone.history.navigate('/', {
                    trigger: true
                });
            }
        });
    },
    logout: function () {
        com.podnoms.utils.showAlert("Success", "You are now logged out");
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
        var ref = this;
        dssSoundHandler.playLive();
        _eventAggregator.trigger("track_playing")
        var button = $(this.el).find('#header-play-pause-button');
        button.data("mode", "pause");
        $.getJSON(
            'ajax/live_now_playing/',
            function (data) {
                alert(data.title);
                $(ref.el).find('#live-now-playing').text(data.title);
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