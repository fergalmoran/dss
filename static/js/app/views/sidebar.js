/** @license

 ----------------------------------------------

 Copyright (c) 2012, Fergal Moran. All rights reserved.
 Code provided under the BSD License:

 */

window.SidebarView = Backbone.View.extend({
    events:{
        "click #sidebar-play-pause-button-small":"togglePlayState",
        "click #sidebar-listen-live":"playLive"
    },
    initialize:function () {
        this.render();
        _.bindAll(this, "trackChanged");
        _.bindAll(this, "trackPlaying");
        _.bindAll(this, "trackPaused");
        _eventAggregator.bind("track_changed", this.trackChanged);
        _eventAggregator.bind("track_playing", this.trackPlaying);
        _eventAggregator.bind("track_paused", this.trackPaused);
        $.getJSON(
            'ajax/live_now_playing/',
            function (data) {
                $("#live-now-playing", this.el).text(data.title);
            });
    },
    render:function () {
        $(this.el).html(this.template());
        return this;
    },
    togglePlayState:function () {

    },
    trackChanged:function (data) {
        $(this.el).find('#now-playing').text(data.title);
        if (data.item_url != undefined)
            $(this.el).find('#now-playing').attr("href", "#" + data.item_url);
    },
    trackPlaying:function (data) {
        $(this.el).find('#header-play-button-icon').removeClass('icon-play');
        $(this.el).find('#header-play-button-icon').addClass('icon-pause');
    },
    trackPaused:function (data) {
        $(this.el).find('#header-play-button-icon').removeClass('icon-pause');
        $(this.el).find('#header-play-button-icon').addClass('icon-play');
    },
    playLive:function () {
        var liveButton = $(this.el).find('#sidebar-listen-live');
        if ((liveButton).hasClass('btn-danger')) {
            com.podnoms.player.stopPlaying();
            liveButton.removeClass('btn-danger').addClass('btn-success').text('Listen live');
            liveButton.blur();
        } else {
            liveButton.button('loading');
            com.podnoms.player.playLive({
                success:function () {
                    $.getJSON(
                        'ajax/live_now_playing/',
                        function (data) {
                            $('#live-now-playing', el).text(data.title);
                            data.title += " (live)";
                            _eventAggregator.trigger("track_changed", data);
                            liveButton.button('reset');
                            liveButton.removeClass('btn-success').addClass('btn-danger').text('Stop listening');
                        });
               }
            });
        }
        _eventAggregator.trigger("track_playing")
        var button = $(this.el).find('#sidebar-play-pause-button-small');
        var el = this.el;
        button
            .removeClass('play-button-smallstart')
            .removeClass('play-button-small-loading')
            .addClass('play-button-small-pause');
    }
});